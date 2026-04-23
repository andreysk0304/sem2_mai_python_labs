import asyncio
import logging

import pytest

from task_platform.domain.task import Task
from task_platform.exceptions import (
    ExecutorHandlerTypeError,
    ExecutorWorkersCountError,
    HandleError,
)
from task_platform.execute.async_queue import AsyncTaskQueue
from task_platform.execute.executor import AsyncTaskExecutor
from task_platform.execute.handler import DemoHandler


def run(coro):
    return asyncio.run(coro)


class RecordingHandler:
    created: list["RecordingHandler"] = []
    handled_ids: list[str] = []
    fail_ids: set[str] = set()

    def __init__(self, name: str, source_name: str) -> None:
        self.name = name
        self.source_name = source_name
        self.entered = False
        self.exited = False
        type(self).created.append(self)

    async def __aenter__(self) -> "RecordingHandler":
        self.entered = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self.exited = True

    async def _can_handle(self, task: Task) -> bool:
        return True

    async def handle(self, task: Task) -> int:
        type(self).handled_ids.append(task.id)
        if task.id in type(self).fail_ids:
            raise HandleError(f"cannot handle task {task.id}")
        return 1


def reset_recording_handler() -> None:
    RecordingHandler.created = []
    RecordingHandler.handled_ids = []
    RecordingHandler.fail_ids = set()


def test_async_queue_put_get_close_and_join() -> None:
    async def scenario() -> None:
        queue = AsyncTaskQueue()
        task = Task(id="1", payload={"action": "run"})

        await queue.put_nowait(task)
        received = await queue.get()
        assert received == task

        await queue.done()
        await queue.join()

        await queue.close()
        assert await queue.get() is None
        await queue.done()
        await queue.join()

    run(scenario())


def test_executor_rejects_invalid_worker_count() -> None:
    async def scenario() -> None:
        with pytest.raises(ExecutorWorkersCountError):
            async with AsyncTaskExecutor(RecordingHandler, handlers_count=0):
                pass

    run(scenario())


def test_executor_rejects_invalid_handler_factory() -> None:
    class InvalidHandler:
        def __init__(self, name: str, source_name: str) -> None:
            self.name = name
            self.source_name = source_name

    async def scenario() -> None:
        with pytest.raises(ExecutorHandlerTypeError):
            async with AsyncTaskExecutor(InvalidHandler):
                pass

    run(scenario())


def test_executor_logs_errors_and_keeps_processing(caplog: pytest.LogCaptureFixture) -> None:
    reset_recording_handler()
    RecordingHandler.fail_ids = {"2"}
    logger = logging.getLogger("task_platform.tests.executor")

    async def scenario() -> AsyncTaskExecutor:
        queue = AsyncTaskQueue()
        await queue.put(Task(id="1", payload={"action": "ok"}))
        await queue.put(Task(id="2", payload={"action": "fail"}))
        await queue.close(workers_count=2)

        async with AsyncTaskExecutor(
            RecordingHandler,
            handlers_count=2,
            source_name="test-source",
            logger=logger,
        ) as executor:
            await executor.run(queue)
            return executor

    with caplog.at_level(logging.INFO, logger=logger.name):
        executor = run(scenario())

    assert sorted(RecordingHandler.handled_ids) == ["1", "2"]
    assert all(handler.entered and handler.exited for handler in RecordingHandler.created)
    assert len(executor.errors) == 1
    assert executor.errors[0][0].id == "2"
    assert isinstance(executor.errors[0][1], HandleError)
    assert "Task 2 failed" in caplog.text
    assert "Executor finished for test-source with 1 errors" in caplog.text


def test_demo_handler_checks_payload_and_handles_task(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_sleep(_: float) -> None:
        return None

    from task_platform.execute import handler as handler_module

    monkeypatch.setattr(handler_module.asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(handler_module, "randint", lambda _start, _end: 1)

    async def scenario() -> None:
        async with DemoHandler("worker-1", "demo") as handler:
            assert await handler._can_handle(Task(id="1", payload={"action": "run"})) is True
            assert await handler._can_handle(Task(id="2", payload={})) is False
            assert await handler.handle(Task(id="3", payload={"action": "run"})) == 1
            with pytest.raises(HandleError):
                await handler.handle(Task(id="4", payload={"foo": "bar"}))

    run(scenario())

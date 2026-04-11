from __future__ import annotations

from dataclasses import dataclass

from typing import Callable, Iterable
from contextlib import AsyncExitStack

from task_platform.exceptions import ExecutorWorkersCountError, ExecutorHandlerTypeError
from task_platform.execute.async_queue import AsyncTaskQueue
from task_platform.execute.handler_protocol import AsyncHandlerProtocol
from task_platform.domain.task import Task

@dataclass(slots=True)
class ExecutorReport:
    processed: int = 0
    succeeded: int = 0
    failed: int = 0


class AsyncTaskExecutor:
    def __init__(
        self,
        handler: Callable[[str, str], AsyncHandlerProtocol],
        workers_count: int = 1,
        source_name: str = "none",
    ) -> None:
        self._workers: list[AsyncHandlerProtocol] = []
        self._stack = AsyncExitStack()
        self._handler: Callable[[str, str], AsyncHandlerProtocol] = handler
        self._workers_count: int = workers_count
        self.source_name: str = source_name

    async def __aenter__(self) -> AsyncTaskExecutor:
        if self._workers_count < 1:
            raise ExecutorWorkersCountError("Кол-во воркеров не можеть быть менее 1")
        if self._handler is None:
            raise ExecutorHandlerTypeError("Обработчик не может быть пустым")
        if isinstance(self._handler, AsyncHandlerProtocol):
            raise ExecutorHandlerTypeError("Обработчик должен соблюдать контракт AsyncHandlerProtocol")

        await self._stack.__aenter__()
        for num in range(self._workers_count):
            worker = await self._stack.enter_async_context(
                self._handler(f"worker-{num}", self.source_name)
            )
            self._workers.append(worker)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._stack.__aexit__(exc_type, exc_val, exc_tb)

    async def run(self, tasks: Iterable[Task]) -> None:
        report = ExecutorReport()
        queue = AsyncTaskQueue()

        while True:
            ...

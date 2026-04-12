from __future__ import annotations

import asyncio

from typing import Callable
from contextlib import AsyncExitStack

from task_platform.exceptions import ExecutorWorkersCountError, ExecutorHandlerTypeError
from task_platform.execute.async_queue import AsyncTaskQueue
from task_platform.execute.handler_protocol import AsyncHandlerProtocol

class AsyncTaskExecutor:
    def __init__(
        self,
        handler: Callable[[str, str], AsyncHandlerProtocol],
        handlers_count: int = 1,
        source_name: str = "none_name",
    ) -> None:
        self._handlers: list[AsyncHandlerProtocol] = []
        self._stack = AsyncExitStack()
        self._handler: Callable[[str, str], AsyncHandlerProtocol] = handler
        self._handlers_count: int = handlers_count
        self.source_name: str = source_name
        self._tasks: list[asyncio.Task] = []

    async def __aenter__(self) -> AsyncTaskExecutor:
        if self._handlers_count < 1:
            raise ExecutorWorkersCountError("Кол-во воркеров не можеть быть менее 1")
        if self._handler is None:
            raise ExecutorHandlerTypeError("Обработчик не может быть пустым")
        if isinstance(self._handler, AsyncHandlerProtocol):
            raise ExecutorHandlerTypeError("Обработчик должен соблюдать контракт AsyncHandlerProtocol")

        await self._stack.__aenter__()
        for num in range(self._handlers_count):
            worker = await self._stack.enter_async_context(
                self._handler(f"worker-{num}", self.source_name)
            )
            self._handlers.append(worker)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._stack.__aexit__(exc_type, exc_val, exc_tb)

    async def _worker(self, handler: AsyncHandlerProtocol, queue: AsyncTaskQueue) -> None:
        while True:
            task = await queue.get()

            if task is None:
                await queue.done()
                break

            try:
                await handler.handle(task)
            finally:
                await queue.done()

    async def run(self, queue: AsyncTaskQueue) -> None:
        async with asyncio.TaskGroup() as task_group:
            for handler in self._handlers:
                task_group.create_task(self._worker(handler, queue))

            await queue.join()

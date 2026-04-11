import asyncio

from task_platform.domain.task import Task

END_QUEUE = object()


class AsyncTaskQueue:
    def __init__(self) -> None:
        self._queue: asyncio.Queue[Task | object] = asyncio.Queue()

    async def put(self, task: Task) -> None:
        await self._queue.put(task)

    async def put_nowait(self, task: Task) -> None:
        self._queue.put_nowait(task)

    async def get(self) -> Task | None:
        item = await self._queue.get()
        if item is END_QUEUE:
            return None
        return item

    async def close(self, workers_count: int = 1) -> None:
        for _ in range(workers_count):
            await self._queue.put(END_QUEUE)

    async def done(self) -> None:
        self._queue.task_done()

    async def join(self) -> None:
        await self._queue.join()
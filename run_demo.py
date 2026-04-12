#!/usr/bin/env python3
"""Демо: TaskQueue и асинхронный исполнитель поверх текущей реализации."""
import asyncio
import json
import os
import tempfile
from pathlib import Path

from task_platform.contracts.task_source import TaskSourceProtocol
from task_platform.domain import TaskQueue
from task_platform.execute.async_queue import AsyncTaskQueue
from task_platform.execute.executor import AsyncTaskExecutor
from task_platform.execute.handler import DemoHandler
from task_platform.sources import ApiTaskSource, FileTaskSource, GeneratorTaskSource
from task_platform.validation import ensure_task_source


class CombinedTaskSource:
    def __init__(self, sources: list[TaskSourceProtocol]) -> None:
        self._sources = tuple(sources)

    def get_tasks(self):
        for source in self._sources:
            yield from source.get_tasks()


async def fill_async_queue(queue: AsyncTaskQueue, tasks: TaskQueue, workers_count: int) -> None:
    for task in tasks:
        await queue.put(task)
    await queue.close(workers_count)


async def main() -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([
            {"id": "file-1", "payload": {"source": "file", "action": "validate"}},
            {"id": "file-2", "payload": {"source": "file", "action": "archive"}},
        ], f, ensure_ascii=False)
        file_path = f.name

    sources: list[TaskSourceProtocol] = [
        FileTaskSource(file_path),
        GeneratorTaskSource(
            count=3,
            start_id=1,
            payload_template={"source": "generator", "action": "generate"},
        ),
    ]
    if api_url := os.environ.get("API_URL"):
        sources.append(ApiTaskSource(api_url))

    for source in sources:
        ensure_task_source(source)

    combined_queue = TaskQueue(CombinedTaskSource(sources))
    preview_ids = [task.id for task in combined_queue.take(3)]
    all_tasks = list(combined_queue)

    async_queue = AsyncTaskQueue()
    workers_count = 3
    await fill_async_queue(async_queue, combined_queue, workers_count)

    print("Демонстрация TaskQueue и AsyncTaskExecutor:\n")
    print(f"Первые задачи через queue.take(3): {preview_ids}")
    print(f"Полный повторный обход очереди: {[task.id for task in all_tasks]}\n")

    async with AsyncTaskExecutor(
        DemoHandler,
        handlers_count=workers_count,
        source_name="demo-run",
    ) as executor:
        await executor.run(async_queue)

    Path(file_path).unlink(missing_ok=True)
    print("\nАсинхронный executor успешно обработал задачи из очереди.\n")


if __name__ == "__main__":
    asyncio.run(main())

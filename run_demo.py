#!/usr/bin/env python3
"""Демо: источники задач и работа TaskQueue поверх них."""
import json
import os
import tempfile
from pathlib import Path

from task_platform.contracts.task_source import TaskSourceProtocol
from task_platform.domain import TaskQueue
from task_platform.sources import ApiTaskSource, FileTaskSource, GeneratorTaskSource
from task_platform.validation import ensure_task_source


def main() -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([
            {"id": "file-1", "payload": {"from": "file"}},
            {"id": "file-2", "payload": None},
        ], f, ensure_ascii=False)
        file_path = f.name

    sources: list[TaskSourceProtocol] = [
        FileTaskSource(file_path),
        GeneratorTaskSource(count=3, start_id=1, payload_template={"from": "generator"}),
    ]
    if api_url := os.environ.get("API_URL"):
        sources.append(ApiTaskSource(api_url))

    print("Демонстрация TaskQueue поверх разных источников:\n")
    for i, source in enumerate(sources, 1):
        ensure_task_source(source)
        queue = TaskQueue(source)

        preview_ids = [task.id for task in queue.take(2)]
        all_tasks = list(queue)

        print(f" Источник {i}: {source.__class__.__name__}")
        print(f"  Первые задачи через queue.take(2): {preview_ids}")
        print(f"  Полный повторный обход очереди: {[task.id for task in all_tasks]}")
        for task in all_tasks:
            print(f"   id={task.id!r}, payload={task.payload}")

    Path(file_path).unlink(missing_ok=True)
    print("\nTaskQueue успешно отработала для всех источников.\n")


if __name__ == "__main__":
    main()

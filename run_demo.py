#!/usr/bin/env python3
"""Демо: приём задач из файла, генератора и API (если задан API_URL)."""
import json
import os
import tempfile
from pathlib import Path

from task_platform.contracts.task_source import TaskSourceProtocol
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

    print("Собираем задачи из источников:\n")
    for i, source in enumerate(sources, 1):
        ensure_task_source(source)
        tasks = list(source.get_tasks())
        print(f" Источник {i}: {len(tasks)} задач")
        for t in tasks:
            print(f"  id={t.id!r}, payload={t.payload}")

    Path(file_path).unlink(missing_ok=True)
    print("\nДанные успешно собраны из всех источников!\n")


if __name__ == "__main__":
    main()

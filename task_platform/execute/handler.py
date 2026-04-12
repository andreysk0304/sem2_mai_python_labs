from __future__ import annotations

import asyncio

from task_platform.domain.task import Task
from random import randint

from task_platform.exceptions import HandleError


class DemoHandler:
    def __init__(self, name: str, source_name: str ) -> None:
        self.name = name
        self.source_name = source_name

    async def __aenter__(self) -> DemoHandler:
        print(f"Воркер запущен {self.name}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        print(f"Воркер выключен {self.name}")

    async def _can_handle(self, task: Task) -> bool:
        payload = task.payload if isinstance(task.payload, dict) else {}
        return payload.get("action") is not None

    async def handle(self, task: Task) -> int:
        print(f"Обработчик {self.name} начал работу.")
        if not await self._can_handle(task):
            raise HandleError("Поле action не найдено внутри payload")
        await asyncio.sleep(0.2 * randint(1, 10))
        print(f"Обработчик {self.name} отработал. Источник: {self.source_name} Action: {task.payload['action']}")
        return randint(0, 100)
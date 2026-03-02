from datetime import datetime
from typing import Any

from task_platform.domain.task import Task, TaskStatus


class TaskMapper:
    """Приведение сырых данных (dict из парсера или API) к Task. Реализует TaskMapperProtocol"""

    def to_task(self, raw: dict[str, Any]) -> Task:
        """
        :param raw: Словарь с ключами id (обязательно), payload, description, priority, status, created_at (опционально)
        :return: Экземпляр Task (валидация через дескрипторы Task)
        """
        task_id = str(raw["id"])
        payload = raw.get("payload")
        description = raw.get("description") or ""
        priority = min(10, max(0, int(raw.get("priority", 0))))
        status = self._parse_status(raw.get("status"))
        created_at = self._parse_created_at(raw.get("created_at"))

        return Task(
            id=task_id,
            payload=payload,
            description=description,
            priority=priority,
            status=status,
            created_at=created_at,
        )

    def _parse_status(self, value: Any) -> TaskStatus:
        if value is None:
            return TaskStatus.DRAFT
        if isinstance(value, TaskStatus):
            return value
        if isinstance(value, str):
            for s in TaskStatus:
                if s.value == value:
                    return s
        return TaskStatus.DRAFT

    def _parse_created_at(self, value: Any) -> datetime | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        return None

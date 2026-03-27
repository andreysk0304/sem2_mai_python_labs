from datetime import datetime
from enum import Enum
from typing import Any

from task_platform.domain.descriptors import (
    DatetimeDescriptor,
    NonEmptyStrDescriptor,
    PriorityDescriptor,
    StatusDescriptor,
    StrDescriptor,
    SummaryDescriptor,
)


class TaskStatus(Enum):
    DRAFT = "draft"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task:
    """
    Модель задачи с валидацией атрибутов через дескрипторы

    id -> id задачи
    description -> описание задачи
    priority -> приоритет задачи
    status -> статус задачи
    created_at -> время создания задачи
    payload -> некоторая информация о задаче ( не проверяется дескриптром )
    is_ready -> вычисляемое свойство, для проверки готовности задаи к проверке
    """

    __slots__ = ("_id", "_payload", "_description", "_priority", "_status", "_created_at")

    id = NonEmptyStrDescriptor("_id")
    description = StrDescriptor("_description")
    priority = PriorityDescriptor("_priority")
    status = StatusDescriptor("_status", TaskStatus)
    created_at = DatetimeDescriptor("_created_at")
    summary = SummaryDescriptor()

    def __init__(self, id: str, payload: Any = None, description: str = "", priority: int = 0, status: TaskStatus = TaskStatus.DRAFT, created_at: datetime | None = None) -> None:
        self.id = id
        self._payload = payload
        self.description = description
        self.priority = priority
        self.status = status
        self.created_at = created_at if created_at is not None else datetime.now()

    @property
    def payload(self) -> Any:
        return self._payload

    @payload.setter
    def payload(self, payload: Any) -> None:
        self._payload = payload

    @property
    def is_ready(self) -> bool:
        """Задача готова к выполнению (статус pending или in_progress)"""
        return self.status in (TaskStatus.PENDING, TaskStatus.IN_PROGRESS)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return False
        return self.id == other.id and self._payload == other._payload

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, status={self.status.value})"
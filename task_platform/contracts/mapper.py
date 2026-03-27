"""Контракт маппера: сырые данные → Task."""
from typing import Any, Protocol, runtime_checkable

from task_platform.domain.task import Task


@runtime_checkable
class TaskMapperProtocol(Protocol):
    """Протокол: объект, преобразующий сырую запись (dict) в Task."""

    def to_task(self, raw: dict[str, Any]) -> Task: ...

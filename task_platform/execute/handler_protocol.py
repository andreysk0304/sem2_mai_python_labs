from __future__ import annotations

from typing import Protocol, runtime_checkable

from task_platform.domain.task import Task


@runtime_checkable
class AsyncHandlerProtocol(Protocol):
    name: str
    source_name: str

    async def __aenter__(self) -> AsyncHandlerProtocol: ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...

    async def _can_handle(self, task: Task) -> bool: ...

    async def handle(self, task: Task) -> int: ...
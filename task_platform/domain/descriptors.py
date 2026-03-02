from datetime import datetime
from enum import Enum
from typing import Any, Type

from task_platform.exceptions import TaskValidationError


class StatusDescriptor:
    """Дескпритор для статуса задачи (значение enum)"""

    def __init__(self, storage: str, enum_cls: Type[Enum]) -> None:
        self._storage = storage
        self._enum_cls = enum_cls

    def __get__(self, obj: Any, owner: Any) -> Any:
        if obj is None:
            return self
        return getattr(obj, self._storage)

    def __set__(self, obj: Any, value: Any) -> None:
        if not isinstance(value, self._enum_cls):
            raise TaskValidationError(f"статус должен быть одним из -> {list(self._enum_cls)}")
        setattr(obj, self._storage, value)


class NonEmptyStrDescriptor:
    """Дескриптор проверки что id задачи не пуст"""

    def __init__(self, storage: str) -> None:
        self._storage = storage

    def __get__(self, obj: Any, owner: Any) -> str:
        if obj is None:
            return self
        return getattr(obj, self._storage, "")

    def __set__(self, obj: Any, value: Any) -> None:
        if not isinstance(value, str) or not value.strip():
            raise TaskValidationError("id задачи должен быть непустой строкой")
        setattr(obj, self._storage, value.strip())


class StrDescriptor:
    """Дескриптор проверки того, что описание это строка"""

    def __init__(self, storage: str) -> None:
        self._storage = storage

    def __get__(self, obj: Any, owner: Any) -> str:
        if obj is None:
            return self

        return getattr(obj, self._storage, "")

    def __set__(self, obj: Any, value: Any) -> None:
        if value is not None and not isinstance(value, str):
            raise TaskValidationError("описание должно быть строкой")

        setattr(obj, self._storage, value if value is not None else "")


class PriorityDescriptor:
    """Дескриптор проверки того, что приоритет в пределах от 0 до 10"""

    def __init__(self, storage: str) -> None:
        self._storage = storage

    def __get__(self, obj: Any, owner: Any) -> int:
        if obj is None:
            return self
        return getattr(obj, self._storage, 0)

    def __set__(self, obj: Any, value: Any) -> None:
        if not isinstance(value, int) or value < 0 or value > 10:
            raise TaskValidationError("приоритет должен быть целым числом от 0 до 10")
        setattr(obj, self._storage, value)


class DatetimeDescriptor:
    """Дескриптор пвоверяет, что время создания имеет тип datetime"""

    def __init__(self, storage: str) -> None:
        self._storage = storage

    def __get__(self, obj: Any, owner: Any) -> datetime:
        if obj is None:
            return self

        return getattr(obj, self._storage)

    def __set__(self, obj: Any, value: Any) -> None:
        if value is not None and not isinstance(value, datetime):
            raise TaskValidationError("время создания должно быть datetime")

        setattr(obj, self._storage, value)


class SummaryDescriptor:
    """Non-data дескриптор, только __get__, вычисляемое значение summary"""

    def __get__(self, obj: Any, owner: Any) -> Any:
        if obj is None:
            return self
        return f"{obj.id}: {obj.status.value}"

from typing import Iterable, Protocol, runtime_checkable

from task_platform.domain.task import Task


@runtime_checkable
class TaskSourceProtocol(Protocol):
    """
    Протокол (контракт) источника задач
    Проверяет удовлетворяет источник условию наличия get_tasks() возвращающего итерацию задач (Iterable[Task])
    """

    def get_tasks(self) -> Iterable[Task]: ...
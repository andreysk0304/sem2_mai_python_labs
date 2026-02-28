from task_platform.contracts.task_source import TaskSourceProtocol
from task_platform.exceptions import InvalidTaskSource


def ensure_task_source(obj: object) -> None:
    """
    Проверяет, что объект реализует контракт TaskSourceProtocol

    :param obj: Источник задач
    :return: Ничего, если объект не подходит, то дропается ошибка InvalidTaskSource
    """
    if not isinstance(obj, TaskSourceProtocol):
        raise InvalidTaskSource("Источник задач должен соблюдать контракт TaskSourceProtocol (метод get_tasks() -> Iterable[Task])")
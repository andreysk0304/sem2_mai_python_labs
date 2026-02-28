from typing import Any, Iterator

from task_platform.domain.task import Task
from task_platform.exceptions import InvalidSourceConfigError


class GeneratorTaskSource:
    """
    Источник задач, генерирующий их по шаблону
    """

    def __init__(self, count: int, start_id: int = 1, payload_template: Any = None) -> None:
        """

        :param count: Кол-во генерируемых задач
        :param start_id: Начальный id ( по умолчанию 1 )
        :param payload_template: Шаблон payload ( будет вставлен в каждую задачу )
        """

        if count < 0:
            raise InvalidSourceConfigError("count не может быть отрицательным")

        self._count = count
        self._start_id = start_id
        self._payload_template = payload_template


    def get_tasks(self) -> Iterator[Task]:
        """
        Генерирует задачи лениво (генератор)
        :return: Задача с уникальным id и шаблоном payload (Task)
        """
        for i in range(self._count):
            task_id = str(self._start_id + i)
            yield Task(id=task_id, payload=self._payload_template)

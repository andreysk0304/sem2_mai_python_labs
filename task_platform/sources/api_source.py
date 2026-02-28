from typing import Iterator

import httpx

from task_platform.domain.task import Task
from task_platform.exceptions import InvalidTaskDataError, InvalidTaskItemError


class ApiTaskSource:
    """
    Источник задач, получающий их по GET запросу к API
    """

    def __init__(self, base_url: str, path: str = "/tasks") -> None:
        """
        :param base_url: Базовый URL API
        :param path: Путь к эндпоинту списка задач
        """
        self._base_url = base_url.rstrip("/")
        self._path = path.lstrip("/")

    def get_tasks(self) -> Iterator[Task]:
        """
        Функция делает GET запрос к API и лениво ( как генератор ) возвращает задачи

        :return: Задачи из API ( Task )
        """
        url = self._base_url + "/" + self._path

        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()

        if not isinstance(data, list):
            raise InvalidTaskDataError("Ответ API должен содержать массив задач")

        for item in data:
            if not isinstance(item, dict):
                raise InvalidTaskItemError("Каждый элемент должен быть объектом с id и payload")

            task_id = item.get("id")
            payload = item.get("payload")

            if task_id is None:
                raise InvalidTaskItemError("Задача должна содержать поле id")

            yield Task(id=str(task_id), payload=payload)

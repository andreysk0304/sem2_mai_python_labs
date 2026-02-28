import json
from pathlib import Path
from typing import Iterator

from task_platform.domain.task import Task
from task_platform.exceptions import InvalidTaskDataError, InvalidTaskItemError


class JsonFileTaskSource:
    """
    Истиочник задач из json файлов
    """

    def __init__(self, path: str | Path) -> None:
        """
        :param path: Путь до json файла
        """
        self._path = Path(path)

    def get_tasks(self) -> Iterator[Task]:
        """
        Читает задачи из json файла и выводит их лениво ( генератор )
        :return: Задача [Task]
        """
        with open(self._path, encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise InvalidTaskDataError("Файл должен содержать JSON-массив задач")

        for item in data:
            if not isinstance(item, dict):
                raise InvalidTaskItemError("Каждый элемент должен быть объектом с id и payload")

            task_id = item.get("id")
            payload = item.get("payload")

            if task_id is None:
                raise InvalidTaskItemError("Задача должна содержать поле id")

            yield Task(id=str(task_id), payload=payload)

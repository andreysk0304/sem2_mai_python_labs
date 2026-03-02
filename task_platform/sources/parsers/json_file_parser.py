"""Сервис парсинга JSON-файла: только чтение и разбор, без доменной модели."""
import json
from pathlib import Path

from task_platform.exceptions import InvalidTaskDataError, InvalidTaskItemError


class JsonFileParser:
    """Читает JSON-файл и возвращает список сырых записей (dict с id, payload и опциональными полями)."""

    def parse(self, path: str | Path) -> list[dict]:
        """
        :param path: Путь к JSON-файлу
        :return: Список словарей, каждый с ключом "id" и опционально "payload", "description", "priority", "status", "created_at"
        :raises InvalidTaskDataError: файл не массив
        :raises InvalidTaskItemError: элемент не dict или нет id
        """
        path = Path(path)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise InvalidTaskDataError("Файл должен содержать JSON-массив задач")

        result: list[dict] = []
        for item in data:
            if not isinstance(item, dict):
                raise InvalidTaskItemError("Каждый элемент должен быть объектом с id и payload")
            if item.get("id") is None:
                raise InvalidTaskItemError("Задача должна содержать поле id")
            result.append(item)
        return result

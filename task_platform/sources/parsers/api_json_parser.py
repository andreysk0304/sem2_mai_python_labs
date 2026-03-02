from typing import Any

import httpx

from task_platform.exceptions import InvalidTaskDataError, InvalidTaskItemError


class ApiJsonParser:
    """Делает GET запрос к API и возвращает список сырых словарей"""

    def parse(self, base_url: str, path: str = "/tasks") -> list[dict[str, Any]]:
        url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()

        if not isinstance(data, list):
            raise InvalidTaskDataError("Ответ API должен содержать массив задач")

        result: list[dict[str, Any]] = []
        for item in data:
            if not isinstance(item, dict):
                raise InvalidTaskItemError("Каждый элемент должен быть объектом с id и payload")
            if item.get("id") is None:
                raise InvalidTaskItemError("Задача должна содержать поле id")
            result.append(item)
        return result

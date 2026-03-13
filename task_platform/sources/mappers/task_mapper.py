from typing import Any

from task_platform.domain.task import Task


class TaskMapper:
    """Приведение сырых данных (dict из парсера или API) к Task. Реализует TaskMapperProtocol"""

    def to_task(self, raw: dict[str, Any]) -> Task:
        """
        :param raw: Словарь с ключами id (обязательно), payload (опционально)
        :return: Экземпляр Task
        """
        task_id = str(raw["id"])
        payload = raw.get("payload")
        return Task(id=task_id, payload=payload)

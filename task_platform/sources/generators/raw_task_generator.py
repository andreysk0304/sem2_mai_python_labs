from typing import Any, Iterator

from task_platform.exceptions import InvalidSourceConfigError


class RawTaskGenerator:
    """Генерирует сырые записи (dict с id, payload) по шаблону."""

    def __init__(
        self,
        count: int,
        start_id: int = 1,
        payload_template: Any = None,
    ) -> None:
        if count < 0:
            raise InvalidSourceConfigError("count не может быть отрицательным")
        self._count = count
        self._start_id = start_id
        self._payload_template = payload_template

    def generate(self) -> Iterator[dict[str, Any]]:
        for i in range(self._count):
            yield {
                "id": str(self._start_id + i),
                "payload": self._payload_template,
            }

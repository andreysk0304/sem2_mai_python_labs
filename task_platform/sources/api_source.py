from typing import Iterator

from task_platform.contracts.mapper import TaskMapperProtocol
from task_platform.domain.task import Task
from task_platform.sources.mappers import TaskMapper
from task_platform.sources.parsers import ApiJsonParser


class ApiTaskSource:
    """Источник задач из HTTP API. Использует ApiJsonParser и TaskMapper"""

    def __init__(
        self,
        base_url: str,
        path: str = "/tasks",
        parser: ApiJsonParser | None = None,
        mapper: TaskMapperProtocol | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._path = path.lstrip("/")
        self._parser = parser or ApiJsonParser()
        self._mapper = mapper or TaskMapper()

    def get_tasks(self) -> Iterator[Task]:
        raw_list = self._parser.parse(self._base_url, self._path)
        for raw in raw_list:
            yield self._mapper.to_task(raw)

from pathlib import Path
from typing import Iterator

from task_platform.contracts.mapper import TaskMapperProtocol
from task_platform.domain.task import Task
from task_platform.sources.mappers import TaskMapper
from task_platform.sources.parsers import JsonFileParser


class JsonFileTaskSource:
    """Источник задач из JSON файла, использует JsonFileParser и TaskMapper (или реализацию TaskMapperProtocol)"""

    def __init__(
        self,
        path: str | Path,
        parser: JsonFileParser | None = None,
        mapper: TaskMapperProtocol | None = None,
    ) -> None:
        self._path = Path(path)
        self._parser = parser or JsonFileParser()
        self._mapper = mapper or TaskMapper()

    def get_tasks(self) -> Iterator[Task]:
        raw_list = self._parser.parse(self._path)
        for raw in raw_list:
            yield self._mapper.to_task(raw)

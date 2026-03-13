import logging
from typing import Any, Iterator

from task_platform.contracts.mapper import TaskMapperProtocol

logger = logging.getLogger(__name__)
from task_platform.domain.task import Task
from task_platform.exceptions import InvalidSourceConfigError
from task_platform.sources.generators import RawTaskGenerator
from task_platform.sources.mappers import TaskMapper


class GeneratorTaskSource:
    """Источник задач из генератора, использует RawTaskGenerator и TaskMapper"""

    def __init__(
        self,
        count: int,
        start_id: int = 1,
        payload_template: Any = None,
        generator: RawTaskGenerator | None = None,
        mapper: TaskMapperProtocol | None = None
    ) -> None:
        if count < 0:
            logger.warning("Передан отрицательный count=%d", count)
            raise InvalidSourceConfigError("count не может быть отрицательным")

        self._generator = generator or RawTaskGenerator(count, start_id, payload_template)
        self._mapper = mapper or TaskMapper()

    def get_tasks(self) -> Iterator[Task]:
        for raw in self._generator.generate():
            yield self._mapper.to_task(raw)

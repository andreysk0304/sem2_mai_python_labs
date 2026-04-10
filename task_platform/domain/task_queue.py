from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from itertools import count, islice
from typing import TypeAlias

from task_platform.contracts.task_source import TaskSourceProtocol
from task_platform.domain.task import Task, TaskStatus

TaskPredicate: TypeAlias = Callable[[Task], bool]


class _ReplayableTasks:
    """Лениво кэширует уже полученные задачи, чтобы очередь можно было обойти повторно"""

    def __init__(self, source: TaskSourceProtocol) -> None:
        self._source = source
        self._cache: list[Task] = []
        self._iterator: Iterator[Task] | None = None
        self._is_exhausted = False

    def __iter__(self) -> Iterator[Task]:
        if self._iterator is None and not self._is_exhausted:
            self._iterator = iter(self._source.get_tasks())

        for index in count():
            if index < len(self._cache):
                yield self._cache[index]
                continue

            if self._is_exhausted or self._iterator is None:
                return

            try:
                task = next(self._iterator)
            except StopIteration:
                self._is_exhausted = True
                self._iterator = None
                return

            self._cache.append(task)
            yield task


class TaskQueue:
    """
    Лениво итерируемое представление задач

    Очередь поддерживает повторный обход, даже если источник возвращает одноразовый итератор
    """

    def __init__(
        self,
        source: TaskSourceProtocol,
        predicates: tuple[TaskPredicate, ...] = (),
        tasks: Iterable[Task] | None = None,
    ) -> None:
        self._source = source
        self._predicates = predicates
        self._tasks = tasks or _ReplayableTasks(source)

    def __iter__(self) -> Iterator[Task]:
        for task in self._tasks:
            if all(predicate(task) for predicate in self._predicates):
                yield task

    def filter(self, predicate: TaskPredicate) -> TaskQueue:
        return TaskQueue(
            source=self._source,
            predicates=self._predicates + (predicate,),
            tasks=self._tasks,
        )

    def filter_by_status(self, status: TaskStatus) -> TaskQueue:
        return self.filter(lambda task: task.status == status)

    def filter_by_priority(
        self,
        min_priority: int = 0,
        max_priority: int | None = None,
    ) -> TaskQueue:
        if max_priority is not None and max_priority < min_priority:
            raise ValueError("max_priority не может быть меньше min_priority")

        return self.filter(
            lambda task: task.priority >= min_priority
            and (max_priority is None or task.priority <= max_priority)
        )

    def take(self, limit: int) -> Iterator[Task]:
        if limit < 0:
            raise ValueError("limit не может быть отрицательным")
        return islice(self, limit)

    def count(self) -> int:
        return sum(1 for _ in self)

    def __repr__(self) -> str:
        return (
            f"TaskQueue(source={self._source!r}, "
            f"predicates={len(self._predicates)})"
        )

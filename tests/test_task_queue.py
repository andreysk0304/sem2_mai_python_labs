import pytest

from task_platform.domain import Task, TaskQueue, TaskStatus
from task_platform.sources import GeneratorTaskSource


class AdHocSource:
    def __init__(self, tasks) -> None:
        self._tasks = tasks

    def get_tasks(self):
        for task in self._tasks:
            yield task


def test_queue_supports_repeat_iteration() -> None:
    """Очередь поверх source должна обходиться повторно"""
    queue = TaskQueue(GeneratorTaskSource(count=3))

    first_pass = [task.id for task in queue]
    second_pass = [task.id for task in queue]

    assert first_pass == ["1", "2", "3"]
    assert second_pass == ["1", "2", "3"]


def test_queue_supports_repeat_iteration_for_single_pass_source() -> None:
    class SinglePassSource:
        def __init__(self) -> None:
            self._iterator = iter(
                [
                    Task(id="1", status=TaskStatus.DRAFT),
                    Task(id="2", status=TaskStatus.DONE),
                ]
            )

        def get_tasks(self):
            return self._iterator

    queue = TaskQueue(SinglePassSource())

    assert [task.id for task in queue] == ["1", "2"]
    assert [task.id for task in queue] == ["1", "2"]


def test_filter_by_status_is_lazy() -> None:
    """Фильтр по статусу не должен исполнять источник до начала обхода"""
    consumed: list[str] = []

    class TrackingSource:
        def get_tasks(self):
            consumed.append("1")
            yield Task(id="1", status=TaskStatus.DRAFT)
            consumed.append("2")
            yield Task(id="2", status=TaskStatus.DONE)

    queue = TaskQueue(TrackingSource())
    filtered = queue.filter_by_status(TaskStatus.DONE)

    assert consumed == []
    assert [task.id for task in filtered] == ["2"]
    assert consumed == ["1", "2"]


def test_filter_chaining_accumulates_predicates() -> None:
    queue = TaskQueue(
        AdHocSource(
            [
                Task(id="1", status=TaskStatus.DONE, priority=1),
                Task(id="2", status=TaskStatus.DONE, priority=5),
                Task(id="3", status=TaskStatus.PENDING, priority=5),
            ]
        )
    )

    result = [
        task.id
        for task in queue
        .filter_by_status(TaskStatus.DONE)
        .filter_by_priority(min_priority=3)
    ]

    assert result == ["2"]


def test_filter_accepts_custom_predicate() -> None:
    queue = TaskQueue(GeneratorTaskSource(count=5))

    result = [task.id for task in queue.filter(lambda task: int(task.id) % 2 == 0)]

    assert result == ["2", "4"]


def test_filter_by_priority_returns_tasks_in_range() -> None:
    queue = TaskQueue(
        AdHocSource(
            [
                Task(id="1", priority=1),
                Task(id="2", priority=5),
                Task(id="3", priority=8),
            ]
        )
    )

    result = [
        task.id
        for task in queue.filter_by_priority(min_priority=3, max_priority=6)
    ]

    assert result == ["2"]


def test_take_returns_only_requested_number_of_tasks() -> None:
    queue = TaskQueue(GeneratorTaskSource(count=5))

    result = [task.id for task in queue.take(2)]

    assert result == ["1", "2"]


def test_take_zero_returns_empty_iterator() -> None:
    queue = TaskQueue(GeneratorTaskSource(count=5))

    assert list(queue.take(0)) == []


def test_take_raises_for_negative_limit() -> None:
    queue = TaskQueue(GeneratorTaskSource(count=1))

    with pytest.raises(ValueError, match="limit"):
        list(queue.take(-1))


def test_count_works_after_filtering() -> None:
    queue = TaskQueue(
        AdHocSource(
            [
                Task(id="1", status=TaskStatus.DONE),
                Task(id="2", status=TaskStatus.PENDING),
                Task(id="3", status=TaskStatus.DONE),
            ]
        )
    )

    assert queue.filter_by_status(TaskStatus.DONE).count() == 2


def test_filter_by_priority_raises_for_invalid_range() -> None:
    queue = TaskQueue(AdHocSource([Task(id="1", priority=1)]))

    with pytest.raises(ValueError, match="max_priority"):
        queue.filter_by_priority(min_priority=5, max_priority=2)


def test_repr_includes_source_and_predicate_count() -> None:
    source = GeneratorTaskSource(count=1)
    queue = TaskQueue(source).filter_by_status(TaskStatus.DONE).filter_by_priority(1)

    result = repr(queue)

    assert "TaskQueue" in result
    assert "predicates=2" in result
    assert "GeneratorTaskSource" in result

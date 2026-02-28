import pytest

from task_platform.exceptions import InvalidSourceConfigError
from task_platform.sources import GeneratorTaskSource


def test_generates_count_tasks() -> None:
    """Тест того, что генерируется ровно count задач"""
    source = GeneratorTaskSource(count=5)
    tasks = list(source.get_tasks())

    assert len(tasks) == 5
    assert [t.id for t in tasks] == ["1", "2", "3", "4", "5"]


def test_start_id() -> None:
    """Тест того, что start_id корректно задаёт начальный числовой id"""
    source = GeneratorTaskSource(count=3, start_id=10)
    tasks = list(source.get_tasks())

    assert [t.id for t in tasks] == ["10", "11", "12"]


def test_payload_template() -> None:
    """Тест того, что payload_template попадает в каждую задачу"""
    source = GeneratorTaskSource(count=2, payload_template={"type": "тест так то"})
    tasks = list(source.get_tasks())

    assert tasks[0].payload == {"type": "тест так то"}
    assert tasks[1].payload == {"type": "тест так то"}


def test_zero_count() -> None:
    """Тест того, что count=0 даёт пустую итерацию"""
    source = GeneratorTaskSource(count=0)

    assert list(source.get_tasks()) == []


def test_negative_count_raises() -> None:
    """Тест того, что отрицательный count вызывает InvalidSourceConfigError"""
    with pytest.raises(InvalidSourceConfigError, match="отрицательным"):
        GeneratorTaskSource(count=-1)


def test_lazy_iteration() -> None:
    """Тест того, что get_tasks возвращает итератор (ленивая генерация)"""
    source = GeneratorTaskSource(count=100)
    it = source.get_tasks()
    first = next(it)
    second = next(it)

    assert first.id == "1"
    assert second.id == "2"

from datetime import datetime

import pytest

from task_platform.domain.task import Task, TaskStatus
from task_platform.exceptions import TaskValidationError


def test_task_has_id_and_payload():
    """Тест того, что Task содержит id и payload"""
    t = Task(id="1", payload={"x": 1})
    assert t.id == "1"
    assert t.payload == {"x": 1}


def test_task_has_default_values() -> None:
    """Тест того, что Task получает значения по умолчанию"""
    t = Task(id="1")

    assert t.description == ""
    assert t.priority == 0
    assert t.status == TaskStatus.DRAFT
    assert isinstance(t.created_at, datetime)
    assert t.summary == "1: draft"
    assert t.is_ready is False


def test_id_is_stripped() -> None:
    """Тест того, что id очищается от пробелов по краям"""
    t = Task(id="  1  ")

    assert t.id == "1"


def test_description_none_becomes_empty_string() -> None:
    """Тест того, что description=None приводится к пустой строке"""
    t = Task(id="1", description=None)

    assert t.description == ""


def test_payload_can_be_reassigned() -> None:
    """Тест того, что payload можно менять после создания задачи"""
    t = Task(id="1", payload={"x": 1})
    t.payload = ["a", "b"]

    assert t.payload == ["a", "b"]


def test_is_ready_depends_on_status() -> None:
    """Тест того, что is_ready зависит от статуса задачи"""
    draft = Task(id="1", status=TaskStatus.DRAFT)
    pending = Task(id="2", status=TaskStatus.PENDING)
    in_progress = Task(id="3", status=TaskStatus.IN_PROGRESS)
    done = Task(id="4", status=TaskStatus.DONE)

    assert draft.is_ready is False
    assert pending.is_ready is True
    assert in_progress.is_ready is True
    assert done.is_ready is False


def test_summary_uses_current_status() -> None:
    """Тест того, что summary вычисляется по текущему статусу"""
    t = Task(id="1", status=TaskStatus.DRAFT)
    t.status = TaskStatus.DONE

    assert t.summary == "1: done"


def test_task_equality_depends_on_id_and_payload() -> None:
    """Тест того, что равенство Task зависит от id и payload"""
    left = Task(id="1", payload={"x": 1}, status=TaskStatus.DRAFT)
    same = Task(id="1", payload={"x": 1}, status=TaskStatus.DONE)
    other = Task(id="2", payload={"x": 1})

    assert left == same
    assert left != other
    assert left != 42


def test_task_repr() -> None:
    """Тест строкового представления Task"""
    t = Task(id="1", status=TaskStatus.PENDING)

    assert repr(t) == "Task(id='1', status=pending)"


def test_empty_id_raises() -> None:
    """Тест того, что пустой id вызывает TaskValidationError"""
    with pytest.raises(TaskValidationError, match="непустой строкой"):
        Task(id="   ")


def test_description_must_be_string() -> None:
    """Тест того, что description должен быть строкой"""
    with pytest.raises(TaskValidationError, match="описание"):
        Task(id="1", description=123)


def test_priority_must_be_int_in_range() -> None:
    """Тест того, что priority должен быть целым числом от 0 до 10"""
    with pytest.raises(TaskValidationError, match="приоритет"):
        Task(id="1", priority=-1)

    with pytest.raises(TaskValidationError, match="приоритет"):
        Task(id="1", priority="high")


def test_status_must_be_enum() -> None:
    """Тест того, что status должен быть значением TaskStatus"""
    with pytest.raises(TaskValidationError, match="статус"):
        Task(id="1", status="draft")


def test_created_at_must_be_datetime() -> None:
    """Тест того, что created_at должен быть объектом datetime"""
    with pytest.raises(TaskValidationError, match="datetime"):
        Task(id="1", created_at="2024-01-01")

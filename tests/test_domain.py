import pytest

from task_platform.domain.task import Task


def test_task_has_id_and_payload():
    """Тест того, что Task содержит id и payload"""
    t = Task(id="1", payload={"x": 1})
    assert t.id == "1"
    assert t.payload == {"x": 1}
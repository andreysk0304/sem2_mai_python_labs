import json
import pytest

from task_platform.domain.task import Task
from task_platform.exceptions import InvalidTaskDataError, InvalidTaskItemError
from task_platform.sources import FileTaskSource


def test_read_tasks_from_json(tmp_path) -> None:
    """Тест чтения списка задач из JSON-файла"""
    data = [
        {"id": "1", "payload": {"a": 1}},
        {"id": "2", "payload": "hello"},
    ]
    path = tmp_path / "tasks.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    source = FileTaskSource(path)
    tasks = list(source.get_tasks())

    assert len(tasks) == 2
    assert tasks[0] == Task(id="1", payload={"a": 1})
    assert tasks[1] == Task(id="2", payload="hello")


def test_id_coerced_to_string(tmp_path) -> None:
    """Тест того, что id приводится к строке"""
    path = tmp_path / "t.json"
    path.write_text('[{"id": 42, "payload": null}]', encoding="utf-8")
    source = FileTaskSource(path)
    tasks = list(source.get_tasks())

    assert tasks[0].id == "42"


def test_empty_array(tmp_path) -> None:
    """Тест того, что пустой массив даёт пустой список задач"""
    path = tmp_path / "empty.json"
    path.write_text("[]", encoding="utf-8")
    source = FileTaskSource(path)

    assert list(source.get_tasks()) == []


def test_not_array_raises(tmp_path) -> None:
    """Тест того, что не массив в файле вызывает InvalidTaskDataError"""
    path = tmp_path / "bad.json"
    path.write_text('{"id": "1"}', encoding="utf-8")
    source = FileTaskSource(path)

    with pytest.raises(InvalidTaskDataError, match="массив"):
        list(source.get_tasks())


def test_missing_id_raises(tmp_path) -> None:
    """Тест того, что отсутствие id в объекте вызывает InvalidTaskItemError"""
    path = tmp_path / "bad.json"
    path.write_text('[{"payload": "x"}]', encoding="utf-8")
    source = FileTaskSource(path)

    with pytest.raises(InvalidTaskItemError, match="id"):
        list(source.get_tasks())


def test_path_as_path_object(tmp_path) -> None:
    """Тест того, что путь можно передать как pathlib.Path"""
    path = tmp_path / "p.json"
    path.write_text('[{"id": "1", "payload": null}]', encoding="utf-8")
    source = FileTaskSource(path)
    tasks = list(source.get_tasks())

    assert len(tasks) == 1
    assert tasks[0].id == "1"

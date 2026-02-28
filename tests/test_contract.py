import pytest

from task_platform.contracts.task_source import TaskSourceProtocol
from task_platform.domain.task import Task
from task_platform.exceptions import InvalidTaskSource
from task_platform.sources import FileTaskSource, GeneratorTaskSource, ApiTaskSource
from task_platform.validation import ensure_task_source


def test_file_source_implements_protocol(tmp_path) -> None:
    """Тест того, что FileTaskSource соблюдает TaskSourceProtocol"""
    path = tmp_path / "tasks.json"
    path.write_text('[{"id": "1", "payload": {"x": 1}}]', encoding="utf-8")
    source = FileTaskSource(path)

    assert isinstance(source, TaskSourceProtocol)
    assert issubclass(FileTaskSource, type(source))


def test_generator_source_implements_protocol() -> None:
    """Тест того, что GeneraorTaskSource соблюдает TaskSourceProtocol"""
    source = GeneratorTaskSource(count=3)

    assert isinstance(source, TaskSourceProtocol)


def test_api_source_implements_protocol() -> None:
    """Проверка того, что ApiTaskSource соблюдает TaskSourceProtocol"""
    source = ApiTaskSource(base_url="http://localhost:8000")

    assert isinstance(source, TaskSourceProtocol)


def test_ensure_task_valid_sources(tmp_path) -> None:
    """Тест того, что ensure_task_source корректно валидирует источники"""
    path = tmp_path / "t.json"
    path.write_text('[{"id": "1", "payload": null}]', encoding="utf-8")

    ensure_task_source(FileTaskSource(path))
    ensure_task_source(GeneratorTaskSource(count=1))
    ensure_task_source(ApiTaskSource(base_url="http://localhost:8000"))


def test_ensure_task_source_raises_for_invalid() -> None:
    """Тест того, что ensure_task_source выбрасывает InvalidTaskSource для объекта без get_tasks"""
    class NotASource:
        pass

    with pytest.raises(InvalidTaskSource):
        ensure_task_source(NotASource())

    with pytest.raises(InvalidTaskSource):
        ensure_task_source(42)


def test_protocol_structural_check_get_tasks_callable() -> None:
    """Тест того, что объект с методом get_tasks удовлетворяет протоколу"""
    class AdHocSource:
        def get_tasks(self):
            return [Task(id="x", payload=None)]

    source = AdHocSource()
    assert isinstance(source, TaskSourceProtocol)
    tasks = list(source.get_tasks())
    assert len(tasks) == 1
    assert tasks[0].id == "x"

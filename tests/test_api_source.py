from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

from task_platform.api.main import app
from task_platform.domain.task import Task
from task_platform.sources.api_source import ApiTaskSource


def test_fastapi_get_tasks_returns_list() -> None:
    """Тест того, что GET эндпоинт /tasks возвращает список задач правильно"""
    with TestClient(app) as client:
        response = client.get("/tasks")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1

    assert all("id" in item and "payload" in item for item in data)


def test_api_source_parses_response() -> None:
    """Тест того, что ApiTaskSource корректно парсит JSON в дата класс Task, полученный из запроса к API"""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"id": "api-1", "payload": {"source": "api"}},
        {"id": "api-2", "payload": None},
    ]
    mock_response.raise_for_status = MagicMock()

    with patch("task_platform.sources.parsers.api_json_parser.httpx") as mock_httpx:
        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_httpx.Client.return_value = mock_client

        source = ApiTaskSource(base_url="http://test")
        tasks = list(source.get_tasks())

    assert len(tasks) == 2
    assert tasks[0] == Task(id="api-1", payload={"source": "api"})
    assert tasks[1] == Task(id="api-2", payload=None)

    mock_client.get.assert_called_once()
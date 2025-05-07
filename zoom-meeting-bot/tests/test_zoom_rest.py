import pytest
from unittest.mock import patch, MagicMock
from src.zoom_rest import ZoomREST

@pytest.fixture(autouse=True)
def mock_auth(monkeypatch):
    class FakeAuth:
        def get_access_token(self): return "fake-token"
    monkeypatch.setattr("src.zoom_rest.ZoomAuth", lambda: FakeAuth())

@patch("src.zoom_rest.requests.post")
def test_create_meeting(mock_post):
    mock_post.return_value = MagicMock(status_code=201, json=lambda: {"id": "1234", "topic": "Test"})
    client = ZoomREST()
    result = client.create_meeting("Test", "2025-05-01T10:00:00Z", 30)
    assert result["id"] == "1234"
    mock_post.assert_called_once()

@patch("src.zoom_rest.requests.get")
def test_get_meetings(mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {"meetings": [{"id":"1"}]})
    client = ZoomREST()
    meetings = client.get_meetings()
    assert len(meetings) == 1
    assert meetings[0]["id"] == "1"

@patch("src.zoom_rest.requests.patch")
def test_update_meeting(mock_patch):
    mock_patch.return_value = MagicMock(status_code=204)
    client = ZoomREST()
    status = client.update_meeting("1234", topic="New")
    assert status == 204

@patch("src.zoom_rest.requests.delete")
def test_delete_meeting(mock_delete):
    mock_delete.return_value = MagicMock(status_code=204)
    client = ZoomREST()
    assert client.delete_meeting("1234") is True
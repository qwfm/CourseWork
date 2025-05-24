import pytest
from unittest.mock import patch, MagicMock
from src.zoom_chat import ZoomChat

@pytest.fixture(autouse=True)
def mock_auth(monkeypatch):
    class FakeAuth:
        def get_access_token(self): return "fake-token"
    monkeypatch.setattr("src.zoom_chat.ZoomAuth", lambda: FakeAuth())

@patch("src.zoom_chat.requests.post")
def test_send_message_to_user(mock_post):
    fake_resp = MagicMock(status_code=201, json=lambda: {"message": "ok"})
    mock_post.return_value = fake_resp

    chat = ZoomChat()
    result = chat.send_message("miner19870@gmail.com", "Hello!")
    assert result == {"message": "ok"}
    mock_post.assert_called_once()
    called_url = mock_post.call_args[0][0]
    assert called_url.endswith("/chat/users/me/messages")
    sent_payload = mock_post.call_args[1]["json"]
    assert sent_payload["to_contact"] == "miner19870@gmail.com"
    assert sent_payload["message"] == "Hello!"

@patch("src.zoom_chat.requests.post")
def test_send_message_to_channel(mock_post):
    fake_resp = MagicMock(status_code=201, json=lambda: {"message": "ok"})
    mock_post.return_value = fake_resp

    chat = ZoomChat()
    result = chat.send_message("2d6fa43ed0ac4a228b997134f8a63407@conference.xmpp.zoom.us", "Announcement")
    assert result == {"message": "ok"}
    sent_payload = mock_post.call_args[1]["json"]
    assert sent_payload["to_channel"] == "2d6fa43ed0ac4a228b997134f8a63407@conference.xmpp.zoom.us"
    assert "to_contact" not in sent_payload
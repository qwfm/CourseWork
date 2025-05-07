import pytest
from unittest.mock import patch
from src.auth import ZoomAuth

@patch("src.auth.requests.post")
def test_get_access_token(mock_post):
    mock_post.return_value.json.return_value = {
        "access_token": "abc123",
        "expires_in":   3600
    }

    auth = ZoomAuth()
    token1 = auth.get_access_token()
    assert token1 == "abc123"

    token2 = auth.get_access_token()
    assert token2 == "abc123"
    assert mock_post.call_count == 1

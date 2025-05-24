import os
import re
import time
import base64
import json
import pytest
'''
from src.zoom_signature import generate_signature

@pytest.fixture(autouse=True)
def env_vars(monkeypatch):
    monkeypatch.setenv("ZOOM_SDK_KEY", "ABC123")
    monkeypatch.setenv("ZOOM_SDK_SECRET", "SECRET456")

def test_signature_structure():
    sig = generate_signature("9876543210", role=1)
    # JWT має дві точки
    assert sig.count(".") == 2

    header_b64, payload_b64, signature_b64 = sig.split(".")

    # Перевіримо, що header розбирається у валідний JSON
    header = json.loads(base64.urlsafe_b64decode(header_b64 + "==").decode())
    assert header["alg"] == "HS256" and header["typ"] == "JWT"

    # Перевіримо, що payload містить коректні поля
    payload = json.loads(base64.urlsafe_b64decode(payload_b64 + "==").decode())
    assert payload["sdkKey"] == "ABC123"
    assert payload["mn"] == "9876543210"
    assert payload["role"] == 1
    assert "iat" in payload and "exp" in payload

    # Підпис — це Base64 URL-safe
    assert re.match(r'^[A-Za-z0-9_-]+$', signature_b64)

def test_signature_changes_with_time():
    sig1 = generate_signature("111", role=0)
    # імітуємо невеликий час
    time.sleep(1)
    sig2 = generate_signature("111", role=0)
    # через різні iat/exp підписи будуть різні
    assert sig1 != sig2
'''
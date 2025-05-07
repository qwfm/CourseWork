import os
import time
import requests
from dotenv import load_dotenv

load_dotenv() 

class ZoomAuth:
    TOKEN_URL = "https://zoom.us/oauth/token"

    def __init__(self):
        self.client_id     = os.getenv("ZOOM_CLIENT_ID")
        self.client_secret = os.getenv("ZOOM_CLIENT_SECRET")
        self.account_id    = os.getenv("ZOOM_ACCOUNT_ID")   
        self._token        = None
        self._expires_at   = 0

    def get_access_token(self) -> str:
        if self._token and time.time() < self._expires_at:
            return self._token

        resp = requests.post(
            self.TOKEN_URL,
            params={
                "grant_type":   "account_credentials",
                "account_id":   self.account_id,
            },
            auth=(self.client_id, self.client_secret)
        )
        data = resp.json()
        if "access_token" not in data:
            raise RuntimeError(f"Не вдалося отримати токен: {data}")

        self._token      = data["access_token"]
        expires_in       = data.get("expires_in", 3600)
        self._expires_at = time.time() + expires_in - 60
        return self._token

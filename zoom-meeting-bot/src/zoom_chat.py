import os
import requests
from .auth import ZoomAuth

class ZoomChat:
    def __init__(self):
        self.auth = ZoomAuth()
        self.base_url = "https://api.zoom.us/v2"

    def _headers(self):
        token = self.auth.get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def send_message(self, to_jid: str, message: str) -> dict:
        url = f"{self.base_url}/chat/users/me/messages"
        payload = {
            "message": message,
            **({"to_contact": to_jid} if "@" in to_jid else {"to_channel": to_jid})
        }
        resp = requests.post(url, headers=self._headers(), json=payload)
        resp.raise_for_status()
        return resp.json()
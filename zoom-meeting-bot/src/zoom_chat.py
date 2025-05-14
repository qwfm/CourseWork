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
    
      # Визначаємо, чи це канал (специфічний домен Zoom для каналів)
      is_channel = to_jid.endswith("@conference.xmpp.zoom.us")
    
      payload = {
        "message": message,
        "to_channel": to_jid if is_channel else None,
        "to_contact": to_jid if not is_channel else None
      }
      # Видаляємо поля з None
      payload = {k: v for k, v in payload.items() if v is not None}
    
      resp = requests.post(url, headers=self._headers(), json=payload)
      resp.raise_for_status()
      return resp.json()
    
    def get_channels(self):
       url = f"{self.base_url}/chat/users/me/channels"
       headers = self._headers() 
       response = requests.get(url, headers=headers)
       response.raise_for_status()
       return response.json().get("channels", [])
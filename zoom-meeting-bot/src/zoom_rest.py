import os
import requests
from .auth import ZoomAuth

class ZoomREST:
    def __init__(self):
        self.auth = ZoomAuth()
        self.base_url = "https://api.zoom.us/v2"

    def _headers(self):
        token = self.auth.get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def create_meeting(self, topic, start_time, duration):
        url = f"{self.base_url}/users/me/meetings"
        payload = {
            "topic": topic,
            "type": 2,  # scheduled meeting
            "start_time": start_time,
            "duration": duration
        }
        resp = requests.post(url, headers=self._headers(), json=payload)
        resp.raise_for_status()
        return resp.json()

    def get_meetings(self):
        url = f"{self.base_url}/users/me/meetings"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json().get("meetings", [])

    def update_meeting(self, meeting_id, **kwargs):
        url = f"{self.base_url}/meetings/{meeting_id}"
        resp = requests.patch(url, headers=self._headers(), json=kwargs)
        resp.raise_for_status()
        return resp.status_code

    def delete_meeting(self, meeting_id):
        url = f"{self.base_url}/meetings/{meeting_id}"
        resp = requests.delete(url, headers=self._headers())
        if resp.status_code == 204:
            return True
        resp.raise_for_status()
        return False

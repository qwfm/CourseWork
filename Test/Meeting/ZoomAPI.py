import requests
import time
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta

class ZoomAPI:
    ACCOUNT_ID = "7z_dbME-RWCq0YGY0aGL4A"
    CLIENT_ID = "0dDJtWOR068fyDveorz9A"
    CLIENT_SECRET = "3gkaH35musm2l9PwSyjFax3hI5XZNibQ"

    def __init__(self):
        self.cached_token = None
        self.token_expiry = 0
    
    def get_access_token(self):
        url = "https://zoom.us/oauth/token"
        payload = {
            "grant_type": "account_credentials",
            "account_id": self.ACCOUNT_ID
        }
    
        response = requests.post(url, auth=(self.CLIENT_ID, self.CLIENT_SECRET), data=payload)
        response_data = response.json()

        if "access_token" in response_data:
            return response_data["access_token"]
        else:
            raise Exception(f"Error getting access token: {response_data}")


    # Функція для скасування зустрічі
    def delete_meeting(self, meeting_id):
        access_token = self.get_access_token()
        url = f"https://api.zoom.us/v2/meetings/{meeting_id}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 204:
            return f"Зустріч {meeting_id} успішно видалена."
        elif response.status_code == 404:
            return f"Помилка: Зустріч {meeting_id} не знайдена."
        else:
            return f"Помилка при видаленні: {response.json()}"

    def create_meeting(
        self, topic="Test Meeting", start_time="2025-02-15T15:00:00Z", duration=45
    ):
        """Створення зустрічі в Zoom."""
        access_token = self.get_access_token()
        url = "https://api.zoom.us/v2/users/me/meetings"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "topic": topic,
            "type": 2,
            "start_time": start_time,
            "duration": duration,
            "timezone": "Europe/Madrid",
            "agenda": "Test meeting",
            "settings": {
                "host_video": True,
                "participant_video": True,
                "join_before_host": False,
                "mute_upon_entry": True,
                "watermark": True,
                "audio": "voip",
                "auto_recording": "cloud",
            },
        }
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        if "join_url" in response_data:
            event_details = {
            "join_url": response_data['join_url'],
            "title": "Zoom Meeting",
            "start_time": start_time,
            "duration": duration
            }  
            self.create_calendar_event(event_details)
            return f"Конференція створена! Приєднатися: {response_data['join_url']}\nПароль: {response_data.get('password', 'N/A')}"
        else:
            return f"Помилка створення зустрічі: {response_data}"

    def get_scheduled_meetings(self):
        """Отримання списку запланованих зустрічей."""
        access_token = self.get_access_token()
        url = "https://api.zoom.us/v2/users/me/meetings"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        response_data = response.json()
        if "meetings" in response_data:
            meetings = response_data["meetings"]
            if not meetings:
                return "Немає запланованих зустрічей."
            result = "Заплановані зустрічі:\n"
            for meeting in meetings:
                result += f"- {meeting['topic']} | {meeting['start_time']} | {meeting.get('join_url', 'N/A')}\n"
            return result
        else:
            return f"Помилка отримання зустрічей: {response_data}"

    # Функція для скасування зустрічі
    def delete_meeting(self, meeting_id):
        access_token = self.get_access_token()
        url = f"https://api.zoom.us/v2/meetings/{meeting_id}"
    
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
        response = requests.delete(url, headers=headers)
    
        if response.status_code == 204:
            return f"Зустріч {meeting_id} успішно видалена."
        elif response.status_code == 404:
            return f"Помилка: Зустріч {meeting_id} не знайдена."
        else:
            return f"Помилка при видаленні: {response.json()}"
    
    def create_calendar_event(self, event_details):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        service = build('calendar', 'v3', credentials=creds)

        # Парсимо start_time
        start_dt = datetime.strptime(event_details["start_time"], "%Y-%m-%dT%H:%M:%SZ")
        end_dt = start_dt + timedelta(minutes=event_details["duration"])

        # Перетворимо назад у строку у форматі ISO 8601
        start_time_str = start_dt.isoformat() + "Z"
        end_time_str = end_dt.isoformat() + "Z"

        event = {
            'summary': event_details["title"],
            'description': f"Join Zoom Meeting: {event_details['join_url']}",
            'start': {'dateTime': start_time_str, 'timeZone': 'Europe/Kiev'},
            'end': {'dateTime': end_time_str, 'timeZone': 'Europe/Kiev'},
        }

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        return created_event.get('id')


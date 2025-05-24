import os
import webbrowser
from dotenv import load_dotenv
import shlex
from src.zoom_rest import ZoomREST
from src.zoom_chat import ZoomChat
from datetime import datetime
load_dotenv()  

class CommandHandler:
    def __init__(self):
        self.zoom_rest = ZoomREST()
        self.zoom_chat = ZoomChat()
        self.ngrok_domain = os.getenv("NGROK_DOMAIN")

    def handle_create(self, args):
        date_str = args.date  
        try:
            dt = datetime.strptime(date_str, '%d.%m.%Y %H:%M')
        except ValueError:
            print("Невірний формат дати. Очікується 'ДД.MM.РРРР ГГ:ХХ'")
            return
        iso_date = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        print(f"Отримана дата: {iso_date}")

    def handle_get(self, args):
        """Отримати список зустрічей: get"""
        meetings = self.zoom_rest.get_meetings()
        if not meetings:
            print("No meetings found.")
        else:
            for m in meetings:
                print(f"- ID: {m['id']}, Topic: {m['topic']}, Time: {m['start_time']}")

    def handle_update(self, args):
        """Редагувати зустріч: update <meeting_id> <new_topic>"""
        if len(args) < 2:
            print("Usage: update <meeting_id> <new_topic>")
            return
        meeting_id, new_topic = args[0], args[1]
        status = self.zoom_rest.update_meeting(meeting_id, topic=new_topic)
        print("Update status code:", status)

    def handle_delete(self, args):
        """Видалити зустріч: delete <meeting_id>"""
        if len(args) < 1:
            print("Usage: delete <meeting_id>")
            return
        meeting_id = args[0]
        ok = self.zoom_rest.delete_meeting(meeting_id)
        print("Deleted" if ok else "Failed to delete")

    def handle_chat(self, args):
       if len(args) < 2:
         print("Usage: chat <to> <message> [--schedule YYYY-MM-DDTHH:MM:SS]")
         return

       # Парсинг аргументів
       schedule_time = None
       if "--schedule" in args:
        try:
            schedule_index = args.index("--schedule")
            schedule_time = args[schedule_index + 1]
            args = args[:schedule_index] + args[schedule_index + 2:]
        except IndexError:
            print("Invalid schedule time format")
            return

       to_jid, message = args[0], " ".join(args[1:])
    
       # Відправка
       if schedule_time:
        self._schedule_message(to_jid, message, schedule_time)
        print(f"Message scheduled for {schedule_time}")
       else:
        resp = self.zoom_chat.send_message(to_jid, message)
        print("Sent immediately:", resp)
        
    def handle_get_channels(self, args=None):
        """Отримати список каналів: get_channels"""
        try:
            channels = self.zoom_chat.get_channels()
            if not channels:
                print("No channels found.")
                return
                
            for ch in channels:
                print(f"- Name: {ch.get('name', 'N/A')}, JID: {ch.get('jid', 'N/A')}")
                
        except Exception as e:
            print(f"Error: {str(e)}")

    def _schedule_message(self, to_jid, message, schedule_time):
      """Додає повідомлення в чергу з таймером"""
      from datetime import datetime, timezone
      from threading import Timer
    
      try:
        scheduled = datetime.fromisoformat(schedule_time).astimezone(timezone.utc)
        now = datetime.now(timezone.utc)
        delay = (scheduled - now).total_seconds()
        
        if delay < 0:
            print("Cannot schedule in past. Sending now.")
            self.zoom_chat.send_message(to_jid, message)
            return
            
        Timer(delay, self.zoom_chat.send_message, args=(to_jid, message)).start()
        
      except ValueError as e:
        print(f"Invalid time format: {e}. Use ISO 8601 (e.g. 2023-12-31T23:59:00+02:00)")

    def handle_join(self, args):
        """Приєднатися до конференції як бот: join <meeting_id>"""
        if len(args) < 1:
            print("Usage: join <meeting_id>")
            return
        meeting_id = args[0]

        all_meetings = self.zoom_rest.get_meetings()
        meeting = next((m for m in all_meetings if str(m['id']) == str(meeting_id)), None)

        if not meeting:
            print(f"Meeting {meeting_id} not found.")
            return

        join_url = meeting.get("join_url")
        if not join_url:
            print("No join_url available for this meeting.")
            return

        print("Opening Zoom join URL:", join_url)
        webbrowser.open(join_url)


    def handle_help(self, args=None):
        print("Available commands:")
        print("  get_channels")
        print("  create <topic> <start_time> <duration>")
        print("  get")
        print("  update <meeting_id> <new_topic>")
        print("  delete <meeting_id>")
        print("  chat <to_jid_or_channel> <message>")
        print("  join <meeting_id>")
        print("  help")
        print("  exit")

    def execute(self, line):
        parts = shlex.split(line)
        if not parts:
            return
        cmd, args = parts[0].lower(), parts[1:]
        handler = {
            "get_channels": self.handle_get_channels,
            "create": self.handle_create,
            "get":    self.handle_get,
            "update": self.handle_update,
            "delete": self.handle_delete,
            "chat":   self.handle_chat,
            "join":   self.handle_join,
            "help":   self.handle_help,
            "exit":   None
        }.get(cmd)

        if handler:
            handler(args)
        elif cmd == "exit":
            print("Exiting bot.")
            exit(0)
        else:
            print(f"Unknown command: {cmd}. Type 'help' for list of commands.")

def main():
    print("Zoom Meeting Bot CLI")
    handler = CommandHandler()
    handler.handle_help()
    while True:
        try:
            line = input("> ")
            handler.execute(line)
        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
            break
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
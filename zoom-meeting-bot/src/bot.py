import os
import webbrowser
from dotenv import load_dotenv
import shlex
import re
from datetime import datetime, timezone
from threading import Timer
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
        """
        chat <to> <message words...> [дд.мм.рррр гг:хх]
        Якщо в кінці є валідні дата+час у форматі дд.мм.рррр гг:хх –
        буде планування в локальній зоні.
        """
        if len(args) < 2:
            print("Usage: chat <to> <message> [дд.мм.рррр гг:хх]")
            return

        schedule_dt = None
        date_pat = re.compile(r'^\d{2}\.\d{2}\.\d{4}$')
        time_pat = re.compile(r'^\d{2}:\d{2}$')

        if len(args) >= 3 and date_pat.match(args[-2]) and time_pat.match(args[-1]):
            ds, ts = args[-2], args[-1]
            try:
                local_dt = datetime.strptime(f"{ds} {ts}", "%d.%m.%Y %H:%M")
                local_tz = datetime.now().astimezone().tzinfo
                local_dt = local_dt.replace(tzinfo=local_tz)
                schedule_dt = local_dt.astimezone(timezone.utc)
                args = args[:-2]
            except ValueError:
                print("Невірний формат дати/часу. Використовуйте дд.мм.рррр гг:хх")
                return

        to_jid = args[0]
        message = " ".join(args[1:])

        if schedule_dt:
            self._schedule_message(to_jid, message, schedule_dt)
            print("Повідомлення заплановано на",
                  schedule_dt.astimezone().strftime("%d.%m.%Y %H:%M"))
        else:
            resp = self.zoom_chat.send_message(to_jid, message)
            print("Відправлено негайно:", resp)

    def _schedule_message(self, to_jid, message, utc_dt):
        """Планує виклик send_message у заданий UTC-час."""
        now_utc = datetime.now(timezone.utc)
        delay = (utc_dt - now_utc).total_seconds()
        if delay <= 0:
            print("Час у минулому — надсилаю зараз.")
            self.zoom_chat.send_message(to_jid, message)
        else:
            Timer(delay, lambda: self.zoom_chat.send_message(to_jid, message)).start()
        
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
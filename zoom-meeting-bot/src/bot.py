import os
import webbrowser
from dotenv import load_dotenv
import shlex
from src.zoom_rest import ZoomREST
from src.zoom_chat import ZoomChat
from src.zoom_signature import generate_signature

load_dotenv()  

class CommandHandler:
    def __init__(self):
        self.zoom_rest = ZoomREST()
        self.zoom_chat = ZoomChat()
        self.ngrok_domain = os.getenv("NGROK_DOMAIN")
        self.sdk_key = os.getenv("ZOOM_SDK_KEY")

    def handle_create(self, args):
        """Створити зустріч: create <topic> <start_time> <duration>"""
        if len(args) < 3:
            print("Usage: create <topic> <start_time> <duration>")
            return
        topic, start, dur = args[0], args[1], args[2]
        result = self.zoom_rest.create_meeting(topic, start, int(dur))
        print("Meeting created:", result.get("id"), result.get("join_url"))

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
        """Надіслати повідомлення в Team Chat: chat <to_jid_or_channel> <message>"""
        if len(args) < 2:
            print("Usage: chat <to_jid_or_channel> <message>")
            return
        to_jid, message = args[0], " ".join(args[1:])
        resp = self.zoom_chat.send_message(to_jid, message)
        print("Chat response:", resp)

    def handle_join(self, args):
        """Приєднатися до конференції як бот: join <meeting_id>"""
        if len(args) < 1:
            print("Usage: join <meeting_id>")
            return
        meeting_id = args[0]
        sig = generate_signature(meeting_id, role=0)
        url = (
            f"https://{self.ngrok_domain}/meeting_client/index.html"
            f"?mn={meeting_id}&sig={sig}&sdkKey={self.sdk_key}"
        )
        print("Opening meeting client at:", url)
        webbrowser.open(url)

    def handle_help(self, args=None):
        print("Available commands:")
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
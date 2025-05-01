from ZoomAPI import ZoomAPI

class CommandHandler:
    def __init__(self, zoom_api):
        self.zoom_api = zoom_api
        self.commands = {
            "create_meeting": self.handle_create_meeting,
            "get_meetings": self.handle_get_meetings,
            "delete_meeting": self.handle_delete_meeting,
            "help": self.handle_help,
            "exit": self.handle_exit,
        }
        self.exit_flag = False

    def handle_create_meeting(self, args=None):
        print("Створюємо зустріч...")
        result = self.zoom_api.create_meeting()
        print(result)

    def handle_get_meetings(self, args=None):
        print("Отримуємо список запланованих зустрічей...")
        result = self.zoom_api.get_scheduled_meetings()
        print(result)

    def handle_delete_meeting(self, args):
        if not args or len(args) < 1:
            print("Помилка: вкажіть ID зустрічі для видалення.")
            return
        meeting_id = args[0]
        print(f"Видаляємо зустріч {meeting_id}...")
        result = self.zoom_api.delete_meeting(meeting_id)
        print(result)

    def handle_help(self, args=None):
        print("Доступні команди:")
        for cmd in self.commands.keys():
            print(f"- {cmd}")

    def handle_exit(self, args=None):
        print("Завершення роботи.")
        self.exit_flag = True

    def execute_command(self, command_line):
        if not command_line:
            return
        parts = command_line.strip().split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd in self.commands:
            self.commands[cmd](args)
        else:
            print(f"Команда '{cmd}' не розпізнана. Напишіть 'help' для списку команд.")

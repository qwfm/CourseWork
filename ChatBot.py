from ZoomAPI import ZoomAPI
from CommandHandler import CommandHandler 

class ChatBot:
    def __init__(self):
        self.zoom_api = ZoomAPI()
        self.command_handler = CommandHandler(self.zoom_api)

    def run(self):
        print("Чат-бот Zoom. Введіть команду ('help' - список команд, 'exit' - вийти)")
        
        while True:
            try:
                command_line = input("Ви: ").strip()
                if command_line.lower() == "exit":
                    print("Бот завершує роботу.")
                    break
                elif command_line.lower() == "help":
                    self.show_help()
                else:
                    self.command_handler.execute_command(command_line)
            except Exception as e:
                print(f"Помилка: {e}")

    def show_help(self):
        print("Доступні команди:")
        print("- create_meeting [тема] [час] [тривалість] - створити зустріч")
        print("- delete_meeting [meeting_id] - скасувати зустріч")
        print("- get_meetings - отримати список запланованих зустрічей")
        print("- exit - завершити роботу бота")
        
        
if __name__ == "__main__":
    bot = ChatBot()
    bot.run()

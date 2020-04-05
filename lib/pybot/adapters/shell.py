from os import environ as env

from ..adapter import Adapter
from ..messages import Message
from ..user import User


class ShellAdapter(Adapter):
    def send(self, message, text):
        print(text)

    def emote(self, message, text):
        self.send(message, f"* {text}")

    def reply(self, message, text):
        self.send(message, f"{message.user.name}: {text}")

    def run(self):
        name = env.get("PYBOT_SHELL_USER_NAME", "Shell")

        try:
            user_id = env.get("PYBOT_SHELL_USER_ID")
        except ValueError:
            user_id = 1

        self.robot.emit("connected")

        while True:
            try:
                text = input(f"{self.robot.name}> ")
            except EOFError:
                print()
                break

            if text == "quit":
                break

            user = User(user_id, name)
            message = Message(user, "shell", text)
            self.receive(message)

        self.robot.emit("disconnected")
        self.robot.shutdown()

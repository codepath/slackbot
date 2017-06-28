from os import environ as env

from six import print_
from six.moves import input

from ..adapter import Adapter
from ..messages import Message
from ..user import User


class ShellAdapter(Adapter):
    def send(self, message, text):
        print_(text)

    def emote(self, message, text):
        self.send(message, '* {}'.format(text))

    def reply(self, message, text):
        self.send(message, '{}: {}'.format(message.user.name, text))

    def run(self):
        name = env.get('PYBOT_SHELL_USER_NAME', 'Shell')

        try:
            user_id = env.get('PYBOT_SHELL_USER_ID')
        except ValueError:
            user_id = 1

        self.robot.emit('connected')

        while True:
            try:
                text = input('{}> '.format(self.robot.name))
            except EOFError:
                print
                break

            if text == 'quit':
                break

            user = User(user_id, name)
            message = Message(user, 'shell', text)
            self.receive(message)

        self.robot.emit('disconnected')
        self.robot.shutdown()

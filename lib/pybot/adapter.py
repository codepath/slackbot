class Adapter(object):
    def __init__(self, robot):
        self.robot = robot

    def send(self, message, text):
        pass

    def emote(self, message, text):
        self.send(message, text)

    def reply(self, message, text):
        pass

    def topic(self, message, text):
        pass

    def play(self, message, text):
        pass

    def run(self):
        pass

    def close(self):
        pass

    def receive(self, text):
        self.robot.receive(text)

class Response(object):
    def __init__(self, robot, message, match):
        self.robot = robot
        self.message = message
        self.match = match

    def send(self, text):
        self.robot.adapter.send(self.message, text)

    def emote(self, text):
        self.robot.adapter.emote(self.message, text)

    def reply(self, text):
        self.robot.adapter.reply(self.message, text)

    def topic(self, text):
        self.robot.adapter.topic(self.message, text)

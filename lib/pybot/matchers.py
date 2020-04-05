import re


class Matcher:
    def match(self, message):
        pass


class RegexMatcher(Matcher):
    def __init__(self, pattern):
        self.regex = re.compile(pattern, re.IGNORECASE)

    def match(self, message):
        if message.text:
            return self.regex.search(message.text)


class RobotNameMatcher(Matcher):
    def __init__(self, wrapped, robot):
        self.wrapped = wrapped
        self.robot = robot

    def match(self, message):
        if message.was_sent_to(self.robot.name):
            return self.wrapped.match(message)

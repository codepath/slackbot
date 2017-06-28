from .response import Response


class Listener(object):
    def __init__(self, robot, matcher, func):
        self.robot = robot
        self.matcher = matcher
        self.func = func

    def __call__(self, message):
        match = self.matcher.match(message)
        if not match:
            return False

        response = Response(self.robot, message, match)
        self.func(response)
        return True

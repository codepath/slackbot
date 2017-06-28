import traceback

from .adapters import ShellAdapter
from .events import EventBus
from .listener import Listener
from .matchers import RegexMatcher, RobotNameMatcher
from .messages import Message


class Robot(object):
    def __init__(self, name='Pybot'):
        self.name = name
        self._load_adapter()
        self._listeners = []
        self._bus = EventBus()

    def _load_adapter(self):
        # TODO: dynamically load the adapter based on args
        # TODO: catch all errors and exit if failure to load
        self.adapter = ShellAdapter(self)

    def run(self):
        self.adapter.run()

    def shutdown(self):
        self.adapter.close()

    def send(self, room, text):
        fake_message = Message(None, room, None)
        self.adapter.send(fake_message, text)

    def reply(self, user, room, text):
        fake_message = Message(user, room, None)
        self.adapter.reply(fake_message, text)

    def on(self, type):
        def wrapper(f):
            self._bus.subscribe(type, f)
            return f

        return wrapper

    def emit(self, type, data=None):
        self._bus.publish(type, data)

    def receive(self, message):
        for listener in self._listeners:
            try:
                listener(message)
            except:
                traceback.print_exc()


    def respond(self, pattern):
        def wrapper(f):
            matcher = RegexMatcher(pattern)
            wrapper = RobotNameMatcher(matcher, self)
            self._add_listener(wrapper, f)

        return wrapper

    def hear(self, pattern):
        def wrapper(f):
            matcher = RegexMatcher(pattern)
            self._add_listener(matcher, f)
            return f

        return wrapper

    def listen(self, matcher):
        def wrapper(f):
            self._add_listener(matcher, f)
            return f

        return wrapper

    def _add_listener(self, matcher, func):
        listener = Listener(self, matcher, func)
        self._listeners.append(listener)

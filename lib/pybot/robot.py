import traceback

from .adapters import ShellAdapter
from .events import EventBus
from .listener import Listener
from .matchers import RegexMatcher
from .matchers import RobotNameMatcher
from .messages import Message
from .response import Response


class Robot:
    def __init__(self, name="Pybot"):
        self.name = name
        self._load_adapter()
        self._listeners = []
        self._bus = EventBus()
        self._catch_all_handler = None

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
        any_match = any(self._call_listener(l, message) for l in self._listeners)

        if not any_match and self._catch_all_handler:
            if message.was_sent_to(self.name):
                response = Response(self, message, None)
                self._catch_all_handler(response)

        self.emit(
            "processed", {"message": message, "was_match": any_match},
        )

    def catch_all(self, f):
        if self._catch_all_handler:
            raise RuntimeError(
                "Attempting to register more than one catch-all handler",
            )

        self._catch_all_handler = f
        return f

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

    def _call_listener(self, listener, message):
        try:
            return listener(message)
        except Exception:
            traceback.print_exc()

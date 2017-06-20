from collections import defaultdict


class EventBus(object):
    def __init__(self):
        self._listeners = defaultdict(list)

    def publish(self, type, data=None):
        for listener in self._listeners[type]:
            listener(data)

    def subscribe(self, type, f):
        listeners = self._listeners[type]
        if f not in listeners:
            listeners.append(f)

    def unsubscribe(self, type, f):
        self._listeners[type].remove(f)

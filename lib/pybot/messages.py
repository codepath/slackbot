class Message(object):
    def __init__(self, user, room, text, id=None):
        self.user = user
        self.room = room
        self.text = text
        self.id = id

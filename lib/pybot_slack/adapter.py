from os import environ as env
from time import sleep

from slackclient import SlackClient

from lib.pybot import Adapter
from lib.pybot import Message


class SlackAdapter(Adapter):
    def __init__(self, robot):
        super().__init__(robot)

        token = env.get("PYBOT_SLACK_TOKEN")
        if not token:
            raise RuntimeError("Missing environment variable PYBOT_SLACK_TOKEN")

        self.bot_id = None
        self.client = SlackClient(token)

    def send(self, message, text):
        self._send_message(message.room, text)

    def reply(self, message, text):
        thread = None
        if not self._is_direct_message(message.room):
            text = f"<@{message.user.id}>: {text}"
            thread = message.thread_id

        self._send_message(message.room, text, thread)

    def run(self):
        if not self.client.rtm_connect():
            # TODO: use logger once implemented
            print("error: unable to connect to RTM service")
            return

        self._initialize()
        self._loop_forever()

    def _loop_forever(self):
        while True:
            events = self.client.rtm_read()
            if events:
                self._dispatch(events)

            sleep(0.1)

    def _initialize(self):
        name = self.client.server.username
        user = self._find_user(name)

        self.bot_id = user.id
        self.robot.name = user.name

        self.robot.emit("connected")

    def _dispatch(self, events):
        for event in events:
            type = event.get("type")
            if not type:
                continue

            # Ignore any events sent by the bot
            user = self._user_from_event(event)
            if user and user.id == self.bot_id:
                continue

            message = None
            if type == "message":
                # TODO: implement other interesting subtypes
                subtype = event.get("subtype") or "message"
                if subtype == "message":
                    message = self._adapt_message(user, event)

            if message:
                self.receive(message)

    def _adapt_message(self, user, event):
        channel_id = event["channel"]
        text = event["text"]
        ts = event["ts"]
        thread_ts = event.get("thread_ts", ts)
        is_direct_message = self._is_direct_message(channel_id)

        if is_direct_message:
            # Pretend they mentioned the robot's name
            text = f"{self.robot.name} {text}"

        # TODO: chat threads
        return Message(
            user=user,
            room=channel_id,
            text=text,
            id=ts,
            thread_id=thread_ts,
            is_direct_message=is_direct_message,
        )

    def _user_from_event(self, event):
        user = event.get("user")
        if isinstance(user, dict):
            # In certain events, the user value of the event
            # will be the entire user instead of an ID.
            user = user.get("id")

        return self._find_user(user)

    def _send_message(self, channel_id, text, thread=None):
        self.client.rtm_send_message(channel_id, text, thread)

    def _find_user(self, name_or_id):
        return self.client.server.users.find(name_or_id)

    @staticmethod
    def _is_direct_message(channel_id):
        return (channel_id or "").startswith("D")

from os import environ as env
from time import sleep

from lib.pybot import robot, User, Message, Adapter
from slackclient import SlackClient


class SlackAdapter(Adapter):
    def __init__(self, robot):
        super(SlackAdapter, self).__init__(robot)

        token = env.get('PYBOT_SLACK_TOKEN')
        if not token:
            raise RuntimeError("Missing environment variable PYBOT_SLACK_TOKEN")

        self.bot_id = None
        self.client = SlackClient(token)

    def send(self, message, text):
        self._send_message(message.room, text)

    def reply(self, message, text):
        if not self._is_direct_message(message.room):
            text = u'<@{}>: {}'.format(message.user.id, text)

        self._send_message(message.room, text)

    def run(self):
        if not self.client.rtm_connect():
            # TODO: use logger once implemented
            print "error: unable to connect to RTM service"
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

        self.robot.emit('connected')

    def _dispatch(self, events):
        for event in events:
            type = event.get('type')
            if not type:
                continue

            # Ignore any events sent by the bot
            user_id = event.get('user')
            user = self._find_user(user_id)
            if user_id and user_id == self.bot_id:
                continue

            message = None
            if type == 'message':
                # TODO: implement other interesting subtypes
                subtype = event.get('subtype') or 'message'
                if subtype == 'message':
                    message = self._adapt_message(user, event)

            if message:
                self.receive(message)

    def _adapt_message(self, user, event):
        channel_id = event['channel']
        text = event['text']
        ts = event['ts']

        if self._is_direct_message(channel_id):
            # Pretend they mentioned the robot's name
            text = u'{} {}'.format(self.robot.name, text)

        # TODO: chat threads
        return Message(user, channel_id, text, ts)

    def _send_message(self, channel_id, text):
        self.client.rtm_send_message(channel_id, text)

    def _find_user(self, name_or_id):
        return self.client.server.users.find(name_or_id)

    @staticmethod
    def _is_direct_message(channel_id):
        return (channel_id or '').startswith('D')

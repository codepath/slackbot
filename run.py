#!/usr/bin/python

from os import environ as env

from lib.pybot import robot
from lib.pybot_slack import SlackAdapter

from bot.capabilities import *
from bot.utils import (
    DEVELOPMENT,
    PRODUCTION,
    SLACKBOT_TOKENS
)


if __name__ == '__main__':
    mode = PRODUCTION if env.get(PRODUCTION) else DEVELOPMENT
    env['PYBOT_SLACK_TOKEN'] = SLACKBOT_TOKENS[mode]

    robot.adapter = SlackAdapter(robot)
    robot.run()

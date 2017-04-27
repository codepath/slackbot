#!/usr/bin/env python

from os import environ as env

from pybot import robot
from pybot_slack import SlackAdapter

from bot.capabilities import *


if __name__ == '__main__':
    if env.get('PRODUCTION'):
        robot.adapter = SlackAdapter(robot)

    robot.run()

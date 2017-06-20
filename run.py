#!/usr/bin/python

from os import environ as env

from lib.pybot import robot
from lib.pybot_slack import SlackAdapter

from bot.capabilities import *


if __name__ == '__main__':
    if env.get('PRODUCTION'):
        robot.adapter = SlackAdapter(robot)

    robot.run()

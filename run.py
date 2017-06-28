#!/usr/bin/python

from os import environ as env

from lib.pybot.robot import Robot
from lib.pybot_slack import SlackAdapter

from bot.capabilities import *
from bot.model import database


if __name__ == '__main__':
    robot = Robot(post_response_funcs=[database.bot_usage])
    if env.get('PRODUCTION'):
        robot.adapter = SlackAdapter(robot)

    robot.run()

#!/usr/bin/python

from os import environ as env

from lib.pybot.robot import Robot
from lib.pybot_slack import SlackAdapter

from bot.capabilities import *
from models.metric import Metric


if __name__ == '__main__':
    robot = Robot(post_response_funcs=[Metric.insert])
    if env.get('PRODUCTION'):
        robot.adapter = SlackAdapter(robot)

    robot.run()

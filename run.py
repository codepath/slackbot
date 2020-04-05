#!/usr/bin/python
from lib.pybot import robot
from lib.pybot_slack import SlackAdapter
from os import environ as env

from bot.capabilities import *  # noqa:F403,F401
from models.metric import Metric


@robot.on("processed")
def record_metrics(data):
    Metric.insert(data["message"], data["was_match"])


if __name__ == "__main__":
    if env.get("PRODUCTION"):
        robot.adapter = SlackAdapter(robot)

    robot.run()

from os import environ as env

from pybot import robot

from bot.model import database
from bot.utils import (
    render_template,
    DEVELOPMENT,
    PRODUCTION,
    SLACKBOT
)
from models.metric import Metric

MODE = PRODUCTION if env.get(PRODUCTION) else DEVELOPMENT


@robot.hear(r"^({})? help$".format(SLACKBOT[MODE]))
def help(res):
    if res.message.room.startswith('C') and not res.match.group(0).startswith(
            '{}'.format(SLACKBOT[MODE])):
        return

    if MODE == PRODUCTION:
        # Log the message
        Metric.insert(res.message)

    response = render_template('help')
    res.send(response)

from pybot import robot

from bot.model import database
from bot.utils import render_template


@robot.hear(r"help")
def help(res):
    response = render_template('help')
    res.send(response)


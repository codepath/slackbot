from pybot import robot

from fred.model import database
from fred.utils import render_template


@robot.hear(r"help")
def help(res):
    response = render_template('help')
    res.send(response)


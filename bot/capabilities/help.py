from pybot import robot

from bot.model import database
from bot.utils import render_template


@robot.hear(r"^(fred)? help$")
def help(res):
    if res.message.room.startswith('C') and not res.match.group(0).startswith('fred'):
        return

    response = render_template('help')
    res.send(response)

from .middleware import channel_response_deprecated
from bot.utils import render_template
from lib.pybot import robot


@robot.respond(r"(help|hi|hello)$")
@channel_response_deprecated
def help(res):
    response = render_template("help")
    res.reply(response)

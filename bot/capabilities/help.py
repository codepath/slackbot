from bot.utils import render_template
from lib.pybot import robot


@robot.respond(r"(help|hi|hello)$")
def help(res):
    response = render_template("help")
    res.reply(response)

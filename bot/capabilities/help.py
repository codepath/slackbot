from lib.pybot import robot

from bot.utils import render_template


@robot.respond(r"(help|hi|hello)$")
def help(res):
    response = render_template("help")
    res.reply(response)

from .middleware import channel_response_deprecated
from lib.pybot import robot


@robot.catch_all
@channel_response_deprecated
def catch_all(res):
    res.reply(f"Sorry, I don't understand that. Try '{res.robot.name} help'")

from lib.pybot import robot


@robot.catch_all
def catch_all(res):
    res.reply(f"Sorry, I don't understand that. Try '{res.robot.name} help'")

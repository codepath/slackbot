from lib.pybot import robot


@robot.catch_all
def catch_all(res):
    res.reply("Sorry, I don't understand that. Try '%s help'" % res.robot.name)

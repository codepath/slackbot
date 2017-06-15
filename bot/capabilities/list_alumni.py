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


@robot.hear(r"^({})? alumni at (.*)$".format(SLACKBOT[MODE]))
def list_alumni(res):
    if res.message.room.startswith('C') and not res.match.group(0).startswith(
            '{}'.format(SLACKBOT[MODE])):
        return

    if MODE == PRODUCTION:
        # Log the message
        Metric.insert(res.message)

    company_name = res.match.group(2)
    users = database.company_alumns(company_name, filter_hiring=False)
    is_hiring = any(u['is_hiring'] for u in users)

    response = render_template(
        'alumni_at_company',
        company=company_name,
        users=users,
        is_hiring=is_hiring
    )

    res.send(response)

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


@robot.hear(r"^({})? who is hiring(?: at (.*))?$".format(SLACKBOT[MODE]))
def list_hiring_companies(res):
    if res.message.room.startswith('C') and not res.match.group(0).startswith(
            '{}'.format(SLACKBOT[MODE])):
        return

    if MODE == PRODUCTION:
        # Log the message
        Metric.insert(res.message)

    company_name = res.match.group(2)

    if company_name:
        users = database.company_alumns(company_name, filter_hiring=True)
        response = render_template('whos_hiring_at_company', company=company_name, users=users)
    else:
        companies = database.hiring_companies()
        response = render_template('whos_hiring', companies=companies)

    res.send(response)

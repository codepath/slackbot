from pybot import robot

from bot.model import database
from bot.utils import render_template


@robot.hear(r"(fred)? who is hiring(?: at (.*))?")
def list_hiring_companies(res):
    if res.message.room.startswith('C') and not res.match.group(0).startswith('fred'):
        return

    res.match.groups()
    company_name = res.match.group(2)

    if company_name:
        users = database.company_alumns(company_name, filter_hiring=True)
        response = render_template('whos_hiring_at_company', company=company_name, users=users)
    else:
        companies = database.hiring_companies()
        response = render_template('whos_hiring', companies=companies)

    res.send(response)

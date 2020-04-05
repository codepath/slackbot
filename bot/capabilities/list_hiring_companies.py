from bot.model import database
from bot.utils import render_template
from lib.pybot import robot


@robot.respond(r"who is hiring(?: at (.*))?")
def list_hiring_companies(res):
    company_name = res.match.group(1)

    if company_name:
        users = database.company_alumns(company_name, filter_hiring=True)
        response = render_template(
            "whos_hiring_at_company", company=company_name, users=users,
        )
    else:
        companies = database.hiring_companies()
        response = render_template("whos_hiring", companies=companies)

    res.reply(response)

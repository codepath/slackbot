from lib.pybot import robot

from bot.model import database
from bot.utils import render_template


@robot.respond(r"alumni at (.*)")
def list_alumni(res):
    company_name = res.match.group(1)
    users = database.company_alumns(company_name, filter_hiring=False)
    is_hiring = any(u['is_hiring'] for u in users)

    response = render_template(
        'alumni_at_company',
        company=company_name,
        users=users,
        is_hiring=is_hiring
    )

    res.reply(response)

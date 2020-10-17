from .middleware import channel_response_deprecated
from bot.model import database
from bot.utils import render_template
from lib.pybot import robot


@robot.respond(r"alumni at (.*)")
@channel_response_deprecated
def list_alumni(res):
    company_name = res.match.group(1)
    users = database.company_alumns(company_name, filter_hiring=False)
    is_hiring = any(u["is_hiring"] for u in users)

    response = render_template(
        "alumni_at_company", company=company_name, users=users, is_hiring=is_hiring,
    )

    res.reply(response)

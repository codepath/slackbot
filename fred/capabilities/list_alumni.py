from pybot import robot

from fred.model import database
from fred.utils import render_template


@robot.hear(r"alumni at (.*)")
def list_alumni(res):
    company_name = res.match(1)
    users = database.company_alumns(company_name, filter_hiring=False)
    is_hiring = any(u['is_hiring'] for u in users)

    response = render_template(
        'alumni_at_company',
        company=company_name,
        users=users,
        is_hiring=is_hiring
    )

    res.send(response)

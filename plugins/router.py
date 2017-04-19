from jinja2 import Template
from rtmbot.core import Plugin

from model import database

from pprint import pprint

def _render_template(template_id, **kwargs):
    with open('templates/{}.slack'.format(template_id)) as f:
        template = Template(''.join(f.readlines()))

    return template.render(**kwargs)


def whos_hiring():
    companies = database.hiring_companies()
    return _render_template('whos_hiring', companies=companies)


def whos_hiring_at_company(company_name):
    users = database.company_alumns(company_name, filter_hiring=True)
    return _render_template('whos_hiring_at_company', company=company_name, users=users)


def alumni_at_company(company_name):
    users = database.company_alumns(company_name, filter_hiring=False)
    is_hiring = any(u['is_hiring'] for u in users)
    print users

    return _render_template(
        'alumni_at_company',
        company=company_name,
        users=users,
        is_hiring=is_hiring
    )


def match(template, text):
    # returns a tuple of (bool, dict) where the first value is
    # whether or not there was a match and the second value is
    # the data that was matched
    vars = {}
    template_tokens = template.split(' ')
    text_tokens = text.split(' ')

    if len(template_tokens) != len(text_tokens):
        return False, None

    for template_token, text_token in zip(template_tokens, text_tokens):
        if template_token.startswith('{'):
            key = template_token[1:-1]
            vars[key] = text_token
        elif template_token != text_token:
            return False, None

    return True, vars


class RoutingPlugin(Plugin):
    routes = {
        'alumni at {company_name}': alumni_at_company,
        'whos hiring at {company_name}': whos_hiring_at_company,
        'whos hiring': whos_hiring,
    }

    def process_message(self, data):
        # TODO: do we want to support edits? These come in as a diff format
        # TODO: some sort of warmup period to ignore initial messages in mailbox?
        print data
        text = data.get('text')
        if not text:
            return

        text = text.strip().lower()
        for trigger, func in self.routes.iteritems():
            matches, vars = match(trigger, text)
            if matches:
                response = func(**vars)
                if response:
                    self.outputs.append([data['channel'], response])

                break
        else:
            print 'i dont know what to do'

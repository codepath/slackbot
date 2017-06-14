from jinja2 import Template


DEVELOPMENT = 'DEVELOPMENT'
PRODUCTION = 'PRODUCTION'
SLACKBOT_TOKENS = {
    DEVELOPMENT: 'xoxb-196581378240-cpLqyP5VE52Ng6CcVBtoLELA',
    PRODUCTION: 'xoxb-170416673842-WwGXAlLJVjNWCNG4gRrFerwo'
}
SLACKBOT = {
    DEVELOPMENT: 'fredtest',
    PRODUCTION: 'fred'
}


def render_template(template_id, **kwargs):
    with open('templates/{}.slack'.format(template_id)) as f:
        template = Template(''.join(f.readlines()))

    return template.render(**kwargs)

from jinja2 import Template


def render_template(template_id, **kwargs):
    with open('fred/templates/{}.slack'.format(template_id)) as f:
        template = Template(''.join(f.readlines()))

    return template.render(**kwargs)

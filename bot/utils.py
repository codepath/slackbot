from jinja2 import Template


def render_template(template_id, **kwargs):
    with open(f'templates/{template_id}.slack') as f:
        template = Template(''.join(f.readlines()))

    return template.render(**kwargs)

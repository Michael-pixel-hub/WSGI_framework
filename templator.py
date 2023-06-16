from jinja2 import Template


def render(template_name, **kwargs):
    with open(template_name, 'r') as file:
        ready_template = Template(file.read())
    return ready_template.render(**kwargs).encode('utf-8')
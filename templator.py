from jinja2.environment import Environment
from jinja2 import FileSystemLoader


def render(template_name, **kwargs):
    env = Environment()
    env.loader = FileSystemLoader('templates')
    template = env.get_template(template_name)
    return template.render(**kwargs).encode('utf-8')
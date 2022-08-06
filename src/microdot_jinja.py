from jinja2 import Environment, FileSystemLoader, select_autoescape

_jinja_env = None


def init_templates(template_dir='templates'):
    """Initialize the templating subsystem.

    :param template_dir: the directory where templates are stored. This
                         argument is optional. The default is to load templates
                         from a *templates* subdirectory.
    """
    global _jinja_env
    _jinja_env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape()
    )


def render_template(template, *args, **kwargs):
    """Render a template.

    :param template: The filename of the template to render, relative to the
                     configured template directory.
    :param args: Positional arguments to be passed to the render engine.
    :param kwargs: Keyword arguments to be passed to the render engine.

    The return value is a string with the rendered template.
    """
    if _jinja_env is None:  # pragma: no cover
        init_templates()
    template = _jinja_env.get_template(template)
    return template.render(*args, **kwargs)

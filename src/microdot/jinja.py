from jinja2 import Environment, FileSystemLoader, select_autoescape

_jinja_env = None


class Template:
    """A template object.

    :param template: The filename of the template to render, relative to the
                     configured template directory.
    """
    @classmethod
    def initialize(cls, template_dir='templates', enable_async=False,
                   **kwargs):
        """Initialize the templating subsystem.

        :param template_dir: the directory where templates are stored. This
                             argument is optional. The default is to load
                             templates from a *templates* subdirectory.
        :param enable_async: set to ``True`` to enable the async rendering
                             engine in Jinja, and the ``render_async()`` and
                             ``generate_async()`` methods.
        :param kwargs: any additional options to be passed to Jinja's
                       ``Environment`` class.
        """
        global _jinja_env
        _jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(),
            enable_async=enable_async,
            **kwargs
        )

    def __init__(self, template):
        if _jinja_env is None:  # pragma: no cover
            self.initialize()
        #: The name of the template
        self.name = template
        self.template = _jinja_env.get_template(template)

    def generate(self, *args, **kwargs):
        """Return a generator that renders the template in chunks, with the
        given arguments."""
        return self.template.generate(*args, **kwargs)

    def render(self, *args, **kwargs):
        """Render the template with the given arguments and return it as a
        string."""
        return self.template.render(*args, **kwargs)

    def generate_async(self, *args, **kwargs):
        """Return an asynchronous generator that renders the template in
        chunks, using the given arguments."""
        return self.template.generate_async(*args, **kwargs)

    async def render_async(self, *args, **kwargs):
        """Render the template with the given arguments asynchronously and
        return it as a string."""
        return await self.template.render_async(*args, **kwargs)

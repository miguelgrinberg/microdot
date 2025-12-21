Templates
~~~~~~~~~

Many web applications use HTML templates for rendering content to clients.
Microdot includes extensions to render templates with the
`utemplate <https://github.com/pfalcon/utemplate>`_ package on CPython and
MicroPython, and with `Jinja <https://jinja.palletsprojects.com/>`_ only on
CPython.

Using the uTemplate Engine
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `utemplate.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/utemplate.py>`_

   * - Required external dependencies
     - | `utemplate <https://github.com/pfalcon/utemplate/tree/master/utemplate>`_

   * - Examples
     - | `hello.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/templates/utemplate/hello.py>`_

The :class:`Template <microdot.utemplate.Template>` class is used to load a
template. The argument is the template filename, relative to the templates
directory, which is *templates* by default.

The ``Template`` object has a :func:`render() <microdot.utemplate.Template.render>`
method that renders the template to a string. This method receives any
arguments that are used by the template.

Example::

    from microdot.utemplate import Template

    @app.get('/')
    async def index(req):
        return Template('index.html').render()

The ``Template`` object also has a :func:`generate() <microdot.utemplate.Template.generate>`
method, which returns a generator instead of a string. The
:func:`render_async() <microdot.utemplate.Template.render_async>` and
:func:`generate_async() <microdot.utemplate.Template.generate_async>` methods
are the asynchronous versions of these two methods.

The default location from where templates are loaded is the *templates*
subdirectory. This location can be changed with the
:func:`Template.initialize <microdot.utemplate.Template.initialize>` class
method::

    Template.initialize('my_templates')

By default templates are automatically compiled the first time they are
rendered, or when their last modified timestamp is more recent than the
compiledo file's timestamp. This loading behavior can be changed by switching
to a different template loader. For example, if the templates are pre-compiled,
the timestamp check and compile steps can be removed by switching to the
"compiled" template loader::

    from utemplate import compiled
    from microdot.utemplate import Template

    Template.initialize(loader_class=compiled.Loader)

Consult the `uTemplate documentation <https://github.com/pfalcon/utemplate>`_
for additional information regarding template loaders.

Using the Jinja Engine
^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Compatibility
     - | CPython only

   * - Required Microdot source files
     - | `jinja.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/jinja.py>`_

   * - Required external dependencies
     - | `Jinja2 <https://jinja.palletsprojects.com/>`_

   * - Examples
     - | `hello.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/templates/jinja/hello.py>`_

The :class:`Template <microdot.jinja.Template>` class is used to load a
template. The argument is the template filename, relative to the templates
directory, which is *templates* by default.

The ``Template`` object has a :func:`render() <microdot.jinja.Template.render>`
method that renders the template to a string. This method receives any
arguments that are used by the template.

Example::

    from microdot.jinja import Template

    @app.get('/')
    async def index(req):
        return Template('index.html').render()

The ``Template`` object also has a :func:`generate() <microdot.jinja.Template.generate>`
method, which returns a generator instead of a string.

The default location from where templates are loaded is the *templates*
subdirectory. This location can be changed with the
:func:`Template.initialize <microdot.jinja.Template.initialize>` class method::

    Template.initialize('my_templates')

The ``initialize()`` method also accepts ``enable_async`` argument, which
can be set to ``True`` if asynchronous rendering of templates is desired. If
this option is enabled, then the
:func:`render_async() <microdot.jinja.Template.render_async>` and
:func:`generate_async() <microdot.jinja.Template.generate_async>` methods
must be used.

.. note::
    The Jinja extension is not compatible with MicroPython.

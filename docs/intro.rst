Installation
------------

Microdot can be installed with ``pip``::

    pip install microdot

For MicroPython, you can install with ``upip``.

On platforms where ``pip`` or ``upip`` are not viable options, you can manually
copy and install the ``microdot.py`` and ``microdot_asyncio.py`` source files
from the `GitHub reposutory <https://github.com/miguelgrinberg/microdot>`_
into your project directory.

Examples
--------

The following is an example of a standard single or multi-threaded web
server::

    from microdot import Microdot

    app = Microdot()

    @app.route('/')
    def hello(request):
        return 'Hello, world!'

    app.run()

Microdot also supports the asynchronous model and can be used under
``asyncio``. The example that follows is equivalent to the one above, but uses
coroutines for concurrency::

    from microdot_asyncio import Microdot

    app = Microdot()

    @app.route('/')
    async def hello(request):
        return 'Hello, world!'

    app.run()

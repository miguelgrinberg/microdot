Installation
------------

Microdot can be installed with ``pip``::

    pip install microdot

For platforms that do not support or cannot run ``pip``, you can also manually
copy and install the ``microdot.py`` and ``microdot_asyncio.py`` source files.

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

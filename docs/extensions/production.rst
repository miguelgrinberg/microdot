Production Deployments
~~~~~~~~~~~~~~~~~~~~~~

The ``Microdot`` class creates its own simple web server. This is enough for an
application deployed with MicroPython, but when using CPython it may be useful
to use a separate, battle-tested web server. To address this need, Microdot
provides extensions that implement the ASGI and WSGI protocols.

Using an ASGI Web Server
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Compatibility
     - | CPython only

   * - Required Microdot source files
     - | `asgi.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/asgi.py>`_

   * - Required external dependencies
     - | An ASGI web server, such as `Uvicorn <https://www.uvicorn.org/>`_.

   * - Examples
     - | `hello_asgi.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/hello/hello_asgi.py>`_
       | `hello_asgi.py (uTemplate) <https://github.com/miguelgrinberg/microdot/blob/main/examples/templates/utemplate/hello_asgi.py>`_
       | `hello_asgi.py (Jinja) <https://github.com/miguelgrinberg/microdot/blob/main/examples/templates/jinja/hello_asgi.py>`_
       | `echo_asgi.py (WebSocket) <https://github.com/miguelgrinberg/microdot/blob/main/examples/websocket/echo_asgi.py>`_

The ``asgi`` module provides an extended ``Microdot`` class that
implements the ASGI protocol and can be used with a compliant ASGI server such
as `Uvicorn <https://www.uvicorn.org/>`_.

To use an ASGI web server, the application must import the
:class:`Microdot <microdot.asgi.Microdot>` class from the ``asgi`` module::

    from microdot.asgi import Microdot

    app = Microdot()

    @app.route('/')
    async def index(req):
        return 'Hello, World!'

The ``app`` application instance created from this class can be used as the
ASGI callable with any complaint ASGI web server. If the above example
application was stored in a file called *test.py*, then the following command
runs the web application using the Uvicorn web server::

    uvicorn test:app

When using the ASGI support, the ``scope`` dictionary provided by the web
server is available to request handlers as ``request.asgi_scope``.

The application instance can be initialized with ``lifespan_startup`` and
``lifespan_shutdown`` arguments, which are invoked when the web server sends
the ASGI lifespan signals with the ASGI scope as only argument::

    async def startup(scope):
        pass

    async def shutdown(scope):
        pass

    app = Microdot(lifespan_startup=startup, lifespan_shutdown=shutdown)

Using a WSGI Web Server
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Compatibility
     - | CPython only

   * - Required Microdot source files
     - | `wsgi.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/wsgi.py>`_

   * - Required external dependencies
     - | A WSGI web server, such as `Gunicorn <https://gunicorn.org/>`_.

   * - Examples
     - | `hello_wsgi.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/hello/hello_wsgi.py>`_
       | `hello_wsgi.py (uTemplate) <https://github.com/miguelgrinberg/microdot/blob/main/examples/templates/utemplate/hello_wsgi.py>`_
       | `hello_wsgi.py (Jinja) <https://github.com/miguelgrinberg/microdot/blob/main/examples/templates/jinja/hello_wsgi.py>`_
       | `echo_wsgi.py (WebSocket) <https://github.com/miguelgrinberg/microdot/blob/main/examples/websocket/echo_wsgi.py>`_


The ``wsgi`` module provides an extended ``Microdot`` class that implements the
WSGI protocol and can be used with a compliant WSGI web server such as 
`Gunicorn <https://gunicorn.org/>`_ or
`uWSGI <https://uwsgi-docs.readthedocs.io/en/latest/>`_.

To use a WSGI web server, the application must import the
:class:`Microdot <microdot.wsgi.Microdot>` class from the ``wsgi`` module::

    from microdot.wsgi import Microdot

    app = Microdot()

    @app.route('/')
    def index(req):
        return 'Hello, World!'

The ``app`` application instance created from this class can be used as a WSGI
callbable with any complaint WSGI web server. If the above application
was stored in a file called *test.py*, then the following command runs the
web application using the Gunicorn web server::

    gunicorn test:app

When using the WSGI support, the ``environ`` dictionary provided by the web
server is available to request handlers as ``request.environ``.

.. note::
    In spite of WSGI being a synchronous protocol, the Microdot application
    internally runs under an asyncio event loop. For that reason, the
    recommendation to prefer ``async def`` handlers over ``def`` still applies
    under WSGI. Consult the :ref:`Concurrency` section for a discussion of how
    the two types of functions are handled by Microdot.

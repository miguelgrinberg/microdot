Optional Modules
----------------

Microdot is a highly extensible web application framework. The modules
described in this section are also part of the Microdot project, but their use
is optional.

When using CPython, these modules are all installed together with the core
module. Each module documents which source files are needed. This may help
MicroPython users save space by removing the modules that are not used by the
application.

Asynchronous Support with Asyncio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | 📂 microdot/
       |   📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/__init__.py>`_
       |   📃 `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/microdot.py>`_
       |   📂 asyncio/
       |      📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/asyncio/__init__.py>`_
       |      📃 `microdot_asyncio.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/asyncio/microdot_asyncio.py>`_

   * - Required external dependencies
     - | CPython: None
       | MicroPython: `uasyncio <https://github.com/micropython/micropython/tree/master/extmod/uasyncio>`_

   * - Examples
     - | `hello_async.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/hello/hello_async.py>`_

Microdot can be extended to use an asynchronous programming model based on the
``asyncio`` package. When the :class:`Microdot <microdot.asyncio.Microdot>`
class is imported from the ``microdot.asyncio`` package, an asynchronous server
is used, and handlers can be defined as coroutines.

The example that follows uses ``asyncio`` coroutines for concurrency::

    from microdot.asyncio import Microdot

    app = Microdot()

    @app.route('/')
    async def hello(request):
        return 'Hello, world!'

    app.run()

Rendering HTML Templates
~~~~~~~~~~~~~~~~~~~~~~~~

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
     - | 📂 microdot/
       |   📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/__init__.py>`_
       |   📃 `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/microdot.py>`_
       |   📃 `utemplate.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/utemplate.py>`_

   * - Required external dependencies
     - | `utemplate <https://github.com/pfalcon/utemplate/tree/master/utemplate>`_

   * - Examples
     - | `hello.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/templates/utemplate/hello.py>`_
       | `hello_utemplate_async.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/hello/hello_utemplate_async.py>`_

The :func:`render_template <microdot.utemplate.render_template>` function is
used to render HTML templates with the uTemplate engine. The first argument is
the template filename, relative to the templates directory, which is
*templates* by default. Any additional arguments are passed to the template
engine to be used as arguments.

Example::

    from microdot.utemplate import render_template

    @app.get('/')
    def index(req):
        return render_template('index.html')

The default location from where templates are loaded is the *templates*
subdirectory. This location can be changed with the
:func:`init_templates <microdot.utemplate.init_templates>` function::

    from microdot.utemplate import init_templates

    init_templates('my_templates')

Using the Jinja Engine
^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Compatibility
     - | CPython only

   * - Required Microdot source files
     - | 📂 microdot/
       |   📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/__init__.py>`_
       |   📃 `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/microdot.py>`_
       |   📃 `jinja.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/jinja.py>`_

   * - Required external dependencies
     - | `Jinja2 <https://jinja.palletsprojects.com/>`_

   * - Examples
     - | `hello.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/templates/jinja/hello.py>`_

The :func:`render_template <microdot.jinja.render_template>` function is used
to render HTML templates with the Jinja engine. The first argument is the
template filename, relative to the templates directory, which is *templates* by
default. Any additional arguments are passed to the template engine to be used
as arguments.

Example::

    from microdot.jinja import render_template

    @app.get('/')
    def index(req):
        return render_template('index.html')

The default location from where templates are loaded is the *templates*
subdirectory. This location can be changed with the
:func:`init_templates <microdot.jinja.init_templates>` function::

    from microdot.jinja import init_templates

    init_templates('my_templates')

.. note::
    The Jinja extension is not compatible with MicroPython.

Maintaing Secure User Sessions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | 📂 microdot/
       |   📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/__init__.py>`_
       |   📃 `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/microdot.py>`_
       |   📃 `session.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/session.py>`_

   * - Required external dependencies
     - | CPython: `PyJWT <https://pyjwt.readthedocs.io/>`_
       | MicroPython: `jwt.py <https://github.com/micropython/micropython-lib/blob/master/python-ecosys/pyjwt/jwt.py>`_,
                      `hmac <https://github.com/micropython/micropython-lib/blob/master/python-stdlib/hmac/hmac.py>`_

   * - Examples
     - | `login.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/sessions/login.py>`_

The session extension provides a secure way for the application to maintain
user sessions. The session is stored as a signed cookie in the client's
browser, in `JSON Web Token (JWT) <https://en.wikipedia.org/wiki/JSON_Web_Token>`_
format.

To work with user sessions, create an instance of the
:class:`Session <microdot.session.Session>` class and configure a secret key
that will be used to protect user sessions with a cryptographic signature.
Example::

    from microdot import Microdot
    from microdot.session import Session

    app = Microdot()
    Session(app, secret_key='top-secret!')

When the application is created in a factory function, the session extension
can be initialized in two steps::

    from microdot import Microdot
    from microdot.session import Session

    session = Session(secret_key='top-secret!')

    def create_app():
        app = Microdot()
        session.initialize(app)
        return app

It is very important that the secret key is well protected. An attacker who is
in possession of this key can generate user session cookies with any contents
that the server will accept as valid.

The :func:`with_session <microdot.session.with_session>` decorator is provided
as a convenient way to retrieve the session and add it to the route function as
an additional argument. Example::

    from microdot.session import with_session

    @app.route('/')
    @with_session
    def index(request, session):
        # ...

The session object is a standard Python dictionary that is extended with
:func:`save() <microdot.session.SessionDict.save>` and
:func:`delete() <microdot.session.SessionDict.delete>` methods.

The following example demonstrates a simple log in system::

    from microdot import Microdot
    from microdot.session import Session, with_session

    app = Microdot()
    Session(app, secret_key='top-secret')

    @app.route('/', methods=['GET', 'POST'])
    @with_session
    def index(req, session):
        username = session.get('username')
        if req.method == 'POST':
            username = req.form.get('username')
            session['username'] = username
            session.save()
            return redirect('/')
        if username is None:
            return 'Not logged in'
        else:
            return 'Logged in as ' + username

    @app.post('/logout')
    @with_session
    def logout(req, session):
        session.delete()
        return redirect('/')

Cross-Origin Resource Sharing (CORS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | 📂 microdot/
       |   📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/__init__.py>`_
       |   📃 `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/microdot.py>`_
       |   📃 `cors.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/cors.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `cors.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/cors/cors.py>`_

The CORS extension provides support for `Cross-Origin Resource Sharing
(CORS) <https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS>`_. CORS is a
mechanism that allows web applications running on different origins to access
resources from each other. For example, a web application running on
``https://example.com`` can access resources from ``https://api.example.com``.

To enable CORS support, create an instance of the
:class:`CORS <microdot.cors.CORS>` class and configure the desired options.
Example::

    from microdot import Microdot
    from microdot.cors import CORS

    app = Microdot()
    cors = CORS(app, allowed_origins=['https://example.com'],
                allow_credentials=True)

When the application is created in a factory function, this extension can be
initialized in two steps::

    from microdot import Microdot
    from microdot.cors import CORS

    cors = CORS(allowed_origins=['https://example.com'],
                allow_credentials=True)

    def create_app():
        app = Microdot()
        cors.initialize(app)

WebSocket Support
~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | 📂 microdot/
       |   📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/__init__.py>`_
       |   📃 `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/microdot.py>`_
       |   📃 `websocket.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/websocket.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `echo.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/websocket/echo.py>`_
       | `echo_wsgi.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/websocket/echo_wsgi.py>`_

The WebSocket extension provides a way for the application to handle WebSocket
requests. The :func:`websocket <microdot.websocket.with_websocket>` decorator
is used to mark a route handler as a WebSocket handler. The handler receives
a WebSocket object as a second argument. The WebSocket object provides
``send()`` and ``receive()`` methods to send and receive messages respectively.

Example::

        @app.route('/echo')
        @with_websocket
        def echo(request, ws):
            while True:
                message = ws.receive()
                ws.send(message)

.. note::
   An unsupported *microdot.websocket_alt.py* module, with the same
   interface, is also provided. This module uses the native WebSocket support
   in MicroPython that powers the WebREPL, and may provide slightly better
   performance for MicroPython low-end boards. This module is not compatible
   with CPython.

Asynchronous WebSocket
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | 📂 microdot/
       |   📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/__init__.py>`_
       |   📃 `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/microdot.py>`_
       |   📃 `websocket.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/websocket.py>`_
       |   📂 asyncio/
       |      📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/asyncio/__init__.py>`_
       |      📃 `microdot_asyncio.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/asyncio/microdot_asyncio.py>`_
       |      📃 `websocket.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/asyncio/websocket.py>`_

   * - Required external dependencies
     - | CPython: None
       | MicroPython: `uasyncio <https://github.com/micropython/micropython/tree/master/extmod/uasyncio>`_

   * - Examples
     - | `echo_async.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/websocket/echo_async.py>`_

This extension has the same interface as the synchronous WebSocket extension,
but the ``receive()`` and ``send()`` methods are asynchronous.

.. note::
   An unsupported *microdot.asgi.websocket.py* module, with the same
   interface, is also provided. This module must be used instead of
   *microdot.asyncio.websocket.py* when the ASGI support is used. The
   `echo_asgi.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/websocket/echo_asgi.py>`_
   example shows how to use this module.

HTTPS Support
~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | 📂 microdot/
       |    📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/__init__.py>`_
       |    📃 `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/microdot.py>`_
       |    📃 `ssl.py <https://github.com/miguelgrinberg/microdot/tree/main/src/ssl.py>`_

   * - Examples
     - | `hello_tls.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/tls/hello_tls.py>`_
       | `hello_async_tls.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/tls/hello_async_tls.py>`_

The ``run()`` function accepts an optional ``ssl`` argument, through which an
initialized ``SSLContext`` object can be passed. MicroPython does not currently
have a ``SSLContext`` implementation, so the ``microdot.ssl`` module provides
a basic implementation that can be used to create a context.

Example::

    from microdot import Microdot
    from microdot.ssl import create_ssl_context

    app = Microdot()

    @app.route('/')
    def index(req):
        return 'Hello, World!'

    sslctx = create_ssl_context('cert.der', 'key.der')
    app.run(port=4443, debug=True, ssl=sslctx)

.. note::
   The ``microdot.ssl`` module is only needed for MicroPython. When used under
   CPython, this module creates a standard ``SSLContext`` instance.

.. note::
   The ``uasyncio`` library for MicroPython does not currently support TLS, so
   this feature is not available for asynchronous applications on that
   platform. The ``asyncio`` library for CPython is fully supported.

Test Client
~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | 📂 microdot/
       |   📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/__init__.py>`_
       |   📃 `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/microdot.py>`_
       |   📃 `test_client.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/test_client.py>`_

   * - Required external dependencies
     - | None

The Microdot Test Client is a utility class that can be used during testing to
send requests into the application.

Example::

    from microdot import Microdot
    from microdot.test_client import TestClient

    app = Microdot()

    @app.route('/')
    def index(req):
        return 'Hello, World!'

    def test_app():
        client = TestClient(app)
        response = client.get('/')
        assert response.text == 'Hello, World!'

See the documentation for the :class:`TestClient <microdot.test_client.TestClient>`
class for more details.

Asynchronous Test Client
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | 📂 microdot/
       |   📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/__init__.py>`_
       |   📃 `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/microdot.py>`_
       |   📃 `test_client.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/test_client.py>`_
       |   📂 asyncio/
       |      📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/asyncio/__init__.py>`_
       |      📃 `microdot_asyncio.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/asyncio/microdot_asyncio.py>`_
       |      📃 `test_client.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/asyncio/test_client.py>`_

   * - Required external dependencies
     - | None

Similar to the :class:`TestClient <microdot.test_client.TestClient>` class
above, but for asynchronous applications.

Example usage::

    from microdot.asyncio.test_client import TestClient

    async def test_app():
        client = TestClient(app)
        response = await client.get('/')
        assert response.text == 'Hello, World!'

See the :class:`reference documentation <microdot.asyncio.test_client.TestClient>`
for details.

Deploying on a Production Web Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Microdot`` class creates its own simple web server. This is enough for an
application deployed with MicroPython, but when using CPython it may be useful
to use a separate, battle-tested web server. To address this need, Microdot
provides extensions that implement the WSGI and ASGI protocols.

Using a WSGI Web Server
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Compatibility
     - | CPython only

   * - Required Microdot source files
     - | 📂 microdot/
       |   📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/__init__.py>`_
       |   📃 `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/microdot.py>`_
       |   📂 wsgi/
       |      📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/wsgi/__init__.py>`_
       |      📃 `microdot_wsgi.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/wsgi/microdot_wsgi.py>`_

   * - Required external dependencies
     - | A WSGI web server, such as `Gunicorn <https://gunicorn.org/>`_.

   * - Examples
     - | `hello_wsgi.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/hello/hello_wsgi.py>`_


The ``microdot.wsgi`` module provides an extended ``Microdot`` class that
implements the WSGI protocol and can be used with a compliant WSGI web server
such as `Gunicorn <https://gunicorn.org/>`_ or
`uWSGI <https://uwsgi-docs.readthedocs.io/en/latest/>`_.

To use a WSGI web server, the application must import the
:class:`Microdot <microdot.wsgi.Microdot>` class from the ``microdot.wsgi``
module::

    from microdot.wsgi import Microdot

    app = Microdot()

    @app.route('/')
    def index(req):
        return 'Hello, World!'

The ``app`` application instance created from this class is a WSGI application
that can be used with any complaint WSGI web server. If the above application
is stored in a file called *test.py*, then the following command runs the
web application using the Gunicorn web server::

    gunicorn test:app

When using this WSGI adapter, the ``environ`` dictionary provided by the web
server is available to request handlers as ``request.environ``.

Using an ASGI Web Server
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Compatibility
     - | CPython only

   * - Required Microdot source files
     - | 📂 microdot/
       |   📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/__init__.py>`_
       |   📃 `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/microdot.py>`_
       |   📂 asyncio/
       |      📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/asyncio/__init__.py>`_
       |      📃 `microdot_asyncio.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/asyncio/microdot_asyncio.py>`_
       |   📂 asgi/
       |      📃 `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/asgi/__init__.py>`_
       |      📃 `microdot_asgi.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/asgi/microdot_asgi.py>`_

   * - Required external dependencies
     - | An ASGI web server, such as `Uvicorn <https://uvicorn.org/>`_.

   * - Examples
     - | `hello_asgi.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/hello/hello_asgi.py>`_

The ``microdot.asgi`` module provides an extended ``Microdot`` class that
implements the ASGI protocol and can be used with a compliant ASGI server such
as `Uvicorn <https://www.uvicorn.org/>`_.

To use an ASGI web server, the application must import the
:class:`Microdot <microdot.asgi.Microdot>` class from the ``microdot.asgi``
module::

    from microdot.asgi import Microdot

    app = Microdot()

    @app.route('/')
    async def index(req):
        return 'Hello, World!'

The ``app`` application instance created from this class is an ASGI application
that can be used with any complaint ASGI web server. If the above application
is stored in a file called *test.py*, then the following command runs the
web application using the Uvicorn web server::

    uvicorn test:app

When using this ASGI adapter, the ``scope`` dictionary provided by the web
server is available to request handlers as ``request.asgi_scope``.

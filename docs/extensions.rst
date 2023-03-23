Core Extensions
---------------

Microdot is a highly extensible web application framework. The extensions
described in this section are maintained as part of the Microdot project and
can be obtained from the same source code repository.

Asynchronous Support with Asyncio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_asyncio.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_asyncio.py>`_

   * - Required external dependencies
     - | CPython: None
       | MicroPython: `uasyncio <https://github.com/micropython/micropython/tree/master/extmod/uasyncio>`_

   * - Examples
     - | `hello_async.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/hello/hello_async.py>`_

Microdot can be extended to use an asynchronous programming model based on the
``asyncio`` package. When the :class:`Microdot <microdot_asyncio.Microdot>`
class is imported from the ``microdot_asyncio`` package, an asynchronous server
is used, and handlers can be defined as coroutines.

The example that follows uses ``asyncio`` coroutines for concurrency::

    from microdot_asyncio import Microdot

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
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_utemplate.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_utemplate.py>`_

   * - Required external dependencies
     - | `utemplate <https://github.com/pfalcon/utemplate/tree/master/utemplate>`_

   * - Examples
     - | `hello.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/templates/utemplate/hello.py>`_
       | `hello_utemplate_async.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/hello/hello_utemplate_async.py>`_

The :func:`render_template <microdot_utemplate.render_template>` function is
used to render HTML templates with the uTemplate engine. The first argument is
the template filename, relative to the templates directory, which is
*templates* by default. Any additional arguments are passed to the template
engine to be used as arguments.

Example::

    from microdot_utemplate import render_template

    @app.get('/')
    def index(req):
        return render_template('index.html')

The default location from where templates are loaded is the *templates*
subdirectory. This location can be changed with the
:func:`init_templates <microdot_utemplate.init_templates>` function::

    from microdot_utemplate import init_templates

    init_templates('my_templates')

Using the Jinja Engine
^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Compatibility
     - | CPython only

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_jinja.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_jinja.py>`_

   * - Required external dependencies
     - | `Jinja2 <https://jinja.palletsprojects.com/>`_

   * - Examples
     - | `hello.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/templates/jinja/hello.py>`_

The :func:`render_template <microdot_jinja.render_template>` function is used
to render HTML templates with the Jinja engine. The first argument is the
template filename, relative to the templates directory, which is *templates* by
default. Any additional arguments are passed to the template engine to be used
as arguments.

Example::

    from microdot_jinja import render_template

    @app.get('/')
    def index(req):
        return render_template('index.html')

The default location from where templates are loaded is the *templates*
subdirectory. This location can be changed with the
:func:`init_templates <microdot_jinja.init_templates>` function::

    from microdot_jinja import init_templates

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
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_session.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_session.py>`_

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

To work with user sessions, the application first must configure the secret key
that will be used to sign the session cookies. It is very important that this
key is kept secret. An attacker who is in possession of this key can generate
valid user session cookies with any contents.

To set the secret key, use the :func:`set_session_secret_key <microdot_session.set_session_secret_key>` function::

    from microdot_session import set_session_secret_key

    set_session_secret_key('top-secret!')

To :func:`get_session <microdot_session.get_session>`,
:func:`update_session <microdot_session.update_session>` and
:func:`delete_session <microdot_session.delete_session>` functions are used
inside route handlers to retrieve, store and delete session data respectively.
The :func:`with_session <microdot_session.with_session>` decorator is provided
as a convenient way to retrieve the session at the start of a route handler.

Example::

    from microdot import Microdot
    from microdot_session import set_session_secret_key, with_session, \
        update_session, delete_session

    app = Microdot()
    set_session_secret_key('top-secret')

    @app.route('/', methods=['GET', 'POST'])
    @with_session
    def index(req, session):
        username = session.get('username')
        if req.method == 'POST':
            username = req.form.get('username')
            update_session(req, {'username': username})
            return redirect('/')
        if username is None:
            return 'Not logged in'
        else:
            return 'Logged in as ' + username

    @app.post('/logout')
    def logout(req):
        delete_session(req)
        return redirect('/')

Cross-Origin Resource Sharing (CORS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_cors.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_cors.py>`_

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
:class:`CORS <microdot_cors.CORS>` class and configure the desired options.
Example::

    from microdot import Microdot
    from microdot_cors import CORS

    app = Microdot()
    cors = CORS(app, allowed_origins=['https://example.com'],
                allow_credentials=True)

WebSocket Support
~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_websocket.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_websocket.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `echo.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/websocket/echo.py>`_
       | `echo_wsgi.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/websocket/echo_wsgi.py>`_

The WebSocket extension provides a way for the application to handle WebSocket
requests. The :func:`websocket <microdot_websocket.with_websocket>` decorator
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
   An unsupported *microdot_websocket_alt.py* module, with the same
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
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_asyncio.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_asyncio.py>`_
       | `microdot_websocket.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_websocket.py>`_
       | `microdot_asyncio_websocket.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_asyncio_websocket.py>`_

   * - Required external dependencies
     - | CPython: None
       | MicroPython: `uasyncio <https://github.com/micropython/micropython/tree/master/extmod/uasyncio>`_

   * - Examples
     - | `echo_async.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/websocket/echo_async.py>`_

This extension has the same interface as the synchronous WebSocket extension,
but the ``receive()`` and ``send()`` methods are asynchronous.

.. note::
   An unsupported *microdot_asgi_websocket.py* module, with the same
   interface, is also provided. This module must be used instead of
   *microdot_asyncio_websocket.py* when the ASGI support is used. The
   `echo_asgi.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/websocket/echo_asgi.py>`_
   example shows how to use this module.

HTTPS Support
~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_ssl.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_ssl.py>`_

   * - Examples
     - | `hello_tls.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/tls/hello_tls.py>`_
       | `hello_async_tls.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/tls/hello_async_tls.py>`_

The ``run()`` function accepts an optional ``ssl`` argument, through which an
initialized ``SSLContext`` object can be passed. MicroPython does not currently
have a ``SSLContext`` implementation, so the ``microdot_ssl`` module provides
a basic implementation that can be used to create a context.

Example::

    from microdot import Microdot
    from microdot_ssl import create_ssl_context

    app = Microdot()

    @app.route('/')
    def index(req):
        return 'Hello, World!'

    sslctx = create_ssl_context('cert.der', 'key.der')
    app.run(port=4443, debug=True, ssl=sslctx)

.. note::
   The ``microdot_ssl`` module is only needed for MicroPython. When used under
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
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_test_client.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_test_client.py>`_

   * - Required external dependencies
     - | None

The Microdot Test Client is a utility class that can be used during testing to
send requests into the application.

Example::

    from microdot import Microdot
    from microdot_test_client import TestClient

    app = Microdot()

    @app.route('/')
    def index(req):
        return 'Hello, World!'

    def test_app():
        client = TestClient(app)
        response = client.get('/')
        assert response.text == 'Hello, World!'

See the documentation for the :class:`TestClient <microdot_test_client.TestClient>`
class for more details.

Asynchronous Test Client
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_asyncio.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_asyncio.py>`_
       | `microdot_test_client.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_test_client.py>`_
       | `microdot_asyncio_test_client.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_asyncio_test_client.py>`_

   * - Required external dependencies
     - | None

Similar to the :class:`TestClient <microdot_test_client.TestClient>` class
above, but for asynchronous applications.

Example usage::

    from microdot_asyncio_test_client import TestClient

    async def test_app():
        client = TestClient(app)
        response = await client.get('/')
        assert response.text == 'Hello, World!'

See the :class:`reference documentation <microdot_asyncio_test_client.TestClient>`
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
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_wsgi.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_wsgi.py>`_

   * - Required external dependencies
     - | A WSGI web server, such as `Gunicorn <https://gunicorn.org/>`_.

   * - Examples
     - | `hello_wsgi.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/hello/hello_wsgi.py>`_


The ``microdot_wsgi`` module provides an extended ``Microdot`` class that
implements the WSGI protocol and can be used with a compliant WSGI web server
such as `Gunicorn <https://gunicorn.org/>`_ or
`uWSGI <https://uwsgi-docs.readthedocs.io/en/latest/>`_.

To use a WSGI web server, the application must import the
:class:`Microdot <microdot_wsgi.Microdot>` class from the ``microdot_wsgi``
module::

    from microdot_wsgi import Microdot

    app = Microdot()

    @app.route('/')
    def index(req):
        return 'Hello, World!'

The ``app`` application instance created from this class is a WSGI application
that can be used with any complaint WSGI web server. If the above application
is stored in a file called *test.py*, then the following command runs the
web application using the Gunicorn web server::

    gunicorn test:app

Using an ASGI Web Server
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Compatibility
     - | CPython only

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_asyncio.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_asyncio.py>`_
       | `microdot_asgi.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_asgi.py>`_

   * - Required external dependencies
     - | An ASGI web server, such as `Uvicorn <https://uvicorn.org/>`_.

   * - Examples
     - | `hello_asgi.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/hello/hello_asgi.py>`_

The ``microdot_asgi`` module provides an extended ``Microdot`` class that
implements the ASGI protocol and can be used with a compliant ASGI server such
as `Uvicorn <https://www.uvicorn.org/>`_.

To use an ASGI web server, the application must import the
:class:`Microdot <microdot_asgi.Microdot>` class from the ``microdot_asgi``
module::

    from microdot_asgi import Microdot

    app = Microdot()

    @app.route('/')
    async def index(req):
        return 'Hello, World!'

The ``app`` application instance created from this class is an ASGI application
that can be used with any complaint ASGI web server. If the above application
is stored in a file called *test.py*, then the following command runs the
web application using the Uvicorn web server::

    uvicorn test:app


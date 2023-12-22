Core Extensions
---------------

Microdot is a highly extensible web application framework. The extensions
described in this section are maintained as part of the Microdot project in
the same source code repository.

WebSocket Support
~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     -  | `websocket.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/websocket.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `echo.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/websocket/echo.py>`_

The WebSocket extension gives the application the ability to handle WebSocket
requests. The :func:`with_websocket <microdot.websocket.with_websocket>`
decorator is used to mark a route handler as a WebSocket handler. Decorated
routes receive a WebSocket object as a second argument. The WebSocket object
provides ``send()`` and ``receive()`` asynchronous methods to send and receive
messages respectively.

Example::

        @app.route('/echo')
        @with_websocket
        async def echo(request, ws):
            while True:
                message = await ws.receive()
                await ws.send(message)

Server-Sent Events Support
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     -  | `sse.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/sse.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `counter.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/sse/counter.py>`_

The Server-Sent Events (SSE) extension simplifies the creation of a streaming
endpoint that follows the SSE web standard. The :func:`with_sse <microdot.sse.with_sse>`
decorator is used to mark a route as an SSE handler. Decorated routes receive
an SSE object as second argument. The SSE object provides a ``send()``
asynchronous method to send an event to the client.

Example::

    @app.route('/events')
    @with_sse
    async def events(request, sse):
        for i in range(10):
            await asyncio.sleep(1)
            await sse.send({'counter': i})  # unnamed event
        await sse.send('end', event='comment')  # named event

.. note::
   The SSE protocol is unidirectional, so there is no ``receive()`` method in
   the SSE object. For bidirectional communication with the client, use the
   WebSocket extension.

Rendering Templates
~~~~~~~~~~~~~~~~~~~

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
:func:`init_templates <microdot.utemplate.init_templates>` function::

    from microdot.jinja import init_templates

    init_templates('my_templates')

The ``init_templates()`` function also accepts ``enable_async`` argument, which
can be set to ``True`` if asynchronous rendering of templates is desired. If
this option is enabled, then the
:func:`render_async() <microdot.utemplate.Template.render_async>` and
:func:`generate_async() <microdot.utemplate.Template.generate_async>` methods
must be used.

.. note::
    The Jinja extension is not compatible with MicroPython.

Maintaining Secure User Sessions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `session.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/session.py>`_

   * - Required external dependencies
     - | CPython: `PyJWT <https://pyjwt.readthedocs.io/>`_
       | MicroPython: `jwt.py <https://github.com/micropython/micropython-lib/blob/master/python-ecosys/pyjwt/jwt.py>`_,
                      `hmac.py <https://github.com/micropython/micropython-lib/blob/master/python-stdlib/hmac/hmac.py>`_

   * - Examples
     - | `login.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/sessions/login.py>`_

The session extension provides a secure way for the application to maintain
user sessions. The session data is stored as a signed cookie in the client's
browser, in `JSON Web Token (JWT) <https://en.wikipedia.org/wiki/JSON_Web_Token>`_
format.

To work with user sessions, the application first must configure a secret key
that will be used to sign the session cookies. It is very important that this
key is kept secret, as its name implies. An attacker who is in possession of
this key can generate valid user session cookies with any contents.

To initialize the session extension and configure the secret key, create a
:class:`Session <microdot.session.Session>` object::

    Session(app, secret_key='top-secret')

The :func:`with_session <microdot.session.with_session>` decorator is the
most convenient way to retrieve the session at the start of a request::

    from microdot import Microdot, redirect
    from microdot.session import Session, with_session

    app = Microdot()
    Session(app, secret_key='top-secret')

    @app.route('/', methods=['GET', 'POST'])
    @with_session
    async def index(req, session):
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
    async def logout(req, session):
        session.delete()
        return redirect('/')

The :func:`save() <microdot.session.SessionDict.save>` and
:func:`delete() <microdot.session.SessionDict.delete>` methods are used to update
and destroy the user session respectively.

Cross-Origin Resource Sharing (CORS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `cors.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/cors.py>`_

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

Testing with the Test Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `test_client.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/test_client.py>`_

   * - Required external dependencies
     - | None

The Microdot Test Client is a utility class that can be used in tests to send
requests into the application without having to start a web server.

Example::

    from microdot import Microdot
    from microdot.test_client import TestClient

    app = Microdot()

    @app.route('/')
    def index(req):
        return 'Hello, World!'

    async def test_app():
        client = TestClient(app)
        response = await client.get('/')
        assert response.text == 'Hello, World!'

See the documentation for the :class:`TestClient <microdot.test_client.TestClient>`
class for more details.

Deploying on a Production Web Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
     - | An ASGI web server, such as `Uvicorn <https://uvicorn.org/>`_.

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

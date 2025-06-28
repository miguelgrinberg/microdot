Core Extensions
---------------

Microdot is a highly extensible web application framework. The extensions
described in this section are maintained as part of the Microdot project in
the same source code repository.

Multipart Forms
~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     -  | `multipart.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/multipart.py>`_
        | `helpers.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/helpers.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `formdata.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/uploads/formdata.py>`_

The multipart extension handles multipart forms, including those that have file
uploads.

The :func:`with_form_data <microdot.multipart.with_form_data>` decorator
provides the simplest way to work with these forms. With this decorator added
to the route, whenever the client sends a multipart request the
:attr:`request.form <microdot.Request.form>` and
:attr:`request.files <microdot.Request.files>` properties are populated with
the submitted data. For form fields the field values are always strings. For
files, they are instances of the
:class:`FileUpload <microdot.multipart.FileUpload>` class.

Example::

    from microdot.multipart import with_form_data

    @app.post('/upload')
    @with_form_data
    async def upload(request):
        print('form fields:', request.form)
        print('files:', request.files)

One disadvantage of the ``@with_form_data`` decorator is that it has to copy
any uploaded files to memory or temporary disk files, depending on their size.
The :attr:`FileUpload.max_memory_size <microdot.multipart.FileUpload.max_memory_size>`
attribute can be used to control the cutoff size above which a file upload
is transferred to a temporary file.

A more performant alternative to the ``@with_form_data`` decorator is the
:class:`FormDataIter <microdot.multipart.FormDataIter>` class, which iterates
over the form fields sequentially, giving the application the option to parse
the form fields on the fly and decide what to copy and what to discard. When
using ``FormDataIter`` the ``request.form`` and ``request.files`` attributes
are not used.

Example::


    from microdot.multipart import FormDataIter

    @app.post('/upload')
    async def upload(request):
        async for name, value in FormDataIter(request):
            print(name, value)

For fields that contain an uploaded file, the ``value`` returned by the
iterator is the same ``FileUpload`` instance. The application can choose to
save the file with the :meth:`save() <microdot.multipart.FileUpload.save>`
method, or read it with the :meth:`read() <microdot.multipart.FileUpload.read>`
method, optionally passing a size to read it in chunks. The
:meth:`copy() <microdot.multipart.FileUpload.copy>` method is also available to
apply the copying logic used by the ``@with_form_data`` decorator, which is
inefficient but allows the file to be set aside to be processed later, after
the remaining form fields.

WebSocket
~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     -  | `websocket.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/websocket.py>`_
        | `helpers.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/helpers.py>`_

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

    from microdot.websocket import with_websocket

    @app.route('/echo')
    @with_websocket
    async def echo(request, ws):
        while True:
            message = await ws.receive()
            await ws.send(message)

To end the WebSocket connection, the route handler can exit, without returning
anything::

    @app.route('/echo')
    @with_websocket
    async def echo(request, ws):
        while True:
            message = await ws.receive()
            if message == 'exit':
                break
            await ws.send(message)
        await ws.send('goodbye')

If the client ends the WebSocket connection from their side, the route function
is cancelled. The route function can catch the ``CancelledError`` exception
from asyncio to perform cleanup tasks::

    @app.route('/echo')
    @with_websocket
    async def echo(request, ws):
        try:
            while True:
                message = await ws.receive()
                await ws.send(message)
        except asyncio.CancelledError:
            print('Client disconnected!')

Server-Sent Events
~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     -  | `sse.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/sse.py>`_
        | `helpers.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/helpers.py>`_

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

    from microdot.sse import with_sse

    @app.route('/events')
    @with_sse
    async def events(request, sse):
        for i in range(10):
            await asyncio.sleep(1)
            await sse.send({'counter': i})  # unnamed event
        await sse.send('end', event='comment')  # named event

To end the SSE connection, the route handler can exit, without returning
anything, as shown in the above examples.

If the client ends the SSE connection from their side, the route function is
cancelled. The route function can catch the ``CancelledError`` exception from
asyncio to perform cleanup tasks::

    @app.route('/events')
    @with_sse
    async def events(request, sse):
        try:
            i = 0
            while True:
                await asyncio.sleep(1)
                await sse.send({'counter': i})
                i += 1
        except asyncio.CancelledError:
            print('Client disconnected!')

.. note::
   The SSE protocol is unidirectional, so there is no ``receive()`` method in
   the SSE object. For bidirectional communication with the client, use the
   WebSocket extension.

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

Secure User Sessions
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `session.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/session.py>`_
       | `helpers.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/helpers.py>`_

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

Authentication
~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `auth.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/auth.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `basic_auth.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/auth/basic_auth.py>`_
       | `token_auth.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/auth/token_auth.py>`_

The authentication extension provides helper classes for two commonly used
authentication patterns, described below.

Basic Authentication
^^^^^^^^^^^^^^^^^^^^

`Basic Authentication <https://en.wikipedia.org/wiki/Basic_access_authentication>`_
is a method of authentication that is part of the HTTP specification. It allows
clients to authenticate to a server using a username and a password. Web
browsers have native support for Basic Authentication and will automatically
prompt the user for a username and a password when a protected resource is
accessed.

To use Basic Authentication, create an instance of the :class:`BasicAuth <microdot.auth.BasicAuth>`
class::

    from microdot.auth import BasicAuth

    auth = BasicAuth(app)

Next, create an authentication function. The function must accept a request
object and a username and password pair provided by the user. If the
credentials are valid, the function must return an object that represents the
user. If the authentication function cannot validate the user provided
credentials it must return ``None``. Decorate the function with
``@auth.authenticate``::

    @auth.authenticate
    async def verify_user(request, username, password):
        user = await load_user_from_database(username)
        if user and user.verify_password(password):
            return user

To protect a route with authentication, add the ``auth`` instance as a
decorator::

    @app.route('/')
    @auth
    async def index(request):
        return f'Hello, {request.g.current_user}!'

While running an authenticated request, the user object returned by the
authenticaction function is accessible as ``request.g.current_user``.

If an endpoint is intended to work with or without authentication, then it can
be protected with the ``auth.optional`` decorator::

    @app.route('/')
    @auth.optional
    async def index(request):
        if request.g.current_user:
            return f'Hello, {request.g.current_user}!'
        else:
            return 'Hello, anonymous user!'

As shown in the example, a route can check ``request.g.current_user`` to
determine if the user is authenticated or not.

Token Authentication
^^^^^^^^^^^^^^^^^^^^

To set up token authentication, create an instance of
:class:`TokenAuth <microdot.auth.TokenAuth>`::

    from microdot.auth import TokenAuth

    auth = TokenAuth()

Then add a function that verifies the token and returns the user it belongs to,
or ``None`` if the token is invalid or expired::

    @auth.authenticate
    async def verify_token(request, token):
        return load_user_from_token(token)

As with Basic authentication, the ``auth`` instance is used as a decorator to
protect your routes, and the authenticated user is accessible from the request
object as ``request.g.current_user``::

    @app.route('/')
    @auth
    async def index(request):
        return f'Hello, {request.g.current_user}!'

Optional authentication can also be used with tokens::

    @app.route('/')
    @auth.optional
    async def index(request):
        if request.g.current_user:
            return f'Hello, {request.g.current_user}!'
        else:
            return 'Hello, anonymous user!'

User Logins
~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `login.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/auth.py>`_
       | `session.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/session.py>`_
       | `helpers.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/helpers.py>`_
   * - Required external dependencies
     - | CPython: `PyJWT <https://pyjwt.readthedocs.io/>`_
       | MicroPython: `jwt.py <https://github.com/micropython/micropython-lib/blob/master/python-ecosys/pyjwt/jwt.py>`_,
                      `hmac.py <https://github.com/micropython/micropython-lib/blob/master/python-stdlib/hmac/hmac.py>`_
   * - Examples
     - | `login.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/login/login.py>`_

The login extension provides user login functionality. The logged in state of
the user is stored in the user session cookie, and an optional "remember me"
cookie can also be added to keep the user logged in across browser sessions.

To use this extension, create instances of the
:class:`Session <microdot.session.Session>` and :class:`Login <microdot.login.Login>`
class::

    Session(app, secret_key='top-secret!')
    login = Login()

The ``Login`` class accept an optional argument with the URL of the login page.
The default for this URL is */login*.

The application must represent users as objects with an ``id`` attribute. A
function decorated with ``@login.user_loader`` is used to load a user object::

    @login.user_loader
    async def get_user(user_id):
        return database.get_user(user_id)

The application must implement the login form. At the point in which the user
credentials have been received and verified, a call to the
:func:`login_user() <microdot.login.Login.login_user>` function must be made to
record the user in the user session::

    @app.route('/login', methods=['GET', 'POST'])
    async def login(request):
        # ...
        if user.check_password(password):
            return await login.login_user(request, user, remember=remember_me)
        return redirect('/login')

The optional ``remember`` argument is used to add a remember me cookie that
will log the user in automatically in future sessions. A value of ``True`` will
keep the log in active for 30 days. Alternatively, an integer number of days
can be passed in this argument.

Any routes that require the user to be logged in must be decorated with
:func:`@login <microdot.login.Login.__call__>`::

    @app.route('/')
    @login
    async def index(request):
        # ...

Routes that are of a sensitive nature can be decorated with
:func:`@login.fresh <microdot.login.Login.fresh>`
instead. This decorator requires that the user has logged in during the current
session, and will ask the user to logged in again if the session was
authenticated through a remember me cookie::

    @app.get('/fresh')
    @login.fresh
    async def fresh(request):
        # ...

To log out a user, the :func:`logout_user() <microdot.auth.Login.logout_user>`
is used::

    @app.post('/logout')
    @login
    async def logout(request):
        await login.logout_user(request)
        return redirect('/')

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
     - | `app.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/cors/app.py>`_

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

Test Client
~~~~~~~~~~~

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

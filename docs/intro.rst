Installation
------------

The installation method is different depending on the version of Python.

CPython Installation
~~~~~~~~~~~~~~~~~~~~

For use with standard Python (CPython) projects, Microdot and all of its core
extensions are installed with ``pip``::

    pip install microdot

MicroPython Installation
~~~~~~~~~~~~~~~~~~~~~~~~

For MicroPython, the recommended approach is to manually copy the necessary
source files from the
`GitHub repository <https://github.com/miguelgrinberg/microdot/tree/main/src>`_
into your device, ideally after
`compiling <https://docs.micropython.org/en/latest/reference/mpyfiles.html>`_
them to *.mpy* files. These source files can also be
`frozen <https://docs.micropython.org/en/latest/develop/optimizations.html?highlight=frozen#frozen-bytecode>`_
and incorporated into a custom MicroPython firmware.

Use the following guidelines to know what files to copy:

* For a minimal setup with only the base web server functionality, copy
  `microdot.py <https://github.com/miguelgrinberg/microdot/blob/main/src/microdot/microdot.py>`_
  into your project.
* For a configuration that includes one or more optional extensions, create a
  *microdot* directory in your device and copy the following files:

  * `__init__.py <https://github.com/miguelgrinberg/microdot/blob/main/src/microdot/__init__.py>`_
  * `microdot.py <https://github.com/miguelgrinberg/microdot/blob/main/src/microdot/microdot.py>`_
  * any needed `extensions <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot>`_.


Getting Started
---------------

This section describes the main features of Microdot in an informal manner.

For detailed reference information, consult the :ref:`API Reference`.

If you are familiar with releases of Microdot before 2.x, review the
:ref:`Migration Guide <Migrating to Microdot 2.x from Older Releases>`.

A Simple Microdot Web Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following is an example of a simple web server::

    from microdot import Microdot

    app = Microdot()

    @app.route('/')
    async def index(request):
        return 'Hello, world!'

    app.run()

The script imports the :class:`Microdot <microdot.Microdot>` class and creates
an application instance from it.

The application instance provides a :func:`route() <microdot.Microdot.route>`
decorator, which is used to define one or more routes, as needed by the
application.

The ``route()`` decorator takes the path portion of the URL as an
argument, and maps it to the decorated function, so that the function is called
when the client requests the URL.

When the function is called, it is passed a :class:`Request <microdot.Request>`
object as an argument, which provides access to the information passed by the
client. The value returned by the function is sent back to the client as the
response.

Microdot is an asynchronous framework that uses the ``asyncio`` package. Route
handler functions can be defined as ``async def`` or ``def`` functions, but
``async def`` functions are recommended for performance.

The :func:`run() <microdot.Microdot.run>` method starts the application's web
server on port 5000 by default, and creates its own asynchronous loop. This
method blocks while it waits for connections from clients.

For some applications it may be necessary to run the web server alongside other
asynchronous tasks, on an already running loop. In that case, instead of
``app.run()`` the web server can be started by invoking the
:func:`start_server() <microdot.Microdot.start_server>` coroutine as shown in
the following example::

    import asyncio
    from microdot import Microdot

    app = Microdot()

    @app.route('/')
    async def index(request):
        return 'Hello, world!'

    async def main():
        # start the server in a background task
        server = asyncio.create_task(app.start_server())

        # ... do other asynchronous work here ...

        # cleanup before ending the application
        await server

    asyncio.run(main())

Running with CPython
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/blob/main/src/microdot/microdot.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `hello.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/hello/hello.py>`_

When using CPython, you can start the web server by running the script that
has the ``app.run()`` call at the bottom::

    python main.py

After starting the script, open a web browser and navigate to
*http://localhost:5000/* to access the application at the default address for
the Microdot web server. From other computers in the same network, use the IP
address or hostname of the computer running the script instead of
``localhost``.

Running with MicroPython
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/blob/main/src/microdot/microdot.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `hello.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/hello/hello.py>`_
       | `gpio.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/gpio/gpio.py>`_

When using MicroPython, you can upload a *main.py* file containing the web
server code to your device, along with the required Microdot files, as defined
in the :ref:`MicroPython Installation` section.

MicroPython will automatically run *main.py* when the device is powered on, so
the web server will automatically start. The application can be accessed on
port 5000 at the device's IP address. As indicated above, the port can be
changed by passing the ``port`` argument to the ``run()`` method.

.. note::
   Microdot does not configure the network interface of the device in which it
   is running. If your device requires a network connection to be made in
   advance, for example to a Wi-Fi access point, this must be configured before
   the ``run()`` method is invoked.

Web Server Configuration
^^^^^^^^^^^^^^^^^^^^^^^^

The :func:`run() <microdot.Microdot.run>` and
:func:`start_server() <microdot.Microdot.start_server>` methods support a few
arguments to configure the web server.

- ``port``: The port number to listen on. Pass the desired port number in this
  argument to use a port different than the default of 5000. For example::

    app.run(port=6000)

- ``host``: The IP address of the network interface to listen on. By default
  the server listens on all available interfaces. To listen only on the local
  loopback interface, pass ``'127.0.0.1'`` as value for this argument.
- ``debug``: when set to ``True``, the server ouputs logging information to the
  console. The default is ``False``.
- ``ssl``: an ``SSLContext`` instance that configures the server to use TLS
  encryption, or ``None`` to disable TLS use. The default is ``None``. The
  following example demonstrates how to configure the server with an SSL
  certificate stored in *cert.pem* and *key.pem* files::

    import ssl

    # ...

    sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslctx.load_cert_chain('cert.pem', 'key.pem')
    app.run(port=4443, debug=True, ssl=sslctx)

.. note::
   When using CPython, the certificate and key files must be given in PEM
   format. When using MicroPython, these files must be given in DER format.

Defining Routes
~~~~~~~~~~~~~~~

The :func:`route() <microdot.Microdot.route>` decorator is used to associate an
application URL with the function that handles it. The only required argument
to the decorator is the path portion of the URL.

The following example creates a route for the root URL of the application::

    @app.route('/')
    async def index(request):
        return 'Hello, world!'

When a client requests the root URL (for example, *http://localhost:5000/*),
Microdot will call the ``index()`` function, passing it a
:class:`Request <microdot.Request>` object. The return value of the function
is the response that is sent to the client.

Below is another example, this one with a route for a URL with two components
in its path::

    @app.route('/users/active')
    async def active_users(request):
        return 'Active users: Susan, Joe, and Bob'

The complete URL that maps to this route is
*http://localhost:5000/users/active*.

An application can include multiple routes. Microdot uses the path portion of
the URL to determine the correct route function to call for each incoming
request.

Choosing the HTTP Method
^^^^^^^^^^^^^^^^^^^^^^^^

All the example routes shown above are associated with ``GET`` requests, which
are the default. Applications often need to define routes for other HTTP
methods, such as ``POST``, ``PUT``, ``PATCH`` and ``DELETE``. The ``route()``
decorator takes a ``methods`` optional argument, in which the application can
provide a list of HTTP methods that the route should be associated with on the
given path.

The following example defines a route that handles ``GET`` and ``POST``
requests within the same function::

    @app.route('/invoices', methods=['GET', 'POST'])
    async def invoices(request):
        if request.method == 'GET':
            return 'get invoices'
        elif request.method == 'POST':
            return 'create an invoice'

As an alternative to the example above, in which a single function is used to
handle multiple HTTP methods, sometimes it may be desirable to write a separate
function for each HTTP method. The above example can be implemented with two
routes as follows::

    @app.route('/invoices', methods=['GET'])
    async def get_invoices(request):
        return 'get invoices'

    @app.route('/invoices', methods=['POST'])
    async def create_invoice(request):
        return 'create an invoice'

Microdot provides the :func:`get() <microdot.Microdot.get>`,
:func:`post() <microdot.Microdot.post>`, :func:`put() <microdot.Microdot.put>`,
:func:`patch() <microdot.Microdot.patch>`, and
:func:`delete() <microdot.Microdot.delete>` decorators as shortcuts for the
corresponding HTTP methods. The two example routes above can be written more
concisely with them::

    @app.get('/invoices')
    async def get_invoices(request):
        return 'get invoices'

    @app.post('/invoices')
    async def create_invoice(request):
        return 'create an invoice'

Including Dynamic Components in the URL Path
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The examples shown above all use hardcoded URL paths. Microdot also supports
the definition of routes that have dynamic components in the path. For example,
the following route associates all URLs that have a path following the pattern
*http://localhost:5000/users/<username>* with the ``get_user()`` function::

    @app.get('/users/<username>')
    async def get_user(request, username):
        return 'User: ' + username

As shown in the example, a path component that is enclosed in angle brackets
is considered a placeholder. Microdot accepts any values for that portion of
the URL path, and passes the value received to the function as an argument
after the request object.

Routes are not limited to a single dynamic component. The following route shows
how multiple dynamic components can be included in the path::

    @app.get('/users/<firstname>/<lastname>')
    async def get_user(request, firstname, lastname):
        return 'User: ' + firstname + ' ' + lastname

Dynamic path components are considered to be strings by default. An explicit
type can be specified as a prefix, separated from the dynamic component name by
a colon. The following route has two dynamic components declared as an integer
and a string respectively::

    @app.get('/users/<int:id>/<string:username>')
    async def get_user(request, id, username):
        return 'User: ' + username + ' (' + str(id) + ')'

If a dynamic path component is defined as an integer, the value passed to the
route function is also an integer. If the client sends a value that is not an
integer in the corresponding section of the URL path, then the URL will not
match and the route will not be called.

A special type ``path`` can be used to capture the remainder of the path as a
single argument. The difference between an argument of type ``path`` and one of
type ``string`` is that the latter stops capturing when a ``/`` appears in the
URL::

    @app.get('/tests/<path:path>')
    async def get_test(request, path):
        return 'Test: ' + path

The ``re`` type allows the application to provide a custom regular expression
for the dynamic component. The next example defines a route that only matches
usernames that begin with an upper or lower case letter, followed by a sequence
of letters or numbers::

    @app.get('/users/<re:[a-zA-Z][a-zA-Z0-9]*:username>')
    async def get_user(request, username):
        return 'User: ' + username

The ``re`` type returns the URL component as a string, which sometimes may not
be the most convenient. To convert a path component to something more
meaningful than a string, the application can register a custom URL component
type and provide a parser function that performs the conversion. In the
following example, a ``hex`` custom type is registered to automatically
convert hex numbers given in the path to numbers::

    from microdot import URLPattern

    URLPattern.register_type('hex', parser=lambda value: int(value, 16))

    @app.get('/users/<hex:user_id>')
    async def get_user(request, user_id):
        user = get_user_by_id(user_id)
        # ...

In addition to the parser, the custom URL component can include a pattern,
given as a regular expression. When a pattern is provided, the URL component
will only match if the regular expression matches the value passed in the URL.
The ``hex`` example above can be expanded with a pattern as follows::

    URLPattern.register_type('hex', pattern='[0-9a-fA-F]+',
                             parser=lambda value: int(value, 16))

In cases where a pattern isn't provided, or when the pattern is unable to
filter out all invalid values, the parser function can return ``None`` to
indicate a failed match. The next example shows how the parser for the ``hex``
type can be expanded to do that::

    def hex_parser(value):
        try:
            return int(value, 16)
        except ValueError:
            return None

    URLPattern.register_type('hex', parser=hex_parser)

.. note::
   Dynamic path components are passed to route functions as keyword arguments,
   so the names of the function arguments must match the names declared in the
   path specification.

Before and After Request Handlers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is common for applications to need to perform one or more actions before a
request is handled. Examples include authenticating and/or authorizing the
client, opening a connection to a database, or checking if the requested
resource can be obtained from a cache. The
:func:`before_request() <microdot.Microdot.before_request>` decorator registers
a function to be called before the request is dispatched to the route function.

The following example registers a before-request handler that ensures that the
client is authenticated before the request is handled::

    @app.before_request
    async def authenticate(request):
        user = authorize(request)
        if not user:
            return 'Unauthorized', 401
        request.g.user = user

Before-request handlers receive the request object as an argument. If the
function returns a value, Microdot sends it to the client as the response, and
does not invoke the route function. This gives before-request handlers the
power to intercept a request if necessary. The example above uses this
technique to prevent an unauthorized user from accessing the requested
route.

After-request handlers registered with the
:func:`after_request() <microdot.Microdot.after_request>` decorator are called
after the route function returns a response. Their purpose is to perform any
common closing or cleanup tasks. The next example shows a combination of
before- and after-request handlers that print the time it takes for a request
to be handled::

    @app.before_request
    async def start_timer(request):
        request.g.start_time = time.time()

    @app.after_request
    async def end_timer(request, response):
        duration = time.time() - request.g.start_time
        print(f'Request took {duration:0.2f} seconds')

After-request handlers receive the request and response objects as arguments,
and they can return a modified response object to replace the original. If
no value is returned from an after-request handler, then the original response
object is used.

The after-request handlers are only invoked for successful requests. The
:func:`after_error_request() <microdot.Microdot.after_error_request>`
decorator can be used to register a function that is called after an error
occurs. The function receives the request and the error response and is
expected to return an updated response object after performing any necessary
cleanup.

.. note::
   The :ref:`request.g <The "g" Object>` object used in many of the above
   examples is a special object that allows the before- and after-request
   handlers, as well as the route function to share data during the life of the
   request.

Error Handlers
^^^^^^^^^^^^^^

When an error occurs during the handling of a request, Microdot ensures that
the client receives an appropriate error response. Some of the common errors
automatically handled by Microdot are:

- 400 for malformed requests.
- 404 for URLs that are unknown.
- 405 for URLs that are known, but not implemented for the requested HTTP
  method.
- 413 for requests that are larger than the allowed size.
- 500 when the application raises an unhandled exception.

While the above errors are fully complaint with the HTTP specification, the
application might want to provide custom responses for them. The
:func:`errorhandler() <microdot.Microdot.errorhandler>` decorator registers
functions to respond to specific error codes. The following example shows a
custom error handler for 404 errors::

    @app.errorhandler(404)
    async def not_found(request):
        return {'error': 'resource not found'}, 404

The ``errorhandler()`` decorator has a second form, in which it takes an
exception class as an argument. Microdot will invoke the handler when an
unhandled exception that is an instance of the given class is raised. The next
example provides a custom response for division by zero errors::

    @app.errorhandler(ZeroDivisionError)
    async def division_by_zero(request, exception):
        return {'error': 'division by zero'}, 500

When the raised exception class does not have an error handler defined, but
one or more of its parent classes do, Microdot makes an attempt to invoke the
most specific handler.

Mounting a Sub-Application
^^^^^^^^^^^^^^^^^^^^^^^^^^

Small Microdot applications can be written as a single source file, but this
is not the best option for applications that pass a certain size. To make it
simpler to write large applications, Microdot supports the concept of
sub-applications that can be "mounted" on a larger application, possibly with
a common URL prefix applied to all of its routes. For developers familiar with
the Flask framework, this is a similar concept to Flask's blueprints.

Consider, for example, a *customers.py* sub-application that implements
operations on customers::

    from microdot import Microdot

    customers_app = Microdot()

    @customers_app.get('/')
    async def get_customers(request):
        # return all customers

    @customers_app.post('/')
    async def new_customer(request):
        # create a new customer

Similar to the above, the *orders.py* sub-application implements operations on
customer orders::

    from microdot import Microdot

    orders_app = Microdot()

    @orders_app.get('/')
    async def get_orders(request):
        # return all orders

    @orders_app.post('/')
    async def new_order(request):
        # create a new order

Now the main application, which is stored in *main.py*, can import and mount
the sub-applications to build the larger combined application::

    from microdot import Microdot
    from customers import customers_app
    from orders import orders_app

    def create_app():
        app = Microdot()
        app.mount(customers_app, url_prefix='/customers')
        app.mount(orders_app, url_prefix='/orders')
        return app

    app = create_app()
    app.run()

The resulting application will have the customer endpoints available at
*/customers/* and the order endpoints available at */orders/*.

.. note::
   During the handling of a request, the
   :attr:`Request.url_prefix <microdot.Microdot.url_prefix>` attribute is
   set to the URL prefix under which the sub-application was mounted, or an
   empty string if the endpoint did not come from a sub-application or the
   sub-application was mounted without a URL prefix. It is possible to issue a
   redirect that is relative to the sub-application as follows::

      return redirect(request.url_prefix + '/relative-url')

When mounting an application as shown above, before-request, after-request and
error handlers defined in the sub-application are copied over to the main
application at mount time. Once installed in the main application, these
handlers will apply to the whole application and not just the sub-application
in which they were created.

The :func:`mount() <microdot.Microdot.mount>` method has a ``local`` argument
that defaults to ``False``. When this argument is set to ``True``, the
before-request, after-request and error handlers defined in the sub-application
will only apply to the sub-application.

Shutting Down the Server
^^^^^^^^^^^^^^^^^^^^^^^^

Web servers are designed to run forever, and are often stopped by sending them
an interrupt signal. But having a way to gracefully stop the server is
sometimes useful, especially in testing environments. Microdot provides a
:func:`shutdown() <microdot.Microdot.shutdown>` method that can be invoked
during the handling of a route to gracefully shut down the server when that
request completes. The next example shows how to use this feature::

    @app.get('/shutdown')
    async def shutdown(request):
        request.app.shutdown()
        return 'The server is shutting down...'

The request that invokes the ``shutdown()`` method will complete, and then the
server will not accept any new requests and stop once any remaining requests
complete. At this point the ``app.run()`` call will return.

The Request Object
~~~~~~~~~~~~~~~~~~

The :class:`Request <microdot.Request>` object encapsulates all the information
passed by the client. It is passed as an argument to route handlers, as well as
to before-request, after-request and error handlers.

Request Attributes
^^^^^^^^^^^^^^^^^^

The request object provides access to the request attributes, including:

- :attr:`method <microdot.Request.method>`: The HTTP method of the request.
- :attr:`path <microdot.Request.path>`: The path of the request.
- :attr:`args <microdot.Request.args>`: The query string parameters of the
  request, as a :class:`MultiDict <microdot.MultiDict>` object.
- :attr:`headers <microdot.Request.headers>`: The headers of the request, as a
  dictionary.
- :attr:`cookies <microdot.Request.cookies>`: The cookies that the client sent
  with the request, as a dictionary.
- :attr:`content_type <microdot.Request.content_type>`: The content type
  specified by the client, or ``None`` if no content type was specified.
- :attr:`content_length <microdot.Request.content_length>`: The content
  length of the request, or 0 if no content length was specified.
- :attr:`json <microdot.Request.json>`: The parsed JSON data in the request
  body. See :ref:`below <JSON Payloads>` for additional details.
- :attr:`form <microdot.Request.form>`: The parsed form data in the request
  body, as a dictionary. See :ref:`below <Form Data>` for additional details.
- :attr:`files <microdot.Request.files>`: A dictionary with the file uploads
  included in the request body. Note that file uploads are only supported when
  the :ref:`Multipart Forms` extension is used.
- :attr:`client_addr <microdot.Request.client_addr>`: The network address of
  the client, as a tuple (host, port).
- :attr:`app <microdot.Request.app>`: The application instance that created the
  request.
- :attr:`g <microdot.Request.g>`: The ``g`` object, where handlers can store
  request-specific data to be shared among handlers. See :ref:`The "g" Object`
  for details.

JSON Payloads
^^^^^^^^^^^^^

When the client sends a request that contains JSON data in the body, the
application can access the parsed JSON data using the
:attr:`json <microdot.Request.json>` attribute. The following example shows how
to use this attribute::

    @app.post('/customers')
    async def create_customer(request):
        customer = request.json
        # do something with customer
        return {'success': True}

.. note::
   The client must set the ``Content-Type`` header to ``application/json`` for
   the ``json`` attribute of the request object to be populated.

Form Data
^^^^^^^^^

The request object also supports standard HTML form submissions through the
:attr:`form <microdot.Request.form>` attribute, which presents the form data
as a :class:`MultiDict <microdot.MultiDict>` object. Example::

    @app.route('/', methods=['GET', 'POST'])
    async def index(req):
        name = 'Unknown'
        if req.method == 'POST':
            name = req.form.get('name')
        return f'Hello {name}'

.. note::
   Form submissions automatically parsed when the ``Content-Type`` header is
   set by the client to ``application/x-www-form-urlencoded``. For form
   submissions that use the ``multipart/form-data`` content type the
   :ref:`Multipart Forms` extension must be used.

Accessing the Raw Request Body
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For cases in which neither JSON nor form data is expected, the
:attr:`body <microdot.Request.body>` request attribute returns the entire body
of the request as a byte sequence.

If the expected body is too large to fit safely in memory, the application can
use the :attr:`stream <microdot.Request.stream>` request attribute to read the
body contents as a file-like object. The
:attr:`max_body_length <microdot.Request.max_body_length>` attribute of the
request object defines the size at which bodies are streamed instead of loaded
into memory.

Cookies
^^^^^^^

Cookies that are sent by the client are made available through the
:attr:`cookies <microdot.Request.cookies>` attribute of the request object in
dictionary form.

The "g" Object
^^^^^^^^^^^^^^

Sometimes applications need to store data during the lifetime of a request, so
that it can be shared between the before- and after-request handlers, the
route function and any error handlers. The request object provides the
:attr:`g <microdot.Request.g>` attribute for that purpose.

In the following example, a before request handler authorizes the client and
stores the username so that the route function can use it::

    @app.before_request
    async def authorize(request):
        username = authenticate_user(request)
        if not username:
            return 'Unauthorized', 401
        request.g.username = username

    @app.get('/')
    async def index(request):
        return f'Hello, {request.g.username}!'

Request-Specific After-Request Handlers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes applications need to perform operations on the response object
before it is sent to the client, for example to set or remove a cookie. A good
option to use for this is to define a request-specific after-request handler
using the :func:`after_request <microdot.Microdot.after_request>` decorator.
Request-specific after-request handlers are called by Microdot after the route
function returns and all the application-wide after-request handlers have been
called.

The next example shows how a cookie can be updated using a request-specific
after-request handler defined inside a route function::

    @app.post('/logout')
    async def logout(request):
        @request.after_request
        def reset_session(request, response):
            response.set_cookie('session', '', http_only=True)
            return response

        return 'Logged out'

Request Limits
^^^^^^^^^^^^^^

To help prevent malicious attacks, Microdot provides some configuration options
to limit the amount of information that is accepted:

- :attr:`max_content_length <microdot.Request.max_content_length>`: The
  maximum size accepted for the request body, in bytes. When a client sends a
  request that is larger than this, the server will respond with a 413 error.
  The default is 16KB.
- :attr:`max_body_length <microdot.Request.max_body_length>`: The maximum
  size that is loaded in the :attr:`body <microdot.Request.body>` attribute, in
  bytes. Requests that have a body that is larger than this size but smaller
  than the size set for ``max_content_length`` can only be accessed through the
  :attr:`stream <microdot.Request.stream>` attribute. The default is also 16KB.
- :attr:`max_readline <microdot.Request.max_readline>`: The maximum allowed
  size for a request line, in bytes. The default is 2KB.

The following example configures the application to accept requests with
payloads up to 1MB in size, but prevents requests that are larger than 8KB from
being loaded into memory::

    from microdot import Request

    Request.max_content_length = 1024 * 1024
    Request.max_body_length = 8 * 1024

Responses
~~~~~~~~~

The value or values that are returned from the route function are used by
Microdot to build the response that is sent to the client. The following
sections describe the different types of responses that are supported.

The Three Parts of a Response
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Route functions can return one, two or three values. The first and most
important value is the response body::

    @app.get('/')
    async def index(request):
        return 'Hello, World!'

In the above example, Microdot issues a standard 200 status code response
indicating a successful request. The body of the response is the
``'Hello, World!'`` string returned by the function. Microdot includes default
headers with this response, including the ``Content-Type`` header set to
``text/plain`` to indicate a response in plain text.

The application can provide its own status code as a second value returned from
the route to override the 200 default. The example below returns a 202 status
code::

    @app.get('/')
    async def index(request):
        return 'Hello, World!', 202

The application can also return a third value, a dictionary with additional
headers that are added to, or replace the default ones included by Microdot.
The next example returns an HTML response, instead of the default plain text
response::

    @app.get('/')
    async def index(request):
        return '<h1>Hello, World!</h1>', 202, {'Content-Type': 'text/html'}

If the application does not need to return a body, then it can omit it and
have the status code as the first or only returned value::

    @app.get('/')
    async def index(request):
        return 204

Likewise, if the application needs to return a body and custom headers, but
does not need to change the default status code, then it can return two values,
omitting the status code::

    @app.get('/')
    async def index(request):
        return '<h1>Hello, World!</h1>', {'Content-Type': 'text/html'}

Lastly, the application can also return a :class:`Response <microdot.Response>`
object containing all the details of the response as a single value.

JSON Responses
^^^^^^^^^^^^^^

If the application needs to return a response with JSON formatted data, it can
return a dictionary or a list as the first value, and Microdot will
automatically format the response as JSON.

Example::

    @app.get('/')
    async def index(request):
        return {'hello': 'world'}

.. note::
   A ``Content-Type`` header set to ``application/json`` is automatically added
   to the response.

Redirects
^^^^^^^^^

The :func:`redirect <microdot.Response.redirect>` function is a helper that
creates redirect responses::

    from microdot import redirect

    @app.get('/')
    async def index(request):
        return redirect('/about')

File Responses
^^^^^^^^^^^^^^

The :func:`send_file <microdot.Response.send_file>` function builds a response
object for a file::

        from microdot import send_file

        @app.get('/')
        async def index(request):
            return send_file('/static/index.html')

A suggested caching duration can be returned to the client in the ``max_age``
argument::

        from microdot import send_file

        @app.get('/')
        async def image(request):
            return send_file('/static/image.jpg', max_age=3600)  # in seconds

.. note::
   Unlike other web frameworks, Microdot does not automatically configure a
   route to serve static files. The following is an example route that can be
   added to the application to serve static files from a *static* directory in
   the project::

        @app.route('/static/<path:path>')
        async def static(request, path):
            if '..' in path:
                # directory traversal is not allowed
                return 'Not found', 404
            return send_file('static/' + path, max_age=86400)

Streaming Responses
^^^^^^^^^^^^^^^^^^^

Instead of providing a response as a single value, an application can opt to
return a response that is generated in chunks, by returning a Python generator.
The example below returns all the numbers in the fibonacci sequence below 100::

    @app.get('/fibonacci')
    async def fibonacci(request):
        async def generate_fibonacci():
            a, b = 0, 1
            while a < 100:
                yield str(a) + '\n'
                a, b = b, a + b

        return generate_fibonacci()

.. note::
   Under CPython, the generator function can be a ``def`` or ``async def``
   function, as well as a class-based generator.

   Under MicroPython, asynchronous generator functions are not supported, so
   only ``def`` generator functions can be used. Asynchronous class-based
   generators are supported.

Changing the Default Response Content Type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Microdot uses a ``text/plain`` content type by default for responses that do
not explicitly include the ``Content-Type`` header. The application can change
this default by setting the desired content type in the
:attr:`default_content_type <microdot.Response.default_content_type>` attribute
of the :class:`Response <microdot.Response>` class.

The example that follows configures the application to use ``text/html`` as
default content type::

    from microdot import Response

    Response.default_content_type = 'text/html'

Setting Cookies
^^^^^^^^^^^^^^^

Many web applications rely on cookies to maintain client state between
requests. Cookies can be set with the ``Set-Cookie`` header in the response,
but since this is such a common practice, Microdot provides the
:func:`set_cookie() <microdot.Response.set_cookie>` method in the response
object to add a properly formatted cookie header to the response.

Given that route functions do not normally work directly with the response
object, the recommended way to set a cookie is to do it in a
:ref:`request-specific after-request handler <Request-Specific After-Request Handlers>`.

Example::

    @app.get('/')
    async def index(request):
        @request.after_request
        async def set_cookie(request, response):
            response.set_cookie('name', 'value')
            return response

        return 'Hello, World!'

Another option is to create a response object directly in the route function::

    @app.get('/')
    async def index(request):
        response = Response('Hello, World!')
        response.set_cookie('name', 'value')
        return response

.. note::
   Standard cookies do not offer sufficient privacy and security controls, so
   never store sensitive information in them unless you are adding additional
   protection mechanisms such as encryption or cryptographic signing. The
   :ref:`session <Maintaining Secure User Sessions>` extension implements signed
   cookies that prevent tampering by malicious actors.

Concurrency
~~~~~~~~~~~

Microdot implements concurrency through the ``asyncio`` package, which means
that applications must be careful to prevent blocking in their handlers.

"async def" handlers
^^^^^^^^^^^^^^^^^^^^

The recommendation for route handlers in Microdot is to use asynchronous
functions, declared as ``async def``. Microdot executes these handler
functions as native asynchronous tasks. The standard considerations for writing
asynchronous code apply, and in particular blocking calls should be avoided to
ensure the application runs smoothly and is always responsive.

"def" handlers
^^^^^^^^^^^^^^

Microdot also supports the use of synchronous route handlers, declared as
standard ``def`` functions. These handlers are handled differently under
CPython and MicroPython.

When running on CPython, Microdot executes synchronous handlers in a
`thread executor <https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor>`_,
which uses a thread pool. The use of blocking or CPU intensive code in these
handlers does not have such a negative effect on the application, because
handlers do not run on the same thread as the asynchronous loop. On the other
hand, the application will be affected by threading issues such as those caused
by the Global Interpreter Lock.

Under MicroPython the situation is different. Most microcontroller boards
do not have or have very limited threading support, so Microdot executes
synchronous handlers in the main and often only thread available. This means
that these functions will block the asynchronous loop when they take too long
to complete. The use of properly written asynchronous handlers should be
preferred.

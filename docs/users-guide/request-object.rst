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

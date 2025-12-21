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

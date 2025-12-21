Defining Routes
~~~~~~~~~~~~~~~

In Microdot, routes define the logic of the web application.

The route decorator
^^^^^^^^^^^^^^^^^^^
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

An application can define multiple routes. Microdot uses the path portion of
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

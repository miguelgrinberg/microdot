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

import jwt

secret_key = None


def set_session_secret_key(key):
    """Set the secret key for signing user sessions.

    :param key: The secret key, as a string or bytes object.
    """
    global secret_key
    secret_key = key


def get_session(request):
    """Retrieve the user session.

    :param request: The client request.

    The return value is a dictionary with the data stored in the user's
    session, or ``{}`` if the session data is not available or invalid.
    """
    global secret_key
    if not secret_key:
        raise ValueError('The session secret key is not configured')
    if hasattr(request.g, '_session'):
        return request.g._session
    session = request.cookies.get('session')
    if session is None:
        request.g._session = {}
        return request.g._session
    try:
        session = jwt.decode(session, secret_key, algorithms=['HS256'])
    except jwt.exceptions.PyJWTError:  # pragma: no cover
        request.g._session = {}
    else:
        request.g._session = session
    return request.g._session


def update_session(request, session):
    """Update the user session.

    :param request: The client request.
    :param session: A dictionary with the update session data for the user.

    Calling this function adds a cookie with the updated session to the request
    currently being processed.
    """
    if not secret_key:
        raise ValueError('The session secret key is not configured')

    encoded_session = jwt.encode(session, secret_key, algorithm='HS256')

    @request.after_request
    def _update_session(request, response):
        response.set_cookie('session', encoded_session, http_only=True)
        return response


def delete_session(request):
    """Remove the user session.

    :param request: The client request.

    Calling this function adds a cookie removal header to the request currently
    being processed.
    """
    @request.after_request
    def _delete_session(request, response):
        response.set_cookie('session', '', http_only=True,
                            expires='Thu, 01 Jan 1970 00:00:01 GMT')
        return response


def with_session(f):
    """Decorator that passes the user session to the route handler.

    The session dictionary is passed to the decorated function as an argument
    after the request object. Example::

        @app.route('/')
        @with_session
        def index(request, session):
            return 'Hello, World!'

    Note that the decorator does not save the session. To update the session,
    call the :func:`update_session <microdot_session.update_session>` function.
    """
    def wrapper(request, *args, **kwargs):
        return f(request, get_session(request), *args, **kwargs)

    for attr in ['__name__', '__doc__', '__module__', '__qualname__']:
        try:
            setattr(wrapper, attr, getattr(f, attr))
        except AttributeError:  # pragma: no cover
            pass
    return wrapper

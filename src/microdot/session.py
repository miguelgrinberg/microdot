import jwt
from microdot.microdot import invoke_handler

secret_key = None


class SessionDict(dict):
    """A session dictionary.

    The session dictionary is a standard Python dictionary that has been
    extended with convenience ``save()`` and ``delete()`` methods.
    """
    def __init__(self, request, session_dict):
        super().__init__(session_dict)
        self.request = request

    def save(self):
        """Update the session cookie."""
        self.request.app._session.update(self.request, self)

    def delete(self):
        """Delete the session cookie."""
        self.request.app._session.delete(self.request)


class Session:
    """
    :param app: The application instance.
    :param key: The secret key, as a string or bytes object.
    """
    secret_key = None

    def __init__(self, app=None, secret_key=None):
        self.secret_key = secret_key
        if app is not None:
            self.initialize(app)

    def initialize(self, app, secret_key=None):
        if secret_key is not None:
            self.secret_key = secret_key
        app._session = self

    def get(self, request):
        """Retrieve the user session.

        :param request: The client request.

        The return value is a session dictionary with the data stored in the
        user's session, or ``{}`` if the session data is not available or
        invalid.
        """
        if not self.secret_key:
            raise ValueError('The session secret key is not configured')
        if hasattr(request.g, '_session'):
            return request.g._session
        session = request.cookies.get('session')
        if session is None:
            request.g._session = SessionDict(request, {})
            return request.g._session
        try:
            session = jwt.decode(session, self.secret_key,
                                 algorithms=['HS256'])
        except jwt.exceptions.PyJWTError:  # pragma: no cover
            request.g._session = SessionDict(request, {})
        else:
            request.g._session = SessionDict(request, session)
        return request.g._session

    def update(self, request, session):
        """Update the user session.

        :param request: The client request.
        :param session: A dictionary with the update session data for the user.

        Applications would normally not call this method directly, instead they
        would use the :meth:`SessionDict.save` method on the session
        dictionary, which calls this method. For example::

            @app.route('/')
            @with_session
            def index(request, session):
                session['foo'] = 'bar'
                session.save()
                return 'Hello, World!'

        Calling this method adds a cookie with the updated session to the
        request currently being processed.
        """
        if not self.secret_key:
            raise ValueError('The session secret key is not configured')

        encoded_session = jwt.encode(session, self.secret_key,
                                     algorithm='HS256')

        @request.after_request
        def _update_session(request, response):
            response.set_cookie('session', encoded_session, http_only=True)
            return response

    def delete(self, request):
        """Remove the user session.

        :param request: The client request.

        Applications would normally not call this method directly, instead they
        would use the :meth:`SessionDict.delete` method on the session
        dictionary, which calls this method. For example::

            @app.route('/')
            @with_session
            def index(request, session):
                session.delete()
                return 'Hello, World!'

        Calling this method adds a cookie removal header to the request
        currently being processed.
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
    call the :func:`session.save() <microdot.session.SessionDict.save>` method.
    """
    async def wrapper(request, *args, **kwargs):
        return await invoke_handler(
            f, request, request.app._session.get(request), *args, **kwargs)

    for attr in ['__name__', '__doc__', '__module__', '__qualname__']:
        try:
            setattr(wrapper, attr, getattr(f, attr))
        except AttributeError:  # pragma: no cover
            pass
    return wrapper

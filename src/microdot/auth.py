from time import time
from microdot import abort, redirect
from microdot.microdot import urlencode, invoke_handler


class BaseAuth:
    def __init__(self):
        self.auth_callback = None
        self.error_callback = lambda request: abort(401)

    def __call__(self, f):
        """Decorator to protect a route with authentication.

        Microdot will only call the route if the authentication callback
        returns a valid user object, otherwise it will call the error
        callback."""
        async def wrapper(request, *args, **kwargs):
            auth = self._get_auth(request)
            if not auth:
                return await invoke_handler(self.error_callback, request)
            request.g.current_user = await invoke_handler(
                self.auth_callback, request, *auth)
            if not request.g.current_user:
                return await invoke_handler(self.error_callback, request)
            return await invoke_handler(f, request, *args, **kwargs)

        return wrapper


class HTTPAuth(BaseAuth):
    def authenticate(self, f):
        """Decorator to configure the authentication callback.

        Microdot calls the authentication callback to allow the application to
        check user credentials.
        """
        self.auth_callback = f


class BasicAuth(HTTPAuth):
    def __init__(self, realm='Please login', charset='UTF-8', scheme='Basic',
                 error_status=401):
        super().__init__()
        self.realm = realm
        self.charset = charset
        self.scheme = scheme
        self.error_status = error_status
        self.error_callback = self.authentication_error

    def _get_auth(self, request):
        auth = request.headers.get('Authorization')
        if auth and auth.startswith('Basic '):
            import binascii
            try:
                username, password = binascii.a2b_base64(
                    auth[6:]).decode().split(':', 1)
            except Exception:  # pragma: no cover
                return None
            return username, password

    def authentication_error(self, request):
        return '', self.error_status, {
            'WWW-Authenticate': '{} realm="{}", charset="{}"'.format(
                self.scheme, self.realm, self.charset)}


class TokenAuth(HTTPAuth):
    def __init__(self, header='Authorization', scheme='Bearer'):
        super().__init__()
        self.header = header
        self.scheme = scheme.lower()

    def _get_auth(self, request):
        auth = request.headers.get(self.header)
        if auth:
            if self.header == 'Authorization':
                try:
                    scheme, token = auth.split(' ', 1)
                except Exception:
                    return None
                if scheme.lower() == self.scheme:
                    return (token.strip(),)
            else:
                return (auth,)

    def errorhandler(self, f):
        """Decorator to configure the error callback.

        Microdot calls the error callback to allow the application to generate
        a custom error response. The default error response is to call
        ``abort(401)``.
        """
        self.error_callback = f


class LoginAuth(BaseAuth):
    def __init__(self, login_url='/login'):
        super().__init__()
        self.login_url = login_url
        self.user_callback = None
        self.user_id_callback = None
        self.auth_callback = self._authenticate
        self.error_callback = self._redirect_to_login

    def id_to_user(self, f):
        """Decorator to configure the user callback.

        Microdot calls the user callback to load the user object from the
        user ID stored in the user session.
        """
        self.user_callback = f

    def user_to_id(self, f):
        """Decorator to configure the user ID callback.

        Microdot calls the user ID callback to load the user ID from the
        user session.
        """
        self.user_id_callback = f

    def _get_session(self, request):
        return request.app._session.get(request)

    def _update_remember_cookie(self, request, days, user_id=None):
        remember_payload = request.app._session.encode({
            'user_id': user_id,
            'days': days,
            'exp': time() + days * 24 * 60 * 60
        })

        @request.after_request
        async def _set_remember_cookie(request, response):
            response.set_cookie('_remember', remember_payload,
                                max_age=days * 24 * 60 * 60)
            return response

    def _get_auth(self, request):
        session = self._get_session(request)
        if session and '_user_id' in session:
            return (session['_user_id'],)
        if '_remember' in request.cookies:
            remember_payload = request.app._session.decode(
                request.cookies['_remember'])
            user_id = remember_payload.get('user_id')
            if user_id:
                self._update_remember_cookie(
                    request, remember_payload.get('_days', 30), user_id)
                session['_user_id'] = user_id
                session['_fresh'] = False
                session.save()
                return (user_id,)

    async def _authenticate(self, request, user_id):
        return await invoke_handler(self.user_callback, user_id)

    async def _redirect_to_login(self, request):
        return '', 302, {'Location': self.login_url + '?next=' + urlencode(
            request.url)}

    async def login_user(self, request, user, remember=False,
                         redirect_url='/'):
        """Log a user in.

        :param request: the request object
        :param user: the user object
        :param remember: if the user's logged in state should be remembered
                         with a cookie after the session ends. Set to the
                         number of days the remember cookie should last, or to
                         ``True`` to use a default duration of 30 days.
        :param redirect_url: the URL to redirect to after login

        This call marks the user as logged in by storing their user ID in the
        user session. The application must call this method to log a user in
        after their credentials have been validated.

        The method returns a redirect response, either to the URL the user
        originally intended to visit, or if there is no original URL to the URL
        specified by the `redirect_url`.
        """
        session = self._get_session(request)
        session['_user_id'] = await invoke_handler(self.user_id_callback, user)
        session['_fresh'] = True
        session.save()

        if remember:
            days = 30 if remember is True else int(remember)
            self._update_remember_cookie(request, days, session['_user_id'])

        next_url = request.args.get('next', redirect_url)
        if not next_url.startswith('/'):
            next_url = redirect_url
        return redirect(next_url)

    async def logout_user(self, request):
        """Log a user out.

        :param request: the request object

        This call removes information about the user's log in from the user
        session. If a remember cookie exists, it is removed as well.
        """
        session = self._get_session(request)
        session.pop('_user_id', None)
        session.pop('_fresh', None)
        session.save()
        if '_remember' in request.cookies:
            self._update_remember_cookie(request, 0)

    def __call__(self, f):
        """Decorator to protect a route with authentication.

        If the user is not logged in, Microdot will redirect to the login page
        first. The decorated route will only run after successful login by the
        user. If the user is already logged in, the route will run immediately.
        """
        return super().__call__(f)

    def fresh(self, f):
        """Decorator to protect a route with "fresh" authentication.

        This decorator prevents the route from running when the login session
        is not fresh. A fresh session is a session that has been created from
        direct user interaction with the login page, as opposite to a session
        that was restored from a "remember me" cookie.
        """
        base_wrapper = super().__call__(f)

        async def wrapper(request, *args, **kwargs):
            session = self._get_session(request)
            if session.get('_fresh'):
                return await base_wrapper(request, *args, **kwargs)
            return await invoke_handler(self.error_callback, request)

        return wrapper

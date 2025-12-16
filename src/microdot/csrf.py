import binascii
import hashlib
import hmac
import os
from time import time

from microdot import abort

# TODO
# add HSTS header (secure.py?)
# add current user to HMAC if logged in
# make expiration optional (defaults to no expiration?)
# add samesite=strict
# update csrf token when user logs in or out


class CSRF:
    """CSRF protection for Microdot routes.

    This class adds CSRF protection to all requests that use state changing
    verbs (all methods except ``GET``, ``QUERY``, ``HEAD`` and ``OPTIONS``).

    :param app: The application instance.
    :param secret_key: The secret key for token signing, as a string or bytes
                       object. If not given, the secret key configured in the
                       session is used.
    :param cookie_options: A dictionary with cookie options to pass as
                           arguments to :meth:`Response.set_cookie()
                           <microdot.Response.set_cookie>`.
    :param protect_all: If ``True``, all state changing routes are protected by
                        default. If ``False``, only routes decorated with the
                        :meth:`protect` decorator are protected.
    :param time_limit: The time limit for CSRF tokens, in seconds. The default
                       is 0, which means that tokens do not expire. Note that
                       using an expiration time can create some usability
                       issues if the user stays on a page for a long time and
                       the token expires.

    The CSRF token is returned to the client in a ``csrf_token`` cookie, and
    the client is expected to send this token back in requests that have CSRF
    protection enabled. If the request includes a form submission, then the
    token can be added as a ``csrf_token`` form field. Otherwise, the client
    must include it in a ``X-CSRF-Token`` header.
    """
    def __init__(self, app=None, secret_key=None, cookie_options=None,
                 protect_all=True, time_limit=0):
        if isinstance(secret_key, str):
            self.secret_key = secret_key.encode()
        else:
            self.secret_key = secret_key
        self.cookie_options = cookie_options or {}
        self.protect_all = protect_all
        self.time_limit = time_limit
        self.exempt_routes = []
        self.protected_routes = []
        if app is not None:
            self.initialize(app, secret_key)

    def get_current_user_id(self, request):
        user_id = None
        session = None
        try:
            session = request.app._session.get(request)
        except AttributeError:
            pass
        if session and '_user_id' in session:
            user_id = session['_user_id']
        if user_id and not isinstance(user_id, bytes):
            user_id = str(user_id).encode()
        return user_id or b''

    def generate_csrf_token_payload(self):
        session_id = binascii.hexlify(os.urandom(20))
        current_time = str(int(time())).encode()
        return session_id + b'.' + current_time

    def generate_csrf_token(self, request):
        csrf_token = self.generate_csrf_token_payload()
        signature = hmac.new(
            self.secret_key,
            csrf_token + b'.' + self.get_current_user_id(request),
            hashlib.sha256
        ).hexdigest()
        return csrf_token.decode() + '.' + signature

    def validate_csrf_token(self, token, request):
        try:
            csrf_token, signature = token.rsplit('.', 1)
        except Exception:
            return False
        if hmac.new(
            self.secret_key,
            csrf_token.encode() + b'.' + self.get_current_user_id(request),
            hashlib.sha256
        ).hexdigest() != signature:
            return False
        if self.time_limit > 0:
            tm = int(csrf_token.split('.', 1)[1])
            return tm + self.time_limit >= time()
        return True

    def initialize(self, app, secret_key=None, cookie_options=None,
                   protect_all=None, time_limit=None):
        """Initialize the CSRF class.

        :param app: The application instance.
        :param secret_key: The secret key for token signing, as a string or
                           bytes object.
        :param cookie_options: A dictionary with cookie options to pass as
                               arguments to :meth:`Response.set_cookie()
                               <microdot.Response.set_cookie>`.
        :param protect_all: If ``True``, all state changing routes are
                            protected by default. If ``False``, only routes
                            decorated with the :meth:`protect` decorator are
                            protected.
        :param time_limit: The time limit for CSRF tokens, in seconds. The
                           default is 0, which means that tokens do not expire.
                           Note that using an expiration time can create some
                           usability issues if the user stays on a page for a
                           long time and the token expires.
        """
        if secret_key is not None:
            if isinstance(secret_key, str):
                self.secret_key = secret_key.encode()
            else:
                self.secret_key = secret_key
        if self.secret_key is None:
            if isinstance(app._session.secret_key, str):
                self.secret_key = app._session.secret_key.encode()
            else:
                self.secret_key = app._session.secret_key
        if cookie_options is not None:
            self.cookie_options = cookie_options
        if protect_all is not None:
            self.protect_all = protect_all
        if time_limit is not None:
            self.time_limit = time_limit

        @app.before_request
        async def csrf_before_request(request):
            if (
                self.protect_all
                and request.method not in ['GET', 'QUERY', 'HEAD', 'OPTIONS']
                and request.route not in self.exempt_routes
            ) or request.route in self.protected_routes:
                # ensure that a valid CSRF token was provided
                csrf_token = None
                if request.method == 'POST' and request.form and \
                        'csrf_token' in request.form:
                    csrf_token = request.form['csrf_token']
                else:
                    csrf_token = request.headers.get('X-CSRF-Token')
                if not self.validate_csrf_token(csrf_token, request):
                    abort(403, 'Invalid CSRF token')

        @app.after_request
        def csrf_after_request(request, response):
            if '_csrf_token' not in request.cookies:
                options = self.cookie_options
                if 'secure' not in options and request.scheme == 'https':
                    options['secure'] = True
                response.set_cookie('_csrf_token',
                                    self.generate_csrf_token(request),
                                    **options)

    def exempt(self, f):
        """Decorator to exempt a route from CSRF protection.

        This decorator must be added immediately after the route decorator to
        disable CSRF protection on the route. Example::

            @app.post('/submit')
            @csrf.exempt
            # add additional decorators here
            def submit(request):
                # ...
        """
        self.exempt_routes.append(f)
        return f

    def protect(self, f):
        """Decorator to protect a route against CSRF attacks.

        This is useful when it is necessary to protect a request that uses one
        of the safe methods that are not supposed to make state changes. The
        decorator must be added immediately after the route decorator to
        disable CSRF protection on the route. Example::

            @app.get('/data')
            @csrf.force
            # add additional decorators here
            def get_data(request):
                # ...
        """
        self.protected_routes.append(f)
        return f

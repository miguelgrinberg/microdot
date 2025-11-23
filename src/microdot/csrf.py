import binascii
import hashlib
import hmac
import os
import time

from microdot import abort


class CSRF:
    """CSRF protection for Microdot routes.

    This class adds CSRF protection to all requests that use state changing
    verbs (all methods except ``GET``, ``HEAD`` and ``OPTIONS``).

    :param app: The application instance.
    :param secret_key: The secret key for token signing, as a string or bytes
                       object.
    :param time_limit: the duration of the CSRF token, in seconds. Defaults to
                       one hour.
    :param cookie_options: A dictionary with cookie options to pass as
                           arguments to :meth:`Response.set_cookie()
                           <microdot.Response.set_cookie>`.

    The CSRF token is returned to the client in a ``csrf_token`` cookie, and
    the client is expected to send this token back in all state changing
    requests. If the request includes a form submission, then the token can be
    added as a ``csrf_token`` form field. Otherwise, the client must include it
    in a ``X-CSRF-Token`` header.
    """
    def __init__(self, app=None, secret_key=None, time_limit=60 * 60,
                 cookie_options=None):
        self.app = None
        if isinstance(secret_key, str):
            self.secret_key = secret_key.encode()
        else:
            self.secret_key = secret_key
        self.time_limit = time_limit
        self.cookie_options = cookie_options or {}
        self.exempt_routes = []
        self.forced_routes = []
        if app is not None:
            self.initialize(app, secret_key)

    def generate_csrf_token(self):
        csrf_token = binascii.hexlify(os.urandom(20))
        expiration = str(int(time.time()) + self.time_limit).encode()
        signature = hmac.new(self.secret_key, csrf_token + b'.' + expiration,
                             hashlib.sha256).hexdigest()
        return csrf_token.decode() + '.' + expiration.decode() + '.' + \
            signature

    def validate_csrf_token(self, token):
        try:
            csrf_token, expiration, signature = token.split('.')
            if time.time() > int(expiration):
                return False
        except Exception:
            return False
        return hmac.new(self.secret_key,
                        (csrf_token + '.' + expiration).encode(),
                        hashlib.sha256).hexdigest() == signature

    def initialize(self, app, secret_key=None, time_limit=None,
                   cookie_options=None):
        """Initialize the CSRF class.

        :param app: The application instance.
        :param secret_key: The secret key for token signing, as a string or
                           bytes object.
        :param time_limit: the duration of the CSRF token, in seconds. Defaults
                           to one hour.
        :param cookie_options: A dictionary with cookie options to pass as
                               arguments to :meth:`Response.set_cookie()
                               <microdot.Response.set_cookie>`.
        """
        self.app = app
        if secret_key:
            if isinstance(secret_key, str):
                self.secret_key = secret_key.encode()
            else:
                self.secret_key = secret_key
        if time_limit:
            self.time_limit = time_limit
        if cookie_options:
            self.cookie_options = cookie_options
        if 'secure' not in self.cookie_options and not app.debug:
            self.cookie_options['secure'] = True

        @self.app.before_request
        async def csrf_before_request(request):
            if (request.method not in ['GET', 'HEAD', 'OPTIONS']
                    and request.route not in self.exempt_routes) or \
                    request.route in self.forced_routes:
                # ensure that a valid CSRF token was provided
                csrf_token = None
                if request.method == 'POST' and request.form and \
                        'csrf_token' in request.form:
                    csrf_token = request.form['csrf_token']
                else:
                    csrf_token = request.headers.get('X-CSRF-Token')
                if not self.validate_csrf_token(csrf_token):
                    abort(403, 'Invalid CSRF token')

        @self.app.after_request
        def csrf_after_request(request, response):
            if 'csrf_token' not in request.cookies:
                response.set_cookie('csrf_token', self.generate_csrf_token(),
                                    **self.cookie_options)

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

    def force(self, f):
        """Decorator to force a route to be included in CSRF protection.

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
        self.forced_routes.append(f)
        return f

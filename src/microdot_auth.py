from microdot import abort


class BaseAuth:
    def __init__(self, header='Authorization', scheme=None):
        self.auth_callback = None
        self.error_callback = self.auth_failed
        self.header = header
        self.scheme = scheme.lower()

    def callback(self, f):
        """Decorator to configure the authentication callback.

        Microdot calls the authentication callback to allow the application to
        check user credentials.
        """
        self.auth_callback = f

    def errorhandler(self, f):
        """Decorator to configure the error callback.

        Microdot calls the error callback to allow the application to generate
        a custom error response. The default error response is to call
        ``abort(401)``.
        """
        self.error_callback = f

    def auth_failed(self):
        abort(401)

    def __call__(self, func):
        def wrapper(request, *args, **kwargs):
            auth = request.headers.get(self.header)
            if not auth:
                return self.error_callback()
            if self.header == 'Authorization':
                if ' ' not in auth:
                    return self.error_callback()
                scheme, auth = auth.split(' ', 1)
                if scheme.lower() != self.scheme:
                    return self.error_callback()
            if not self.auth_callback(request, *self._get_auth_args(auth)):
                return self.error_callback()
            return func(request, *args, **kwargs)

        return wrapper


class BasicAuth(BaseAuth):
    def __init__(self):
        super().__init__(scheme='Basic')

    def _get_auth_args(self, auth):
        import binascii
        username, password = binascii.a2b_base64(auth).decode('utf-8').split(
            ':', 1)
        return (username, password)


class TokenAuth(BaseAuth):
    def __init__(self, header='Authorization', scheme='Bearer'):
        super().__init__(header=header, scheme=scheme)

    def _get_auth_args(self, token):
        return (token,)

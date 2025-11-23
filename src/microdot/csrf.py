from microdot import abort


class CSRF:
    """CSRF protection for Microdot routes.

    This class implements CSRF protection for routes.

    :param app: The application instance.
    :param protect_all: If ``True``, all state changing routes are protected by
                        default, with the exception of routes that are
                        decorated with the :meth:`exempt` decorator. If
                        ``False``, only routes decorated with the
                        :meth:`protect` decorator are protected. The default
                        is ``True``.

    CSRF protection is implemented by checking the ``Sec-Fetch-Site`` or
    ``Origin`` headers sent by browsers.
    """
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS', 'TRACE']

    def __init__(self, app=None, protect_all=True, allow_subdomains=False,
                 allowed_origins=[]):
        self.protect_all = protect_all
        self.allow_subdomains = allow_subdomains
        self.allowed_origins = allowed_origins
        self.exempt_routes = []
        self.protected_routes = []
        if app is not None:
            self.initialize(app)

    def initialize(self, app, protect_all=None, allow_subdomains=None,
                   allowed_origins=None):
        """Initialize the CSRF class.

        :param app: The application instance.
        :param protect_all: If ``True``, all state changing routes are
                            protected by default. If ``False``, only routes
                            decorated with the :meth:`protect` decorator are
                            protected.
        """
        if protect_all is not None:
            self.protect_all = protect_all
        if allow_subdomains is not None:
            self.allow_subdomains = allow_subdomains
        if allowed_origins is not None:
            self.allowed_origins = allowed_origins

        @app.before_request
        async def csrf_before_request(request):
            origin = request.headers.get('Origin')
            if origin not in self.allowed_origins:
                if (
                    self.protect_all
                    and request.method not in self.SAFE_METHODS
                    and request.route not in self.exempt_routes
                ) or request.route in self.protected_routes:
                    allow = False
                    sfs = request.headers.get('Sec-Fetch-Site')
                    if sfs:
                        if sfs in ['same-origin', 'none']:
                            allow = True
                        elif sfs == 'same-site' and self.allow_subdomains:
                            allow = True
                    elif origin is None:
                        # origin wasn't given so this isn't a browser
                        allow = True
                    if not allow:
                        abort(403, 'Forbidden')

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

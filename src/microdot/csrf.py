from microdot import abort


class CSRF:
    """CSRF protection for Microdot routes.

    :param app: The application instance.
    :param cors: The ``CORS`` instance that defines the origins that are
                 trusted by the application. This is used to validate requests
                 from older browsers that do not send the ``Sec-Fetch-Site``
                 header.
    :param protect_all: If ``True``, all state changing routes are protected by
                        default, with the exception of routes that are
                        decorated with the :meth:`exempt <exempt>` decorator.
                        If ``False``, only routes decorated with the
                        :meth:`protect <protect>` decorator are protected. The
                        default is ``True``.
    :param allow_subdomains: If ``True``, requests from subdomains of the
                             application domain are trusted. The default is
                             ``False``.

    CSRF protection is implemented by checking the ``Sec-Fetch-Site`` sent by
    browsers. When the ``cors`` argument is provided, requests from older
    browsers that do not support the ``Sec-Fetch-Site`` header are validated
    by checking the ``Origin`` header.
    """
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

    def __init__(self, app=None, cors=None, protect_all=True,
                 allow_subdomains=False):
        self.cors = None
        self.protect_all = protect_all
        self.allow_subdomains = allow_subdomains
        self.exempt_routes = []
        self.protected_routes = []
        if app is not None:
            self.initialize(app, cors)

    def initialize(self, app, cors=None):
        """Initialize the CSRF class.

        :param app: The application instance.
        :param cors: The ``CORS`` instance that defines the origins that are
                     trusted by the application. This is used to validate
                     requests from older browsers that do not send the
                     ``Sec-Fetch-Site`` header.
        """
        self.cors = cors

        @app.before_request
        async def csrf_before_request(request):
            if (
                self.protect_all
                and request.method not in self.SAFE_METHODS
                and request.route not in self.exempt_routes
            ) or request.route in self.protected_routes:
                allow = False
                sfs = request.headers.get('Sec-Fetch-Site')
                origin = request.headers.get('Origin')
                if sfs:
                    # if the Sec-Fetch-Site header was given, ensure it is not
                    # cross-site
                    if sfs in ['same-origin', 'none']:
                        allow = True
                    elif sfs == 'same-site' and self.allow_subdomains:
                        allow = True
                if not allow and origin and self.cors and \
                        self.cors.allowed_origins != '*':
                    # if we have a list of allowed origins, then we can
                    # validate the origin
                    if not self.allow_subdomains:
                        allow = origin in self.cors.allowed_origins
                    else:
                        origin_scheme, origin_host = origin.split('://', 1)
                        for allowed_origin in self.cors.allowed_origins:
                            allowed_scheme, allowed_host = \
                                allowed_origin.split('://', 1)
                            if origin == allowed_origin or (
                                origin_host.endswith('.' + allowed_host)
                                and origin_scheme == allowed_scheme
                            ):
                                allow = True
                                break
                if not allow and not sfs and not origin:
                    allow = True  # no headers to check

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

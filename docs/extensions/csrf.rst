Cross-Site Request Forgery (CSRF) Protection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `csrf.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/csrf.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `app.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/csrf/app.py>`_

The CSRF extension provides protection against `Cross-Site Request Forgery
(CSRF) <https://owasp.org/www-community/attacks/csrf>`_ attacks. This
protection defends against attackers attempting to submit forms or other
state-changing requests from their own site on behalf of unsuspecting victims,
while taking advantage of the victims previously established sessions or
cookies to impersonate them.

This extension checks the ``Sec-Fetch-Site`` header sent by all modern web
browsers to achieve this protection. As a fallback mechanism for older browsers
that do not support this header, this extension can be linked to the CORS
extension to validate the ``Origin`` header. If you are interested in the
details of this protection mechanism, it is described in the
`OWASP CSRF Prevention Cheat Sheet <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#fetch-metadata-headers>`_
page.

.. note::
   As of December 2025, OWASP considers the use of Fetch Metadata Headers for
   CSRF protection a
   `defense in depth <https://en.wikipedia.org/wiki/Defence_in_depth>`_
   technique that is insufficient on its own.

   There is an interesting
   `discussion <https://github.com/OWASP/CheatSheetSeries/issues/1803>`_ on
   this topic in the OWASP GitHub repository where it appears to be agreement
   that this technique provides complete protection for the vast majority of
   use cases. If you are unsure if this method works for your use case, please
   read this discussion to have more context and make the right decision. 

To enable CSRF protection, create an instance of the
:class:`CSRF <microdot.csrf.CSRF>` class and configure the desired options.
Example::

    from microdot import Microdot
    from microdot.cors import CORS
    from microdot.csrf import CSRF

    app = Microdot()
    cors = CORS(app, allowed_origins=['https://example.com'])
    csrf = CSRF(app, cors)

This will protect all routes that use a state-changing method (``POST``,
``PUT``, ``PATCH`` or ``DELETE``) and will return a 403 status code response to
any requests that fail the CSRF check.

If there are routes that need to be exempted from the CSRF check, they can be
decorated with the :meth:`csrf.exempt <microdot.csrf.CSRF.exempt>` decorator::

    @app.post('/webhook')
    @csrf.exempt
    async def webhook(request):
        # ...

For some applications it may be more convenient to have CSRF checks turned off
by default, and only apply them to explicitly selected routes. In this case,
pass ``protect_all=False`` when you construct the ``CSRF`` instance and use the
:meth:`csrf.protect <microdot.csrf.CSRF.protect>` decorator::

    csrf = CSRF(app, cors, protect_all=False)

    @app.post('/submit-form')
    @csrf.protect
    async def submit_form(request):
        # ...

By default, requests coming from different subdomains are considered to be
cross-site, and as such they will not pass the CSRF check. If you'd like
subdomain requests to be considered safe, then set the
``allow_subdomains=True`` option when you create the ``CSRF`` class.

.. note::
   This extension is designed to block requests issued by web browsers when
   they are found to be unsafe or unauthorized by the application owner. The
   method used to determine if a request should be allowed or not is based on
   the value of headers that are only sent by web browsers. Clients other than
   web browsers are not affected by this extension and can send requests
   freely.

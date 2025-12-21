Cross-Origin Resource Sharing (CORS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `cors.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/cors.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `app.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/cors/app.py>`_

The CORS extension provides support for `Cross-Origin Resource Sharing
(CORS) <https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS>`_. CORS is a
mechanism that allows web applications running on different origins to access
resources from each other. For example, a web application running on
``https://example.com`` can access resources from ``https://api.example.com``.

To enable CORS support, create an instance of the
:class:`CORS <microdot.cors.CORS>` class and configure the desired options.
Example::

    from microdot import Microdot
    from microdot.cors import CORS

    app = Microdot()
    cors = CORS(app, allowed_origins=['https://example.com'],
                allow_credentials=True)

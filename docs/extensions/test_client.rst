Test Client
~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `test_client.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/test_client.py>`_

   * - Required external dependencies
     - | None

The Microdot Test Client is a utility class that can be used in tests to send
requests into the application without having to start a web server.

Example::

    from microdot import Microdot
    from microdot.test_client import TestClient

    app = Microdot()

    @app.route('/')
    def index(req):
        return 'Hello, World!'

    async def test_app():
        client = TestClient(app)
        response = await client.get('/')
        assert response.text == 'Hello, World!'

See the documentation for the :class:`TestClient <microdot.test_client.TestClient>`
class for more details.

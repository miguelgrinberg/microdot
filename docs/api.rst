API Reference
=============

Core API
--------

.. autoclass:: microdot.Microdot
   :members:

.. autoclass:: microdot.Request
   :members:

.. autoclass:: microdot.Response
   :members:

.. autoclass:: microdot.URLPattern
   :members:

Multipart Forms
---------------

.. automodule:: microdot.multipart
   :members:

WebSocket
---------

.. automodule:: microdot.websocket
   :members:

Server-Sent Events (SSE)
------------------------

.. automodule:: microdot.sse
   :members:

Templates (uTemplate)
---------------------

.. automodule:: microdot.utemplate
   :members:

Templates (Jinja)
-----------------

.. automodule:: microdot.jinja
   :members:

User Sessions
-------------

.. automodule:: microdot.session
   :members:

Authentication
--------------

.. automodule:: microdot.auth
   :inherited-members:
   :special-members: __call__
   :members:

User Logins
-----------

.. automodule:: microdot.login
   :inherited-members:
   :special-members: __call__
   :members:

Cross-Origin Resource Sharing (CORS)
------------------------------------

.. automodule:: microdot.cors
   :members:

Test Client
-----------

.. automodule:: microdot.test_client
   :members:

ASGI
----

.. autoclass:: microdot.asgi.Microdot
   :members:
   :exclude-members: shutdown, run

WSGI
----

.. autoclass:: microdot.wsgi.Microdot
   :members:
   :exclude-members: shutdown, run

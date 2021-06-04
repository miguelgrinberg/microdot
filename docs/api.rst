API Reference
=============

``microdot`` module
-------------------

The ``microdot`` module defines a few classes that help implement HTTP-based
servers for MicroPython and standard Python, with multithreading support for
Python interpreters that support it.

``Microdot`` class
~~~~~~~~~~~~~~~~~~

.. autoclass:: microdot.Microdot
   :members:

``Request`` class
~~~~~~~~~~~~~~~~~

.. autoclass:: microdot.Request
   :members:

``Response`` class
~~~~~~~~~~~~~~~~~~

.. autoclass:: microdot.Response
   :members:

``microdot_asyncio`` module
---------------------------

The ``microdot_asyncio`` module defines a few classes that help implement
HTTP-based servers for MicroPython and standard Python that use ``asyncio``
and coroutines.

``Microdot`` class
~~~~~~~~~~~~~~~~~~

.. autoclass:: microdot_asyncio.Microdot
   :inherited-members:
   :members:

``Request`` class
~~~~~~~~~~~~~~~~~

.. autoclass:: microdot_asyncio.Request
   :inherited-members:
   :members:

``Response`` class
~~~~~~~~~~~~~~~~~~

.. autoclass:: microdot_asyncio.Response
   :inherited-members:
   :members:


Installation
------------

The installation method is different depending on which flavor of Python you 
are using.

CPython Installation
~~~~~~~~~~~~~~~~~~~~

For use with standard Python (CPython) projects, Microdot and all of its core
extensions are installed with ``pip`` or any of its alternatives::

    pip install microdot

MicroPython Installation
~~~~~~~~~~~~~~~~~~~~~~~~

For MicroPython, the recommended approach is to manually copy the necessary
source files from the
`GitHub repository <https://github.com/miguelgrinberg/microdot/tree/main/src>`_
into your device.

Use the following guidelines to know what files to copy:

* For a minimal setup with only the base web server functionality, copy
  `microdot.py <https://github.com/miguelgrinberg/microdot/blob/main/src/microdot/microdot.py>`_
  to your device.
* For a configuration that includes one or more of the optional extensions,
  create a *microdot* directory in your device and copy the following files:

  * `__init__.py <https://github.com/miguelgrinberg/microdot/blob/main/src/microdot/__init__.py>`_
  * `microdot.py <https://github.com/miguelgrinberg/microdot/blob/main/src/microdot/microdot.py>`_
  * any needed `extensions <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot>`_.

Some of the low end devices are perfectly capable of running Microdot once
compiled, but do not have enough RAM for the compiler. For these cases you can
`pre-compile <https://docs.micropython.org/en/latest/reference/mpyfiles.html>`_
the files to *.mpy* files for the version of MicroPython that you use in your
device.

If space in your device is extremely tight, you may also consider
`freezing <https://docs.micropython.org/en/latest/develop/optimizations.html?highlight=frozen#frozen-bytecode>`_
the Microdot files and incorporating them into a custom MicroPython firmware.


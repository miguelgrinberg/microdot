Cross-Compiling and Freezing Microdot
-------------------------------------

.. note::
   This section only applies when using Microdot on MicroPython.

Microdot is a fairly small framework, so its size is not something you need to
be concerned about unless you are working with MicroPython on hardware with a
very small amount of disk space and/or RAM. In such cases every byte counts, so
this section provides some recommendations on how to keep Microdot's footprint
as small as possible.

Choosing What Modules to Install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Microdot has a modular design that allows you to only install the modules that
your application needs.

For minimal web application support based on the core Microdot web server
without extensions, you can just copy `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/microdot.py>`_
to the source directory on your device. The core Microdot web server does not
have any dependencies, so you don't need to install anything else.

If your application uses some of the provided extensions to the core web
server, then instead of installing *microdot.py* you'll need to create a
*microdot* subdirectory and install the following files in it:

- `__init__.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/__init__.py>`_
- `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/microdot.py>`_
- Any extension modules that you need from the `microdot <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot>`_ source directory.

Some of the extensions also have dependencies of their own, so you may need to
install those in your device as well (outside of the ``microdot``
subdirectory). Consult the documentation of each extension to learn if any
third-party dependencies are required.

Cross-Compiling
~~~~~~~~~~~~~~~

An issue that is common with low-end microcontroller boards is that they do not
have enough RAM for the MicroPython compiler to compile the source files, but
once the code is compiled they are able to run it just fine.

To address this, MicroPython allows you to cross-compile source files on your
desktop or laptop computer and then upload their compiled versions to the
device. A good strategy is to cross-compile all the dependencies that are used
by your application, since these are not going to be updated very often. If the
goal is to minimize the use of RAM, you can also opt to cross-compile your
application source files.

The MicroPython cross-compiler is available as a package that you can install
on standard Python. You must determine the version of MicroPython that you will
be running on your device, and install the compiler that matches that version.
For example, if you plan to use MicroPython 1.21.0 on your device, you can
install the cross-compiler for this version with the following command::

    pip install mpy-cross==1.21.0

Then run the cross-compiler for each source file that you want to compile.
Since the cross-compilation happens on your computer, you will need to have
copies of all the source files you need to compile locally on your disk. Here
is how you can compile the *microdot.py* file, assuming you have a copy in the
current directory in your computer::

    mpy-cross microdot.py

The cross-compiler will create a file with the same name as the source file,
but with the extension changed to *.mpy*.

Once you have all your dependencies compiled, you can replace the *.py* files
in your device with their corresponding *.mpy* versions. MicroPython
automatically recognizes *.mpy* files, so there is no need to make any changes
to any source code to start using compiled files.

Freezing
~~~~~~~~

The ultimate option to reduce the size of a MicroPython application is to
"freeze" it. Freezing is a process that takes MicroPython source code (either
dependencies, application code or both), pre-compiles it and incorporates it
into a custom-built MicroPython firmware that is flashed to the device.

Freezing MicroPython modules to firmware has the advantage that the code is
imported directly from the device's ROM, leaving more RAM available for
application use.

The process to create a custom firmware is unfortunately non-trivial and
different for each microcontroller platform, so you will need to consult the
MicroPython documentation that applies to your device to learn how to do this.

The part of the process that is common to all devices is the creation of a
`manifest file <https://docs.micropython.org/en/latest/reference/manifest.html>`_
to tell the MicroPython firmware builder which packages and modules to freeze.

For a minimal installation of Microdot consisting only in its *microdot.py*
source file, the manifest file that you need use to build the firmware must
include the following declaration::

    module('microdot')

If instead you are working with a version of Microdot that includes some or all
of its extensions, then the manifest file must reference the ``microdot``
package plus any third-party dependencies that are needed. Below is a manifest
file for a complete Microdot installation that includes all the extensions::

    package('microdot')
    package('utemplate')  # required only if templates are used
    module('pyjwt')       # required only if user sessions are used

In this example, the *microdot* and *utemplate* packages must be available in
the directory where the manifest file is located so that the MicroPython build
can find them. The `pyjwt` module is part of the MicroPython standard library
and will be downloaded as part of the build.

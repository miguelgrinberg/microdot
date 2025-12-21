Multipart Forms
~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     -  | `multipart.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/multipart.py>`_
        | `helpers.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/helpers.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `formdata.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/uploads/formdata.py>`_

The multipart extension handles multipart forms, including those that have file
uploads.

The :func:`with_form_data <microdot.multipart.with_form_data>` decorator
provides the simplest way to work with these forms. With this decorator added
to the route, whenever the client sends a multipart request the
:attr:`request.form <microdot.Request.form>` and
:attr:`request.files <microdot.Request.files>` properties are populated with
the submitted data. For form fields the field values are always strings. For
files, they are instances of the
:class:`FileUpload <microdot.multipart.FileUpload>` class.

Example::

    from microdot.multipart import with_form_data

    @app.post('/upload')
    @with_form_data
    async def upload(request):
        print('form fields:', request.form)
        print('files:', request.files)

One disadvantage of the ``@with_form_data`` decorator is that it has to copy
any uploaded files to memory or temporary disk files, depending on their size.
The :attr:`FileUpload.max_memory_size <microdot.multipart.FileUpload.max_memory_size>`
attribute can be used to control the cutoff size above which a file upload
is transferred to a temporary file.

A more performant alternative to the ``@with_form_data`` decorator is the
:class:`FormDataIter <microdot.multipart.FormDataIter>` class, which iterates
over the form fields sequentially, giving the application the option to parse
the form fields on the fly and decide what to copy and what to discard. When
using ``FormDataIter`` the ``request.form`` and ``request.files`` attributes
are not used.

Example::


    from microdot.multipart import FormDataIter

    @app.post('/upload')
    async def upload(request):
        async for name, value in FormDataIter(request):
            print(name, value)

For fields that contain an uploaded file, the ``value`` returned by the
iterator is the same ``FileUpload`` instance. The application can choose to
save the file with the :meth:`save() <microdot.multipart.FileUpload.save>`
method, or read it with the :meth:`read() <microdot.multipart.FileUpload.read>`
method, optionally passing a size to read it in chunks. The
:meth:`copy() <microdot.multipart.FileUpload.copy>` method is also available to
apply the copying logic used by the ``@with_form_data`` decorator, which is
inefficient but allows the file to be set aside to be processed later, after
the remaining form fields.

from microdot import abort, iscoroutine
from microdot.helpers import wraps


class FormDataIter:
    """Asynchronous iterator that parses a ``multipart/form-data`` body and
    returns form fields and files as they are parsed.

    :param request: the request object to parse.

    Example usage::

        from microdot.multipart import FormDataIter

        async for name, value in FormDataIter(request):
            print(name, value)

    The iterator returns no values when the request has a content type other
    than ``multipart/form-data``. For a file field, the returned value is of
    type :class:`FileUpload`, which supports the
    :meth:`read() <FileUpload.read>` and :meth:`save() <FileUpload.save>`
    methods. Values for regular fields are provided as strings.

    The request body is read efficiently in chunks of size
    :attr:`buffer_size <FormDataIter.buffer_size>`. On iterations in which a
    file field is encountered, the file must be consumed before moving on to
    the next iteration, as the internal stream stored in ``FileUpload``
    instances is invalidated at the end of the iteration.
    """
    #: The size of the buffer used to read chunks of the request body.
    buffer_size = 256

    def __init__(self, request):
        self.request = request
        self.buffer = None
        self.current_file = None
        try:
            mimetype, boundary = request.content_type.rsplit('; boundary=', 1)
        except ValueError:
            return  # not a multipart request
        if mimetype.split(';', 1)[0] == \
                'multipart/form-data':  # pragma: no branch
            self.boundary = b'--' + boundary.encode()
            self.extra_size = len(boundary) + 4
            self.buffer = b''

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.buffer is None:
            raise StopAsyncIteration
        if self.current_file is not None:
            # invalidate the stream of the file previously returned
            self.current_file._read = None
            self.current_file = None

        # make sure we have consumed the previous entry
        while await self._read_buffer(self.buffer_size) != b'':
            pass

        # make sure we are at a boundary
        s = self.buffer.split(self.boundary, 1)
        if len(s) != 2 or s[0] != b'':
            abort(400)  # pragma: no cover
        self.buffer = s[1]
        if self.buffer[:2] == b'--':
            # we have reached the end
            raise StopAsyncIteration
        elif self.buffer[:2] != b'\r\n':
            abort(400)  # pragma: no cover
        self.buffer = self.buffer[2:]

        # parse the headers of this part
        name = ''
        filename = None
        content_type = None
        while True:
            await self._fill_buffer()
            lines = self.buffer.split(b'\r\n', 1)
            if len(lines) != 2:
                abort(400)  # pragma: no cover
            line, self.buffer = lines
            if line == b'':
                # we reached the end of the headers
                break
            header, value = line.decode().split(':', 1)
            header = header.lower()
            value = value.strip()
            if header == 'content-disposition':
                parts = value.split(';')
                if len(parts) < 2 or parts[0] != 'form-data':
                    abort(400)  # pragma: no cover
                for part in parts[1:]:
                    part = part.strip()
                    if part.startswith('name="'):
                        name = part[6:-1]
                    elif part.startswith('filename="'):  # pragma: no branch
                        filename = part[10:-1]
            elif header == 'content-type':  # pragma: no branch
                content_type = value

        if filename is None:
            # this is a regular form field, so we read the value
            value = b''
            while True:
                v = await self._read_buffer(self.buffer_size)
                value += v
                if len(v) < self.buffer_size:  # pragma: no branch
                    break
            return name, value.decode()
        self.current_file = FileUpload(filename, content_type,
                                       self._read_buffer)
        return name, self.current_file

    async def _fill_buffer(self):
        self.buffer += await self.request.stream.read(
            self.buffer_size + self.extra_size - len(self.buffer))

    async def _read_buffer(self, n=None):
        data = b''
        while n is None or len(data) < n:
            await self._fill_buffer()
            s = self.buffer.split(self.boundary, 1)
            data += s[0][:n] if n is not None else s[0]
            self.buffer = s[0][n:] if n is not None else b''
            if len(s) == 2:  # pragma: no branch
                # the end of this part is in the buffer
                if len(self.buffer) < 2:
                    # we have read all the way to the end of this part
                    data = data[:-(2 - len(self.buffer))]  # remove last "\r\n"
                self.buffer += self.boundary + s[1]
                return data
        return data


class FileUpload:
    """Class that represents an uploaded file.

    :param filename: the name of the uploaded file.
    :param content_type: the content type of the uploaded file.
    :param read: a coroutine that reads from the uploaded file's stream.

    An uploaded file can be read from the stream using the :meth:`read()`
    method, or saved to a file using the :meth:`save()` method.

    Instances of this class do not normally need to be created directly.
    """
    def __init__(self, filename, content_type, read):
        self.filename = filename
        self.content_type = content_type
        self._read = read

    async def read(self, n=None):
        """Read up to ``n`` bytes from the uploaded file's stream."""
        return await self._read(n)

    async def save(self, path):
        """Save the uploaded file to the given path.

        The file is saved in chunks of size :attr:`FormDataIter.buffer_size`.
        """
        with open(path, 'wb') as f:
            while True:
                data = await self.read(FormDataIter.buffer_size)
                if not data:
                    break
                f.write(data)


def with_form_data(f):
    """Decorator that parses a ``multipart/form-data`` body and updates the
    request object with the parsed form fields and files.

    Example usage::

        from microdot.multipart import with_form_data

        @app.post('/upload')
        @with_form_data
        async def upload(request):
            print('form fields:', request.form)
            print('file:', request.files)

    Note: this decorator assumes that the uploaded form contains a single file
    field, and that this field is the last field in the form. To work with
    forms that have other configurations the :class:`FormDataIter` class should
    be used directly.
    """
    @wraps(f)
    async def wrapper(request, *args, **kwargs):
        form = {}
        files = {}
        async for name, value in FormDataIter(request):
            if isinstance(value, FileUpload):
                files[name] = value

                # We stop when we reach a file upload, to give the application
                # the chance to process the file data as it sees fit.
                # To handle forms with more than one file field the
                # FormDataIter can be used directly.
                break
            else:
                form[name] = value
        if form or files:
            request._form = form
            request._files = files
        ret = f(request, *args, **kwargs)
        if iscoroutine(ret):
            ret = await ret
        return ret
    return wrapper

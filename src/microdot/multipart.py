from microdot import AsyncBytesIO, abort
from microdot.helpers import wraps


class FormDataIter:
    """Asynchronous iterator that parses a ``multipart/form-data`` body and
    returns form fields and files as they are parsed. Example::

        async for name, value in FormDataIter(request):

    """
    buffer_size = 256

    def __init__(self, request):
        self.request = request
        self.buffer = None
        mimetype, boundary = request.content_type.rsplit('; boundary=', 1)
        if mimetype.split(';', 1)[0] == 'multipart/form-data':
            self.boundary = b'--' + boundary.encode()
            self.extra_size = len(boundary) + 4
            self.buffer = b''

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.buffer is None:
            raise StopAsyncIteration

        # make sure we have consumed the previous entry
        while await self._read_buffer(128) != b'':
            pass

        # make sure we are at a boundary
        s = self.buffer.split(self.boundary, 1)
        if len(s) != 2 or s[0] != b'':
            abort(400)
        self.buffer = s[1]
        if self.buffer[:2] == b'--':
            # we have reached the end
            raise StopAsyncIteration
        elif self.buffer[:2] != b'\r\n':
            abort(400)
        self.buffer = self.buffer[2:]

        # parse the headers of this part
        name = ''
        filename = None
        content_type = None
        while True:
            await self._fill_buffer()
            lines = self.buffer.split(b'\r\n', 1)
            if len(lines) != 2:
                abort(400)
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
                    abort(400)
                for part in parts[1:]:
                    part = part.strip()
                    if part.startswith('name="'):
                        name = part[6:-1]
                    elif part.startswith('filename="'):
                        filename = part[10:-1]
            elif header == 'content-type':
                content_type = value

        if filename is None:
            # this is a regular form field, so we read the value
            value = b''
            while True:
                v = await self._read_buffer(self.buffer_size)
                value += v
                if len(v) < self.buffer_size:
                    break
            return name, value.decode()
        return name, FileUpload(filename, content_type, self._read_buffer)

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
            if len(s) == 2:
                # the end of this part is in the buffer
                if len(self.buffer) == 0:
                    # we have read all the way to the end of this part
                    data = data[:-2]  # remove trailing "\r\n"
                self.buffer += self.boundary + s[1]
                return data
        return data


class FileUpload:
    def __init__(self, filename, content_type, read):
        self.filename = filename
        self.content_type = content_type
        self._read = read

    async def read(self, n=None):
        return await self._read(n)

    async def save(self, path):
        with open(path, 'wb') as f:
            while True:
                data = await self.read(FormDataIter.buffer_size)
                if not data:
                    break
                f.write(data)

    async def copy(self):
        self._read = AsyncBytesIO(await self.read()).read


def with_form_data(f):
    @wraps(f)
    async def wrapper(request, *args, **kwargs):
        form = {}
        files = {}
        async for name, value in FormDataIter(request):
            if isinstance(value, FileUpload):
                await value.copy()
                files[name] = value
            else:
                form[name] = value
        if form or files:
            request._form = form
            request._files = files
        return await f(request, *args, **kwargs)
    return wrapper

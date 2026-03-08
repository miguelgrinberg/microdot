from typing import Any, Awaitable, BinaryIO, Callable, Iterable, Tuple
from asyncio import StreamReader, StreamWriter, Server
from datetime import datetime
from io import BytesIO
from re import Pattern
from ssl import SSLContext
from microdot.multipart import FileUpload

async def invoke_handler(handler: Callable[..., Any | Awaitable[Any]], *args: Any, **kwargs: Any):
    ...

MUTED_SOCKET_ERRORS: list[int]
def urldecode(s: bytes | str) -> str:
    ...

def urlencode(s: str) -> str:
    ...

class NoCaseDict(dict):
    keymap: dict[str, str]
    def __init__(self, initial_dict: dict[str, Any] | None = ...) -> None:
        ...
    
    def __setitem__(self, key: str, value: Any) -> None:
        ...
    
    def __getitem__(self, key: str) -> Any:
        ...
    
    def __delitem__(self, key: str) -> None:
        ...
    
    def __contains__(self, key: str) -> bool:  # type: ignore[override]
        ...
    
    def get(self, key: str, default: Any = ...) -> Any:
        ...
    
    def update(self, other_dict: dict[str, Any]) -> None:  # type: ignore[override]
        ...
    


def mro(cls):
    ...

class MultiDict(dict):
    def __init__(self, initial_dict: dict[str, Any] | None = ...) -> None:
        ...
    
    def __setitem__(self, key: str, value: Any) -> None:
        ...
    
    def __getitem__(self, key: str) -> Any:
        ...
    
    def get(self, key: str, default: Any | None = ..., type: type | None = ...):
        ...
    
    def getlist(self, key: str, type: type | None = ...) -> list[Any]:
        ...
    


class AsyncBytesIO:
    stream: BytesIO
    def __init__(self, data: bytes) -> None:
        ...
    
    async def read(self, n: int = ...) -> bytes:
        ...
    
    async def readline(self) -> bytes:
        ...
    
    async def readexactly(self, n: int) -> bytes:
        ...
    
    async def readuntil(self, separator: bytes = ...) -> bytes:
        ...
    
    async def awrite(self, data: bytes) -> int:
        ...
    
    async def aclose(self) -> None:
        ...
    


class Request:
    class G:
        def __getattr__(self, key: str):
            ...

        def __setattr__(self, key: str, value: Any):
            ...
    
    max_content_length: int
    max_body_length: int
    max_readline: int
    app: "Microdot"
    client_addr: Tuple[str, int]
    method: str
    scheme: str
    url: str
    url_prefix: str
    subapp: "Microdot"
    route: Callable[..., Any | Awaitable[Any]]
    path: str
    query_string: str | None
    args: dict[str, str]
    headers: dict[str, str]
    cookies: dict[str, str]
    content_length: int
    content_type: str | None
    g: G
    http_version: str
    body_used: bool
    sock: Tuple[StreamReader, StreamWriter]
    after_request_handlers: list[Callable[[Request, "Response"], "Response" | Awaitable["Response"] | None | Awaitable[None]]]
    def __init__(self, app, client_addr: Tuple[str, int], method: str, url: str, http_version: str, headers: dict[str, str], body: bytes | None = ..., stream: StreamReader | None = ..., sock: Tuple[StreamReader, StreamWriter] = ..., url_prefix: str = ..., subapp: "Microdot" | None = ..., scheme: str | None = ..., route: Callable[..., Any | Awaitable[Any]] | None = ...) -> None:
        ...
    
    @staticmethod
    async def create(app, client_reader: StreamReader, client_writer: StreamWriter, client_addr: Tuple[str, int], scheme: str | None = ...) -> Request:
        ...
    
    @property
    def body(self) -> bytes | None:
        ...
    
    @property
    def stream(self) -> StreamReader | None:
        ...
    
    @property
    def json(self) -> dict[str, Any] | list[Any] | None:
        ...
    
    @property
    def form(self) -> dict[str, str] | None:
        ...
    
    @property
    def files(self) -> dict[str, FileUpload]:
        ...
    
    def after_request(self, f: Callable[[Request, "Response"], "Response" | Awaitable["Response"] | None | Awaitable[None]]):
        ...
    


class Response:
    types_map: dict[str, str]
    send_file_buffer_size: int
    default_content_type: str
    default_send_file_max_age: int | None
    already_handled: "Response"
    status_code: int
    headers: NoCaseDict
    reason: str
    body: bytes
    is_head: bool
    i: int
    def __init__(self, body: str | bytes = ..., status_code: int = ..., headers: dict[str, str] = ..., reason: str = ...) -> None:
        ...
    
    def set_cookie(self, cookie: str, value: str, path: str | None = ..., domain: str | None = ..., expires: str | datetime = ..., max_age: int | None = ..., secure: bool = ..., http_only: bool = ..., partitioned: bool = ...) -> None:
        ...
    
    def delete_cookie(self, cookie: str, **kwargs: Any) -> None:
        ...
    
    def complete(self) -> None:
        ...
    
    async def write(self, stream: StreamWriter) -> None:
        ...
    
    def body_iter(self) -> Iterable[bytes]:
        ...
    
    @classmethod
    def redirect(cls, location: str, status_code: int = ...) -> Response:
        ...
    
    @classmethod
    def send_file(cls, filename: str, status_code: int = ..., content_type: str | None = ..., stream: BinaryIO | None = ..., max_age: int | None = ..., compressed: bool = ..., file_extension: str = ...) -> Response:
        ...
    


class URLPattern:
    segment_patterns: dict[str, str]
    segment_parsers: dict[str, Callable[[str], Any]]
    url_pattern: str
    segments: dict[str, Any]
    regex: Pattern | None
    @classmethod
    def register_type(cls, type_name: str, pattern: str = ..., parser: Callable[[str], Any] | None=...) -> None:
        ...
    
    def __init__(self, url_pattern: str) -> None:
        ...
    
    def compile(self) -> Pattern:
        ...
    
    def match(self, path) -> dict[str, Any]:
        ...
    


class HTTPException(Exception):
    status_code: int
    reason: str
    def __init__(self, status_code: int, reason: str | None = ...) -> None:
        ...
    


class Microdot:
    url_map: list[Tuple[list[str], URLPattern, Callable[..., Any], str, Microdot | None]]
    before_request_handlers: list[Callable[[Request], Any | None]]
    after_request_handlers: list[Callable[[Request, Response], Response | None]]
    after_error_request_handlers: list[Callable[[Request, Response], Response | None]]
    error_handlers: dict[int | Exception, Callable[[Request], Any] | Callable[[Request, Exception], Any]]
    options_handler: Callable[[Request], dict[str, str]]
    ssl: bool
    debug: bool
    server: Server
    def __init__(self) -> None:
        ...
    
    def route(self, url_pattern: str, methods: list[str] = ...):
        ...
    
    def get(self, url_pattern: str):
        ...
    
    def post(self, url_pattern: str):
        ...
    
    def put(self, url_pattern: str):
        ...
    
    def patch(self, url_pattern: str):
        ...
    
    def delete(self, url_pattern: str):
        ...
    
    def before_request(self, f: Callable[[Request], Any | None]) -> Callable[[Request], Any | None]:
        ...
    
    def after_request(self, f: Callable[[Request, Response], Any | None]) -> Callable[[Request, Response], Any | None]:
        ...
    
    def after_error_request(self, f: Callable[[Request, Response], Any | None]) -> Callable[[Request, Response], Any | None]:
        ...
    
    def errorhandler(self, status_code_or_exception_class: int | type) -> Callable[[Callable[[Request], Any] | Callable[[Request, Exception], Any]], Any]:
        ...
    
    def mount(self, subapp: Microdot, url_prefix: str = ..., local: bool = ...) -> None:
        ...
    
    @staticmethod
    def abort(status_code: int, reason: str | None = ...) -> None:
        ...
    
    async def start_server(self, host: str = ..., port: int = ..., debug: bool = ..., ssl=...) -> None:
        ...
    
    def run(self, host: str = ..., port: int = ..., debug: bool = ..., ssl: SSLContext | None = ...) -> None:
        ...
    
    def shutdown(self) -> None:
        ...
    
    def find_route(self, req: Request) -> Tuple[int | Callable[..., Any], str, Microdot | None]:
        ...
    
    def default_options_handler(self, req: Request) -> dict[str, str]:
        ...
    
    async def handle_request(self, reader: StreamReader, writer: StreamWriter) -> None:
        ...
    
    def get_request_handlers(self, req: Request, attr: str, local_first: bool = ...) -> list[Callable[..., Any]]:
        ...
    
    async def error_response(self, req: Request, status_code: int, reason: str = ...):
        ...
    
    async def dispatch_request(self, req: Request):
        ...
    

def abort(status_code: int, reason: str | None = ...) -> None:
    ...

def redirect(location: str, status_code: int = ...) -> Response:
    ...

def send_file(filename: str, status_code: int = ..., content_type: str | None = ..., stream: BinaryIO | None = ..., max_age: int | None = ..., compressed: bool = ..., file_extension: str = ...) -> Response:
    ...

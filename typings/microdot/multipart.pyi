from typing import Any, Awaitable, Callable, Iterator, Tuple
from microdot import Request

class FormDataIter:
    buffer_size: int
    request: Request
    buffer: bytes | None
    boundary: bytes
    extra_size: int
    def __init__(self, request: Request) -> None:
        ...
    
    def __aiter__(self) -> Iterator[Tuple[str, Any]]:
        ...
    
    async def __anext__(self) -> Tuple[str, str | "FileUpload"]:
        ...
    


class FileUpload:
    max_memory_size: int
    filename: str
    content_type: str
    def __init__(self, filename: str, content_type: str, read: Callable[[int], Awaitable[bytes]]) -> None:
        ...
    
    async def read(self, n: int = ...) -> bytes:
        ...
    
    async def save(self, path_or_file: str) -> None:
        ...
    
    async def copy(self, max_memory_size: int | None = ...):
        ...
    
    async def close(self) -> None:
        ...
    


def with_form_data(f: Callable[..., Any]) -> Callable[..., Any]:
    ...

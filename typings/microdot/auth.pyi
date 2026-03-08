from typing import Any, Awaitable, Callable
from microdot import Request

class BaseAuth:
    auth_callback: Callable[..., Any | Awaitable[Any]]
    error_callback: Callable[[Request], Any | Awaitable[Any]]
    def __init__(self) -> None:
        ...
    
    def __call__(self, f: Callable[..., Any]):
        ...
    
    def optional(self, f: Callable[..., Any]):
        ...
    


class BasicAuth(BaseAuth):
    realm: str
    charset: str
    scheme: str
    error_status: int
    error_callback: Callable[[Request], Any | Awaitable[Any]]
    def __init__(self, realm: str = ..., charset: str = ..., scheme: str = ..., error_status: int = ...) -> None:
        ...
    
    async def authentication_error(self, request):
        ...
    
    auth_callback: Callable[[Request, str, str], Any | Awaitable[Any]]
    def authenticate(self, f: Callable[[Request, str, str], Any | Awaitable[Any]]) -> None:
        ...
    


class TokenAuth(BaseAuth):
    header: str
    scheme: str
    error_status: int
    error_callback: Callable[[Request], Any | Awaitable[Any]]
    def __init__(self, header: str = ..., scheme: str = ..., error_status: int = ...) -> None:
        ...
    
    auth_callback: Callable[[Request, str], Any | Awaitable[Any]]
    def authenticate(self, f: Callable[..., Any | Awaitable[Any]]) -> None:
        ...
    
    def errorhandler(self, f: Callable[[Request], Any | Awaitable[Any]]) -> None:
        ...
    
    async def authentication_error(self, request) -> None:
        ...

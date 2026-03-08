from typing import Any, Awaitable, Callable
from microdot import Microdot
from microdot.cors import CORS

class CSRF:
    SAFE_METHODS: list[str]
    cors: CORS | None
    protect_all: bool
    allow_subdomains: bool
    exempt_routes: list[Callable[..., Any | Awaitable[Any]]]
    protected_routes: list[Callable[..., Any | Awaitable[Any]]]
    def __init__(self, app: Microdot | None = ..., cors: CORS | None = ..., protect_all: bool = ..., allow_subdomains: bool = ...) -> None:
        ...
    
    def initialize(self, app: Microdot, cors: CORS | None = ...) -> None:
        ...
    
    def exempt(self, f: Callable[..., Any | Awaitable[Any]]) -> Callable[..., Any | Awaitable[Any]]:
        ...
    
    def protect(self, f: Callable[..., Any | Awaitable[Any]]) -> Callable[..., Any | Awaitable[Any]]:
        ...

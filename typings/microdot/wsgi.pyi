from typing import Any, Callable, Tuple
import asyncio
from microdot import *  # type: ignore
from microdot.microdot import Microdot as BaseMicrodot

class Microdot(BaseMicrodot):  # type: ignore[no-redef]
    loop: asyncio.EventLoop
    embedded_server: bool
    def __init__(self) -> None:
        ...
    
    def wsgi_app(self, environ: dict[str, Any], start_response: Callable[[int, list[Tuple[str, str]]], Callable[[str | bytes], None]]):
        ...
    
    def __call__(self, environ: dict[str, Any], start_response: Callable[[int, list[Tuple[str, str]]], Callable[[str | bytes], None]]):
        ...
    
    def shutdown(self) -> None:
        ...
    
    def run(self, host: str = ..., port: int = ..., debug: bool = ..., **options: Any) -> None:  # type: ignore[override]
        ...

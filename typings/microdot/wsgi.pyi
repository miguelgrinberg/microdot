from typing import Any, Callable, Tuple
from asyncio import EventLoop
from microdot import *  # type: ignore
from microdot.microdot import Microdot as BaseMicrodot

class Microdot(BaseMicrodot):  # type: ignore[no-redef]
    loop: EventLoop
    embedded_server: bool
    def __init__(self) -> None:
        ...
    
    def wsgi_app(self, environ: dict[str, Any], start_response: Callable[[int, list[Tuple[str, str]]]]):
        ...
    
    def __call__(self, environ: dict[str, Any], start_response: Callable[[int, list[Tuple[str, str]]]]):
        ...
    
    def shutdown(self) -> None:
        ...
    
    def run(self, host: str = ..., port: int = ..., debug: bool = ..., **options: Any) -> None:  # type: ignore[override]
        ...

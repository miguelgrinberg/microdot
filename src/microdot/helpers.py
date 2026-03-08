try:
    from functools import wraps
except ImportError:  # pragma: no cover
    # MicroPython does not currently implement functools.wraps
    def wraps(wrapped):  # type: ignore[misc]
        def _(wrapper):
            return wrapper
        return _

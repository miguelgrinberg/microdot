# SPDX-FileCopyrightText: 2019 Damien P. George
#
# SPDX-License-Identifier: MIT
#
# MicroPython uasyncio module
# MIT license; Copyright (c) 2019 Damien P. George
#
# This code comes from MicroPython, and has not been run through black or pylint there.
# Altering these files significantly would make merging difficult, so we will not use
# pylint or black.
# pylint: skip-file
# fmt: off

from .core import *

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/Adafruit/Adafruit_CircuitPython_asyncio.git"

_attrs = {
    "wait_for": "funcs",
    "wait_for_ms": "funcs",
    "gather": "funcs",
    "Event": "event",
    "ThreadSafeFlag": "event",
    "Lock": "lock",
    "open_connection": "stream",
    "start_server": "stream",
    "StreamReader": "stream",
    "StreamWriter": "stream",
}

# Lazy loader, effectively does:
#   global attr
#   from .mod import attr
def __getattr__(attr):
    mod = _attrs.get(attr, None)
    if mod is None:
        raise AttributeError(attr)
    value = getattr(__import__(mod, None, None, True, 1), attr)
    globals()[attr] = value
    return value

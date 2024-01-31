# SPDX-FileCopyrightText: 2019-2020 Damien P. George
#
# SPDX-License-Identifier: MIT
#
# MicroPython uasyncio module
# MIT license; Copyright (c) 2019-2020 Damien P. George
"""
Fallback traceback module if the system traceback is missing.
"""

try:
    from typing import List
except ImportError:
    pass

import sys


def _print_traceback(traceback, limit=None, file=sys.stderr) -> List[str]:
    if limit is None:
        if hasattr(sys, "tracebacklimit"):
            limit = sys.tracebacklimit

    n = 0
    while traceback is not None:
        frame = traceback.tb_frame
        line_number = traceback.tb_lineno
        frame_code = frame.f_code
        filename = frame_code.co_filename
        name = frame_code.co_name
        print('  File "%s", line %d, in %s' % (filename, line_number, name), file=file)
        traceback = traceback.tb_next
        n = n + 1
        if limit is not None and n >= limit:
            break


def print_exception(exception, value=None, traceback=None, limit=None, file=sys.stderr):
    """
    Print exception information and stack trace to file.
    """
    if traceback:
        print("Traceback (most recent call last):", file=file)
        _print_traceback(traceback, limit=limit, file=file)

    if isinstance(exception, BaseException):
        exception_type = type(exception).__name__
    elif hasattr(exception, "__name__"):
        exception_type = exception.__name__
    else:
        exception_type = type(value).__name__

    valuestr = str(value)
    if value is None or not valuestr:
        print(exception_type, file=file)
    else:
        print("%s: %s" % (str(exception_type), valuestr), file=file)

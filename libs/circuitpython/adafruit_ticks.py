# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_ticks`
================================================================================

Work with intervals and deadlines in milliseconds


* Author(s): Jeff Epler

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
from micropython import const

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ticks.git"

_TICKS_PERIOD = const(1 << 29)
_TICKS_MAX = const(_TICKS_PERIOD - 1)
_TICKS_HALFPERIOD = const(_TICKS_PERIOD // 2)

# Get the correct implementation of ticks_ms.  There are three possibilities:
#
#  - supervisor.ticks_ms is present.  This will be the case starting in CP7.0
#
#  - time.ticks_ms is present. This is the case for MicroPython & for the "unix
#    port" of CircuitPython, used for some automated testing.
#
#  - time.monotonic_ns is present, and works.  This is the case on most
#    Express boards in CP6.x, and most host computer versions of Python.
#
#  - Otherwise, time.monotonic is assumed to be present.  This is the case
#    on most non-express boards in CP6.x, and some old host computer versions
#    of Python.
#
#    Note that on microcontrollers, this time source becomes increasingly
#    inaccurate when the board has not been reset in a long time, losing the
#    ability to measure 1ms intervals after about 1 hour, and losing the
#    ability to meausre 128ms intervals after 6 days.  The only solution is to
#    either upgrade to a version with supervisor.ticks_ms, or to switch to a
#    board with time.monotonic_ns.

try:
    from supervisor import ticks_ms  # pylint: disable=unused-import
except (ImportError, NameError):
    import time

    if _ticks_ms := getattr(time, "ticks_ms", None):

        def ticks_ms() -> int:
            """Return the time in milliseconds since an unspecified moment,
            wrapping after 2**29ms.

            The wrap value was chosen so that it is always possible to add or
            subtract two `ticks_ms` values without overflow on a board without
            long ints (or without allocating any long integer objects, on
            boards with long ints).

            This ticks value comes from a low-accuracy clock internal to the
            microcontroller, just like `time.monotonic`.  Due to its low
            accuracy and the fact that it "wraps around" every few days, it is
            intended for working with short term events like advancing an LED
            animation, not for long term events like counting down the time
            until a holiday."""
            return _ticks_ms() & _TICKS_MAX  # pylint: disable=not-callable

    else:
        try:
            from time import monotonic_ns as _monotonic_ns

            _monotonic_ns()  # Check that monotonic_ns is usable

            def ticks_ms() -> int:
                """Return the time in milliseconds since an unspecified moment,
                wrapping after 2**29ms.

                The wrap value was chosen so that it is always possible to add or
                subtract two `ticks_ms` values without overflow on a board without
                long ints (or without allocating any long integer objects, on
                boards with long ints).

                This ticks value comes from a low-accuracy clock internal to the
                microcontroller, just like `time.monotonic`.  Due to its low
                accuracy and the fact that it "wraps around" every few days, it is
                intended for working with short term events like advancing an LED
                animation, not for long term events like counting down the time
                until a holiday."""
                return (_monotonic_ns() // 1_000_000) & _TICKS_MAX

        except (ImportError, NameError, NotImplementedError):
            from time import monotonic as _monotonic

            def ticks_ms() -> int:
                """Return the time in milliseconds since an unspecified moment,
                wrapping after 2**29ms.

                The wrap value was chosen so that it is always possible to add or
                subtract two `ticks_ms` values without overflow on a board without
                long ints (or without allocating any long integer objects, on
                boards with long ints).

                This ticks value comes from a low-accuracy clock internal to the
                microcontroller, just like `time.monotonic`.  Due to its low
                accuracy and the fact that it "wraps around" every few days, it is
                intended for working with short term events like advancing an LED
                animation, not for long term events like counting down the time
                until a holiday."""
                return int(_monotonic() * 1000) & _TICKS_MAX


def ticks_add(ticks: int, delta: int) -> int:
    "Add a delta to a base number of ticks, performing wraparound at 2**29ms."
    return (ticks + delta) % _TICKS_PERIOD


def ticks_diff(ticks1: int, ticks2: int) -> int:
    """Compute the signed difference between two ticks values,
    assuming that they are within 2**28 ticks"""
    diff = (ticks1 - ticks2) & _TICKS_MAX
    diff = ((diff + _TICKS_HALFPERIOD) & _TICKS_MAX) - _TICKS_HALFPERIOD
    return diff


def ticks_less(ticks1: int, ticks2: int) -> bool:
    """Return true if ticks1 is before ticks2 and false otherwise,
    assuming that they are within 2**28 ticks"""
    return ticks_diff(ticks1, ticks2) < 0

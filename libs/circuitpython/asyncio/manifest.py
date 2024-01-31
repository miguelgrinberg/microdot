# SPDX-FileCopyrightText: 2019 Damien P. George
#
# SPDX-License-Identifier: MIT
#
#
# This code comes from MicroPython, and has not been run through black or pylint there.
# Altering these files significantly would make merging difficult, so we will not use
# pylint or black.
# pylint: skip-file
# fmt: off

# This list of frozen files doesn't include task.py because that's provided by the C module.
freeze(
    "..",
    (
        "uasyncio/__init__.py",
        "uasyncio/core.py",
        "uasyncio/event.py",
        "uasyncio/funcs.py",
        "uasyncio/lock.py",
        "uasyncio/stream.py",
    ),
    opt=3,
)

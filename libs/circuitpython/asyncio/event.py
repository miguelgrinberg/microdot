# SPDX-FileCopyrightText: 2019-2020 Damien P. George
#
# SPDX-License-Identifier: MIT
#
# MicroPython uasyncio module
# MIT license; Copyright (c) 2019-2020 Damien P. George
#
# This code comes from MicroPython, and has not been run through black or pylint there.
# Altering these files significantly would make merging difficult, so we will not use
# pylint or black.
# pylint: skip-file
# fmt: off
"""
Events
======
"""

from . import core

# Event class for primitive events that can be waited on, set, and cleared
class Event:
    """Create a new event which can be used to synchronize tasks. Events
    start in the cleared state.
    """

    def __init__(self):
        self.state = False  # False=unset; True=set
        self.waiting = core.TaskQueue()  # Queue of Tasks waiting on completion of this event

    def is_set(self):
        """Returns ``True`` if the event is set, ``False`` otherwise."""

        return self.state

    def set(self):
        """Set the event. Any tasks waiting on the event will be scheduled to run.
        """

        # Event becomes set, schedule any tasks waiting on it
        # Note: This must not be called from anything except the thread running
        # the asyncio loop (i.e. neither hard or soft IRQ, or a different thread).
        while self.waiting.peek():
            core._task_queue.push_head(self.waiting.pop_head())
        self.state = True

    def clear(self):
        """Clear the event."""

        self.state = False

    async def wait(self):
        """Wait for the event to be set. If the event is already set then it returns
        immediately.

        This is a coroutine.
        """

        if not self.state:
            # Event not set, put the calling task on the event's waiting queue
            self.waiting.push_head(core.cur_task)
            # Set calling task's data to the event's queue so it can be removed if needed
            core.cur_task.data = self.waiting
            await core._never()
        return True


# MicroPython-extension: This can be set from outside the asyncio event loop,
# such as other threads, IRQs or scheduler context. Implementation is a stream
# that asyncio will poll until a flag is set.
# Note: Unlike Event, this is self-clearing.
try:
    import uio

    class ThreadSafeFlag(uio.IOBase):
        def __init__(self):
            self._flag = 0

        def ioctl(self, req, flags):
            if req == 3:  # MP_STREAM_POLL
                return self._flag * flags
            return None

        def set(self):
            self._flag = 1

        async def wait(self):
            if not self._flag:
                yield core._io_queue.queue_read(self)
            self._flag = 0

except ImportError:
    pass

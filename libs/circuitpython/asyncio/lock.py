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
Locks
=====
"""

from . import core

# Lock class for primitive mutex capability
class Lock:
    """Create a new lock which can be used to coordinate tasks. Locks start in
    the unlocked state.

    In addition to the methods below, locks can be used in an ``async with``
    statement.
    """

    def __init__(self):
        # The state can take the following values:
        # - 0: unlocked
        # - 1: locked
        # - <Task>: unlocked but this task has been scheduled to acquire the lock next
        self.state = 0
        # Queue of Tasks waiting to acquire this Lock
        self.waiting = core.TaskQueue()

    def locked(self):
        """Returns ``True`` if the lock is locked, otherwise ``False``."""

        return self.state == 1

    def release(self):
        """Release the lock. If any tasks are waiting on the lock then the next
        one in the queue is scheduled to run and the lock remains locked. Otherwise,
        no tasks are waiting and the lock becomes unlocked.
        """

        if self.state != 1:
            raise RuntimeError("Lock not acquired")
        if self.waiting.peek():
            # Task(s) waiting on lock, schedule next Task
            self.state = self.waiting.pop_head()
            core._task_queue.push_head(self.state)
        else:
            # No Task waiting so unlock
            self.state = 0

    async def acquire(self):
        """Wait for the lock to be in the unlocked state and then lock it in an
        atomic way. Only one task can acquire the lock at any one time.

        This is a coroutine.
        """

        if self.state != 0:
            # Lock unavailable, put the calling Task on the waiting queue
            self.waiting.push_head(core.cur_task)
            # Set calling task's data to the lock's queue so it can be removed if needed
            core.cur_task.data = self.waiting
            try:
                await core._never()
            except core.CancelledError as er:
                if self.state == core.cur_task:
                    # Cancelled while pending on resume, schedule next waiting Task
                    self.state = 1
                    self.release()
                raise er
        # Lock available, set it as locked
        self.state = 1
        return True

    async def __aenter__(self):
        return await self.acquire()

    async def __aexit__(self, exc_type, exc, tb):
        return self.release()

"""
DO NOT UPLOAD THIS FILE TO YOUR MICROPYTHON DEVICE

This module emulates parts of MicroPython's `machine` module, to enable to run
MicroPython applications on UNIX, Mac or Windows systems without dedicated
hardware.
"""


class Pin:
    def __init__(self, pin):
        self.pin = pin

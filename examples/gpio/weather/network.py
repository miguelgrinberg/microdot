"""
DO NOT UPLOAD THIS FILE TO YOUR MICROPYTHON DEVICE

This module emulates parts of MicroPython's `network` module, in particular
those related to establishing a Wi-Fi connection. This enables to run
MicroPython applications on UNIX, Mac or Windows systems without dedicated
hardware.

Note that no connections are attempted. The assumption is that the system is
already connected. The "127.0.0.1" address is always returned.
"""

AP_IF = 1
STA_IF = 2


class WLAN:
    def __init__(self, network):
        self.network = network

    def isconnected(self):
        return True

    def ifconfig(self):
        return ('127.0.0.1', 'n/a', 'n/a', 'n/a')

    def connect(self):
        pass

    def active(self, active=None):
        pass

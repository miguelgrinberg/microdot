"""
DO NOT UPLOAD THIS FILE TO YOUR MICROPYTHON DEVICE

This module emulates MicroPython's DHT22 driver. It can be used when running
on a system without the DHT22 hardware.

The temperature and humidity values that are returned are random values.
"""

from random import random


class DHT22:
    def __init__(self, pin):
        self.pin = pin

    def measure(self):
        pass

    def temperature(self):
        """Return a random temperature between 10 and 30 degrees Celsius."""
        return random() * 20 + 10

    def humidity(self):
        """Return a random humidity between 30 and 70 percent."""
        return random() * 40 + 30

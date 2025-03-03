import unittest
from microdot.microdot import urlencode, urldecode


class TestURLEncode(unittest.TestCase):
    def test_urlencode(self):
        self.assertEqual(urlencode('?foo=bar&x'), '%3Ffoo%3Dbar%26x')

    def test_urldecode(self):
        self.assertEqual(urldecode('%3Ffoo%3Dbar%26x'), '?foo=bar&x')
        self.assertEqual(urldecode(b'%3Ffoo%3Dbar%26x'), '?foo=bar&x')

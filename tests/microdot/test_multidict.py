import unittest
from microdot import MultiDict


class TestMultiDict(unittest.TestCase):
    def test_multidict(self):
        d = MultiDict()

        assert dict(d) == {}
        assert d.get('zero') is None
        assert d.get('zero', default=0) == 0
        assert d.getlist('zero') == []
        assert d.getlist('zero', type=int) == []

        d['one'] = 1
        assert d['one'] == 1
        assert d.get('one') == 1
        assert d.get('one', default=2) == 1
        assert d.get('one', type=int) == 1
        assert d.get('one', type=str) == '1'

        d['two'] = 1
        d['two'] = 2
        assert d['two'] == 1
        assert d.get('two') == 1
        assert d.get('two', default=2) == 1
        assert d.get('two', type=int) == 1
        assert d.get('two', type=str) == '1'
        assert d.getlist('two') == [1, 2]
        assert d.getlist('two', type=int) == [1, 2]
        assert d.getlist('two', type=str) == ['1', '2']

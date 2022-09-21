import unittest
from microdot import MultiDict, NoCaseDict


class TestMultiDict(unittest.TestCase):
    def test_multidict(self):
        d = MultiDict()

        self.assertEqual(dict(d), {})
        self.assertIsNone(d.get('zero'))
        self.assertEqual(d.get('zero', default=0), 0)
        self.assertEqual(d.getlist('zero'), [])
        self.assertEqual(d.getlist('zero', type=int), [])

        d['one'] = 1
        self.assertEqual(d['one'], 1)
        self.assertEqual(d.get('one'), 1)
        self.assertEqual(d.get('one', default=2), 1)
        self.assertEqual(d.get('one', type=int), 1)
        self.assertEqual(d.get('one', type=str), '1')

        d['two'] = 1
        d['two'] = 2
        self.assertEqual(d['two'], 1)
        self.assertEqual(d.get('two'), 1)
        self.assertEqual(d.get('two', default=2), 1)
        self.assertEqual(d.get('two', type=int), 1)
        self.assertEqual(d.get('two', type=str), '1')
        self.assertEqual(d.getlist('two'), [1, 2])
        self.assertEqual(d.getlist('two', type=int), [1, 2])
        self.assertEqual(d.getlist('two', type=str), ['1', '2'])

    def test_case_insensitive_dict(self):
        d = NoCaseDict()

        d['One'] = 1
        d['one'] = 2
        d['ONE'] = 3
        d['One'] = 4
        d['two'] = 5
        self.assertEqual(d['one'], 4)
        self.assertEqual(d['One'], 4)
        self.assertEqual(d['ONE'], 4)
        self.assertEqual(d['onE'], 4)
        self.assertIn(('One', 4), list(d.items()))
        self.assertIn(('two', 5), list(d.items()))
        self.assertIn(4, list(d.values()))
        self.assertIn(5, list(d.values()))

        del d['oNE']
        self.assertEqual(list(d.items()), [('two', 5)])
        self.assertEqual(list(d.values()), [5])

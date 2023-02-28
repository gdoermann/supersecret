"""
Test other parts of the supersecret package.
"""

import unittest

from supersecret import get_version
from supersecret.util import AttrDict


class TestOther(unittest.TestCase):
    def test_version(self):
        self.assertEqual(len(get_version().split('.')), 3)

    def test_attrdict(self):
        """
        Test the AttrDict class.
        """
        d = AttrDict()
        d['test'] = 'test'
        self.assertEqual(d.test, 'test')

        d.test = 'test2'
        self.assertEqual(d['test'], 'test2')

        d = AttrDict({'test': 'test'})
        self.assertEqual(d.test, 'test')

        del d.test
        self.assertEqual(dict(d), {})

"""
Test other parts of the supersecret package.
"""

import unittest

from supersecret import get_version


class TestOther(unittest.TestCase):
    def test_version(self):
        self.assertEqual(len(get_version().split('.')), 3)

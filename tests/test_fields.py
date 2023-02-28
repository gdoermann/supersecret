"""
Test fields.py
"""
import datetime
import decimal
import logging
import pathlib
import unittest

import marshmallow.exceptions

from supersecret import fields


class TestFields(unittest.TestCase):
    def test_str(self):
        """
        Test the Str field class.
        """
        field = fields.Str()
        self.assertEqual(field.deserialize('test'), 'test')
        self.assertEqual(field.deserialize(u'test'), 'test')

    def test_int(self):
        """
        Test the Int field class.
        """
        field = fields.Int()
        self.assertEqual(field.deserialize('1'), 1)
        self.assertEqual(field.deserialize(u'1'), 1)

    def test_float(self):
        """
        Test the Float field class.
        """
        field = fields.Float()
        self.assertEqual(field.deserialize('1.1'), 1.1)
        self.assertEqual(field.deserialize(u'1.1'), 1.1)

    def test_decimal(self):
        """
        Test the Decimal field class.
        """
        field = fields.Decimal()
        self.assertEqual(field.deserialize('1.1'), decimal.Decimal('1.1'))
        self.assertEqual(field.deserialize(u'1.1'), decimal.Decimal('1.1'))

    def test_bool(self):
        """
        Test the Bool field class.
        """
        field = fields.Bool()
        self.assertEqual(field.deserialize('True'), True)
        self.assertEqual(field.deserialize(u'True'), True)
        self.assertEqual(field.deserialize('true'), True)
        self.assertEqual(field.deserialize(u'true'), True)
        self.assertEqual(field.deserialize('1'), True)
        self.assertEqual(field.deserialize('False'), False)
        self.assertEqual(field.deserialize(u'False'), False)
        self.assertEqual(field.deserialize('false'), False)
        self.assertEqual(field.deserialize(u'false'), False)
        self.assertEqual(field.deserialize('0'), False)

    def test_choices(self):
        """
        Test the Choices field class.
        """
        field = fields.Choices()
        self.assertEqual(field.deserialize('a:1,b:2'), [('a', '1'), ('b', '2')])
        self.assertEqual(field.deserialize(u'a:1,b:2'), [('a', '1'), ('b', '2')])
        self.assertEqual(field.deserialize([('a', '1'), ('b', '2')]), [('a', '1'), ('b', '2')])

    def test_timedelta(self):
        """
        Test TimeDelta field class.
        """
        field = fields.TimeDelta()
        self.assertEqual(field.deserialize('1:0:0'), datetime.timedelta(hours=1))


    def test_timedeltaseconds(self):
        """
        Test the TimeDeltaSeconds field class.
        """
        field = fields.TimeDeltaSeconds()
        self.assertEqual(field.deserialize('1'), datetime.timedelta(seconds=1))

    def test_path(self):
        """
        Test the Path field class.
        """
        field = fields.Path()
        self.assertEqual(field.deserialize('/tmp'), pathlib.Path('/tmp'))
        self.assertEqual(field.deserialize(u'/tmp'), pathlib.Path('/tmp'))
        self.assertEqual(field.deserialize(pathlib.Path('/tmp')), pathlib.Path('/tmp'))


    def test_loglevel(self):
        """
        Test the LogLevel field class.
        """
        field = fields.LogLevel()
        self.assertEqual(field.deserialize('DEBUG'), logging.DEBUG)
        self.assertEqual(field.deserialize('INFO'), logging.INFO)
        self.assertEqual(field.deserialize('WARNING'), logging.WARNING)
        self.assertEqual(field.deserialize('ERROR'), logging.ERROR)
        self.assertEqual(field.deserialize('CRITICAL'), logging.CRITICAL)

        # Test invalid log levels
        with self.assertRaises(marshmallow.exceptions.ValidationError):
            field.deserialize('INVALID')

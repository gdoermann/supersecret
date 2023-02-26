"""
Tests for the supersecret.manager module.
"""
import datetime
import decimal
import unittest
import json
import uuid
from unittest.mock import patch
import os

from botocore.client import BaseClient

from supersecret.manager import SecretManager
from supersecret.util import AttrDict

SECRETS_MOCK = {
    'TestingSecret': {
        'ARN': 'arn:aws:secretsmanager:us-east-1:123456789:secret:TestingSecret-123456',
        'Name': 'TestingSecret',
        'VersionId': '123456',
        'SecretString': json.dumps({
            'username': 'test_username',
            'password': 'test_password',
            'database__host': 'localhost',
            'database__port': '1234',
            'database__name': 'test_database',
            'database__username': 'test_database_username',
            'database__password': 'test_database_password',
            'database__options__ssl': 'True',
            'test_float': '1.234',
            'test_int': '1234',
            'test_bool': 'True',
            'test_list': 'test1,test2,test3',
            'test_choices': 'test1:test2,test3:test4',
            'test_datetime': '2020-01-01 00:00:00',
            'test_date': '2020-01-01',
            'test_decimal': '1.234',
            'test_time': '00:00:00',
            'test_timedelta': '1:00:00',
            'test_timedelta_seconds': '3600',
            'test_uuid': '12345678-1234-5678-1234-567812345678',
        }),
        'VersionStages': ['AWSCURRENT'],
        'CreatedDate': datetime.datetime.now(),
        'ResponseMetadata': {'RequestId': 'abc123',
                             'HTTPStatusCode': 200,
                             'HTTPHeaders': {'x-amzn-requestid': 'abc123',
                                             'content-type': 'application/x-amz-json-1.1',
                                             'content-length': '2033',
                                             'date': 'Sun, 26 Feb 2023 07:44:38 GMT'},
                             'RetryAttempts': 0}}
}


class MockSecretsClient:
    """
    Mock class for the boto3 client.
    """

    def get_secret_value(self, SecretId):
        """
        Mock method for the get_secret_value method.
        """
        return AttrDict(SECRETS_MOCK[SecretId])


class TestSecretManager(unittest.TestCase):
    """
    Tests for the SecretManager class.
    """

    def test_get_value_env(self):
        """
        Test that the get_value method returns the expected value.
        """
        os.environ['test'] = 'test'
        with patch.object(SecretManager, 'connect') as mock_connect_to_session:
            mock_connect_to_session.return_value = MockSecretsClient()
            secret_manager = SecretManager('TestingSecret')
            self.assertEqual(secret_manager.str('test'), 'test')

    def test_connect_to_session(self):
        """
        Test that the connect_to_session method returns the expected value.
        """
        secret_manager = SecretManager('TestingSecret')
        self.assertIsInstance(secret_manager.connect(), BaseClient)

    def test_get_str(self):
        """
        Test that the get_str method returns the expected value.
        """
        with patch.object(SecretManager, 'connect') as mock_connect_to_session:
            mock_connect_to_session.return_value = MockSecretsClient()
            secret_manager = SecretManager('TestingSecret')
            self.assertEqual(secret_manager.str('username'), 'test_username')

    def test_get_int(self):
        """
        Test that the get_int method returns the expected value.
        """
        with patch.object(SecretManager, 'connect') as mock_connect_to_session:
            mock_connect_to_session.return_value = MockSecretsClient()
            secret_manager = SecretManager('TestingSecret')
            self.assertEqual(secret_manager.int('test_int'), 1234)

    def test_get_float(self):
        """
        Test that the get_float method returns the expected value.
        """
        with patch.object(SecretManager, 'connect') as mock_connect_to_session:
            mock_connect_to_session.return_value = MockSecretsClient()
            secret_manager = SecretManager('TestingSecret')
            self.assertEqual(secret_manager.float('test_float'), 1.234)

    def test_get_bool(self):
        """
        Test that the get_bool method returns the expected value.
        """
        with patch.object(SecretManager, 'connect') as mock_connect_to_session:
            mock_connect_to_session.return_value = MockSecretsClient()
            secret_manager = SecretManager('TestingSecret')
            self.assertTrue(secret_manager.bool('test_bool'))

    def test_get_list(self):
        """
        Test that the get_list method returns the expected value.
        """
        with patch.object(SecretManager, 'connect') as mock_connect_to_session:
            mock_connect_to_session.return_value = MockSecretsClient()
            secret_manager = SecretManager('TestingSecret')
            self.assertEqual(secret_manager.list('test_list'), ['test1', 'test2', 'test3'])

    def test_get_choices(self):
        """
        Test that the get_choices method returns the expected value.
        """
        with patch.object(SecretManager, 'connect') as mock_connect_to_session:
            mock_connect_to_session.return_value = MockSecretsClient()
            secret_manager = SecretManager('TestingSecret')
            self.assertEqual(secret_manager.choices('test_choices'), [('test1', 'test2'), ('test3', 'test4')])

    def test_get_datetime(self):
        """
        Test that the get_datetime method returns the expected value.
        """
        with patch.object(SecretManager, 'connect') as mock_connect_to_session:
            mock_connect_to_session.return_value = MockSecretsClient()
            secret_manager = SecretManager('TestingSecret')
            self.assertEqual(secret_manager.datetime('test_datetime'), datetime.datetime(2020, 1, 1, 0, 0))

    def test_get_date(self):
        """
        Test that the get_date method returns the expected value.
        """
        with patch.object(SecretManager, 'connect') as mock_connect_to_session:
            mock_connect_to_session.return_value = MockSecretsClient()
            secret_manager = SecretManager('TestingSecret')
            self.assertEqual(secret_manager.date('test_date'), datetime.date(2020, 1, 1))

    def test_get_decimal(self):
        """
        Test that the get_decimal method returns the expected value.
        """
        with patch.object(SecretManager, 'connect') as mock_connect_to_session:
            mock_connect_to_session.return_value = MockSecretsClient()
            secret_manager = SecretManager('TestingSecret')
            self.assertEqual(secret_manager.decimal('test_decimal'), decimal.Decimal('1.234'))

    def test_get_time(self):
        """
        Test that the get_time method returns the expected value.
        """
        with patch.object(SecretManager, 'connect') as mock_connect_to_session:
            mock_connect_to_session.return_value = MockSecretsClient()
            secret_manager = SecretManager('TestingSecret')
            self.assertEqual(secret_manager.time('test_time'), datetime.time(0, 0))

    def test_get_timedelta(self):
        """
        Test that the get_timedelta method returns the expected value.
        """
        with patch.object(SecretManager, 'connect') as mock_connect_to_session:
            mock_connect_to_session.return_value = MockSecretsClient()
            secret_manager = SecretManager('TestingSecret')
            self.assertEqual(secret_manager.timedelta('test_timedelta'), datetime.timedelta(seconds=3600))

    def test_get_uuid(self):
        """
        Test that the get_uuid method returns the expected value.
        """
        with patch.object(SecretManager, 'connect') as mock_connect_to_session:
            mock_connect_to_session.return_value = MockSecretsClient()
            secret_manager = SecretManager('TestingSecret')
            self.assertEqual(secret_manager.uuid('test_uuid'), uuid.UUID('12345678-1234-5678-1234-567812345678'))

    def test_default(self):
        """
        Test that the default method returns the expected value.
        """
        with patch.object(SecretManager, 'connect') as mock_connect_to_session:
            mock_connect_to_session.return_value = MockSecretsClient()
            secret_manager = SecretManager('TestingSecret')
            self.assertEqual(secret_manager.str('test_default', default='test'), 'test')
            self.assertEqual(secret_manager.int('test_default', default=123), 123)

    def test_dict(self):
        """
        Test that the dict method returns the expected value.
        """
        desired_response = AttrDict({
                'host': 'localhost',
                'port': '1234',
                'name': 'test_database',
                'username': 'test_database_username',
                'password': 'test_database_password',
                'options': AttrDict({'ssl': 'True'}),
        })
        with patch.object(SecretManager, 'connect') as mock_connect_to_session:
            mock_connect_to_session.return_value = MockSecretsClient()
            secret_manager = SecretManager('TestingSecret')
            secret_dict = secret_manager.dict('database')
            self.assertEqual(secret_dict, desired_response)

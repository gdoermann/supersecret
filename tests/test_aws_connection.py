"""
This is a testing set to actually connect to AWS and test
pulling and parsing secrets from AWS Secrets Manager.
This is not a unit test, but a functional test.

Only runs if environment variable AWS_TESTING is set to True.

Your AWS IAM user must have the following permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:*",
                "secretsmanager:DeleteSecret"
            ],
            "Resource": "*"
        }
    ]
}
```


"""

import unittest
import os
import json
import uuid
from collections import OrderedDict

import boto3
from botocore.exceptions import ClientError

from supersecret.exceptions import BaseSecretsManagerException
from supersecret.manager import SecretManager
from .test_manager import SECRETS_MOCK

# Set up the AWS testing environment
AWS_TESTING = bool(os.environ.get('AWS_TESTING', False))

UUID = str(uuid.uuid4())

if AWS_TESTING:
    # Setup AWS Connection
    CLIENT = boto3.client('secretsmanager', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
else:
    CLIENT = None


class TestAwsConnections(unittest.TestCase):
    """
    Tests for the SecretManager class.
    """
    secrets = OrderedDict()
    SECRET_NAMES = {f'{name}-{UUID}': name for name in SECRETS_MOCK.keys()}

    def setUp(self) -> None:
        """
        Set up the testing environment.
        """
        if not AWS_TESTING:
            self.skipTest('AWS_TESTING not set to True')

        if not self.secrets:
            self.create_secrets()

        for i, secret in enumerate(self.secrets.keys()):
            if i == 0:
                self.secret_manager = SecretManager(secret)
            else:
                self.secret_manager.load(secret)

    # Remove secret after ALL tests have run
    @classmethod
    def tearDownClass(cls) -> None:
        """
        Tear down the testing environment.
        """
        if cls.secrets:
            cls.delete_secrets()

    def create_secrets(self):
        """
        Create a test secret in AWS Secrets Manager.
        """
        for secret_name, secret in self.SECRET_NAMES.items():
            secret_string = SECRETS_MOCK['TestingSecret']['SecretString']
            CLIENT.create_secret(
                Name=secret_name,
                SecretString=secret_string
            )
            self.secrets[secret_name] = json.loads(secret_string)

    @classmethod
    def delete_secrets(cls):
        """
        Delete the test secret from AWS Secrets Manager.
        """
        for secret_name in cls.SECRET_NAMES.keys():
            CLIENT.delete_secret(SecretId=secret_name, ForceDeleteWithoutRecovery=True)

    def test_exceptions(self):
        """
        Test that the exceptions are raised as expected.
        """
        os.environ['test'] = 'test'

        self.assertRaises(ClientError, self.secret_manager.load, 'does_not_exist')

    def test_get_value_env(self):
        """
        Test that the get_value method returns the expected value.
        """
        os.environ['test'] = 'test'
        self.assertEqual(self.secret_manager.str('test'), 'test')

    def test_get_str(self):
        """
        Test that the get_str method returns the expected value.
        """
        # Should be the value from the last secret
        secret = self.secrets[list(self.secrets.keys())[-1]]
        self.assertEqual(self.secret_manager.str('username'), secret['username'])

    def test_get_int(self):
        """
        Test that the get_int method returns the expected value.
        """
        # Should be the value from the last secret
        secret = self.secrets[list(self.secrets.keys())[-1]]
        self.assertEqual(self.secret_manager.int('test_int'), int(secret['test_int']))

    def test_context_manager_usage(self):
        """
        Test that the context manager usage works as expected.
        We mock the connect method to return a mock secrets client.
        We are unable to test the client status or close because the method is mocked.
        We do this test in the actual AWS connection tests.
        """
        name = list(self.secrets.keys())[0]
        with SecretManager(name) as secret_manager:
            self.assertIsNone(secret_manager.client)
            self.assertEqual(secret_manager.str('username'), 'test_username')
            self.assertEqual(secret_manager.str('password'), 'test_password')
            self.assertIsNotNone(secret_manager.client)

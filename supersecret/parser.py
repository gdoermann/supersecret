"""
AWS Secrets Parser
"""
import base64
import json
import os
from collections import OrderedDict

from botocore.exceptions import ClientError

from .dto import GetValue
from .exceptions import define_error
from botocore.client import BaseClient


class SecretParser:
    """
    SecretParser connects to AWS and parses the secret
    """
    SERVICE_NAME: str = 'secretsmanager'

    def __init__(self, default_secret_name: str = None, **aws_kwargs):
        """
        :param secret_name: The AWS Secrets Manager secret name
        :param aws_kwargs: AWS connection kwargs for boto3.client
        """
        if default_secret_name is None:
            default_secret_name = os.environ.get('SECRET_NAME', None)
        if default_secret_name is None:
            raise KeyError('No secret name provided')

        self.client = None
        self.__client_created = False
        self.default_secret_name = default_secret_name

        self.aws_kwargs = aws_kwargs
        self._secrets = OrderedDict()

    def connect(self) -> BaseClient:
        """
        Connect to AWS Secrets Manager to the default aws session
        :return: client
        """
        if self.client:
            return self.client
        import boto3
        self.aws_kwargs.setdefault('region_name', os.environ.get('AWS_REGION', 'us-east-1'))

        self.client = boto3.client(self.SERVICE_NAME, **self.aws_kwargs)
        self.__client_created = True
        return self.client

    def load(self, secret_name: str = None, client: BaseClient = None) -> GetValue:
        """
        Load secret from AWS Secrets Manager
        """
        if secret_name is None:
            secret_name = self.default_secret_name
        if secret_name in self._secrets:
            return self._secrets[secret_name]
        if client is None:
            client = self.client
        if client is None:
            client = self.connect()
        response = self._load_secret(secret_name, client)
        self._secrets[secret_name] = response
        return response

    def _load_secret(self, secret_name: str, client: BaseClient) -> GetValue:
        try:
            raw_secret = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as error:
            error_code = error.response['Error']['Code']
            err = define_error(error_code)
            str(error)
            raise error

        else:
            if raw_secret.get('SecretBinary'):
                raw_secret['SecretValues'] = base64.b64decode(raw_secret['SecretBinary'])
                del raw_secret['SecretBinary']
            else:
                value = raw_secret['SecretString']
                if isinstance(value, str):
                    value = json.loads(value)
                raw_secret['SecretValues'] = value
                del raw_secret['SecretString']

            return GetValue(**raw_secret)

    def close(self):
        try:
            if self.__client_created and self.client:
                self.client.close()
        finally:
            self.client = None
            self._secrets = OrderedDict()

    # Context Management
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

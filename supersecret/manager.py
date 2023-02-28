"""
AWS Secrets Manager
"""
import datetime
import os
import uuid
from decimal import Decimal
from pathlib import Path
import marshmallow as ma

from .util import AttrDict
from .parser import SecretParser
from . import fields


class NotSet:
    """
    NotSet is a placeholder for when a value is not set
    """
    pass


class SecretManager(SecretParser):
    """
    Secret Manager resolves secrets from AWS Secrets Manager
    This inherits from SecretParser that handles connecting to AWS and parsing the secret(s)

    Methods for type casting values:
    * `str`: String - This is the default type
    * `int`: Integer
    * `float`: Float
    * `decimal`: decimal.Decimal
    * `bool`: Boolean
    * `list`: List - You can specify a `delimiter` and a `subcast` type for list elements
    * `choices`: List[tuple] - You can specify a `delimiter` and a `subcast` type for list elements.
        Returns the form: [(key, value), (key, value)]
    * `datetime`: datetime.datetime - You can specify a `format` for the datetime string
    * `date`: datetime.date - You can specify a `format` for the date string
    * `time`: datetime.time - You can specify a `format` for the time string
    * `timedelta`: datetime.timedelta - You can specify a `format` for the timedelta string
    * `timedelta_seconds`: datetime.timedelta - Parses from seconds
    * `uuid`: uuid.UUID - You can specify a `version` for the UUID. 1=Time-based, 3=Name-based, 4=Random, 5=Name-based
    * `log_level`: int - Parses a log level string to an int
    * `path`: pathlib.Path - Parses a string to a pathlib.Path object
    * `dict`: AttrDict - You can specify a `prefix` for the dictionary keys, a `subcast_keys` type,
        and a `subcast_values` type
    """

    def value(self, name, default=NotSet) -> str:
        """
        Get the value of a secret.  Returns raw format.
        """
        if not self._secrets:
            self.load()
        # Try to get the value from secrets
        for secret in reversed(self._secrets.values()):  # We want to get the most recent secret first
            try:
                return secret.SecretValues[name]
            except KeyError:
                pass
        # Try to get value from environment variables
        if name in os.environ:
            return os.environ[name]
        elif name.upper() in os.environ:
            return os.environ[name.upper()]

        if default is not NotSet:
            return default

        # No value found
        raise KeyError(f'Key "{name}" is not found.')

    def str(self, name, default: (str, NotSet) = NotSet) -> str:
        """
        Get the value of a secret as a string
        """
        return fields.Str().deserialize(self.value(name, default=default))

    def int(self, name, default: (str, NotSet) = NotSet) -> int:
        """
        Get the value of a secret as an integer
        """
        return fields.Int().deserialize(self.value(name, default=default))

    def float(self, name, default: (str, NotSet) = NotSet) -> float:
        """
        Get the value of a secret as a float
        """
        return fields.Float().deserialize(self.value(name, default=default))

    def decimal(self, name, default: (str, NotSet) = NotSet) -> Decimal:
        """
        Get the value of a secret as a decimal
        """
        return fields.Decimal().deserialize(self.value(name, default=default))

    def bool(self, name, default: (str, NotSet) = NotSet) -> bool:
        """
        Get the value of a secret as a boolean
        """
        return fields.Bool().deserialize(self.value(name, default=default))

    def list(self, name, delimiter=',', subcast=fields.Str, default: (str, NotSet) = NotSet) -> list:
        """
        Get the value of a secret as a list
        """
        if isinstance(subcast, type):
            subcast = subcast()
        return [subcast.deserialize(v) for v in self.value(name, default=default).split(delimiter)]

    def choices(self, name, delimiter=',', subcast: ma.fields.Field = fields.Str,
                default: (str, NotSet) = NotSet) -> list:
        """
        Get the value of a secret as a list of tuples
        """
        return fields.Choices(delimiter=delimiter, subcast=subcast).deserialize(self.value(name, default=default))

    def datetime(self, name, format='%Y-%m-%d %H:%M:%S', default: (str, NotSet) = NotSet) -> datetime:
        """
        Get the value of a secret as a datetime
        """
        return fields.Datetime(format=format).deserialize(self.value(name, default=default))

    def date(self, name, format='%Y-%m-%d', default: (str, NotSet) = NotSet) -> datetime:
        """
        Get the value of a secret as a date
        """
        return fields.Date(format=format).deserialize(self.value(name, default=default))

    def time(self, name, format='%H:%M:%S', default: (str, NotSet) = NotSet) -> datetime:
        """
        Get the value of a secret as a time
        """
        return fields.Time(format=format).deserialize(self.value(name, default=default))

    def timedelta(self, name, default: (str, NotSet) = NotSet) -> datetime:
        """
        Get the value of a secret as a timedelta
        Format: HH:MM:SS
        """
        value = self.value(name, default=default)
        return datetime.timedelta(**{k: int(v) for k, v in zip(['hours', 'minutes', 'seconds'], value.split(':'))})

    def timedelta_seconds(self, name, default: (str, NotSet) = NotSet) -> datetime:
        """
        Get the value of a secret as a timedelta
        """
        return datetime.timedelta(seconds=self.int(name, default=default))

    def uuid(self, name, version=4, default: (str, NotSet) = NotSet) -> uuid:
        """
        Get the value of a secret as a UUID
        """
        return fields.UUID(metadata=dict(version=version)).deserialize(self.value(name, default=default))

    def log_level(self, name, default: (str, NotSet) = NotSet) -> int:
        """
        Get the value of a secret as a log level
        """
        return fields.LogLevel().deserialize(self.value(name, default=default))

    def path(self, name, default: (str, NotSet) = NotSet) -> Path:
        """
        Get the value of a secret as a Path
        """
        return fields.Path().deserialize(self.value(name, default=default))

    def _parse_dict(self, prefix, dictionary: dict, response_dict: AttrDict = None,
                    subcast_keys: ma.fields.Field = fields.Str,
                    subcast_values: ma.fields.Field = fields.Str) -> AttrDict:
        """
        Parse a dictionary from a dictionary of any type.

        WILL NOT OVERRIDE EXISTING KEYS. If a key already exists, it will be skipped.

        :param prefix: Filter prefix
        :param dictionary: Dictionary to parse
        :param subcast_keys: The type to cast the keys to
        :param subcast_values:  The type to cast the values to
        :return: AttrDict
        """
        for _key, _value in dictionary.items():
            if _key.startswith(prefix) or _key.startswith(prefix.upper()):
                # Remove the prefix from the key
                clean_key = _key.split('__', 1)[1]
                subkeys = clean_key.split('__')
                _dict = response_dict
                for subkey in subkeys[:-1]:
                    subkey = subcast_keys.deserialize(subkey)
                    if subkey not in _dict:
                        _dict[subkey] = AttrDict()
                    _dict = _dict[subkey]

                final_key = subcast_keys.deserialize(subkeys[-1])
                if final_key in _dict:
                    continue
                _dict[final_key] = subcast_values.deserialize(_value)
        return response_dict

    def dict(self, prefix, subcast_keys: ma.fields.Field = fields.Str,
             subcast_values: ma.fields.Field = fields.Str) -> AttrDict:
        """
        Get the value of a secret as a dictionary.

        # Key format
        DATABASE__default__HOST=localhost
        DATABASE__default__PORT=5432
        DATABASE__default__USER=postgres
        DATABASE__default__PASSWORD=postgres
        DATABASE__default__NAME=postgres
        DATABASE__default__OPTIONS__sslmode=disable

        # Returns
        {
            'default': {
                'HOST': 'localhost',
                'PORT': 5432,
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'NAME': 'postgres',
                'OPTIONS': {
                    'sslmode': 'disable'
                }
            }
        }
        """
        if isinstance(subcast_keys, type):
            subcast_keys = subcast_keys()
        if isinstance(subcast_values, type):
            subcast_values = subcast_values()

        if not self._secrets:
            self.load()
        filter_prefix = f'{prefix}__'

        response = AttrDict()
        # Load all values that begin with prefix
        for secret in reversed(self._secrets.values()):  # We want to get the most recent secret first
            response.update(self._parse_dict(filter_prefix, secret.SecretValues, response,
                                             subcast_keys, subcast_values))

        # Load all environment variables that begin with prefix
        response.update(self._parse_dict(filter_prefix, os.environ, response, subcast_keys, subcast_values))

        return response

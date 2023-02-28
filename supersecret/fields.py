"""
Marshmallow fields for supersecret.

Fields:
* `Str`: String - This is the default type
* `Int`: Integer
* `Float`: Float
* `Decimal`: decimal.Decimal
* `Bool`: Boolean
* `List`: List - You can specify a `delimiter` and a `subcast` type for list elements
* `Choices`: List[tuple] - You can specify a `delimiter` and a `subcast` type for list elements.
        Returns the form: [(key, value), (key, value)]
* `Datetime`: datetime.datetime - You can specify a `format` for the datetime string
* `Date`: datetime.date - You can specify a `format` for the date string
* `Time`: datetime.time - You can specify a `format` for the time string
* `TimeDelta`: datetime.timedelta - You can specify a `format` for the timedelta string
* `UUID`: uuid.UUID - You can specify a `version` for the UUID. 1=Time-based, 3=Name-based, 4=Random, 5=Name-based
* `LogLevel`: int - Parses a log level string to an int
* `Path`: pathlib.Path - Parses a string to a pathlib.Path object

"""
import datetime
import logging
import pathlib

import marshmallow as ma

Str = ma.fields.Str
Int = ma.fields.Int
Float = ma.fields.Float
Decimal = ma.fields.Decimal
Bool = ma.fields.Bool
List = ma.fields.List


class Choices(ma.fields.List):
    """
    A field that parses a string to a list of choices.
    Choices should be stored as: key:value,key:value
    Choices are returned as: [(key, value), (key, value)]
    """
    def __init__(self, delimiter=',', subcast=Str, *args, **kwargs):
        super().__init__(subcast, *args, **kwargs)
        self.delimiter = delimiter

    def _deserialize(self, value, *args, **kwargs) -> list:
        if isinstance(value, list):
            return value
        subcast = self.inner
        return [(v[0], subcast.deserialize(v[1])) for v in [v.split(':') for v in value.split(self.delimiter)]]


Datetime = ma.fields.DateTime
Date = ma.fields.Date
Time = ma.fields.Time


class TimeDelta(ma.fields.Str):
    """
    A field that parses a string to a datetime.timedelta object.
    """
    def _deserialize(self, value, *args, **kwargs) -> datetime.timedelta:
        if isinstance(value, datetime.timedelta):
            return value
        ret = super()._deserialize(value, *args, **kwargs)
        hours, minutes, seconds = ret.split(':')
        return datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))


TimeDeltaSeconds = ma.fields.TimeDelta
UUID = ma.fields.UUID


class Path(ma.fields.Str):
    """
    A field that parses a string to a pathlib.Path object.
    """
    def _deserialize(self, value, *args, **kwargs) -> pathlib.Path:
        if isinstance(value, pathlib.Path):
            return value
        ret = super()._deserialize(value, *args, **kwargs)
        return pathlib.Path(ret)


class LogLevel(ma.fields.Int):
    """
    A field that parses a log level string to an int.
    """
    def _format_num(self, value) -> int:
        try:
            return super()._format_num(value)
        except (TypeError, ValueError) as error:
            value = value.upper()
            if hasattr(logging, value) and isinstance(getattr(logging, value), int):
                return getattr(logging, value)
            else:
                raise ma.ValidationError("Not a valid log level.") from error

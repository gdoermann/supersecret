import dataclasses
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

from supersecret.util import AttrDict


def nested_dataclass(*args, **kwargs):
    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                field_type = cls.__annotations__.get(name, None)
                try:
                    if field_type.__dataclass_fields__.get('data'):
                        new_obj = field_type(data=value)
                        kwargs[name] = new_obj

                    else:
                        raise AttributeError

                except AttributeError:
                    if dataclasses.is_dataclass(field_type) and isinstance(value, dict):
                        new_obj = field_type(**value)
                        kwargs[name] = new_obj

            original_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper


@dataclass
class SecretValues:
    """
    The class signature is unknown and depends on the returned data
    """
    data: dataclasses.field(default_factory=AttrDict) = None

    def __post_init__(self):
        [setattr(self, k, v) for k, v in self.data.items()]

    def __getattr__(self, item):
        if item in self.data:
            return self.data[item]
        raise KeyError(f'Key "{item}" is not found.')

    def __getitem__(self, item):
        return self.data[item]

    def items(self):
        return self.data.items()


@dataclass
class MetadataDTO:
    pass


@dataclass
class ResponseMetadata:
    HTTPHeaders: Dict
    HTTPStatusCode: int
    RequestId: str
    RetryAttempts: int


@nested_dataclass
@dataclass
class GetValue:
    ARN: str
    Name: str
    VersionId: str
    SecretValues: SecretValues
    VersionStages: List[str]
    CreatedDate: datetime
    ResponseMetadata: ResponseMetadata

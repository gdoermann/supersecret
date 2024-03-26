# Version of the supersecret library

__version__ = "1.1.0"

from .manager import SecretManager  # noqa: F401


def get_version():
    return __version__

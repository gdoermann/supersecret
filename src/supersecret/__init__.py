# Version of the supersecret library
import os

__version__ = open(os.path.join(os.path.dirname(__file__), 'VERSION.txt')).read().strip()


def get_version():
    return __version__

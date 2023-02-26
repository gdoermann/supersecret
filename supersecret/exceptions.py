import inspect
import sys


def define_error(response_error):
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if obj.__name__ == response_error:
                return obj


class DecryptionFailureException(Exception):
    """
    Secrets Manager can't decrypt the protected secret text using the provided KMS key.
    """

    def __str__(self):
        return self.__doc__


class InternalServiceErrorException(Exception):
    """
    An error occurred on the server side.
    """

    def __str__(self):
        return self.__doc__


class InvalidParameterException(Exception):
    """
    You provided an invalid value for a parameter.Deal with the exception here, and/or rethrow at your discretion.
    """

    def __str__(self):
        return self.__doc__


class InvalidRequestException(Exception):
    """
    You provided a parameter value that is not valid for the current state of the resource.
    """

    def __str__(self):
        return self.__doc__


class ResourceNotFoundException(Exception):
    """
    We can't find the resource that you asked for. Deal with the exception here, and/or rethrow at your discretion.
    """

    def __str__(self):
        return self.__doc__

import inspect
import sys


def define_error(response_error):
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if obj.__name__ == response_error:
                return obj


class BaseSecretsManagerException(Exception):
    """
    Base exception for all Secrets Manager exceptions
    """

    def __str__(self):
        return self.__doc__


class DecryptionFailureException(BaseSecretsManagerException):
    """
    Secrets Manager can't decrypt the protected secret text using the provided KMS key.
    """


class InternalServiceErrorException(BaseSecretsManagerException):
    """
    An error occurred on the server side.
    """


class InvalidParameterException(BaseSecretsManagerException):
    """
    You provided an invalid value for a parameter.Deal with the exception here, and/or rethrow at your discretion.
    """


class InvalidRequestException(BaseSecretsManagerException):
    """
    You provided a parameter value that is not valid for the current state of the resource.
    """


class ResourceNotFoundException(BaseSecretsManagerException):
    """
    We can't find the resource that you asked for. Deal with the exception here, and/or rethrow at your discretion.
    """

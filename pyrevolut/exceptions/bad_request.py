from .common import PyRevolutAPIException


class BadRequestException(PyRevolutAPIException):
    """Exception raised when the API returns a 400 Bad Request error."""

    pass

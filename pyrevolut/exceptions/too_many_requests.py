from .common import PyRevolutBaseException


class PyRevolutTooManyRequests(PyRevolutBaseException):
    """Too Many Requests -- You're sending too many requests."""

    def __init__(
        self,
        msg="You're sending too many requests. Please wait a while and try again.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)

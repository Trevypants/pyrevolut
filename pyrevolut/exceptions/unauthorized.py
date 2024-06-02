from .common import PyRevolutBaseException


class PyRevolutUnauthorized(PyRevolutBaseException):
    """Unauthorized -- Your access token is wrong."""

    def __init__(
        self,
        msg="Your access token is wrong. Please check the access token and try again.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)

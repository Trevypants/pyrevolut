from .common import PyRevolutBaseException


class PyRevolutServerUnavailable(PyRevolutBaseException):
    """Service Unavailable -- We're temporarily offline for maintenance. Please try again later."""

    def __init__(
        self,
        msg="The Revolut server is temporarily offline for maintenance. Please try again later.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)

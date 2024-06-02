from .common import PyRevolutBaseException


class PyRevolutTimeoutError(PyRevolutBaseException):
    """Timeout Error -- The request timed out."""

    def __init__(
        self,
        msg="The request timed out. Please try again.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)

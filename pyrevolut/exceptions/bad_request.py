from .common import PyRevolutBaseException


class PyRevolutBadRequest(PyRevolutBaseException):
    """Bad Request -- Your request is invalid."""

    def __init__(
        self,
        msg="Your request is invalid. Please check the request and try again.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)

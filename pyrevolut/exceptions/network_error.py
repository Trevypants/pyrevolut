from .common import PyRevolutBaseException


class PyRevolutNetworkError(PyRevolutBaseException):
    """Network Error -- The request failed due to a network error."""

    def __init__(
        self,
        msg="The request failed due to a network error. Please check your network connection and try again.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)

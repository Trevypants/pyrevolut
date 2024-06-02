from .common import PyRevolutBaseException


class PyRevolutNotAcceptable(PyRevolutBaseException):
    """Not Acceptable -- You requested a format that isn't JSON."""

    def __init__(
        self,
        msg="You requested a format that isn't JSON. Please check the request and try again.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)

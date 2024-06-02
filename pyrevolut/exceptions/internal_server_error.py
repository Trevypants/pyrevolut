from .common import PyRevolutBaseException


class PyRevolutInternalServerError(PyRevolutBaseException):
    """Internal Server Error -- We had a problem with our server. Try again later."""

    def __init__(
        self,
        msg="The Revolut server had a problem. Please try again later.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)

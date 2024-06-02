from .common import PyRevolutBaseException


class PyRevolutMethodNotAllowed(PyRevolutBaseException):
    """Method Not Allowed -- You tried to access an endpoint with an invalid method."""

    def __init__(
        self,
        msg="You tried to access an endpoint with an invalid method. Please check the method and try again.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)

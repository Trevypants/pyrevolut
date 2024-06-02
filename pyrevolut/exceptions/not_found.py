from .common import PyRevolutBaseException


class PyRevolutNotFound(PyRevolutBaseException):
    """Not Found -- The requested resource could not be found."""

    def __init__(
        self,
        msg="The requested resource could not be found on the Revolut server.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)

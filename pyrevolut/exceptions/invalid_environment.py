from .common import PyRevolutBaseException


class PyRevolutInvalidEnvironment(PyRevolutBaseException):
    """Raised when the environment is invalid"""

    def __init__(
        self,
        msg="This request is not valid for the current environment. Please check the environment and try again.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)

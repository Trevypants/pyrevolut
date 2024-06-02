from .common import PyRevolutBaseException


class PyRevolutConflict(PyRevolutBaseException):
    """Conflict -- Your request conflicts with current state of a resource."""

    def __init__(
        self,
        msg="Your request conflicts with the current state of a resource. Please check the request and try again.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)

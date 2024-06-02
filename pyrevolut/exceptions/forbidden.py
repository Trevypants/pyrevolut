from .common import PyRevolutBaseException


class PyRevolutForbidden(PyRevolutBaseException):
    """Forbidden -- Access to the requested resource or action is forbidden."""

    def __init__(
        self,
        msg="Access to the requested resource or action is forbidden.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)

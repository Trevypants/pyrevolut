from .common import PyRevolutAPIException


class InternalRevolutError(PyRevolutAPIException):
    """An internal error in the Revolut API. This is a bug in the Revolut API.
    Please report this issue to the Revolut API team."""

    pass

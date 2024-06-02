from .common import PyRevolutBaseException


class PyRevolutInvalidPayload(PyRevolutBaseException):
    """Invalid Webhook Payload -- The webhook payload is invalid."""

    def __init__(
        self,
        msg="The webhook payload is invalid. Either the payload signature is invalid or the payload timestamp is too old.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)

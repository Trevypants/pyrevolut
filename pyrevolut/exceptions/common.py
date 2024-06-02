class PyRevolutBaseException(Exception):
    """Base exception for all pyrevolut exceptions."""

    def __init__(
        self,
        msg="An error occurred while processing your request to Revolut.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)

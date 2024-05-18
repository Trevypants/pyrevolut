from pydantic import BaseModel


class DeleteCounterparty:
    """Delete a counterparty with the given ID.
    When a counterparty is deleted, you cannot make any payments to the counterparty.
    """

    ROUTE = "/1.0/counterparty/{counterparty_id}"

    class Params(BaseModel):
        """
        Query parameters for the endpoint.
        """

        pass

    class Response(BaseModel):
        """
        Response model for the endpoint.
        """

        pass

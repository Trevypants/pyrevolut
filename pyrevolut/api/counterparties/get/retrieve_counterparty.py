from pydantic import BaseModel

from pyrevolut.api.counterparties.resources import ResourceCounterparty


class RetrieveCounterparty:
    """Get the information about a specific counterparty by ID."""

    ROUTE = "/1.0/counterparty/{counterparty_id}"

    class Params(BaseModel):
        """
        Query parameters for the endpoint.
        """

        pass

    class Response(ResourceCounterparty):
        """
        Response model for the endpoint.
        """

        pass

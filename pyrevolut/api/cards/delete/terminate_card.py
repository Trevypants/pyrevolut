from pydantic import BaseModel


class TerminateCard:
    """
    Terminate a specific card, based on its ID.

    Once the card is terminated, it will not be returned by the API.

    A successful response does not get any content in return.
    """

    ROUTE = "cards/{card_id}"

    class Params(BaseModel):
        """Query parameters for the endpoint."""

        pass

    class Response(BaseModel):
        """Response model for the endpoint."""

        pass

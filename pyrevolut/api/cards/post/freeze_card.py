from pydantic import BaseModel


class FreezeCard:
    """
    Freeze a card to make it temporarily unavailable for spending.
    You can only freeze a card that is in the state active.

    A successful freeze changes the card's state to frozen,
    and no content is returned in the response.
    """

    ROUTE = "/1.0/cards/{card_id}/freeze"

    class Body(BaseModel):
        """
        Request body for the endpoint.
        """

        pass

    class Response(BaseModel):
        """
        Response model for the endpoint.
        """

        pass

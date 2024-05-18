from pydantic import BaseModel


class UnfreezeCard:
    """
    Unfreeze a card to re-enable spending for that card.
    You can only unfreeze a card that is in the state frozen.

    A successful unfreeze changes the card's state back to active,
    and no content is returned in the response.
    """

    ROUTE = "/1.0/cards/{card_id}/unfreeze"

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

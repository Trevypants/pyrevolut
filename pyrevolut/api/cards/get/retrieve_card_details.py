from pydantic import BaseModel

from pyrevolut.api.cards.resources import ResourceCard


class RetrieveCardDetails:
    """
    Get the details of a specific card, based on its ID.
    """

    ROUTE = "/cards/{card_id}"

    class Params(BaseModel):
        """
        Query parameters for the endpoint.
        """

        pass

    class Response(ResourceCard):
        """
        Response model for the endpoint.
        """

        pass

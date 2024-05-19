from typing import Annotated

from pydantic import BaseModel, Field

from pyrevolut.utils import Date


class RetrieveSensitiveCardDetails:
    """
    Get sensitive details of a specific card, based on its ID.
    Requires the READ_SENSITIVE_CARD_DATA token scope.
    """

    ROUTE = "/1.0/cards/{card_id}/sensitive-details"

    class Params(BaseModel):
        """
        Query parameters for the endpoint.
        """

        pass

    class Response(BaseModel):
        """
        Response model for the endpoint.
        """

        pan: Annotated[
            str, Field(description="The PAN (Primary Account Number) of the card.")
        ]
        cvv: Annotated[
            str, Field(description="The CVV (Card Verification Value) of the card.")
        ]
        expiry: Annotated[Date, Field(description="The card expiration date.")]

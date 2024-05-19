from pydantic import BaseModel


class CancelPayoutLink:
    """
    Cancel a payout link.
    You can only cancel a link that hasn't been claimed yet.
    A successful request does not get any content in response.

    Note
    ----
    This feature is available in the UK and the EEA.
    """

    ROUTE = "/1.0/payout-links/{payout_link_id}/cancel"

    class Body(BaseModel):
        """
        The request body model for the request.
        """

        pass

    class Response(BaseModel):
        """
        The response model for the request.
        """

        pass

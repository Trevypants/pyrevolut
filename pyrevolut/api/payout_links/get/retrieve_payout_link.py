from pydantic import BaseModel

from pyrevolut.api.payout_links.resources import ResourcePayoutLink


class RetrievePayoutLink:
    """
    Get the information about a specific link by its ID.

    Note
    ----
    This feature is available in the UK and the EEA.
    """

    ROUTE = "/1.0/payout-links/{payout_link_id}"

    class Params(BaseModel):
        """
        The query parameters for the request.
        """

        pass

    class Response(ResourcePayoutLink):
        """
        The response model for the request.
        """

        pass

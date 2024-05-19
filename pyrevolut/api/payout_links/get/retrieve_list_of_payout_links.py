from typing import Annotated

from pydantic import BaseModel, Field

from pyrevolut.utils import DateTime
from pyrevolut.api.common import EnumPayoutLinkState
from pyrevolut.api.payout_links.resources import ResourcePayoutLink


class RetrieveListOfPayoutLinks:
    """
    Get all the links that you have created, or use the query parameters to filter the results.

    The links are sorted by the created_at date in reverse chronological order.

    The returned links are paginated. The maximum number of payout links returned per
    page is specified by the limit parameter. To get to the next page, make a
    new request and use the created_at date of the last payout link returned in the previous response.

    Note
    ----
    This feature is available in the UK and the EEA.
    """

    ROUTE = "/1.0/payout-links"

    class Params(BaseModel):
        """
        The query parameters for the request.
        """

        state: Annotated[
            EnumPayoutLinkState | None,
            Field(
                description="""
                The state that the payout link is in. Possible states are:

                    created:
                        The payout link has been created, but the amount has not yet been blocked.
                    failed:
                        The payout link couldn't be generated due to a failure during transaction booking.
                    awaiting:
                        The payout link is awaiting approval.
                    active:
                        The payout link can be redeemed.
                    expired:
                        The payout link cannot be redeemed because it wasn't claimed before its expiry date.
                    cancelled:
                        The payout link cannot be redeemed because it was cancelled.
                    processing:
                        The payout link has been redeemed and is being processed.
                    processed:
                        The payout link has been redeemed and the money has been transferred to the recipient.
                """,
            ),
        ] = None
        created_before: Annotated[
            DateTime | None,
            Field(
                description="""
                Retrieves links with created_at < created_before. 
                The default value is the current date and time at which you are calling the endpoint.

                Provided in ISO 8601 format.
                """
            ),
        ] = None
        limit: Annotated[
            int | None,
            Field(
                description="""
                The maximum number of links returned per page.
                To get to the next page, make a new request and use the 
                created_at date of the last payout link returned in the previous 
                response as the value for created_before.              
                
                If not provided, the default value is 100.  
                """,
                ge=1,
                le=100,
            ),
        ] = None

    class Response(ResourcePayoutLink):
        """
        The response model for the request.
        """

        pass

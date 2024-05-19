from typing import Annotated

from pydantic import BaseModel, Field

from pyrevolut.utils import DateTime
from pyrevolut.api.cards.resources import ResourceCard


class RetrieveListOfCards:
    """
    Get the list of all cards in your organisation.
    The results are paginated and sorted by the created_at date in reverse chronological order.
    """

    ROUTE = "/1.0/cards"

    class Params(BaseModel):
        """
        Query parameters for the endpoint.
        """

        created_before: Annotated[
            DateTime | None,
            Field(
                description="""
                Retrieves cards with created_at < created_before. 
                The default value is the current date and time at which you are calling the endpoint.
                Provided in ISO 8601 format.
                """
            ),
        ] = None
        limit: Annotated[
            int | None,
            Field(
                description="""
                The maximum number of cards returned per page.
                To get to the next page, make a new request and use the 
                created_at date of the last card returned in the previous 
                response as the value for created_before.              
                
                If not provided, the default value is 100.  
                """,
                ge=1,
                le=100,
            ),
        ] = None

    class Response(ResourceCard):
        """
        Response model for the endpoint.
        """

        pass

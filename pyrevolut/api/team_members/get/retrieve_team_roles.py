from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from pyrevolut.utils import DateTime


class RetrieveTeamRoles:
    """
    Get the list of roles for your business.

    The results are paginated and sorted by the created_at date in reverse chronological order.

    This feature is available in the UK, US and the EEA.

    This feature is not available in Sandbox.
    """

    ROUTE = "/1.0/roles"

    class Params(BaseModel):
        """
        The query parameters of the request.
        """

        created_before: Annotated[
            DateTime | None,
            Field(
                description="""
                Retrieves roles with created_at < created_before. 
                The default value is the current date and time at which you are calling the endpoint.
                Provided in ISO 8601 format.
                """
            ),
        ] = None
        limit: Annotated[
            int | None,
            Field(
                description="""
                The maximum number of roles returned per page.
                To get to the next page, make a new request and use the 
                created_at date of the last role returned in the previous 
                response as the value for created_before.              
                
                If not provided, the default value is 100.  
                """,
                ge=1,
                le=100,
            ),
        ] = None

    class Response(BaseModel):
        """
        The response model.
        """

        id: Annotated[
            UUID | str,
            Field(
                description="The ID of the role. This can be a UUID or other default role such as OWNER."
            ),
        ]
        name: Annotated[str, Field(description="The name of the role.")]
        created_at: Annotated[
            DateTime,
            Field(
                description="The date and time the role was created in ISO 8601 format."
            ),
        ]
        updated_at: Annotated[
            DateTime,
            Field(
                description="The date and time the role was last updated in ISO 8601 format."
            ),
        ]

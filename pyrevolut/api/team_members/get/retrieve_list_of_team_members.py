from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr

from pyrevolut.utils import DateTime
from pyrevolut.api.common import EnumTeamMemberState


class RetrieveListOfTeamMembers:
    """
    Get information about all the team members of your business.

    The results are paginated and sorted by the created_at date in reverse chronological order.

    Note
    ----
    This feature is available in the UK, US and the EEA.

    This feature is not available in Sandbox.
    """

    ROUTE = "/1.0/team-members"

    class Params(BaseModel):
        """The parameters of the request."""

        created_before: Annotated[
            DateTime | None,
            Field(
                description="""
                Retrieves team members with created_at < created_before. 
                The default value is the current date and time at which you are calling the endpoint.
                Provided in ISO 8601 format.
                """
            ),
        ] = None
        limit: Annotated[
            int | None,
            Field(
                description="""
                The maximum number of team members returned per page.
                To get to the next page, make a new request and use the 
                created_at date of the last team member returned in the previous 
                response as the value for created_before.              
                
                If not provided, the default value is 100.  
                """,
                ge=1,
                le=100,
            ),
        ] = None

    class Response(BaseModel):
        """The response model."""

        id: Annotated[UUID, Field(description="The ID of the team member.")]
        email: Annotated[
            EmailStr, Field(description="The email address of the team member.")
        ]
        first_name: Annotated[
            str | None, Field(description="The team member's first name.")
        ] = None
        last_name: Annotated[
            str | None, Field(description="The team member's last name.")
        ] = None
        state: Annotated[
            EnumTeamMemberState,
            Field(description="The state that the team member is in."),
        ]
        role_id: Annotated[
            UUID | str,
            Field(
                description="The ID of the team member's role. This can be a UUID or other default role such as Owner."
            ),
        ]
        created_at: Annotated[
            DateTime,
            Field(
                description="The date and time the team member was created in ISO 8601 format."
            ),
        ]
        updated_at: Annotated[
            DateTime,
            Field(
                description="The date and time the team member was last updated in ISO 8601 format."
            ),
        ]

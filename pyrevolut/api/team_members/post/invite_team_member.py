from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr

from pyrevolut.utils import DateTime


class InviteTeamMember:
    """
    Invite a new member to your business account.

    When you invite a new team member to your business account,
    an invitation is sent to their email address that you provided in this request.
    To join your business account, the new team member has to accept this invitation.

    Note
    ----
    This feature is available in the UK, US and the EEA.

    This feature is not available in Sandbox.
    """

    ROUTE = "/1.0/team-members"

    class Body(BaseModel):
        """
        The body of the request.
        """

        email: Annotated[
            EmailStr, Field(description="The email address of the invited member.")
        ]
        role_id: Annotated[
            UUID | str,
            Field(description="The ID of the role to assign to the new member."),
        ]

    class Response(BaseModel):
        """The response model."""

        email: Annotated[
            EmailStr, Field(description="The email address of the invited member.")
        ]
        id: Annotated[UUID, Field(description="The ID of the invited member.")]
        role_id: Annotated[
            UUID | str,
            Field(description="The ID of the role assigned to the member."),
        ]
        created_at: Annotated[
            DateTime,
            Field(description="The date and time when the member was created."),
        ]
        updated_at: Annotated[
            DateTime,
            Field(description="The date and time when the member was last updated."),
        ]

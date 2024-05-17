from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from pyrevolut.api.common import EnumPayoutLinkState


class ResourcePayoutLinkCreated(BaseModel):
    """
    Payout Link Created resource model.
    """

    id: Annotated[
        UUID,
        Field(description="The ID of the payout link."),
    ]
    state: Annotated[
        EnumPayoutLinkState,
        Field(description="The state of the payout link."),
    ]
    request_id: Annotated[
        str | None,
        Field(description="The request ID provided by the client."),
    ] = None

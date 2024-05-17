from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from pyrevolut.api.common import EnumPayoutLinkState


class ResourcePayoutLinkStateChanged(BaseModel):
    """
    Payout Link State Changed resource model.
    """

    id: Annotated[
        UUID,
        Field(description="The ID of the payout link."),
    ]
    request_id: Annotated[
        str | None,
        Field(description="The request ID provided by the client."),
    ] = None
    old_state: Annotated[
        EnumPayoutLinkState,
        Field(description="The previous state of the payout link."),
    ]
    new_state: Annotated[
        EnumPayoutLinkState,
        Field(description="The new state of the payout link."),
    ]

from typing import Annotated

from pydantic import BaseModel, Field

from pyrevolut.utils import DateTime
from pyrevolut.api.common import EnumWebhookEvent

from .payout_link_created import ResourcePayoutLinkCreated
from .payout_link_state_changed import ResourcePayoutLinkStateChanged
from .transaction_created import ResourceTransactionCreated
from .transaction_state_changed import ResourceTransactionStateChanged


class ResourceWebhookPayload(BaseModel):
    """
    Webhook payload resource model.
    """

    event: Annotated[
        EnumWebhookEvent,
        Field(description="The event type."),
    ]
    timestamp: Annotated[
        DateTime,
        Field(description="The event time."),
    ]
    data: Annotated[
        ResourcePayoutLinkCreated
        | ResourcePayoutLinkStateChanged
        | ResourceTransactionCreated
        | ResourceTransactionStateChanged,
        Field(description="The event data."),
    ]

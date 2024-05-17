from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl

from pyrevolut.api.common import EnumWebhookEvent


class ResourceWebhook(BaseModel):
    """
    Webhook resource model.
    """

    id: Annotated[UUID, Field(description="The ID of the webhook.")]
    url: Annotated[
        HttpUrl,
        Field(
            description="The valid webhook URL that event notifications are sent to. The supported protocol is https."
        ),
    ]
    events: Annotated[
        list[EnumWebhookEvent],
        Field(description="The list of events that the webhook is subscribed to."),
    ]

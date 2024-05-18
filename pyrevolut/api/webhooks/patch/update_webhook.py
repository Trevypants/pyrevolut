from typing import Annotated

from pydantic import BaseModel, Field, HttpUrl

from pyrevolut.api.common import EnumWebhookEvent
from pyrevolut.api.webhooks.resources import ResourceWebhook


class UpdateWebhook:
    """
    Update an existing webhook. Change the URL to which event notifications are
    sent or the list of event types to be notified about.

    You must specify at least one of these two.
    The fields that you don't specify are not updated.
    """

    ROUTE = "/2.0/webhooks/{webhook_id}"

    class Body(BaseModel):
        """
        The body of the request.
        """

        url: Annotated[
            HttpUrl | None,
            Field(
                description="""
                A valid webhook URL to which to send event notifications. 
                The supported protocol is https.
                """,
            ),
        ] = None
        events: Annotated[
            list[EnumWebhookEvent] | None,
            Field(
                description="""
                A list of event types to subscribe to. 
                """,
            ),
        ] = None

    class Response(ResourceWebhook):
        """
        The response model for the request.
        """

        pass

from typing import Annotated

from pydantic import BaseModel, Field, HttpUrl

from pyrevolut.api.common import EnumWebhookEvent
from pyrevolut.api.webhooks.resources import ResourceWebhook


class CreateWebhook:
    """
    Create a new webhook to receive event notifications to the specified URL.
    Provide a list of event types that you want to subscribe to and a URL for the webhook.
    Only HTTPS URLs are supported.
    """

    ROUTE = "/2.0/webhooks"

    class Body(BaseModel):
        """
        The body of the request.
        """

        url: Annotated[
            HttpUrl,
            Field(
                description="""
                A valid webhook URL to which to send event notifications. 
                The supported protocol is https.
                """,
            ),
        ]
        events: Annotated[
            list[EnumWebhookEvent] | None,
            Field(
                description="""
                A list of event types to subscribe to. 
                If you don't provide it, you're automatically subscribed to the default event types:
                - TransactionCreated
                - TransactionStateChanged
                """,
            ),
        ] = None

    class Response(ResourceWebhook):
        """
        The response model for the request.
        """

        signing_secret: Annotated[
            str,
            Field(
                description="""
                The signing secret for the webhook.
                """,
            ),
        ]

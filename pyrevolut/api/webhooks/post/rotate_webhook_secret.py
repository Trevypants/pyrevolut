from typing import Annotated

from pydantic import BaseModel, Field
from pydantic_extra_types.pendulum_dt import Duration

from pyrevolut.api.webhooks.resources import ResourceWebhook


class RotateWebhookSecret:
    """
    Rotate a signing secret for a specific webhook.
    """

    ROUTE = "/2.0/webhooks/{webhook_id}/rotate-signing-secret"

    class Body(BaseModel):
        """
        The body of the request.
        """

        expiration_period: Annotated[
            Duration | None,
            Field(
                description="""
                The expiration period for the signing secret in ISO 8601 format. 
                If set, when you rotate the secret, it continues to be valid until the 
                expiration period has passed. Otherwise, on rotation, the secret is 
                invalidated immediately. 
                The maximum value is 7 days.
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

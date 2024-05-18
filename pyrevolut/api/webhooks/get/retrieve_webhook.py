from typing import Annotated

from pydantic import BaseModel, Field

from pyrevolut.api.webhooks.resources import ResourceWebhook


class RetrieveWebhook:
    """
    Get the information about a specific webhook by ID.
    """

    ROUTE = "/2.0/webhooks/{webhook_id}"

    class Params(BaseModel):
        """
        The query parameters for the request.
        """

        pass

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

from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl

from pyrevolut.utils import DateTime
from pyrevolut.api.webhooks.resources import ResourceWebhookPayload


class RetrieveListOfFailedWebhooks:
    """
    Get the list of all your failed webhook events, or use the query
    parameters to filter the results.

    The events are sorted by the created_at date in reverse chronological order.

    The returned failed events are paginated. The maximum number of events returned
    per page is specified by the limit parameter.
    To get to the next page, make a new request and use the created_at date of the
    last event returned in the previous response.
    """

    ROUTE = "/2.0/webhooks/{webhook_id}/failed-events"

    class Params(BaseModel):
        """
        The query parameters for the request.
        """

        limit: Annotated[
            int | None,
            Field(
                description="""
                The maximum number of events returned per page.

                To get to the next page, make a new request and use the created_at date of 
                the last event returned in the previous response as value for created_before.
                
                If not specified, the default value is 100.
                """,
                ge=1,
                le=1000,
            ),
        ] = None
        created_before: Annotated[
            DateTime | None,
            Field(
                description="""
                Retrieves events with created_at < created_before. 
                Cannot be older than the current date minus 21 days. 
                The default value is the current date and time at which you are calling the endpoint.

                Provided in ISO 8601 format.
                """,
            ),
        ] = None

    class Response(BaseModel):
        """
        The response model for the request.
        """

        id: Annotated[UUID, Field(description="The ID of the webhook event.")]
        created_at: Annotated[
            DateTime,
            Field(
                description="The date and time the event was created in ISO 8601 format.",
            ),
        ]
        updated_at: Annotated[
            DateTime,
            Field(
                description="The date and time the event was last updated in ISO 8601 format.",
            ),
        ]
        webhook_id: Annotated[
            UUID,
            Field(description="The ID of the webhook for which the event failed."),
        ]
        webhook_url: Annotated[
            HttpUrl,
            Field(
                description="The valid webhook URL that event notifications are sent to. The supported protocol is https",
            ),
        ]
        payload: Annotated[
            ResourceWebhookPayload,
            Field(description="The details of the failed event."),
        ]
        last_sent_date: Annotated[
            DateTime,
            Field(
                description="The date and time the last attempt at the event delivery occurred in ISO 8601 format.",
            ),
        ]

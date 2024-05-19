from uuid import UUID
from datetime import datetime

from pydantic_extra_types.pendulum_dt import Duration

from pyrevolut.utils import DateTime
from pyrevolut.api.common import (
    BaseEndpointSync,
    EnumWebhookEvent,
)

from pyrevolut.api.webhooks.get import (
    RetrieveListOfWebhooks,
    RetrieveWebhook,
    RetrieveListOfFailedWebhooks,
)
from pyrevolut.api.webhooks.post import CreateWebhook, RotateWebhookSecret
from pyrevolut.api.webhooks.patch import UpdateWebhook
from pyrevolut.api.webhooks.delete import DeleteWebhook


class EndpointWebhooksSync(BaseEndpointSync):
    """The Webhooks API

    A webhook (also called a web callback) allows your system to receive
    updates about your account to an HTTPS endpoint that you provide.
    When a supported event occurs, a notification is posted via HTTP POST method
    to the specified endpoint.

    If the receiver returns an HTTP error response, Revolut will retry the webhook
    event three more times, each with a 10-minute interval.

    The following events are supported:

    TransactionCreated
    TransactionStateChanged
    PayoutLinkCreated
    PayoutLinkStateChanged
    """

    def get_all_webhooks(
        self,
        **kwargs,
    ) -> list[dict] | list[RetrieveListOfWebhooks.Response]:
        """
        Get the list of all your existing webhooks and their details.

        Parameters
        ----------
        None

        Returns
        -------
        list[dict] | list[RetrieveListOfWebhooks.Response]
            The list of all your existing webhooks and their details.
        """
        endpoint = RetrieveListOfWebhooks
        path = endpoint.ROUTE
        params = endpoint.Params()

        return self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    def get_webhook(
        self,
        webhook_id: UUID,
        **kwargs,
    ) -> dict | RetrieveWebhook.Response:
        """
        Get the information about a specific webhook by ID.

        Parameters
        ----------
        webhook_id : UUID
            The ID of the webhook.

        Returns
        -------
        dict | RetrieveWebhook.Response
            The information about the webhook.
        """
        endpoint = RetrieveWebhook
        path = endpoint.ROUTE.format(webhook_id=webhook_id)
        params = endpoint.Params()

        return self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    def get_failed_webhook_events(
        self,
        webhook_id: UUID,
        limit: int | None = None,
        created_before: datetime | DateTime | str | int | float | None = None,
        **kwargs,
    ) -> list[dict] | list[RetrieveListOfFailedWebhooks.Response]:
        """
        Get the list of all your failed webhook events, or use the query
        parameters to filter the results.

        The events are sorted by the created_at date in reverse chronological order.

        The returned failed events are paginated. The maximum number of events returned
        per page is specified by the limit parameter.
        To get to the next page, make a new request and use the created_at date of the
        last event returned in the previous response.

        Parameters
        ----------
        webhook_id : UUID
            The ID of the webhook.
        limit : int, optional
            The maximum number of events returned per page.
            To get to the next page, make a new request and use the created_at date of
            the last event returned in the previous response as value for created_before.
            If not specified, the default value is 100.
        created_before : datetime | DateTime | str | int | float, optional
            Retrieves events with created_at < created_before.
            Cannot be older than the current date minus 21 days.
            The default value is the current date and time at which you are calling the endpoint.
            Provided in ISO 8601 format.

        Returns
        -------
        list[dict] | list[RetrieveListOfFailedWebhooks.Response]
            The list of all your failed webhook events.
        """
        endpoint = RetrieveListOfFailedWebhooks
        path = endpoint.ROUTE.format(webhook_id=webhook_id)
        params = endpoint.Params(
            limit=limit,
            created_before=created_before,
        )

        return self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    def create_webhook(
        self,
        url: str,
        events: list[EnumWebhookEvent] | None = None,
        **kwargs,
    ) -> dict | CreateWebhook.Response:
        """
        Create a new webhook to receive event notifications to the specified URL.
        Provide a list of event types that you want to subscribe to and a URL for the webhook.
        Only HTTPS URLs are supported.

        Parameters
        ----------
        url : str
            A valid webhook URL to which to send event notifications.
            The supported protocol is https.
        events : list[EnumWebhookEvent], optional
            A list of event types to subscribe to.
            If you don't provide it, you're automatically subscribed to the default event types:
            - TransactionCreated
            - TransactionStateChanged

        Returns
        -------
        dict | CreateWebhook.Response
            The response model for the request.
        """
        endpoint = CreateWebhook
        path = endpoint.ROUTE
        body = endpoint.Body(
            url=url,
            events=events,
        )

        return self.client.post(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

    def rotate_webhook_secret(
        self,
        webhook_id: UUID,
        expiration_period: Duration | None = None,
        **kwargs,
    ) -> dict | RotateWebhookSecret.Response:
        """
        Rotate a signing secret for a specific webhook.

        Parameters
        ----------
        webhook_id : UUID
            The ID of the webhook.
        expiration_period : Duration, optional
            The expiration period for the signing secret in ISO 8601 format.
            If set, when you rotate the secret, it continues to be valid until the
            expiration period has passed.
            Otherwise, on rotation, the secret is invalidated immediately.
            The maximum value is 7 days.

        Returns
        -------
        dict | RotateWebhookSecret.Response
            The response model for the request.
        """
        endpoint = RotateWebhookSecret
        path = endpoint.ROUTE.format(webhook_id=webhook_id)
        body = endpoint.Body(
            expiration_period=expiration_period,
        )

        return self.client.post(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

    def update_webhook(
        self,
        webhook_id: UUID,
        url: str | None = None,
        events: list[EnumWebhookEvent] | None = None,
        **kwargs,
    ) -> dict | UpdateWebhook.Response:
        """
        Update an existing webhook. Change the URL to which event notifications are
        sent or the list of event types to be notified about.

        You must specify at least one of these two.
        The fields that you don't specify are not updated.

        Parameters
        ----------
        webhook_id : UUID
            The ID of the webhook.
        url : str, optional
            A valid webhook URL to which to send event notifications.
            The supported protocol is https.
        events : list[EnumWebhookEvent], optional
            A list of event types to subscribe to.

        Returns
        -------
        dict | UpdateWebhook.Response
            The response model for the request.
        """
        endpoint = UpdateWebhook
        path = endpoint.ROUTE.format(webhook_id=webhook_id)
        body = endpoint.Body(
            url=url,
            events=events,
        )

        return self.client.patch(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

    def delete_webhook(
        self,
        webhook_id: UUID,
        **kwargs,
    ) -> dict | DeleteWebhook.Response:
        """
        Delete a specific webhook.

        A successful response does not get any content in return.

        Parameters
        ----------
        webhook_id : UUID
            The ID of the webhook.

        Returns
        -------
        dict | DeleteWebhook.Response
            An empty dictionary.
        """
        endpoint = DeleteWebhook
        path = endpoint.ROUTE.format(webhook_id=webhook_id)
        params = endpoint.Params()

        return self.client.delete(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

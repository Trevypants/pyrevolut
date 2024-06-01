from pyrevolut.api.common import BaseEndpointSync
from pyrevolut.api.webhooks.resources import ResourceWebhookPayload


class BaseEndpointWebhooks(BaseEndpointSync):
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

    def receive_webhook_event(
        self,
        payload: dict,
        **kwargs,
    ):
        """
        Receive a webhook event notification.

        Parameters
        ----------
        payload : dict
            The webhook event payload.

        Returns
        -------
        dict | ResourceWebhookPayload
            The webhook event payload.
        """
        # Raw response
        if self.client.return_type == "raw":
            return payload

        # Dict response
        model_response = ResourceWebhookPayload(**payload)
        if self.client.return_type == "dict":
            return model_response.model_dump()

        # Model response
        if self.client.return_type == "model":
            return model_response

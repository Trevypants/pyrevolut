"""A webhook (also called a web callback) allows your system to receive
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

Reference link: https://developer.revolut.com/docs/business/webhooks-v-2
"""

# flake8: noqa: F401
from .endpoint import EndpointWebhooksSync, EndpointWebhooksAsync

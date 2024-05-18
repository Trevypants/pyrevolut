"""Create a payment draft to request an approval for a payment from a
business owner or admin before the payment is executed.
The business owner or admin must manually approve it in the
Revolut Business User Interface.

You can also retrieve one or all payment drafts, and delete a payment draft.

Reference link: https://developer.revolut.com/docs/business/payment-drafts
"""

# flake8: noqa: F401
from .endpoint import EndpointPaymentDraftsSync, EndpointPaymentDraftsAsync

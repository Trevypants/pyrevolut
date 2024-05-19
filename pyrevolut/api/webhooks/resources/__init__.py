"""This module holds the Webhooks resource models."""

# flake8: noqa: F401

from .payout_link_created import ResourcePayoutLinkCreated
from .payout_link_state_changed import ResourcePayoutLinkStateChanged
from .transaction_created import ResourceTransactionCreated
from .transaction_state_changed import ResourceTransactionStateChanged
from .webhook_payload import ResourceWebhookPayload
from .webhook import ResourceWebhook

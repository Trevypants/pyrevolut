from enum import StrEnum


class EnumWebhookEvent(StrEnum):
    """
    Enum for webhook event types
    """

    TRANSACTION_CREATED = "TransactionCreated"
    TRANSACTION_STATE_CHANGED = "TransactionStateChanged"
    PAYOUT_LINK_CREATED = "PayoutLinkCreated"
    PAYOUT_LINK_STATE_CHANGED = "PayoutLinkStateChanged"

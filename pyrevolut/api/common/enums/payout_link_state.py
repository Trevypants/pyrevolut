from enum import StrEnum


class EnumPayoutLinkState(StrEnum):
    """Payout link state.

    The state that the payout link is in. Possible states are:

    created:
        The payout link has been created, but the amount has not yet been blocked.
    failed:
        The payout link couldn't be generated due to a failure during transaction booking.
    awaiting:
        The payout link is awaiting approval.
    active:
        The payout link can be redeemed.
    expired:
        The payout link cannot be redeemed because it wasn't claimed before its expiry date.
    cancelled:
        The payout link cannot be redeemed because it was cancelled.
    processing:
        The payout link has been redeemed and is being processed.
    processed:
        The payout link has been redeemed and the money has been transferred to the recipient.
    """

    CREATED = "created"
    FAILED = "failed"
    AWAITING = "awaiting"
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    PROCESSING = "processing"
    PROCESSED = "processed"

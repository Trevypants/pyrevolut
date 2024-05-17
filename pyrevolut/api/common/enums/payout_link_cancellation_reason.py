from enum import StrEnum


class EnumPayoutLinkCancellationReason(StrEnum):
    """Payout link cancellation reason.

    The reason why the payout link was cancelled. Possible reasons are:

    too_many_name_check_attempts:
        The name check failed too many times.
    """

    TOO_MANY_NAME_CHECK_ATTEMPTS = "too_many_name_check_attempts"

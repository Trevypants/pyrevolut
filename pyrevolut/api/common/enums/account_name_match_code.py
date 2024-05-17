from enum import StrEnum


class EnumAccountNameMatchCode(StrEnum):
    """Account Name Match Code Enum

    The result of the account name check. Possible values:

        matched:
            The name and account type match the provided values.
        close_match:
            The name and account type are similar to the provided values.
            The actual values are returned.
        not_matched:
            The name and account type don't match the provided values.
        cannot_be_checked:
            The check cannot be performed and retries won't help.
            For example, the recipient's bank doesn't support CoP.
        temporarily_unavailable:
            The check cannot be performed right now.
            For example, the recipient's bank didn't respond to our request.
            You should retry the request later.
    """

    MATCHED = "matched"
    CLOSE_MATCH = "close_match"
    NOT_MATCHED = "not_matched"
    CANNOT_BE_CHECKED = "cannot_be_checked"
    TEMPORARILY_UNAVAILABLE = "temporarily_unavailable"

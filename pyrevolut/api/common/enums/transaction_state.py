from enum import StrEnum


class EnumTransactionState(StrEnum):
    """
    Indicates the transaction state. Possible values:

    created:
        The transaction has been created and is either processed asynchronously
        or scheduled for a later time.
    pending:
        The transaction is pending until it's being processed.
        If the transfer is made between Revolut accounts,
        this state is skipped and the transaction is executed instantly.
    completed:
        The transaction was successful.
    declined:
        The transaction was unsuccessful. This can happen for a variety of reasons,
        for example, insufficient account balance, wrong receiver information, etc.
    failed:
        The transaction was unsuccessful. This can happen for a variety of reasons,
        for example, invalid API calls, blocked payments, etc.
    reverted:
        The transaction was reverted. This can happen for a variety of reasons,
        for example, the receiver being inaccessible.
    cancelled:
        The transaction was cancelled.
    """

    CREATED = "created"
    PENDING = "pending"
    COMPLETED = "completed"
    DECLINED = "declined"
    FAILED = "failed"
    REVERTED = "reverted"
    CANCELLED = "cancelled"

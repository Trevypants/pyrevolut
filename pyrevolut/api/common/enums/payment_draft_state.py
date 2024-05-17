from enum import StrEnum


class EnumPaymentDraftState(StrEnum):
    """Indicates the payment draft state."""

    CREATED = "CREATED"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    REVERTED = "REVERTED"
    DECLINED = "DECLINED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
    DELETED = "DELETED"

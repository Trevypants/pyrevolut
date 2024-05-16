from enum import StrEnum


class EnumCardState(StrEnum):
    """Card state enumeration"""

    CREATED = "created"
    PENDING = "pending"
    ACTIVE = "active"
    FROZEN = "frozen"
    LOCKED = "locked"

from enum import StrEnum


class EnumAccountType(StrEnum):
    """Account type enum"""

    SELF = "self"
    REVOLUT = "revolut"
    EXTERNAL = "external"

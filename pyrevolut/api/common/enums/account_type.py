from enum import StrEnum


class EnumAccountType(StrEnum):
    """Account type enum"""

    REVOLUT = "revolut"
    EXTERNAL = "external"

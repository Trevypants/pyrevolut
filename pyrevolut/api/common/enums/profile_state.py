from enum import StrEnum


class EnumProfileState(StrEnum):
    """Profile state enum"""

    CREATED = "created"
    DRAFTED = "drafted"
    DELETED = "deleted"

from enum import StrEnum


class EnumTeamMemberState(StrEnum):
    """Enum for team member state"""

    CREATED = "created"
    CONFIRMED = "confirmed"
    WAITING = "waiting"
    ACTIVE = "active"
    LOCKED = "locked"
    DISABLED = "disabled"

from enum import StrEnum


class EnumAccountNameMatchReasonType(StrEnum):
    """Account Name Match Reason Type Enum

    The reason type. Possible values:

        uk_cop:
            The CoP reason.
    """

    UK_COP = "uk_cop"

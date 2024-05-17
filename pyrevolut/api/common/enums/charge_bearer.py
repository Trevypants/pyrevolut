from enum import StrEnum


class EnumChargeBearer(StrEnum):
    """Enum for the party that will be charged the transaction fees"""

    SHARED = "shared"
    DEBTOR = "debtor"

from enum import StrEnum


class EnumSimulateTransferStateAction(StrEnum):
    """
    Enum for simulate transfer state action
    """

    COMPLETE = "complete"
    REVERT = "revert"
    DECLINE = "decline"
    FAIL = "fail"

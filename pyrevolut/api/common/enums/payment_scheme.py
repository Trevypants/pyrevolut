from enum import StrEnum


class EnumPaymentScheme(StrEnum):
    """Payment scheme enum"""

    CHAPS = "chaps"
    BACS = "bacs"
    FASTER_PAYMENTS = "faster_payments"
    SEPA = "sepa"
    SWIFT = "swift"
    ACH = "ach"
    ELIXIR = "elixir"
    SORBNET = "sorbnet"
    NICS = "nics"
    RIX = "rix"
    SUMCLEARING = "sumclearing"

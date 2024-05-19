from enum import StrEnum


class EnumTransactionType(StrEnum):
    """Transaction type enum."""

    ATM = "atm"
    CARD_PAYMENT = "card_payment"
    CARD_REFUND = "card_refund"
    CARD_CHARGEBACK = "card_chargeback"
    CARD_CREDIT = "card_credit"
    EXCHANGE = "exchange"
    TRANSFER = "transfer"
    LOAN = "loan"
    FEE = "fee"
    REFUND = "refund"
    TOPUP = "topup"
    TOPUP_RETURN = "topup_return"
    TAX = "tax"
    TAX_REFUND = "tax_refund"
    TEMP_BLOCK = "temp_block"

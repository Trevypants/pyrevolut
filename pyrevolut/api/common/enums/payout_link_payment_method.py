from enum import StrEnum


class EnumPayoutLinkPaymentMethod(StrEnum):
    """Payout link payment method.

    The list of payout methods that the recipient can use to claim the payout, where:

        revolut:
            Revolut peer-to-peer (P2P) transfer

        bank_account:
            External bank transfer

        card:
            Card transfer
    """

    REVOLUT = "revolut"
    BANK_ACCOUNT = "bank_account"
    CARD = "card"

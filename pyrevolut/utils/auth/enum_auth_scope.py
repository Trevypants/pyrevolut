from enum import StrEnum


class EnumAuthScope(StrEnum):
    """Enum class for the scopes

    Access tokens can be issued with four security scopes and require a JWT (JSON Web Token)
    signature to be obtained:

        READ: Permissions for GET operations.

        WRITE: Permissions to update counterparties, webhooks, and issue payment drafts.

        PAY: Permissions to initiate or cancel transactions and currency exchanges.

        READ_SENSITIVE_CARD_DATA: Permissions to retrieve sensitive card details.

    Caution
    -------
    If you enable the READ_SENSITIVE_CARD_DATA scope for your access token, you must
    set up IP whitelisting.
    Failing to do so will prevent you from accessing any Business API endpoint.
    """

    READ = "READ"
    WRITE = "WRITE"
    PAY = "PAY"
    READ_SENSITIVE_CARD_DATA = "READ_SENSITIVE_CARD_DATA"

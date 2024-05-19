from typing import Annotated
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, Field
from pydantic_extra_types.currency_code import Currency
from pydantic_extra_types.country import CountryAlpha2, CountryAlpha3
from pydantic_extra_types.phone_numbers import PhoneNumber

from pyrevolut.utils import DateTime, Date
from pyrevolut.api.common import (
    EnumTransactionType,
    EnumTransactionState,
    EnumAccountType,
)


class ResourceTransaction(BaseModel):
    """
    Transaction resource model.
    """

    class ModelMerchant(BaseModel):
        """The information about the merchant (only for card transfers)"""

        name: Annotated[str, Field(description="The name of the merchant.")]
        city: Annotated[str, Field(description="The city of the merchant.")]
        category_code: Annotated[
            str, Field(description="The category code of the merchant.")
        ]
        country: Annotated[
            CountryAlpha2 | CountryAlpha3,
            Field(
                description="The country of the merchant as the 2-letter ISO 3166 code."
            ),
        ]

    class ModelLeg(BaseModel):
        """
        The legs of the transaction:

            - For transactions between your Revolut accounts,
            there can be 2 legs, for example, an internal transfer made out of
            the GBP account and into the EUR account.

            - For transactions in other cases, there is only 1 leg.
        """

        class ModelCounterparty(BaseModel):
            """The counterparty of the transaction."""

            account_id: Annotated[
                UUID | None,
                Field(description="The ID of the counterparty account."),
            ] = None
            account_type: Annotated[
                EnumAccountType,
                Field(description="Indicates the type of the account."),
            ]
            id: Annotated[
                UUID | None,
                Field(description="The ID of the counterparty."),
            ] = None

        leg_id: Annotated[UUID, Field(description="The ID of the leg.")]
        amount: Annotated[
            Decimal,
            Field(description="The amount of the transaction leg."),
        ]
        fee: Annotated[
            Decimal | None,
            Field(description="The amount of the transaction leg fee."),
        ] = None
        currency: Annotated[
            Currency,
            Field(description="ISO 4217 currency code in upper case."),
        ]
        bill_amount: Annotated[
            Decimal | None,
            Field(description="The billing amount for cross-currency payments."),
        ] = None
        bill_currency: Annotated[
            Currency | None,
            Field(description="The billing currency for cross-currency payments."),
        ] = None
        account_id: Annotated[
            UUID,
            Field(
                description="The ID of the account that the transaction leg is associated with."
            ),
        ]
        counterparty: Annotated[
            ModelCounterparty | None,
            Field(description="The counterparty of the transaction leg."),
        ] = None
        description: Annotated[
            str | None,
            Field(description="The transaction leg purpose."),
        ] = None
        balance: Annotated[
            Decimal | None,
            Field(
                description="The total balance of the account that the transaction is associated with."
            ),
        ] = None

    class ModelCard(BaseModel):
        """The card details (only for card transfers)."""

        card_number: Annotated[
            str,
            Field(description="The masked card number."),
        ]
        first_name: Annotated[
            str | None,
            Field(description="The first name of the cardholder."),
        ] = None
        last_name: Annotated[
            str | None,
            Field(description="The last name of the cardholder."),
        ] = None
        phone: Annotated[
            PhoneNumber | None,
            Field(
                description="The phone number of the cardholder in the E.164 format."
            ),
        ] = None

    id: Annotated[UUID, Field(description="The ID of the transaction.")]
    type: Annotated[
        EnumTransactionType, Field(description="Indicates the transaction type.")
    ]
    request_id: Annotated[
        str | None,
        Field(
            description="The request ID that you provided previously.", max_length=40
        ),
    ] = None
    state: Annotated[
        EnumTransactionState, Field(description="Indicates the transaction state.")
    ]
    reason_code: Annotated[
        str | None,
        Field(
            description="The reason code when the transaction state is declined or failed."
        ),
    ] = None
    created_at: Annotated[
        DateTime,
        Field(
            description="The date and time the transaction was created in ISO 8601 format."
        ),
    ]
    updated_at: Annotated[
        DateTime,
        Field(
            description="The date and time the transaction was last updated in ISO 8601 format."
        ),
    ]
    completed_at: Annotated[
        DateTime | None,
        Field(
            description="""
            The date and time the transaction was completed in ISO 8601 format. 
            This is required when the transaction state is completed.
            """
        ),
    ] = None
    scheduled_for: Annotated[
        Date | None,
        Field(
            description="""
            The scheduled date of the payment, if applicable. Provided in ISO 8601 format.
            """
        ),
    ] = None
    related_transaction_id: Annotated[
        UUID | None,
        Field(description="The ID of the original transaction that has been refunded."),
    ] = None
    merchant: Annotated[
        ModelMerchant | None,
        Field(
            description="The information about the merchant (only for card transfers)."
        ),
    ] = None
    reference: Annotated[
        str | None,
        Field(description="The reference of the transaction."),
    ] = None
    legs: Annotated[
        list[ModelLeg],
        Field(
            description="""
            The legs of the transaction:

            - For transactions between your Revolut accounts,
            there can be 2 legs, for example, an internal transfer made out of
            the GBP account and into the EUR account.

            - For transactions in other cases, there is only 1 leg.
            """
        ),
    ]
    card: Annotated[
        ModelCard | None,
        Field(description="The card details (only for card transfers)."),
    ] = None

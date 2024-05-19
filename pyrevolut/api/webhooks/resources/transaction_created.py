from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic_extra_types.currency_code import Currency

from pyrevolut.utils import DateTime, Date
from pyrevolut.api.common import (
    EnumTransactionType,
    EnumTransactionState,
    EnumAccountType,
)


class ResourceTransactionCreated(BaseModel):
    """
    Transaction Created resource model.
    """

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
        amount: Annotated[
            float,
            Field(description="The amount of the transaction leg."),
        ]
        fee: Annotated[
            float | None,
            Field(description="The amount of the transaction leg fee."),
        ] = None
        currency: Annotated[
            Currency,
            Field(description="ISO 4217 currency code in upper case."),
        ]
        bill_amount: Annotated[
            float | None,
            Field(description="The billing amount for cross-currency payments."),
        ] = None
        bill_currency: Annotated[
            Currency | None,
            Field(description="The billing currency for cross-currency payments."),
        ] = None
        description: Annotated[
            str | None,
            Field(description="The transaction leg purpose."),
        ] = None
        balance: Annotated[
            float | None,
            Field(
                description="The total balance of the account that the transaction is associated with."
            ),
        ] = None

    id: Annotated[UUID, Field(description="The ID of the transaction.")]
    type: Annotated[
        EnumTransactionType, Field(description="Indicates the transaction type.")
    ]
    state: Annotated[
        EnumTransactionState, Field(description="Indicates the transaction state.")
    ]
    request_id: Annotated[
        str | None,
        Field(
            description="The request ID that you provided previously.", max_length=40
        ),
    ] = None
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
    reference: Annotated[
        str | None,
        Field(description="The reference of the transaction."),
    ] = None
    related_transaction_id: Annotated[
        UUID | None,
        Field(description="The ID of the original transaction that has been refunded."),
    ] = None
    legs: Annotated[
        list[ModelLeg],
        Field(
            description="The legs of a transaction. There are 2 legs between your Revolut accounts and 1 leg in other cases."
        ),
    ]

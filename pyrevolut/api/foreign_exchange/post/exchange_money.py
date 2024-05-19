from typing import Annotated
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator, ConfigDict
from pydantic_extra_types.currency_code import Currency

from pyrevolut.utils import DateTime
from pyrevolut.api.common import EnumTransactionType, EnumTransactionState


class ExchangeMoney:
    """
    Exchange money using one of these methods:

    Sell currency:
        You know the amount of currency to sell.
        For example, you want to exchange 135.5 USD to some EUR.
        Specify the amount in the from object.

    Buy currency:
        You know the amount of currency to buy.
        For example, you want to exchange some USD to 200 EUR.
        Specify the amount in the to object.
    """

    ROUTE = "/1.0/exchange"

    class Body(BaseModel):
        """
        The request body for the endpoint.
        """

        model_config = ConfigDict(
            populate_by_name=True,
            from_attributes=True,
        )

        class ModelFrom(BaseModel):
            """The details of the currency to exchange from."""

            account_id: Annotated[
                UUID, Field(description="The ID of the account to sell currency from.")
            ]
            currency: Annotated[
                Currency,
                Field(description="The currency to sell in ISO 4217 format."),
            ]
            amount: Annotated[
                Decimal | None,
                Field(
                    description="The amount of currency. Specify ONLY if you want to sell currency."
                ),
            ] = None

        class ModelTo(BaseModel):
            """The details of the currency to exchange to."""

            account_id: Annotated[
                UUID,
                Field(
                    description="The ID of the account to receive exchanged currency into."
                ),
            ]
            currency: Annotated[
                Currency,
                Field(description="The currency to buy in ISO 4217 format."),
            ]
            amount: Annotated[
                Decimal | None,
                Field(
                    description="The amount of currency. Specify ONLY if you want to buy currency."
                ),
            ] = None

        from_: Annotated[
            ModelFrom,
            Field(
                alias="from",
                description="The details of the currency to exchange from.",
            ),
        ]
        to: Annotated[
            ModelTo,
            Field(description="The details of the currency to exchange to."),
        ]
        reference: Annotated[
            str | None,
            Field(
                description="""
                The reference for the exchange transaction, provided by you. 
                It helps you to identify the transaction if you want to look it up later.
                """
            ),
        ] = None
        request_id: Annotated[
            str,
            Field(
                description="""
                The ID of the request, provided by you. 
                It helps you identify the transaction in your system.

                To ensure that an exchange transaction is not processed multiple 
                times if there are network or system errors, the same request_id 
                should be used for requests related to the same transaction.
                """,
                max_length=40,
            ),
        ]

        @model_validator(mode="after")
        def check_inputs(self) -> "ExchangeMoney.Body":
            """Check if the amount is specified in either the from or to object."""
            if self.from_.amount is None and self.to.amount is None:
                raise ValueError(
                    "Either the amount in the from or to object must be specified."
                )
            if self.from_.amount is not None and self.to.amount is not None:
                raise ValueError(
                    "Only the amount in either the from or to object must be specified."
                )
            return self

    class Response(BaseModel):
        """
        Response model for the endpoint.
        """

        id: Annotated[
            UUID | None, Field(description="The ID of the created transaction.")
        ] = None
        type: Annotated[
            EnumTransactionType,
            Field(
                description="The type of the transaction. For money exchange, it is 'exchange'."
            ),
        ] = EnumTransactionType.EXCHANGE
        reason_code: Annotated[
            str | None,
            Field(
                description="The reason code when the state parameter of the transaction is declined or failed."
            ),
        ] = None
        created_at: Annotated[
            DateTime,
            Field(
                description="The date and time the transaction was created in ISO 8601 format."
            ),
        ]
        completed_at: Annotated[
            DateTime | None,
            Field(
                description="The date and time the transaction was completed in ISO 8601 format."
            ),
        ] = None
        state: Annotated[
            EnumTransactionState | None,
            Field(
                description="""
                Indicates the transaction state. Possible values:

                    created:
                        The transaction has been created and is either processed asynchronously
                        or scheduled for a later time.
                    pending:
                        The transaction is pending until it's being processed.
                        If the transfer is made between Revolut accounts,
                        this state is skipped and the transaction is executed instantly.
                    completed:
                        The transaction was successful.
                    declined:
                        The transaction was unsuccessful. This can happen for a variety of reasons,
                        for example, insufficient account balance, wrong receiver information, etc.
                    failed:
                        The transaction was unsuccessful. This can happen for a variety of reasons,
                        for example, invalid API calls, blocked payments, etc.
                    reverted:
                        The transaction was reverted. This can happen for a variety of reasons,
                        for example, the receiver being inaccessible.
                """
            ),
        ] = None

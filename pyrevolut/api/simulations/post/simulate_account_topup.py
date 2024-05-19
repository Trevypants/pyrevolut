from typing import Annotated
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator
from pydantic_extra_types.currency_code import Currency

from pyrevolut.utils import DateTime
from pyrevolut.api.common import EnumTransactionState


class SimulateAccountTopup:
    """
    Simulate a top-up of your account in the Sandbox environment.

    This is useful during testing, when you run out of money in your test account
    and need to add more.
    """

    ROUTE = "/1.0/sandbox/topup"

    class Body(BaseModel):
        """
        The body of the request.
        """

        account_id: Annotated[
            UUID,
            Field(description="The ID of the account that you want to top up."),
        ]
        amount: Annotated[
            Decimal,
            Field(
                description="The amount with which you want to top up the account. Must be <= 10000",
                gt=0,
                le=10000,
            ),
        ]
        currency: Annotated[
            Currency,
            Field(
                description="The currency of the top-up amount. Must be a valid ISO 4217 currency code.",
            ),
        ]
        reference: Annotated[
            str | None,
            Field(
                description="""
                A short description for your top up.
                Default value: 'Test Top-up' if not provided.
                """,
            ),
        ] = None
        state: Annotated[
            EnumTransactionState | None,
            Field(
                description="""
                The state to which you want to set the top-up transaction. 
                
                If not provided, the default value is 'completed'.
                
                Possible values:

                    pending:
                        The transaction is pending until it's being processed.
                        If the transfer is made between Revolut accounts,
                        this state is skipped and the transaction is executed instantly.
                    completed:
                        The transaction was successful.
                    failed:
                        The transaction was unsuccessful. This can happen for a variety of reasons,
                        for example, invalid API calls, blocked payments, etc.
                    reverted:
                        The transaction was reverted. This can happen for a variety of reasons,
                        for example, the receiver being inaccessible.
                """
            ),
        ] = None

        @model_validator(mode="after")
        def check_inputs(self) -> "SimulateAccountTopup.Body":
            """
            Check that the input is correct.
            """

            if self.state is not None:
                assert self.state in [
                    EnumTransactionState.PENDING,
                    EnumTransactionState.COMPLETED,
                    EnumTransactionState.FAILED,
                    EnumTransactionState.REVERTED,
                ], (
                    f"Invalid state: {self.state}. "
                    f"Possible values: {EnumTransactionState.PENDING}, "
                    f"{EnumTransactionState.COMPLETED}, {EnumTransactionState.FAILED}, "
                    f"{EnumTransactionState.REVERTED}."
                )
            return self

    class Response(BaseModel):
        """
        The response model.
        """

        id: Annotated[
            UUID, Field(description="The ID of the account that was topped up.")
        ]
        state: Annotated[
            EnumTransactionState,
            Field(
                description="""
                The state of the top-up transaction. Possible values:

                pending:
                    The transaction is pending until it's being processed.
                    If the transfer is made between Revolut accounts,
                    this state is skipped and the transaction is executed instantly.
                completed:
                    The transaction was successful.
                failed:
                    The transaction was unsuccessful. This can happen for a variety of reasons,
                    for example, invalid API calls, blocked payments, etc.
                reverted:
                    The transaction was reverted. This can happen for a variety of reasons,
                    for example, the receiver being inaccessible.
                """
            ),
        ]
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

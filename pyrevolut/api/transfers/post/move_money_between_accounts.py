from typing import Annotated
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, Field
from pydantic_extra_types.currency_code import Currency

from pyrevolut.api.transfers.resources import ResourceTransfer


class MoveMoneyBetweenAccounts:
    """
    Move money between the Revolut accounts of the business in the same currency.

    The resulting transaction has the type transfer.
    """

    ROUTE = "/1.0/transfer"

    class Body(BaseModel):
        """
        The body of the request.
        """

        request_id: Annotated[
            str,
            Field(
                description="""
                The ID of the request, provided by you. 
                It helps you identify the transaction in your system.
                To ensure that a transfer is not processed multiple times if 
                there are network or system errors, the same request_id should be used 
                for requests related to the same transfer.
                """,
                max_length=40,
            ),
        ]
        source_account_id: Annotated[
            UUID,
            Field(
                description="The ID of the source account that you transfer the funds from."
            ),
        ]
        target_account_id: Annotated[
            UUID,
            Field(
                description="The ID of the target account that you transfer the funds to."
            ),
        ]
        amount: Annotated[
            Decimal,
            Field(
                description="The amount of the funds to be transferred.",
                gt=0,
            ),
        ]
        currency: Annotated[
            Currency,
            Field(description="The ISO 4217 currency of the funds to be transferred."),
        ]
        reference: Annotated[
            str | None,
            Field(
                description="""
                The reference for the funds transfer.
                """,
            ),
        ] = None

    class Response(ResourceTransfer):
        """
        The response model of the request.
        """

        pass

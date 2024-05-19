from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic_extra_types.currency_code import Currency

from pyrevolut.utils import Date


class CreatePaymentDraft:
    """
    Create a payment draft.
    """

    ROUTE = "/1.0/payment-drafts"

    class Body(BaseModel):
        """
        The body model for the endpoint.
        """

        class ModelPayment(BaseModel):
            """The details of a payment"""

            class ModelReceiver(BaseModel):
                """The details of the transfer recipient.

                If the counterparty has multiple payment methods available
                (e.g. 2 accounts, or 1 account and 1 card), you must specify the
                account (account_id) or card (card_id) to which you want to transfer the money.
                """

                counterparty_id: Annotated[
                    UUID,
                    Field(description="The ID of the receiving counterparty."),
                ]
                account_id: Annotated[
                    UUID | None,
                    Field(
                        description="""
                        The ID of the receiving counterparty's account, which can be own account. 
                        Used for bank transfers.

                        If the counterparty has multiple payment methods available, use it to 
                        specify the account to which you want to send the money.
                        """
                    ),
                ] = None
                card_id: Annotated[
                    UUID | None,
                    Field(
                        description="""
                        The ID of the receiving counterparty's card. Used for card transfers.

                        If the counterparty has multiple payment methods available, use it to 
                        specify the card to which you want to send the money.
                        """
                    ),
                ] = None

            account_id: Annotated[
                UUID,
                Field(
                    description="""
                    The ID of the account to pay from.
                    You can specify only one account ID for multiple payments in the same payment draft.
                    """
                ),
            ]
            receiver: Annotated[
                ModelReceiver,
                Field(
                    description="""
                    The details of the transfer recipient.

                    If the counterparty has multiple payment methods available 
                    (e.g. 2 accounts, or 1 account and 1 card), you must specify the 
                    account (account_id) or card (card_id) to which you want to transfer the money.
                    """
                ),
            ]
            amount: Annotated[
                float,
                Field(description="The amount of the payment."),
            ]
            currency: Annotated[
                Currency,
                Field(description="ISO 4217 currency code in upper case."),
            ]
            reference: Annotated[
                str,
                Field(description="The reference for the payment."),
            ]

        title: Annotated[
            str | None,
            Field(description="The title of the payment draft."),
        ] = None
        schedule_for: Annotated[
            Date | None,
            Field(
                description="The scheduled date of the payment draft in ISO 8601 format."
            ),
        ] = None
        payments: Annotated[
            list[ModelPayment],
            Field(description="The details of the payments."),
        ]

    class Response(BaseModel):
        """
        The response model for the endpoint.
        """

        id: Annotated[UUID, Field(description="The ID of the payment draft created.")]

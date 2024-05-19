from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic_extra_types.currency_code import Currency

from pyrevolut.api.common import EnumChargeBearer, EnumTransferReasonCode
from pyrevolut.api.transfers.resources import ResourceTransfer


class CreateTransferToAnotherAccount:
    """
    Make a payment to a counterparty.
    The resulting transaction has the type transfer.

    If you make the payment to another Revolut account, either business or personal,
    the transaction is executed instantly.

    If the counterparty has multiple payment methods available, for example, 2 accounts,
    or 1 account and 1 card, you must specify the account or card to which you want to
    transfer the money (receiver.account_id or receiver.card_id respectively).

    Caution
    -------
    Due to PSD2 Strong Customer Authentication regulations, this endpoint is
    only available for customers on Revolut Business Company plans. If you're a
    freelancer and wish to make payments via our API, we advise that you instead
    leverage our Payment drafts (/payment-drafts) endpoint.
    """

    ROUTE = "/1.0/pay"

    class Body(BaseModel):
        """
        The body of the request.
        """

        class ModelReceiver(BaseModel):
            """
            The details of the transfer recipient.

            If the counterparty has multiple payment methods available
            (e.g. 2 accounts, or 1 account and 1 card), you must specify the account
            (account_id) or card (card_id) to which you want to transfer the money.
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
                    """,
                ),
            ] = None
            card_id: Annotated[
                UUID | None,
                Field(
                    description="""
                    The ID of the receiving counterparty's card. Used for card transfers.

                    If the counterparty has multiple payment methods available, use it to 
                    specify the card to which you want to send the money.
                    """,
                ),
            ] = None

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
        account_id: Annotated[
            UUID,
            Field(description="The ID of the account that you send the funds from."),
        ]
        receiver: Annotated[
            ModelReceiver,
            Field(
                description="""
                The details of the transfer recipient.

                If the counterparty has multiple payment methods available
                (e.g. 2 accounts, or 1 account and 1 card), you must specify the account
                (account_id) or card (card_id) to which you want to transfer the money.
                """
            ),
        ]
        amount: Annotated[
            float,
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
                The reference for the transaction.
                """,
            ),
        ] = None
        charge_bearer: Annotated[
            EnumChargeBearer | None,
            Field(
                description="""
                The party to which any transaction fees are charged if the resulting 
                transaction route has associated fees. Some transactions with fees might 
                not be possible with the specified option, in which case error 3287 is returned.

                Possible values:
                - shared: The transaction fees are shared between the sender and the receiver.
                - debtor: The sender pays the transaction fees.
                """,
            ),
        ] = None
        transfer_reason_code: Annotated[
            EnumTransferReasonCode | None,
            Field(
                description="""
                The reason code for the transaction. 
                Transactions to certain countries and currencies might require 
                you to provide a transfer reason. 
                You can check available reason codes with the getTransferReasons operation.

                If a transfer reason is not required for the given currency and country, 
                this field is ignored.
                """,
            ),
        ] = None

    class Response(ResourceTransfer):
        """
        The response model of the request.
        """

        pass

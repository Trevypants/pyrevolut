from typing import Annotated
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, Field
from pydantic_extra_types.currency_code import Currency
from pydantic_extra_types.pendulum_dt import Duration

from pyrevolut.api.common import EnumTransferReasonCode, EnumPayoutLinkPaymentMethod
from pyrevolut.api.payout_links.resources import ResourcePayoutLink


class CreatePayoutLink:
    """
    Create a payout link to send money even when you don't have the full
    banking details of the counterparty.
    After you have created the link, send it to the recipient so that
    they can claim the payment.

    Note
    ----
    This feature is available in the UK and the EEA.
    """

    ROUTE = "/1.0/payout-links"

    class Body(BaseModel):
        """
        The request body model for the request.
        """

        counterparty_name: Annotated[
            str,
            Field(
                description="""
                The name of the counterparty provided by the sender.                
                """,
            ),
        ]
        save_counterparty: Annotated[
            bool | None,
            Field(
                description="""
                Indicates whether to save the recipient as your counterparty upon link claim. 
                If false then the counterparty will not show up on your counterparties list, 
                for example, when you retrieve your counterparties. 
                However, you will still be able to retrieve this counterparty by its ID.

                If you don't choose to save the counterparty on link creation, you can do it later 
                from your transactions list in the Business app.
                
                If not provided, the default value is false.
                """,
            ),
        ] = None
        request_id: Annotated[
            str,
            Field(
                description="""
                The ID of the request, provided by the sender.
                
                To ensure that a link payment is not processed multiple times if there
                are network or system errors, the same request_id should be used for 
                requests related to the same link.
                """,
                max_length=40,
            ),
        ]
        account_id: Annotated[
            UUID,
            Field(
                description="""
                The ID of the sender's account.
                """,
            ),
        ]
        amount: Annotated[
            Decimal,
            Field(
                description="""
                The amount of money to be transferred.
                The amount must be between £1 and £2,500, or equivalent in the selected currency.
                """,
            ),
        ]
        currency: Annotated[
            Currency,
            Field(
                description="""
                ISO 4217 currency code in upper case.
                """,
            ),
        ]
        reference: Annotated[
            str,
            Field(
                description="""
                The reference for the payout transaction, provided by the sender.
                """,
            ),
        ]
        payout_methods: Annotated[
            list[EnumPayoutLinkPaymentMethod],
            Field(
                description="""
                The list of payout methods that the recipient can use to claim the payout, where:

                    revolut:
                        Revolut peer-to-peer (P2P) transfer

                    bank_account:
                        External bank transfer

                    card:
                        Card transfer
                """
            ),
        ]
        expiry_period: Annotated[
            Duration | None,
            Field(
                description="""
                Possible values: >= P1D and <= P7D

                Default value: P7D

                The period after which the payout link expires if not claimed before, 
                provided in ISO 8601 format.

                The default and maximum value is 7 days from the link creation.
                """,
            ),
        ] = None
        transfer_reason_code: Annotated[
            EnumTransferReasonCode | None,
            Field(
                description="""
                The reason code for the transaction. 
                Transactions to certain countries and currencies might require you to 
                provide a transfer reason. 
                You can check available reason codes with the getTransferReasons operation.

                If a transfer reason is not required for the given currency and country, 
                this field is ignored.
                """
            ),
        ] = None

    class Response(ResourcePayoutLink):
        """
        The response model for the request.
        """

        pass

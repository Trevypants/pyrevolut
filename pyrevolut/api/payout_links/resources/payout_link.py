from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl
from pydantic_extra_types.currency_code import Currency

from pyrevolut.utils import DateTime
from pyrevolut.api.common import (
    EnumPayoutLinkState,
    EnumPayoutLinkPaymentMethod,
    EnumTransferReasonCode,
    EnumPayoutLinkCancellationReason,
)


class ResourcePayoutLink(BaseModel):
    """
    Payout Link resource model.
    """

    id: Annotated[UUID, Field(description="The ID of the payout link.")]
    state: Annotated[
        EnumPayoutLinkState,
        Field(
            description="""
            The state that the payout link is in. Possible states are:

                created:
                    The payout link has been created, but the amount has not yet been blocked.
                failed:
                    The payout link couldn't be generated due to a failure during transaction booking.
                awaiting:
                    The payout link is awaiting approval.
                active:
                    The payout link can be redeemed.
                expired:
                    The payout link cannot be redeemed because it wasn't claimed before its expiry date.
                cancelled:
                    The payout link cannot be redeemed because it was cancelled.
                processing:
                    The payout link has been redeemed and is being processed.
                processed:
                    The payout link has been redeemed and the money has been transferred to the recipient.
            """
        ),
    ]
    created_at: Annotated[
        DateTime,
        Field(
            description="The date and time the payout link was created in ISO 8601 format."
        ),
    ]
    updated_at: Annotated[
        DateTime,
        Field(
            description="The date and time the payout link was last updated in ISO 8601 format."
        ),
    ]
    counterparty_name: Annotated[
        str, Field(description="The name of the counterparty provided by the sender.")
    ]
    counterparty_id: Annotated[
        UUID | None,
        Field(
            description="""
            The ID of the counterparty created based on the recipient's details.
            
            By default, the newly created counterparty is hidden from your counterparties list.
            To automatically save it when the link is claimed, pass the save_counterparty parameter set to true.
            Alternatively, you can add the recipient to your counterparties later from the list of transactions 
            in the Business app.
            """
        ),
    ] = None
    save_counterparty: Annotated[
        bool,
        Field(
            description="""
            Indicates whether you chose to save the recipient as your counterparty upon link claim. 
            If false then the counterparty will not show up on your counterparties list, 
            for example, when you retrieve your counterparties. 
            However, you can still retrieve this counterparty by its ID.

            If you didn't choose to save the counterparty on link creation, you can still do it 
            from your transactions list in the Business app.
            """
        ),
    ]
    request_id: Annotated[
        str,
        Field(
            description="The ID of the request, provided by the sender.", max_length=40
        ),
    ]
    expiry_date: Annotated[
        DateTime,
        Field(description="The datetime the payout link expires in ISO 8601 format."),
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
    account_id: Annotated[UUID, Field(description="The ID of the sender's account.")]
    amount: Annotated[
        float,
        Field(
            description="""
            The amount of money to be transferred.
            The amount must be between £1 and £2,500, or equivalent in the selected currency.
            """
        ),
    ]
    currency: Annotated[
        Currency,
        Field(description="ISO 4217 currency code in upper case."),
    ]
    transaction_id: Annotated[
        UUID | None,
        Field(
            description="""
            The ID of the created transaction. Returned only if the payout has been claimed.
            """
        ),
    ] = None
    url: Annotated[
        HttpUrl | None,
        Field(
            description="The URL of the payout link. Returned only for active payout links."
        ),
    ] = None
    reference: Annotated[
        str,
        Field(
            description="The reference for the payout transaction, provided by the sender."
        ),
    ]
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
    cancellation_reason: Annotated[
        EnumPayoutLinkCancellationReason | None,
        Field(
            description="""
            The reason why the payout link was cancelled. Possible reasons are:

                too_many_name_check_attempts:
                    The name check failed too many times.
            """
        ),
    ] = None

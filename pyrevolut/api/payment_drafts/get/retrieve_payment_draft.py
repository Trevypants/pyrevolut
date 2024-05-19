from typing import Annotated
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict
from pydantic_extra_types.currency_code import Currency

from pyrevolut.api.common import ModelBaseAmount, EnumPaymentDraftState
from pyrevolut.utils import Date


class RetrievePaymentDraft:
    """
    Get the information about a specific payment draft by ID.
    """

    ROUTE = "/1.0/payment-drafts/{payment_draft_id}"

    class Params(BaseModel):
        """
        The parameters for the endpoint.
        """

        pass

    class Response(BaseModel):
        """
        The response model for the endpoint.
        """

        class ModelPayment(BaseModel):
            """A payment draft."""

            class ModelAmount(ModelBaseAmount):
                """The amount of the payment draft."""

                pass

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

            class ModelCurrentChargeOptions(BaseModel):
                """The explanation of conversion process"""

                model_config = ConfigDict(
                    populate_by_name=True,
                    from_attributes=True,
                )

                class ModelFrom(ModelBaseAmount):
                    """The source of the conversion"""

                    pass

                class ModelTo(ModelBaseAmount):
                    """The target of the conversion"""

                    pass

                class ModelFee(ModelBaseAmount):
                    """The fee of the conversion"""

                    pass

                from_: Annotated[
                    ModelFrom,
                    Field(alias="from", description="The source of the conversion."),
                ]
                to: Annotated[
                    ModelTo,
                    Field(description="The target of the conversion."),
                ]
                rate: Annotated[
                    Decimal | None,
                    Field(description="The exchange rate used for the conversion."),
                ] = None
                fee: Annotated[
                    ModelFee | None,
                    Field(description="The fee of the conversion."),
                ] = None

            id: Annotated[UUID, Field(description="The ID of the payment draft.")]
            amount: Annotated[
                ModelAmount,
                Field(description="The amount of the payment draft."),
            ]
            currency: Annotated[
                Currency | None,
                Field(description="The currency of the payment draft."),
            ] = None
            account_id: Annotated[
                UUID,
                Field(description="The ID of the account to pay from."),
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
            state: Annotated[
                EnumPaymentDraftState,
                Field(description="The state of the payment draft."),
            ]
            reason: Annotated[
                str | None,
                Field(description="The reason for the payment draft state."),
            ] = None
            error_message: Annotated[
                str | None,
                Field(description="The description of the error message."),
            ] = None
            current_charge_options: Annotated[
                ModelCurrentChargeOptions,
                Field(description="The explanation of conversion process."),
            ]
            reference: Annotated[
                str | None,
                Field(description="The description of the transaction."),
            ] = None

        scheduled_for: Annotated[
            Date | None,
            Field(
                description="The scheduled date of the payment draft in ISO 8601 format."
            ),
        ] = None
        title: Annotated[
            str | None,
            Field(description="The title of the payment draft."),
        ] = None
        payments: Annotated[
            list[ModelPayment],
            Field(description="The list of payment drafts."),
        ]

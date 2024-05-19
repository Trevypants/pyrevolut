from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from pyrevolut.utils import Date


class RetrieveAllPaymentDrafts:
    """
    Get a list of all the payment drafts that aren't processed.
    """

    ROUTE = "/1.0/payment-drafts"

    class Params(BaseModel):
        """
        The parameters for the endpoint.
        """

        pass

    class Response(BaseModel):
        """
        The response model for the endpoint.
        """

        class ModelPaymentOrder(BaseModel):
            """A payment draft."""

            id: Annotated[UUID, Field(description="The ID of the payment draft.")]
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
            payment_counts: Annotated[
                int,
                Field(description="The number of payments in the payment draft.", ge=0),
            ]

        payment_orders: Annotated[
            list[ModelPaymentOrder],
            Field(description="The list of payment drafts."),
        ]

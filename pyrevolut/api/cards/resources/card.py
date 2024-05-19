from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from pyrevolut.utils import DateTime, Date
from pyrevolut.api.common import ModelBaseAmount, EnumCardState, EnumMerchantCategory


class ResourceCard(BaseModel):
    """
    Card resource model
    """

    class ModelSpendingLimits(BaseModel):
        """All spending limits set for the card."""

        class ModelSingle(ModelBaseAmount):
            """The limit for a single transaction."""

            pass

        class ModelDay(ModelBaseAmount):
            """The daily limit for transactions."""

            pass

        class ModelWeek(ModelBaseAmount):
            """The weekly limit for transactions."""

            pass

        class ModelMonth(ModelBaseAmount):
            """The monthly limit for transactions."""

            pass

        class ModelQuarter(ModelBaseAmount):
            """The quarterly limit for transactions."""

            pass

        class ModelYear(ModelBaseAmount):
            """The yearly limit for transactions."""

            pass

        class ModelAllTime(ModelBaseAmount):
            """The all-time limit for transactions."""

            pass

        single: Annotated[
            ModelSingle | None,
            Field(description="The limit for a single transaction."),
        ]
        day: Annotated[
            ModelDay | None,
            Field(description="The daily limit for transactions."),
        ]
        week: Annotated[
            ModelWeek | None,
            Field(description="The weekly limit for transactions."),
        ]
        month: Annotated[
            ModelMonth | None,
            Field(description="The monthly limit for transactions."),
        ]
        quarter: Annotated[
            ModelQuarter | None,
            Field(description="The quarterly limit for transactions."),
        ]
        year: Annotated[
            ModelYear | None,
            Field(description="The yearly limit for transactions."),
        ]
        all_time: Annotated[
            ModelAllTime | None,
            Field(description="The all-time limit for transactions."),
        ]

    id: Annotated[
        UUID,
        Field(description="The ID of the card."),
    ]
    last_digits: Annotated[
        str,
        Field(description="The last 4 digits of the card's PAN."),
    ]
    expiry: Annotated[
        Date,
        Field(description="The card expiration date."),
    ]
    state: Annotated[
        EnumCardState,
        Field(description="The state that the card is in."),
    ]
    label: Annotated[
        str | None,
        Field(description="The label of the card."),
    ]
    virtual: Annotated[
        bool,
        Field(
            description="Specifies whether the card is virtual (true) or physical (false)."
        ),
    ]
    accounts: Annotated[
        list[UUID],
        Field(description="The list of linked accounts."),
    ]
    categories: Annotated[
        list[EnumMerchantCategory] | None,
        Field(
            description="""
            The list of merchant categories that are available for card spending. 
            If not specified, all categories will be allowed.  
            """
        ),
    ]
    spending_limits: Annotated[
        ModelSpendingLimits | None,
        Field(description="All spending limits set for the card."),
    ]
    holder_id: Annotated[
        UUID | None,
        Field(
            description="""
            The ID of the team member who is the holder of the card. 
            If the card belongs to the business, this will be empty.
            """
        ),
    ]
    created_at: Annotated[
        DateTime,
        Field(description="The date and time the card was created in ISO 8601 format."),
    ]
    updated_at: Annotated[
        DateTime,
        Field(
            description="The date and time the card was last updated in ISO 8601 format."
        ),
    ]

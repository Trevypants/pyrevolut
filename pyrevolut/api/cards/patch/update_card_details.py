from typing import Annotated, Literal

from pydantic import BaseModel, Field, model_validator

from pyrevolut.api.common import ModelBaseAmount, EnumMerchantCategory
from pyrevolut.api.cards.resources import ResourceCard


class UpdateCardDetails:
    """
    Update details of a specific card, based on its ID.
    Updating a spending limit does not reset the spending counter.
    """

    ROUTE = "/1.0/cards/{card_id}"

    class Body(BaseModel):
        """
        The body of the request.
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
                ModelSingle | Literal["null"] | None,
                Field(description="The limit for a single transaction."),
            ]
            day: Annotated[
                ModelDay | Literal["null"] | None,
                Field(description="The daily limit for transactions."),
            ]
            week: Annotated[
                ModelWeek | Literal["null"] | None,
                Field(description="The weekly limit for transactions."),
            ]
            month: Annotated[
                ModelMonth | Literal["null"] | None,
                Field(description="The monthly limit for transactions."),
            ]
            quarter: Annotated[
                ModelQuarter | Literal["null"] | None,
                Field(description="The quarterly limit for transactions."),
            ]
            year: Annotated[
                ModelYear | Literal["null"] | None,
                Field(description="The yearly limit for transactions."),
            ]
            all_time: Annotated[
                ModelAllTime | Literal["null"] | None,
                Field(description="The all-time limit for transactions."),
            ]

        label: Annotated[
            str | None,
            Field(description="The label of the card.", max_length=30),
        ] = None
        categories: Annotated[
            EnumMerchantCategory | Literal["null"] | None,
            Field(
                description="""
                List of merchant categories that will be available for card spending. 
                Use null to erase the value and reset to empty (all categories will be allowed).
                """
            ),
        ] = None
        spending_limits: Annotated[
            ModelSpendingLimits | Literal["null"] | None,
            Field(
                description="""
                All spending limits set for the card.

                You can have at most 1 periodic (day/week/month/quarter/all-time) and 1 non-periodic (single transaction) 
                limit at a time. If you try to specify 2 periodic limits at a time, it will result in an error.

                Spending limit currency must match the default business currency. 
                The default currency was assigned to your business during onboarding.

                Use null as the value for a specific limit to erase that limit. 
                Use null as the value for the spending_limits object to erase all limits.
                """
            ),
        ] = None

        @model_validator(mode="after")
        def check_inputs(self) -> "UpdateCardDetails.Body":
            """Check the inputs."""
            if self.spending_limits is not None and self.spending_limits != "null":
                if (
                    sum(
                        [
                            self.spending_limits.day is not None
                            and self.spending_limits.day != "null",
                            self.spending_limits.week is not None
                            and self.spending_limits.week != "null",
                            self.spending_limits.month is not None
                            and self.spending_limits.month != "null",
                            self.spending_limits.quarter is not None
                            and self.spending_limits.quarter != "null",
                            self.spending_limits.year is not None
                            and self.spending_limits.year != "null",
                            self.spending_limits.all_time is not None
                            and self.spending_limits.all_time != "null",
                        ]
                    )
                    > 1
                ):
                    raise ValueError(
                        "You can have at most 1 periodic (day/week/month/quarter/all-time) limit at a time."
                    )
            return self

    class Response(ResourceCard):
        """
        Response model for the endpoint.
        """

        pass

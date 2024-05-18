from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from pyrevolut.api.common import ModelBaseAmount, EnumMerchantCategory
from pyrevolut.api.cards.resources import ResourceCard


class CreateCard:
    """
    Create a new card for an existing member of your Revolut Business team.

    When using the API, you can create only virtual cards.
    To create a physical card, use the Revolut Business app.
    """

    ROUTE = "/1.0/cards"

    class Body(BaseModel):
        """
        Body model for the endpoint.
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

        request_id: Annotated[
            str,
            Field(
                description="""
                A unique ID of the request that you provide.
                This ID is used to prevent duplicate card creation requests in case 
                of a lost connection or client error, so make sure you use the same 
                request_id for requests related to the same card.
                The deduplication is limited to 24 hours counting from the first request 
                using a given ID. 
                """,
                max_length=40,
            ),
        ]
        virtual: Annotated[
            bool,
            Field(
                description="""
                Specifies the type of the card. Must be set to true, as with the API, you can create only virtual cards.
                """,
            ),
        ] = True
        holder_id: Annotated[
            UUID,
            Field(
                description="""
                The ID of the team member who will be the holder of the card.
                """
            ),
        ]
        label: Annotated[
            str | None,
            Field(
                description="""
                The label for the issued card, displayed in the UI to help distinguish between cards. 
                If not specified, no label will be added.
                """,
                max_length=30,
            ),
        ] = None
        accounts: Annotated[
            list[UUID] | None,
            Field(
                description="""
                The list of accounts to link to the card. If not specified, all accounts will be linked.
                """,
            ),
        ] = None
        categories: Annotated[
            list[EnumMerchantCategory] | None,
            Field(
                description="""
                The list of merchant categories to be available for card spending. 
                If not specified, all categories will be allowed.
                """,
            ),
        ] = None
        spending_limits: Annotated[
            ModelSpendingLimits | None,
            Field(
                description="""
                All spending limits set for the card.
                You can have at most 1 periodic (day/week/month/quarter/all-time) and 
                1 non-periodic (single transaction) limit at a time. 
                If you try to specify 2 periodic limits at a time, it will result in an error.

                Spending limit currency must match the default business currency. 
                The default currency was assigned to your business during onboarding.
                """,
            ),
        ] = None

        @model_validator(mode="after")
        def check_inputs(self) -> "CreateCard.Body":
            """Check the inputs."""
            if not self.virtual:
                raise ValueError("You can only create virtual cards via the API.")
            if self.spending_limits is not None:
                if (
                    sum(
                        [
                            self.spending_limits.day is not None,
                            self.spending_limits.week is not None,
                            self.spending_limits.month is not None,
                            self.spending_limits.quarter is not None,
                            self.spending_limits.year is not None,
                            self.spending_limits.all_time is not None,
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

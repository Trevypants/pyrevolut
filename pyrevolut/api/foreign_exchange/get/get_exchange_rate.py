from typing import Annotated
from decimal import Decimal

from pydantic import BaseModel, Field
from pydantic_extra_types.currency_code import Currency

from pyrevolut.api.foreign_exchange.resources import ResourceForeignExchange


class GetExchangeRate:
    """
    Get the sell exchange rate between two currencies.
    """

    ROUTE = "/rate"

    class Params(BaseModel):
        """
        Query parameters for the endpoint.
        """

        from_: Annotated[
            Currency,
            Field(
                alias="from", description="The currency that you exchange from in ISO 4217 format."
            ),
        ]
        to: Annotated[
            Currency,
            Field(description="The currency that you exchange to in ISO 4217 format."),
        ]
        amount: Annotated[
            Decimal | None,
            Field(
                description="The amount of the currency to exchange from. The default value is 1.00."
            ),
        ] = None

    class Response(ResourceForeignExchange):
        """
        Response model for the endpoint.
        """

        pass

from typing import Annotated

from pydantic import BaseModel, Field
from pydantic_extra_types.country import CountryAlpha2
from pydantic_extra_types.currency_code import Currency

from pyrevolut.api.common import EnumTransferReasonCode


class GetTransferReasons:
    """
    In order to initiate a transfer in certain currencies and countries,
    you must provide a transfer reason.
    With this endpoint you can retrieve all transfer reasons available to your business account
    per country and currency.

    After you retrieve the results, use the appropriate reason code in the transfer_reason_code
    field when making a transfer to a counterparty or creating a payout link.
    """

    ROUTE = "/1.0/transfer-reasons"

    class Params(BaseModel):
        """
        The query parameters for the request.
        """

        pass

    class Response(BaseModel):
        """
        The response model for the request.
        """

        country: Annotated[
            CountryAlpha2,
            Field(
                description="""
                The bank country of the counterparty as the 2-letter ISO 3166 code.
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
        code: Annotated[
            EnumTransferReasonCode,
            Field(
                description="""
                Category name of the transfer reason.
                """,
            ),
        ]
        description: Annotated[
            str,
            Field(
                description="""
                The description of the given transfer reason.
                """,
            ),
        ]

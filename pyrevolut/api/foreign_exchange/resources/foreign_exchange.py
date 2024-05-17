from typing import Annotated
from decimal import Decimal

from pydantic import BaseModel, Field

from pyrevolut.utils import DateTime
from pyrevolut.api.common import ModelBaseAmount


class ResourceForeignExchange(BaseModel):
    """
    Foreign Exchange resource model.
    """

    class ModelFrom(ModelBaseAmount):
        """
        The money to sell.
        """

        pass

    class ModelTo(ModelBaseAmount):
        """
        The money to receive.
        """

        pass

    class ModelFee(ModelBaseAmount):
        """
        The expected fee for the transaction.
        """

        pass

    from_: Annotated[ModelFrom, Field(alias="from", description="The money to sell.")]
    to: Annotated[ModelTo, Field(description="The money to receive.")]
    rate: Annotated[Decimal, Field(description="The proposed exchange rate.")]
    fee: Annotated[ModelFee, Field(description="The expected fee for the transaction.")]
    rate_date: Annotated[
        DateTime, Field(description="The date of the proposed exchange rate in ISO 8601 format.")
    ]

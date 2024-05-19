from typing import Annotated

from pydantic import BaseModel, Field
from pydantic_extra_types.currency_code import Currency


class ModelBaseAmount(BaseModel):
    """Base model for amount"""

    amount: Annotated[float, Field(description="The value.")]
    currency: Annotated[
        Currency,
        Field(description="The currency, provided as a 3-letter ISO 4217 code."),
    ]

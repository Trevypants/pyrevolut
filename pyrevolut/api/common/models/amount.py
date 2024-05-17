from typing import Annotated
from decimal import Decimal

from pydantic import BaseModel
from pydantic_extra_types.currency_code import Currency


class ModelBaseAmount(BaseModel):
    """Base model for amount"""

    amount: Annotated[Decimal, "The value."]
    currency: Annotated[Currency, "The currency, provided as a 3-letter ISO 4217 code."]

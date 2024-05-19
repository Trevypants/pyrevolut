from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic_extra_types.currency_code import Currency

from pyrevolut.utils import DateTime
from pyrevolut.api.common import EnumAccountState


class ResourceAccount(BaseModel):
    """
    Account resource model.
    """

    id: Annotated[
        UUID,
        Field(description="The account ID."),
    ]
    name: Annotated[
        str | None,
        Field(description="The account name."),
    ] = None
    balance: Annotated[
        float,
        Field(description="The current balance on the account."),
    ]
    currency: Annotated[
        Currency,
        Field(description="ISO 4217 currency code in upper case."),
    ]
    state: Annotated[
        EnumAccountState,
        Field(description="Indicates the state of the account."),
    ]
    public: Annotated[
        bool,
        Field(
            description="Indicates whether the account is visible to other businesses on Revolut."
        ),
    ]
    created_at: Annotated[
        DateTime,
        Field(
            description="The date and time the account was created in ISO 8601 format."
        ),
    ]
    updated_at: Annotated[
        DateTime,
        Field(
            description="The date and time the account was last updated in ISO 8601 format."
        ),
    ]

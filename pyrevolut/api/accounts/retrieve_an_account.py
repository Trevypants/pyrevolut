from typing import Annotated
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, Field
from pydantic_extra_types.currency_code import Currency

from pyrevolut.utils import DateTime
from .enums import EnumAccountState


class RetrieveAnAccount:
    """
    Get the information about one of your accounts. Specify the account by its ID.
    """

    ROUTE = "/accounts/{account_id}"

    class Params(BaseModel):
        """
        Query parameters for the endpoint.
        """

        pass

    class Response(BaseModel):
        """
        Response model for the endpoint.
        """

        id: Annotated[
            UUID,
            Field(description="The account ID."),
        ]
        name: Annotated[
            str,
            Field(description="The account name."),
        ]
        balance: Annotated[
            Decimal,
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
            Field(description="The date and time the account was created in ISO 8601 format."),
        ]
        updated_at: Annotated[
            DateTime,
            Field(description="The date and time the account was last updated in ISO 8601 format."),
        ]

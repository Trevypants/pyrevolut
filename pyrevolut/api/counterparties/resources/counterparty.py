from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic_extra_types.currency_code import Currency
from pydantic_extra_types.country import CountryAlpha2

from pyrevolut.utils import DateTime
from pyrevolut.api.common import (
    EnumProfileType,
    EnumProfileState,
    EnumAccountType,
    EnumRecipientCharges,
    EnumCardScheme,
)


class ResourceCounterparty(BaseModel):
    """
    Counterparty resource model.
    """

    class ModelAccount(BaseModel):
        """A public account associated with this counterparty."""

        id: Annotated[
            UUID,
            Field(description="The ID of the counterparty's account."),
        ]
        name: Annotated[
            str | None,
            Field(description="The name of the counterparty."),
        ] = None
        bank_country: Annotated[
            CountryAlpha2 | None,
            Field(description="The country of the bank as the 2-letter ISO 3166 code."),
        ]
        currency: Annotated[
            Currency,
            Field(description="ISO 4217 currency code in upper case."),
        ]
        type: Annotated[
            EnumAccountType,
            Field(description="Indicates the type of account."),
        ]
        account_no: Annotated[
            str | None,
            Field(description="The bank account number of the counterparty."),
        ] = None
        iban: Annotated[
            str | None,
            Field(
                description="The IBAN number of the counterparty's account if applicable."
            ),
        ] = None
        sort_code: Annotated[
            str | None,
            Field(
                description="The sort code of the counterparty's account if applicable."
            ),
        ] = None
        routing_number: Annotated[
            str | None,
            Field(
                description="The routing number of the counterparty's account if applicable."
            ),
        ] = None
        bic: Annotated[
            str | None,
            Field(
                description="The BIC number of the counterparty's account if applicable."
            ),
        ] = None
        clabe: Annotated[
            str | None,
            Field(
                description="The CLABE number of the counterparty's account if applicable."
            ),
        ] = None
        ifsc: Annotated[
            str | None,
            Field(
                description="The IFSC number of the counterparty's account if applicable."
            ),
        ] = None
        bsb_code: Annotated[
            str | None,
            Field(
                description="The BSB code of the counterparty's account if applicable."
            ),
        ] = None
        recipient_charges: Annotated[
            EnumRecipientCharges | None,
            Field(description="Indicates the possibility of the recipient charges."),
        ] = None

    class ModelCard(BaseModel):
        """The list of cards associated with this counterparty."""

        id: Annotated[
            UUID,
            Field(description="The ID of the counterparty's card."),
        ]
        name: Annotated[
            str,
            Field(description="The name of the counterparty."),
        ]
        last_digits: Annotated[
            str,
            Field(description="The last four digits of the card number."),
        ]
        scheme: Annotated[
            EnumCardScheme,
            Field(description="The card brand."),
        ]
        country: Annotated[
            CountryAlpha2,
            Field(
                description="The country of the card issuer as the 2-letter ISO 3166 code."
            ),
        ]
        currency: Annotated[
            Currency,
            Field(description="ISO 4217 currency code in upper case."),
        ]

    id: Annotated[
        UUID,
        Field(description="The ID of the counterparty."),
    ]
    name: Annotated[
        str,
        Field(description="The name of the counterparty."),
    ]
    revtag: Annotated[
        str | None,
        Field(description="The Revtag of the counterparty."),
    ] = None
    profile_type: Annotated[
        EnumProfileType | None,
        Field(
            description="The type of the Revolut profile. Used when adding an existing Revolut user via Revtag."
        ),
    ] = None
    country: Annotated[
        CountryAlpha2 | None,
        Field(
            description="The bank country of the counterparty as the 2-letter ISO 3166 code."
        ),
    ] = None
    state: Annotated[
        EnumProfileState,
        Field(description="Indicates the state of the counterparty."),
    ]
    created_at: Annotated[
        DateTime,
        Field(
            description="The date and time the counterparty was created in ISO 8601 format."
        ),
    ]
    updated_at: Annotated[
        DateTime,
        Field(
            description="The date and time the counterparty was last updated in ISO 8601 format."
        ),
    ]
    accounts: Annotated[
        list[ModelAccount] | None,
        Field(
            description="The list of public accounts associated with this counterparty."
        ),
    ] = None
    cards: Annotated[
        list[ModelCard] | None,
        Field(description="The list of cards associated with this counterparty."),
    ] = None

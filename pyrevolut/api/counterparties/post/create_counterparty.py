from typing import Annotated

from pydantic import BaseModel, Field, model_validator
from pydantic_extra_types.country import CountryAlpha2
from pydantic_extra_types.currency_code import Currency

from pyrevolut.api.common import EnumProfileType
from pyrevolut.api.counterparties.resources import ResourceCounterparty


class CreateCounterparty:
    """
    Create a new counterparty to transact with.

    In the Sandbox environment, you cannot add real people and businesses as Revolut counterparties. To help you simulate Create a counterparty requests for counterparties of profile type personal, we created some test accounts. Look inside for test Revtags.

    To add a counterparty via Revtag, use one of these pairs for the name and revtag fields respectively:

        Test User 1 & john1pvki
        Test User 2 & john2pvki
        ...
        Test User 9 & john9pvki
    """

    ROUTE = "/1.0/counterparty"

    class Body(BaseModel):
        """Request body for the endpoint."""

        class ModelIndividualName(BaseModel):
            """
            The name of the individual counterparty.
            Use when company_name isn't specified.
            """

            first_name: Annotated[
                str | None,
                Field(description="The first name of the individual counterparty."),
            ] = None
            last_name: Annotated[
                str | None,
                Field(description="The last name of the individual counterparty."),
            ] = None

        class ModelAddress(BaseModel):
            """
            The address of the counterparty.
            """

            street_line1: Annotated[
                str | None,
                Field(description="Street line 1 information."),
            ] = None
            street_line2: Annotated[
                str | None,
                Field(description="Street line 2 information."),
            ] = None
            region: Annotated[
                str | None,
                Field(description="The name of the region."),
            ] = None
            city: Annotated[
                str | None,
                Field(description="The name of the city."),
            ] = None
            country: Annotated[
                CountryAlpha2,
                Field(
                    description="The country of the counterparty as the 2-letter ISO 3166 code."
                ),
            ]
            postcode: Annotated[
                str,
                Field(description="The postcode of the counterparty address."),
            ]

        company_name: Annotated[
            str | None,
            Field(
                description="""
                The name of the company counterparty. 
                Use when individual_name or name isn't specified and profile_type is business.
                """
            ),
        ] = None
        profile_type: Annotated[
            EnumProfileType | None,
            Field(
                description="""
                The type of the Revolut profile. Used when adding an existing Revolut user via Revtag.
                """
            ),
        ] = None
        name: Annotated[
            str | None,
            Field(
                description="""
                The name of the counterparty that you create for an existing Revolut user via Revtag. 
                Provide the value only when you specify personal for profile_type.                
                """
            ),
        ] = None
        individual_name: Annotated[
            ModelIndividualName | None,
            Field(
                description="""
                The name of the individual counterparty. 
                Use when company_name isn't specified.
                """
            ),
        ] = None
        bank_country: Annotated[
            CountryAlpha2 | None,
            Field(description="The country of the bank as the 2-letter ISO 3166 code."),
        ] = None
        currency: Annotated[
            Currency | None,
            Field(description="ISO 4217 currency code in upper case."),
        ] = None
        revtag: Annotated[
            str | None,
            Field(
                description="""
                The Revtag of the counterparty to add.                
                """
            ),
        ] = None
        account_no: Annotated[
            str | None,
            Field(
                description="""
                The bank account number of the counterparty.               
                """
            ),
        ] = None
        iban: Annotated[
            str | None,
            Field(
                description="""
                The IBAN number of the counterparty's account. This field is displayed for IBAN countries.               
                """
            ),
        ] = None
        sort_code: Annotated[
            str | None,
            Field(
                description="""
                The sort code of the counterparty's account. This field is required for GBP accounts.           
                """
            ),
        ] = None
        routing_number: Annotated[
            str | None,
            Field(
                description="""
                The routing number of the counterparty's account. This field is required for USD accounts.               
                """
            ),
        ] = None
        bic: Annotated[
            str | None,
            Field(
                description="""
                The BIC number of the counterparty's account. This field is required for non-SEPA IBAN/SWIFT.             
                """
            ),
        ] = None
        clabe: Annotated[
            str | None,
            Field(
                description="""
                The CLABE number of the counterparty's account. This field is required for SWIFT MX.               
                """
            ),
        ] = None
        isfc: Annotated[
            str | None,
            Field(
                description="""
                The ISFC number of the counterparty's account. This field is required for INR accounts.               
                """
            ),
        ] = None
        bsb_code: Annotated[
            str | None,
            Field(
                description="""
                The BSB code of the counterparty's account. This field is required for AUD accounts.               
                """
            ),
        ] = None
        address: Annotated[
            ModelAddress | None,
            Field(description="The address of the counterparty."),
        ] = None

        @model_validator(mode="after")
        def check_inputs(self) -> "CreateCounterparty.Body":
            """Validate the input data."""

            # Company name check
            if self.profile_type == EnumProfileType.BUSINESS and (
                self.individual_name is None or self.name is None
            ):
                assert (
                    self.company_name is not None
                ), "company_name is required for business profile type."

            # Name check
            if self.profile_type == EnumProfileType.PERSONAL:
                assert (
                    self.name is not None
                ), "name is required for personal profile type."

            # Profile type check
            if self.profile_type is not None:
                assert (
                    self.revtag is not None
                ), "revtag is required when profile_type is specified."
            else:
                assert (
                    self.revtag is None
                ), "revtag is not required when profile_type is not specified."

            # Individual name check
            # if self.company_name is None:
            #     assert (
            #         self.individual_name is not None
            #     ), "individual_name is required when company_name is not specified."

            # Sort code check
            if self.currency == "GBP":
                assert (
                    self.sort_code is not None
                ), "sort_code is required for GBP accounts."

            # Routing number check
            if self.currency == "USD":
                assert (
                    self.routing_number is not None
                ), "routing_number is required for USD accounts."

            # IFSC check
            if self.currency == "INR":
                assert self.isfc is not None, "isfc is required for INR accounts."

            # BSB code check
            if self.currency == "AUD":
                assert (
                    self.bsb_code is not None
                ), "bsb_code is required for AUD accounts."

            return self

    class Response(ResourceCounterparty):
        """Response model for the endpoint."""

        pass

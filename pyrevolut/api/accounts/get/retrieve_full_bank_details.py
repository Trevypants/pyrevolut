from typing import Annotated

from pydantic import BaseModel, Field
from pydantic_extra_types.country import CountryAlpha2

from pyrevolut.api.common import EnumPaymentScheme, EnumTimeUnit


class RetrieveFullBankDetails:
    """
    Get all the bank details of one of your accounts. Specify the account by its ID.
    """

    ROUTE = "/1.0/accounts/{account_id}/bank-details"

    class Params(BaseModel):
        """
        Query parameters for the endpoint.
        """

        pass

    class Response(BaseModel):
        """
        Response model for the endpoint.
        """

        class ModelBeneficiaryAddress(BaseModel):
            """The address of the beneficiary."""

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

        class ModelEstimatedTime(BaseModel):
            """The estimated time of the inboud transfer of the funds,
            i.e. when we expect the recipient to receive the transfer.
            """

            unit: Annotated[
                EnumTimeUnit,
                Field(
                    description="The estimated time unit of the inbound transfer of the funds."
                ),
            ]
            min: Annotated[
                int | None,
                Field(description="The minimum time estimate.", ge=0),
            ] = None
            max: Annotated[
                int | None,
                Field(description="The maximum time estimate.", ge=0),
            ] = None

        iban: Annotated[
            str | None,
            Field(description="The IBAN number."),
        ] = None
        bic: Annotated[
            str | None,
            Field(description="The BIC number, also known as SWIFT code."),
        ] = None
        account_no: Annotated[
            str | None,
            Field(description="The account number."),
        ] = None
        sort_code: Annotated[
            str | None,
            Field(description="The sort code of the account."),
        ] = None
        routing_number: Annotated[
            str | None,
            Field(description="The routing number of the account."),
        ] = None
        beneficiary: Annotated[
            str,
            Field(description="The name of the counterparty."),
        ]
        beneficiary_address: Annotated[
            ModelBeneficiaryAddress,
            Field(description="The address of the counterparty."),
        ]
        bank_country: Annotated[
            CountryAlpha2 | None,
            Field(description="The country of the bank as the 2-letter ISO 3166 code."),
        ] = None
        pooled: Annotated[
            bool | None,
            Field(
                description="Indicates whether the account address is pooled or unique."
            ),
        ] = None
        unique_reference: Annotated[
            str | None,
            Field(description="The reference of the pooled account."),
        ] = None
        schemes: Annotated[
            list[EnumPaymentScheme],
            Field(
                description="The schemes that are available for this currency account."
            ),
        ]
        estimated_time: Annotated[
            ModelEstimatedTime,
            Field(
                description="""
                The estimated time of the inboud transfer of the funds, 
                i.e. when we expect the recipient to receive the transfer.
                """
            ),
        ]

from typing import Annotated

from pydantic import BaseModel, Field, model_validator

from pyrevolut.utils import DateTime
from pyrevolut.api.counterparties.resources import ResourceCounterparty


class RetrieveListOfCounterparties:
    """
    Get all the counterparties that you have created, or use the query parameters to filter the results.

    The counterparties are sorted by the created_at date in reverse chronological order.

    The returned counterparties are paginated. The maximum number of counterparties returned per page
    is specified by the limit parameter. To get to the next page, make a new request and use the
    created_at date of the last counterparty returned in the previous response.
    """

    ROUTE = "/1.0/counterparties"

    class Params(BaseModel):
        """
        Query parameters for the endpoint.
        """

        name: Annotated[
            str | None,
            Field(
                description="""
                The name of the counterparty to retrieve. It does not need to be an exact match, 
                partial match is also supported.
                """
            ),
        ] = None
        account_no: Annotated[
            str | None,
            Field(
                description="""
                The exact account number of the counterparty to retrieve.
                """
            ),
        ] = None
        sort_code: Annotated[
            str | None,
            Field(
                description="""
                The exact sort code of the counterparty to retrieve.
                Only allowed in combination with the account_no parameter.                
                """
            ),
        ] = None
        iban: Annotated[
            str | None,
            Field(
                description="""
                The exact IBAN of the counterparty to retrieve.
                """
            ),
        ] = None
        bic: Annotated[
            str | None,
            Field(
                description="""
                The exact BIC of the counterparty to retrieve. Only allowed in combination with the iban parameter.
                """
            ),
        ] = None
        created_before: Annotated[
            DateTime | None,
            Field(
                description="""
                Retrieves counterparties with created_at < created_before. 
                The default value is the current date and time at which you are calling the endpoint.
                Provided in ISO 8601 format.
                """
            ),
        ] = None
        limit: Annotated[
            int | None,
            Field(
                description="""
                The maximum number of counterparties returned per page.
                To get to the next page, make a new request and use the 
                created_at date of the last card returned in the previous 
                response as the value for created_before.              
                
                If not provided, the default value is 100.  
                """,
                ge=1,
                le=100,
            ),
        ] = None

        @model_validator(mode="after")
        def check_inputs(self) -> "RetrieveListOfCounterparties.Params":
            """
            Validate the input parameters.
            """
            if self.sort_code and not self.account_no:
                raise ValueError(
                    "The sort_code parameter is only allowed in combination with the account_no parameter."
                )
            if self.bic and not self.iban:
                raise ValueError(
                    "The bic parameter is only allowed in combination with the iban parameter."
                )
            return self

    class Response(ResourceCounterparty):
        """
        Response model for the endpoint.
        """

        pass

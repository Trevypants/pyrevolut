from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from pyrevolut.utils import DateTime, Date
from pyrevolut.api.common import EnumTransactionType
from pyrevolut.api.transactions.resources import ResourceTransaction


class RetrieveListOfTransactions:
    """
    Retrieve the historical transactions based on the provided query criteria.

    The transactions are sorted by the created_at date in reverse chronological order,
    and they're paginated. The maximum number of transactions returned per page is specified by the
    count parameter. To get the next page of results, make a new request and use the created_at date
    from the last item of the previous page as the value for the to parameter.

    Note
    ----
    The API returns a maximum of 1,000 transactions per request.

    Note
    ----
    To be compliant with PSD2 SCA regulations, businesses on the Revolut Business Freelancer
    plans can only access information older than 90 days within 5 minutes of the first authorisation.
    """

    ROUTE = "/1.0/transactions"

    class Params(BaseModel):
        """
        The query parameters for the request.
        """

        model_config = ConfigDict(
            populate_by_name=True,
            from_attributes=True,
        )

        from_: Annotated[
            DateTime | Date | None,
            Field(
                description="""
                The date and time you retrieve the historical transactions from, including 
                this date-time. 
                Corresponds to the created_at value of the transaction. 
                Provided in ISO 8601 format.

                Used also for pagination. To get back to the previous page of results, 
                make a new request and use the created_at date from the first item of the 
                current page as the value for the from parameter.
                """
            ),
        ] = None
        to: Annotated[
            DateTime | Date | None,
            Field(
                description="""
                The date and time you retrieve the historical transactions to, excluding 
                this date-time. 
                Corresponds to the created_at value of the transaction. 
                Provided in ISO 8601 format. 
                The default value is the date and time at which you're calling the endpoint.

                Used also for pagination. 
                To get the next page of results, make a new request and use the created_at 
                date from the last item of the previous (current) page as the value for the 
                to parameter.  
                """
            ),
        ] = None
        account: Annotated[
            UUID | None,
            Field(
                description="""
                The ID of the account
                """
            ),
        ] = None
        count: Annotated[
            int | None,
            Field(
                description="""
                The maximum number of the historical transactions to retrieve per page.

                To get the next page of results, make a new request and use 
                the created_at date from the last item of the previous page as the 
                value for the to parameter.   
                
                If not provided, the default value is 100.             
                """,
                le=1000,
                ge=1,
            ),
        ] = None
        type: Annotated[
            EnumTransactionType | None,
            Field(
                description="""
                The type of the historical transactions to retrieve.
                """
            ),
        ] = None

    class Response(ResourceTransaction):
        """
        The response model for the request.
        """

        pass

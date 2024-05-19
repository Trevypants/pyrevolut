from uuid import UUID
from datetime import datetime

from pyrevolut.utils import DateTime
from pyrevolut.api.common import (
    BaseEndpointAsync,
    EnumTransactionType,
)

from pyrevolut.api.transactions.get import (
    RetrieveListOfTransactions,
    RetrieveTransaction,
)


class EndpointTransactionsAsync(BaseEndpointAsync):
    """The async Transactions API

    Get the details of your transactions.

    Note
    ----
    An incoming or outgoing payment is represented as a transaction.
    """

    async def get_all_transactions(
        self,
        from_datetime: datetime | DateTime | str | int | float | None = None,
        to_datetime: datetime | DateTime | str | int | float | None = None,
        account_id: UUID | None = None,
        limit: int | None = None,
        transaction_type: EnumTransactionType | None = None,
        **kwargs,
    ) -> list[dict] | list[RetrieveListOfTransactions.Response]:
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

        Parameters
        ----------
        from_datetime : datetime | DateTime | str | int | float, optional
            The date and time you retrieve the historical transactions from, including
            this date-time.
            Corresponds to the created_at value of the transaction.
            Provided in ISO 8601 format.

            Used also for pagination. To get back to the previous page of results,
            make a new request and use the created_at date from the first item of the
            current page as the value for the from parameter.
        to_datetime : datetime | DateTime | str | int | float, optional
            The date and time you retrieve the historical transactions to, excluding
            this date-time.
            Corresponds to the created_at value of the transaction.
            Provided in ISO 8601 format.
            The default value is the date and time at which you're calling the endpoint.

            Used also for pagination.
            To get the next page of results, make a new request and use the created_at
            date from the last item of the previous (current) page as the value for the
            to parameter.
        account_id : UUID, optional
            The ID of the account for which you want to retrieve the transactions.
        limit : int, optional
            The maximum number of transactions returned per page.
            To get the next page of results, make a new request and use the created_at
            date from the last item of the previous page as the value for the to parameter.
        transaction_type : EnumTransactionType, optional
            The type of the transaction.

        Returns
        -------
        list[dict] | list[RetrieveListOfTransactions.Response]
            A list of transactions.
        """
        endpoint = RetrieveListOfTransactions
        path = endpoint.ROUTE
        params = endpoint.Params(
            from_=from_datetime,
            to=to_datetime,
            account=account_id,
            count=limit,
            type=transaction_type,
        )

        return await self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    async def get_transaction(
        self,
        transaction_id: UUID | None = None,
        request_id: str | None = None,
        **kwargs,
    ) -> dict | RetrieveTransaction.Response:
        """
        Retrieve the details of a specific transaction.
        The details can include, for example, cardholder details for card payments.

        You can retrieve a transaction with its details either by its transaction ID
        or by the request ID that was provided for this transaction at the time of its
        creation, for example, when you created a payment.

        To retrieve a transaction by its transaction ID, use:

            /transaction/{transaction_id}

        To retrieve a transaction by a request ID provided at transaction creation, use:

            /transaction/{request_id}?id_type=request_id

        Parameters
        ----------
        transaction_id : UUID, optional
            The ID of the transaction.
            Specify either transaction_id or request_id.
        request_id : str, optional
            The request ID of the transaction.
            Specify either transaction_id or request_id.

        Returns
        -------
        dict | RetrieveTransaction.Response
            The details of the transaction.
        """
        assert (
            transaction_id or request_id
        ), "Either transaction_id or request_id must be provided."
        assert not (
            transaction_id and request_id
        ), "Either transaction_id or request_id must be provided, not both."

        endpoint = RetrieveTransaction
        path = endpoint.ROUTE.format(id=transaction_id or request_id)
        params = endpoint.Params(id_type="request_id" if request_id else None)

        return await self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

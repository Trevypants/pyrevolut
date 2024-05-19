from uuid import UUID
from decimal import Decimal

from pyrevolut.api.common import BaseEndpointSync

from pyrevolut.api.foreign_exchange.get import GetExchangeRate
from pyrevolut.api.foreign_exchange.post import ExchangeMoney


class EndpointForeignExchangeSync(BaseEndpointSync):
    """The Foreign Exchange API

    Retrieve information on exchange rates between currencies, buy and sell currencies.
    """

    def get_exchange_rate(
        self,
        from_currency: str,
        to_currency: str,
        amount: Decimal | None = None,
        **kwargs,
    ) -> dict | GetExchangeRate.Response:
        """
        Get the sell exchange rate between two currencies.

        Parameters
        ----------
        from_currency : str
            The currency that you exchange from in ISO 4217 format.
        to_currency : str
            The currency that you exchange to in ISO 4217 format.
        amount : Decimal | None
            The amount of the currency to exchange from.
            The default value is 1.00 if not provided.

        Returns
        -------
        dict | GetExchangeRate.Response
            A dict with the information about the exchange rate.
        """
        endpoint = GetExchangeRate
        path = endpoint.ROUTE
        params = endpoint.Params(
            from_=from_currency,
            to=to_currency,
            amount=amount,
        )

        response = self.client.get(
            path=path,
            params=params,
            **kwargs,
        )

        return self.process_resp(endpoint.Response(**response.json()))

    def exchange_money(
        self,
        request_id: str,
        from_account_id: UUID,
        from_currency: str,
        to_account_id: UUID,
        to_currency: str,
        from_amount: Decimal | None = None,
        to_amount: Decimal | None = None,
        reference: str | None = None,
        **kwargs,
    ) -> dict | ExchangeMoney.Response:
        """
        Exchange money using one of these methods:

        Sell currency:
            You know the amount of currency to sell.
            For example, you want to exchange 135.5 USD to some EUR.
            Specify the amount in the from object.

        Buy currency:
            You know the amount of currency to buy.
            For example, you want to exchange some USD to 200 EUR.
            Specify the amount in the to object.

        Parameters
        ----------
        request_id : str
            The ID of the request, provided by you.
            It helps you identify the transaction in your system.

            To ensure that an exchange transaction is not processed multiple
            times if there are network or system errors, the same request_id
            should be used for requests related to the same transaction.
        from_account_id : UUID
            The ID of the account to sell currency from.
        from_currency : str
            The currency to sell in ISO 4217 format.
        to_account_id : UUID
            The ID of the account to receive exchanged currency into.
        to_currency : str
            The currency to buy in ISO 4217 format.
        from_amount : Decimal | None
            The amount of currency. Specify ONLY if you want to sell currency.
        to_amount : Decimal | None
            The amount of currency. Specify ONLY if you want to buy currency.
        reference : str | None
            The reference for the exchange transaction, provided by you.
            It helps you to identify the transaction if you want to look it up later.

        Returns
        -------
        dict | ExchangeMoney.Response
            A dict with the information about the exchange transaction.
        """
        endpoint = ExchangeMoney
        path = endpoint.ROUTE
        body = endpoint.Body(
            from_=endpoint.Body.ModelFrom(
                account_id=from_account_id,
                currency=from_currency,
                amount=from_amount,
            ),
            to=endpoint.Body.ModelTo(
                account_id=to_account_id,
                currency=to_currency,
                amount=to_amount,
            ),
            reference=reference,
            request_id=request_id,
        )

        response = self.client.post(
            path=path,
            body=body,
            **kwargs,
        )

        return self.process_resp(endpoint.Response(**response.json()))

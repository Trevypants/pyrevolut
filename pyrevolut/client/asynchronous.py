from typing import Type

from pydantic import BaseModel

from httpx import AsyncClient as HTTPClient

from pyrevolut.api import (
    EndpointAccountsAsync,
    EndpointCardsAsync,
    EndpointCounterpartiesAsync,
    EndpointForeignExchangeAsync,
    EndpointPaymentDraftsAsync,
    EndpointPayoutLinksAsync,
    EndpointSimulationsAsync,
    EndpointTeamMembersAsync,
    EndpointTransactionsAsync,
    EndpointTransfersAsync,
    EndpointWebhooksAsync,
)


from .base import BaseClient


class AsyncClient(BaseClient):
    """The asynchronous client for the Revolut API"""

    Accounts: EndpointAccountsAsync | None = None
    Cards: EndpointCardsAsync | None = None
    Counterparties: EndpointCounterpartiesAsync | None = None
    ForeignExchange: EndpointForeignExchangeAsync | None = None
    PaymentDrafts: EndpointPaymentDraftsAsync | None = None
    PayoutLinks: EndpointPayoutLinksAsync | None = None
    Simulations: EndpointSimulationsAsync | None = None
    TeamMembers: EndpointTeamMembersAsync | None = None
    Transactions: EndpointTransactionsAsync | None = None
    Transfers: EndpointTransfersAsync | None = None
    Webhooks: EndpointWebhooksAsync | None = None

    async def open(self):
        """Opens the client connection"""
        if self.client is not None:
            return

        self.client = HTTPClient()
        self.__load_resources()

    async def close(self):
        """Closes the client connection"""
        if self.client is None:
            return

        await self.client.aclose()
        self.client = None

    async def get(
        self,
        path: str,
        response_model: Type[BaseModel],
        params: Type[BaseModel] | None = None,
        **kwargs,
    ):
        """Send an async GET request to the Revolut API

        Parameters
        ----------
        path : str
            The path to send the request to
        response_model : Type[BaseModel]
            The model to use for the response
        params : Type[BaseModel] | None
            The parameters to send in the request

        Returns
        -------
        Response
            The response from the request
        """
        resp = await self.client.get(
            **self._prep_get(
                path=path,
                params=params,
                **kwargs,
            )
        )
        return self.process_response(
            response=resp,
            response_model=response_model,
            return_type=None,
            error_response=None,
        )

    async def post(
        self,
        path: str,
        response_model: Type[BaseModel],
        body: Type[BaseModel] | None = None,
        **kwargs,
    ):
        """Send an async POST request to the Revolut API

        Parameters
        ----------
        path : str
            The path to send the request to
        response_model : Type[BaseModel]
            The model to use for the response
        body : Type[BaseModel] | None
            The body to send in the request

        Returns
        -------
        Response
            The response from the request
        """
        resp = await self.client.post(
            **self._prep_post(
                path=path,
                body=body,
                **kwargs,
            )
        )
        return self.process_response(
            response=resp,
            response_model=response_model,
            return_type=None,
            error_response=None,
        )

    async def patch(
        self,
        path: str,
        response_model: Type[BaseModel],
        body: Type[BaseModel] | None = None,
        **kwargs,
    ):
        """Send an async PATCH request to the Revolut API

        Parameters
        ----------
        path : str
            The path to send the request to
        response_model : Type[BaseModel]
            The model to use for the response
        body : Type[BaseModel] | None
            The body to send in the request

        Returns
        -------
        Response
            The response from the request
        """
        resp = await self.client.patch(
            **self._prep_patch(
                path=path,
                body=body,
                **kwargs,
            )
        )
        return self.process_response(
            response=resp,
            response_model=response_model,
            return_type=None,
            error_response=None,
        )

    async def delete(
        self,
        path: str,
        response_model: Type[BaseModel],
        params: Type[BaseModel] | None = None,
        **kwargs,
    ):
        """Send an async DELETE request to the Revolut API

        Parameters
        ----------
        path : str
            The path to send the request to
        response_model : Type[BaseModel]
            The model to use for the response
        params : Type[BaseModel] | None
            The parameters to add to the request route

        Returns
        -------
        Response
            The response from the request
        """
        resp = await self.client.delete(
            **self._prep_delete(
                path=path,
                params=params,
                **kwargs,
            )
        )
        return self.process_response(
            response=resp,
            response_model=response_model,
            return_type=None,
            error_response=None,
        )

    async def put(
        self,
        path: str,
        response_model: Type[BaseModel],
        body: Type[BaseModel] | None = None,
        **kwargs,
    ):
        """Send an async PUT request to the Revolut API

        Parameters
        ----------
        path : str
            The path to send the request to
        response_model : Type[BaseModel]
            The model to use for the response
        body : Type[BaseModel] | None
            The body to send in the request

        Returns
        -------
        Response
            The response from the request
        """
        resp = await self.client.put(
            **self._prep_put(
                path=path,
                body=body,
                **kwargs,
            )
        )
        return self.process_response(
            response=resp,
            response_model=response_model,
            return_type=None,
            error_response=None,
        )

    def __load_resources(self):
        """Loads all the resources from the resources directory"""
        self.Accounts = EndpointAccountsAsync(client=self)
        self.Cards = EndpointCardsAsync(client=self)
        self.Counterparties = EndpointCounterpartiesAsync(client=self)
        self.ForeignExchange = EndpointForeignExchangeAsync(client=self)
        self.PaymentDrafts = EndpointPaymentDraftsAsync(client=self)
        self.PayoutLinks = EndpointPayoutLinksAsync(client=self)
        self.Simulations = EndpointSimulationsAsync(client=self)
        self.TeamMembers = EndpointTeamMembersAsync(client=self)
        self.Transactions = EndpointTransactionsAsync(client=self)
        self.Transfers = EndpointTransfersAsync(client=self)
        self.Webhooks = EndpointWebhooksAsync(client=self)

    async def __aenter__(self):
        """Open the async client connection"""
        await self.open()
        return self

    async def __aexit__(self, *args, **kwargs):
        """Close the async client connection"""
        await self.close()

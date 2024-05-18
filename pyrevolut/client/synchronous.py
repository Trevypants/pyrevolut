from typing import Type

from pydantic import BaseModel

from httpx import Client as HTTPClient

from pyrevolut.api import (
    EndpointAccountsSync,
    EndpointCardsSync,
    EndpointCounterpartiesSync,
    EndpointForeignExchangeSync,
    EndpointPaymentDraftsSync,
    EndpointPayoutLinksSync,
    EndpointSimulationsSync,
    EndpointTeamMembersSync,
    EndpointTransactionsSync,
    EndpointTransfersSync,
    EndpointWebhooksSync,
)

from .base import BaseClient


class Client(BaseClient):
    """The synchronous client for the Revolut API"""

    Accounts: EndpointAccountsSync | None = None
    Cards: EndpointCardsSync | None = None
    Counterparties: EndpointCounterpartiesSync | None = None
    ForeignExchange: EndpointForeignExchangeSync | None = None
    PaymentDrafts: EndpointPaymentDraftsSync | None = None
    PayoutLinks: EndpointPayoutLinksSync | None = None
    Simulations: EndpointSimulationsSync | None = None
    TeamMembers: EndpointTeamMembersSync | None = None
    Transactions: EndpointTransactionsSync | None = None
    Transfers: EndpointTransfersSync | None = None
    Webhooks: EndpointWebhooksSync | None = None

    def open(self):
        """Opens the client connection"""
        if self.client is not None:
            return

        self.client = HTTPClient()
        self.__load_resources()

    def close(self):
        """Closes the client connection"""
        if self.client is None:
            return

        self.client.close()
        self.client = None

    def get(self, path: str, params: Type[BaseModel] | None = None, **kwargs):
        """Send a GET request to the Revolut API

        Parameters
        ----------
        path : str
            The path to send the request to
        params : Type[BaseModel] | None
            The parameters to add to the request route

        Returns
        -------
        Response
            The response from the request
        """
        resp = self.client.get(
            **self.__prep_get(
                path=path,
                params=params,
                **kwargs,
            )
        )
        self.log_response(response=resp)
        return resp

    def post(self, path: str, body: Type[BaseModel] | None = None, **kwargs):
        """Send a POST request to the Revolut API

        Parameters
        ----------
        path : str
            The path to send the request to
        body : Type[BaseModel] | None
            The body to send in the request

        Returns
        -------
        Response
            The response from the request
        """
        resp = self.client.post(
            **self.__prep_post(
                path=path,
                body=body,
                **kwargs,
            )
        )
        self.log_response(response=resp)
        return resp

    def patch(self, path: str, body: Type[BaseModel] | None = None, **kwargs):
        """Send a PATCH request to the Revolut API

        Parameters
        ----------
        path : str
            The path to send the request to
        body : Type[BaseModel]
            The body to send in the request

        Returns
        -------
        Response
            The response from the request
        """
        resp = self.client.patch(
            **self.__prep_patch(
                path=path,
                body=body,
                **kwargs,
            )
        )
        self.log_response(response=resp)
        return resp

    def delete(
        self,
        path: str,
        params: Type[BaseModel] | None = None,
        **kwargs,
    ):
        """Send a DELETE request to the Revolut API

        Parameters
        ----------
        path : str
            The path to send the request to
        params : Type[BaseModel] | None
            The parameters to add to the request route

        Returns
        -------
        Response
            The response from the request
        """
        resp = self.client.delete(
            **self.__prep_delete(
                path=path,
                params=params,
                **kwargs,
            )
        )
        self.log_response(response=resp)
        return resp

    def put(self, path: str, body: Type[BaseModel] | None = None, **kwargs):
        """Send a PUT request to the Revolut API

        Parameters
        ----------
        path : str
            The path to send the request to
        body : Type[BaseModel] | None
            The body to send in the request

        Returns
        -------
        Response
            The response from the request
        """
        resp = self.client.put(
            **self.__prep_put(
                path=path,
                body=body,
                **kwargs,
            )
        )
        self.log_response(response=resp)
        return resp

    def __load_resources(self):
        """Loads all the resources from the resources directory"""
        self.Accounts = EndpointAccountsSync(client=self)
        self.Cards = EndpointCardsSync(client=self)
        self.Counterparties = EndpointCounterpartiesSync(client=self)
        self.ForeignExchange = EndpointForeignExchangeSync(client=self)
        self.PaymentDrafts = EndpointPaymentDraftsSync(client=self)
        self.PayoutLinks = EndpointPayoutLinksSync(client=self)
        self.Simulations = EndpointSimulationsSync(client=self)
        self.TeamMembers = EndpointTeamMembersSync(client=self)
        self.Transactions = EndpointTransactionsSync(client=self)
        self.Transfers = EndpointTransfersSync(client=self)
        self.Webhooks = EndpointWebhooksSync(client=self)

    def __enter__(self):
        """Open the client connection"""
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        """Close the client connection"""
        self.close()

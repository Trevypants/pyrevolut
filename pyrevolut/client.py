from typing import Type, TypeVar
from enum import StrEnum
import logging

from pydantic import BaseModel

from httpx import AsyncClient
from httpx import Client as SyncClient
from httpx import HTTPStatusError, Response

from .api import (
    EndpointAccounts,
    EndpointCards,
    EndpointCounterparties,
    EndpointForeignExchange,
    EndpointPaymentDrafts,
    EndpointPayoutLinks,
    EndpointSimulations,
    EndpointTeamMembers,
    EndpointTransactions,
    EndpointTransfers,
    EndpointWebhooks,
)


D = TypeVar("D", dict, list)  # TypeVar for dictionary or list


class Environment(StrEnum):
    SANDBOX = "sandbox"
    LIVE = "live"


class Client:
    access_token: str
    refresh_token: str
    environment: Environment
    domain: str
    async_client: AsyncClient | None = None
    sync_client: SyncClient | None = None
    Accounts: EndpointAccounts | None = None
    Cards: EndpointCards | None = None
    Counterparties: EndpointCounterparties | None = None
    ForeignExchange: EndpointForeignExchange | None = None
    PaymentDrafts: EndpointPaymentDrafts | None = None
    PayoutLinks: EndpointPayoutLinks | None = None
    Simulations: EndpointSimulations | None = None
    TeamMembers: EndpointTeamMembers | None = None
    Transactions: EndpointTransactions | None = None
    Transfers: EndpointTransfers | None = None
    Webhooks: EndpointWebhooks | None = None

    def __init__(
        self,
        access_token: str,
        refresh_token: str,
        environment: Environment = Environment.SANDBOX,
    ):
        """Create a new Revolut client

        Parameters
        ----------
        access_token : str
            The access token to use
        refresh_token : str
            The refresh token to use
        environment : Environment
            The environment to use, either Environment.SANDBOX or Environment.LIVE
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.environment = environment

        # Set domain based on environment
        if self.environment == Environment.SANDBOX:
            self.domain = "https://sandbox-b2b.revolut.com/api/1.0/"
        else:
            self.domain = "https://b2b.revolut.com/api/1.0/"

    def open(self):
        """Opens the client connection"""
        if self.sync_client is not None:
            return

        self.sync_client = SyncClient()
        self.__load_resources()

    def close(self):
        """Closes the client connection"""
        if self.sync_client is None:
            return

        self.sync_client.close()
        self.sync_client = None

    async def aopen(self):
        """Opens the async client connection"""
        if self.async_client is not None:
            return

        self.async_client = AsyncClient()
        self.__load_resources()

    async def aclose(self):
        """Closes the async client connection"""
        if self.async_client is None:
            return

        await self.async_client.aclose()
        self.async_client = None

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
        self.__check_sync_client()
        url = f"{self.domain}/{path}"
        headers = self.__create_headers(kwargs.pop("headers", {}))
        params = (
            self.__replace_null_with_none(
                data=params.model_dump(mode="json", exclude_none=True, by_alias=True)
            )
            if params is not None
            else None
        )
        resp = self.sync_client.get(
            url=url,
            params=params,
            headers=headers,
            **kwargs,
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
        self.__check_sync_client()
        url = f"{self.domain}/{path}"
        headers = self.__create_headers(kwargs.pop("headers", {}))
        json = (
            self.__replace_null_with_none(
                data=body.model_dump(mode="json", exclude_none=True, by_alias=True)
            )
            if body is not None
            else None
        )
        resp = self.sync_client.post(
            url=url,
            json=json,
            headers=headers,
            **kwargs,
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
        self.__check_sync_client()
        path = self.__process_path(path)
        url = f"{self.domain}/{path}"
        headers = self.__create_headers(kwargs.pop("headers", {}))
        json = (
            self.__replace_null_with_none(
                data=body.model_dump(mode="json", exclude_none=True, by_alias=True)
            )
            if body is not None
            else None
        )
        resp = self.sync_client.patch(
            url=url,
            json=json,
            headers=headers,
            **kwargs,
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
        self.__check_sync_client()
        path = self.__process_path(path)
        url = f"{self.domain}/{path}"
        headers = self.__create_headers(kwargs.pop("headers", {}))
        params = (
            self.__replace_null_with_none(
                data=params.model_dump(mode="json", exclude_none=True, by_alias=True)
            )
            if params is not None
            else None
        )
        resp = self.sync_client.delete(
            url=url,
            params=params,
            headers=headers,
            **kwargs,
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
        self.__check_sync_client()
        path = self.__process_path(path)
        url = f"{self.domain}/{path}"
        headers = self.__create_headers(kwargs.pop("headers", {}))
        json = (
            self.__replace_null_with_none(
                data=body.model_dump(mode="json", exclude_none=True, by_alias=True)
            )
            if body is not None
            else None
        )
        resp = self.sync_client.put(
            url=url,
            json=json,
            headers=headers,
            **kwargs,
        )
        self.log_response(response=resp)
        return resp

    async def aget(self, path: str, params: Type[BaseModel] | None = None, **kwargs):
        """Send an async GET request to the Revolut API

        Parameters
        ----------
        path : str
            The path to send the request to
        params : Type[BaseModel] | None
            The parameters to send in the request

        """
        self.__check_async_client()
        url = f"{self.domain}/{path}"
        headers = self.__create_headers(kwargs.pop("headers", {}))
        params = (
            self.__replace_null_with_none(
                data=params.model_dump(mode="json", exclude_none=True, by_alias=True)
            )
            if params is not None
            else None
        )
        resp = await self.async_client.get(
            url=url,
            params=params,
            headers=headers,
            **kwargs,
        )
        self.log_response(response=resp)
        return resp

    async def apost(self, path: str, body: Type[BaseModel] | None = None, **kwargs):
        """Send an async POST request to the Revolut API

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
        self.__check_async_client()
        url = f"{self.domain}/{path}"
        headers = self.__create_headers(kwargs.pop("headers", {}))
        json = (
            self.__replace_null_with_none(
                data=body.model_dump(mode="json", exclude_none=True, by_alias=True)
            )
            if body is not None
            else None
        )
        resp = await self.async_client.post(
            url=url,
            json=json,
            headers=headers,
            **kwargs,
        )
        self.log_response(response=resp)
        return resp

    async def apatch(self, path: str, body: Type[BaseModel] | None = None, **kwargs):
        """Send an async PATCH request to the Revolut API

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
        self.__check_async_client()
        path = self.__process_path(path)
        url = f"{self.domain}/{path}"
        headers = self.__create_headers(kwargs.pop("headers", {}))
        json = (
            self.__replace_null_with_none(
                data=body.model_dump(mode="json", exclude_none=True, by_alias=True)
            )
            if body is not None
            else None
        )
        resp = await self.async_client.patch(
            url=url,
            json=json,
            headers=headers,
            **kwargs,
        )
        self.log_response(response=resp)
        return resp

    async def adelete(
        self,
        path: str,
        params: Type[BaseModel] | None = None,
        **kwargs,
    ):
        """Send an async DELETE request to the Revolut API

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
        self.__check_async_client()
        path = self.__process_path(path)
        url = f"{self.domain}/{path}"
        headers = self.__create_headers(kwargs.pop("headers", {}))
        params = (
            self.__replace_null_with_none(
                data=params.model_dump(mode="json", exclude_none=True, by_alias=True)
            )
            if params is not None
            else None
        )
        resp = await self.async_client.delete(
            url=url,
            params=params,
            headers=headers,
            **kwargs,
        )
        self.log_response(response=resp)
        return resp

    async def aput(self, path: str, body: Type[BaseModel] | None = None, **kwargs):
        """Send an async PUT request to the Revolut API

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
        self.__check_async_client()
        path = self.__process_path(path)
        url = f"{self.domain}/{path}"
        headers = self.__create_headers(kwargs.pop("headers", {}))
        json = (
            self.__replace_null_with_none(
                data=body.model_dump(mode="json", exclude_none=True, by_alias=True)
            )
            if body is not None
            else None
        )
        resp = await self.async_client.put(
            url=url,
            json=json,
            headers=headers,
            **kwargs,
        )
        self.log_response(response=resp)
        return resp

    @property
    def required_headers(self) -> dict[str, str]:
        """The headers to be attached to each request

        Returns
        -------
        dict[str, str]
            The headers to be attached to each request
        """
        if self.access_token is None:
            raise {}
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

    def __create_headers(self, headers: dict[str, str] = {}) -> dict[str, str]:
        """Create the headers for the request by adding the required headers

        Parameters
        ----------
        headers : dict[str, str]
            The headers for the request

        Returns
        -------
        dict[str, str]
            The headers for the request
        """
        headers.update(self.required_headers)
        return headers

    def __check_sync_client(self):
        """Check if the sync client is open

        Raises
        ------
        ValueError
            If the client is not open
        """
        if self.sync_client is None:
            raise ValueError("Sync client is not open")

    def __check_async_client(self):
        """Check if the async client is open

        Raises
        ------
        ValueError
            If the client is not open
        """
        if self.async_client is None:
            raise ValueError("Async client is not open")

    def __process_path(self, path: str) -> str:
        """Process the path.

        If 'http' not in the path:
            Removing the leading slash if it exists
        Else:
            Return the path as is

        Parameters
        ----------
        path : str
            The path to process

        Returns
        -------
        str
            The processed path
        """
        if "http" in path:
            return path

        return self.__remove_leading_slash(path)

    def __remove_leading_slash(self, path: str) -> str:
        """Remove the leading slash from a path if it exists and
        return it without the leading slash

        Parameters
        ----------
        path : str
            The path to remove the leading slash from

        Returns
        -------
        str
            The path without the leading slash
        """
        if path.startswith("/"):
            return path[1:]
        return path

    def __replace_null_with_none(self, data: D) -> D:
        """
        Method that replaces all 'null' strings with None in a provided dictionary or list.

        Must be called with either a dictionary or a list, not both.

        Parameters
        ----------
        data : dict | list
            The dictionary or list to replace 'null' strings with None

        Returns
        -------
        dict | list
            The dictionary or list with 'null' strings replaced with None
        """
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict):
                    self.__replace_null_with_none(data_dict=v, data_list=None)
                elif isinstance(v, list):
                    self.__replace_null_with_none(data_dict=None, data_list=v)
                elif v == "null":
                    data[k] = None
        elif isinstance(data, list):
            for i in range(len(data)):
                if isinstance(data[i], dict):
                    self.__replace_null_with_none(data_dict=data[i], data_list=None)
                elif isinstance(data[i], list):
                    self.__replace_null_with_none(data_dict=None, data_list=data[i])
                elif data[i] == "null":
                    data[i] = None
        else:
            raise ValueError("Data must be either a dictionary or a list")

        return data

    def __load_resources(self):
        """Loads all the resources from the resources directory"""
        self.Accounts = EndpointAccounts(client=self)
        self.Cards = EndpointCards(client=self)
        self.Counterparties = EndpointCounterparties(client=self)
        self.ForeignExchange = EndpointForeignExchange(client=self)
        self.PaymentDrafts = EndpointPaymentDrafts(client=self)
        self.PayoutLinks = EndpointPayoutLinks(client=self)
        self.Simulations = EndpointSimulations(client=self)
        self.TeamMembers = EndpointTeamMembers(client=self)
        self.Transactions = EndpointTransactions(client=self)
        self.Transfers = EndpointTransfers(client=self)
        self.Webhooks = EndpointWebhooks(client=self)

    def __enter__(self):
        """Open the client connection"""
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        """Close the client connection"""
        self.close()

    async def __aenter__(self):
        """Open the async client connection"""
        await self.aopen()
        return self

    async def __aexit__(self, *args, **kwargs):
        """Close the async client connection"""
        await self.aclose()

    def log_response(self, response: Response):
        """Log the response from the API.
        If the response is an error, raise an error

        Parameters
        ----------
        response : Response
            The response from the API
        """
        if not response.is_error:
            logging.info(f"Response: {response.status_code} - {response.text}")
        else:
            logging.error(f"Response: {response.status_code} - {response.text}")

            try:
                response.raise_for_status()
            except HTTPStatusError as exc:
                raise ValueError(f"Error {response.status_code}: {response.text}") from exc

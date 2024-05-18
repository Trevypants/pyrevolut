from typing import Type, TypeVar
from enum import StrEnum
import logging

from pydantic import BaseModel

from httpx import AsyncClient
from httpx import Client as SyncClient
from httpx import HTTPStatusError, Response


D = TypeVar("D", dict, list)  # TypeVar for dictionary or list


class EnumEnvironment(StrEnum):
    SANDBOX = "sandbox"
    LIVE = "live"


class BaseClient:
    access_token: str
    refresh_token: str
    environment: EnumEnvironment
    domain: str
    client: SyncClient | AsyncClient | None = None

    def __init__(
        self,
        access_token: str,
        refresh_token: str,
        environment: EnumEnvironment = EnumEnvironment.SANDBOX,
    ):
        """Create a new Revolut client

        Parameters
        ----------
        access_token : str
            The access token to use
        refresh_token : str
            The refresh token to use
        environment : EnumEnvironment
            The environment to use, either Environment.SANDBOX or Environment.LIVE
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.environment = environment

        # Set domain based on environment
        if self.environment == EnumEnvironment.SANDBOX:
            self.domain = "https://sandbox-b2b.revolut.com/api/1.0/"
        else:
            self.domain = "https://b2b.revolut.com/api/1.0/"

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

    def __prep_get(
        self,
        path: str,
        params: Type[BaseModel] | None = None,
        **kwargs,
    ):
        """
        Method to prepare the GET request inputs for the HTTPX client.

        Parameters
        ----------
        path : str
            The path to send the request to
        params : Type[BaseModel] | None
            The parameters to add to the request route
        **kwargs
            Additional keyword arguments to pass to the HTTPX client

        Returns
        -------
        dict
            The prepared inputs for the HTTPX client
        """
        self.__check_client()
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
        return {
            "url": url,
            "params": params,
            "headers": headers,
            **kwargs,
        }

    def __prep_post(
        self,
        path: str,
        body: Type[BaseModel] | None = None,
        **kwargs,
    ):
        """
        Method to prepare the POST request inputs for the HTTPX client.

        Parameters
        ----------
        path : str
            The path to send the request to
        body : Type[BaseModel] | None
            The body to send in the request
        **kwargs
            Additional keyword arguments to pass to the HTTPX client

        Returns
        -------
        dict
            The prepared inputs for the HTTPX client
        """
        self.__check_client()
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
        return {
            "url": url,
            "json": json,
            "headers": headers,
            **kwargs,
        }

    def __prep_patch(
        self,
        path: str,
        body: Type[BaseModel] | None = None,
        **kwargs,
    ):
        """
        Method to prepare the PATCH request inputs for the HTTPX client.

        Parameters
        ----------
        path : str
            The path to send the request to
        body : Type[BaseModel] | None
            The body to send in the request
        **kwargs
            Additional keyword arguments to pass to the HTTPX client

        Returns
        -------
        dict
            The prepared inputs for the HTTPX client
        """
        self.__check_client()
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
        return {
            "url": url,
            "json": json,
            "headers": headers,
            **kwargs,
        }

    def __prep_delete(
        self,
        path: str,
        params: Type[BaseModel] | None = None,
        **kwargs,
    ):
        """
        Method to prepare the DELETE request inputs for the HTTPX client.

        Parameters
        ----------
        path : str
            The path to send the request to
        params : Type[BaseModel] | None
            The parameters to add to the request route
        **kwargs
            Additional keyword arguments to pass to the HTTPX client

        Returns
        -------
        dict
            The prepared inputs for the HTTPX client
        """
        self.__check_client()
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
        return {
            "url": url,
            "params": params,
            "headers": headers,
            **kwargs,
        }

    def __prep_put(
        self,
        path: str,
        body: Type[BaseModel] | None = None,
        **kwargs,
    ):
        """
        Method to prepare the PUT request inputs for the HTTPX client.

        Parameters
        ----------
        path : str
            The path to send the request to
        body : Type[BaseModel] | None
            The body to send in the request
        **kwargs
            Additional keyword arguments to pass to the HTTPX client

        Returns
        -------
        dict
            The prepared inputs for the HTTPX client
        """
        self.__check_client()
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
        return {
            "url": url,
            "json": json,
            "headers": headers,
            **kwargs,
        }

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

    def __check_client(self):
        """Check if the client is open

        Raises
        ------
        ValueError
            If the client is not open
        """
        if self.client is None:
            raise ValueError("Client is not open")

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

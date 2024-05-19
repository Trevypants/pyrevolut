from typing import Type, TypeVar
import logging

from pydantic import BaseModel
import pendulum

from httpx import AsyncClient
from httpx import Client as SyncClient
from httpx import HTTPStatusError, Response

from pyrevolut.utils.auth import (
    ModelCreds,
    refresh_access_token,
    save_creds,
    load_creds,
)


D = TypeVar("D", dict, list)  # TypeVar for dictionary or list


class BaseClient:
    creds_loc: str
    credentials: ModelCreds
    domain: str
    sandbox: bool
    return_dict: bool
    client: SyncClient | AsyncClient | None = None

    def __init__(
        self,
        creds_loc: str = "credentials/creds.json",
        sandbox: bool = True,
        return_dict: bool = True,
    ):
        """Create a new Revolut client

        Parameters
        ----------
        creds_loc : str, optional
            The location of the credentials file, by default "credentials/creds.json"
        sandbox : bool, optional
            Whether to use the sandbox environment, by default True
        return_dict : bool, optional
            Whether to return the API responses as dictionaries or as pydantic models.
            If True, the responses will be returned as dictionaries.
            If False, the responses will be returned as pydantic models.
            By default, True
        """
        self.creds_loc = creds_loc
        self.sandbox = sandbox
        self.return_dict = return_dict

        # Set domain based on environment
        if self.sandbox:
            self.domain = "https://sandbox-b2b.revolut.com/api"
        else:
            self.domain = "https://b2b.revolut.com/api"

        # Load the credentials
        self.__load_credentials()

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

    def _prep_get(
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

    def _prep_post(
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

    def _prep_patch(
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

    def _prep_delete(
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

    def _prep_put(
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
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.credentials.tokens.access_token.get_secret_value()}",
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
        """Check if the client is open and that the credentials are still valid.

        Raises
        ------
        ValueError
            If the client is not open or if the long-term credentials have expired
        """
        if self.client is None:
            raise ValueError("Client is not open")

        if self.credentials.credentials_expired:
            raise ValueError(
                "Long-term credentials have expired. "
                "\n\nPlease reauthenticate using the `pyrevolut auth-manual` command."
            )

        if self.credentials.access_token_expired:
            self.__refresh_access_token()

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

        return self.__remove_leading_slash(path=path)

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
                    self.__replace_null_with_none(data=v)
                elif isinstance(v, list):
                    self.__replace_null_with_none(data=v)
                elif v == "null":
                    data[k] = None
        elif isinstance(data, list):
            for i in range(len(data)):
                if isinstance(data[i], dict):
                    self.__replace_null_with_none(data=data[i])
                elif isinstance(data[i], list):
                    self.__replace_null_with_none(data=data[i])
                elif data[i] == "null":
                    data[i] = None
        else:
            raise ValueError("Data must be either a dictionary or a list")

        return data

    def __load_credentials(self):
        """Load the credentials from the credentials file.

        - If the credentials file does not exist, raise an error.
        - If the credentials file is invalid, raise an error.
        - If the credentials are expired, raise an error.
        - If the access token is expired, refresh it.

        """
        solution_msg = "\n\nPlease reauthenticate using the `pyrevolut auth-manual` command."

        try:
            self.credentials = load_creds(location=self.creds_loc)
        except FileNotFoundError as exc:
            raise ValueError(f"Credentials file not found: {exc}. {solution_msg}") from exc
        except Exception as exc:
            raise ValueError(f"Error loading credentials: {exc}.") from exc

        # Check if the credentials are still valid
        if self.credentials.credentials_expired:
            raise ValueError(f"Credentials are expired. {solution_msg}")

        # Check if the access token is expired
        if self.credentials.access_token_expired:
            self.__refresh_access_token()

    def __refresh_access_token(self):
        """Refresh the access token using the refresh token.
        Will call the endpoint to refresh the access token.
        Then it will save the new access token to the credentials file.

        Parameters
        ----------
        None

        Raises
        ------
        ValueError
            If there is an error refreshing the access token.

        Returns
        -------
        None
        """
        try:
            resp = refresh_access_token(
                client=SyncClient(),
                refresh_token=self.credentials.tokens.refresh_token.get_secret_value(),
                client_assert_jwt=self.credentials.client_assert_jwt.jwt.get_secret_value(),
                sandbox=self.sandbox,
            )
            self.credentials.tokens.access_token = resp.access_token.get_secret_value()
            self.credentials.tokens.token_type = resp.token_type
            self.credentials.tokens.access_token_expiration_dt = pendulum.now(tz="UTC").add(
                seconds=resp.expires_in
            )
            save_creds(creds=self.credentials, location=self.creds_loc, indent=4)
        except Exception as exc:
            raise ValueError(f"Error refreshing access token: {exc}.") from exc

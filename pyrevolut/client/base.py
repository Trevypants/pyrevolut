from typing import Type, TypeVar, Literal, Annotated
import logging
import json

from pydantic import BaseModel, Field
import pendulum

from httpx import AsyncClient
from httpx import Client as SyncClient
from httpx import Request, Response

from pyrevolut.utils.auth import (
    ModelCreds,
    refresh_access_token,
    save_creds,
    load_creds,
)
from pyrevolut.exceptions import (
    PyRevolutAPIException,
    BadRequestException,
    InternalRevolutError,
)


BM = TypeVar("BM", bound=Type[BaseModel])
D = TypeVar("D", dict, list)  # TypeVar for dictionary or list


class ModelError(BaseModel):
    """Model for the error response"""

    code: Annotated[int, Field(description="The error code")]
    message: Annotated[str, Field(description="The error message")]


class BaseClient:
    """The base client for the Revolut API"""

    creds_loc: str
    credentials: ModelCreds
    domain: str
    sandbox: bool
    return_type: Literal["raw", "dict", "model"] = "dict"
    error_response: Literal["raw", "raise", "dict", "model"] = "raise"
    client: SyncClient | AsyncClient | None = None

    def __init__(
        self,
        creds_loc: str = "credentials/creds.json",
        sandbox: bool = True,
        return_type: Literal["raw", "dict", "model"] = "dict",
        error_response: Literal["raw", "raise", "dict", "model"] = "raise",
    ):
        """Create a new Revolut client

        Parameters
        ----------
        creds_loc : str, optional
            The location of the credentials file, by default "credentials/creds.json"
        sandbox : bool, optional
            Whether to use the sandbox environment, by default True
        return_type : Literal["raw", "dict", "model"], optional
            The return type for the API responses, by default "dict"
            If "raw":
                The raw response will be returned
            If "dict":
                The response will be the dictionary representation of the Pydantic model.
                So it will have UUIDs, pendulum DateTimes, etc instead of the raw string values.
            If "model":
                The response will be a Pydantic model containing all processed response data.
        error_response : Literal["raw", "raise", "dict", "model"], optional
            How the client should handle error responses, by default "raise"
            If "raw":
                The client will return the raw error response
            If "raise":
                The client will raise a ValueError if the response is an error
            If "dict":
                The client will return a dictionary representation of the error response
            If "model":
                The client will return a Pydantic model of the error response
        """
        self.creds_loc = creds_loc
        self.sandbox = sandbox
        assert return_type in [
            "raw",
            "dict",
            "model",
        ], "return_type must be 'raw', 'dict', or 'model'"
        self.return_type = return_type
        assert error_response in [
            "raise",
            "dict",
            "model",
        ], "error_response must be 'raise', 'dict', or 'model'"
        self.error_response = error_response

        # Set domain based on environment
        if self.sandbox:
            self.domain = "https://sandbox-b2b.revolut.com/api"
        else:
            self.domain = "https://b2b.revolut.com/api"

        # Load the credentials
        self.__load_credentials()

    def process_response(
        self,
        response: Response,
        response_model: BM,
        return_type: Literal["raw", "dict", "model"] | None = None,
        error_response: Literal["raw", "raise", "dict", "model"] | None = "raise",
    ):
        """Processes the response and returns the desired format.
        Will additionally log the request and response.

        Parameters
        ----------
        response : Response
            The HTTPX response to process
        response_model : BM
            The Pydantic model to use for the response
        return_type : Literal["raw", "dict", "model"] | None, optional
            The return type for the API responses, by default None.
            If "raw":
                The raw response will be returned
            If "dict":
                The response will be the dictionary representation of the Pydantic model.
                So it will have UUIDs, pendulum DateTimes, etc instead of the raw string values.
            If "model":
                The response will be a Pydantic model containing all processed response data.
            If None:
                The default return type of the client will be used.
        error_response : Literal["raw", "raise", "dict", "model"] | None, optional
            How the client should handle error responses, by default None.
            If "raw":
                The client will return the raw error response
            If "raise":
                The client will raise a ValueError if the response is an error
            If "dict":
                The client will return a dictionary representation of the error response
            If "model":
                The client will return a Pydantic model of the error response
            If None:
                The default error response type of the client will be used.

        Returns
        -------
        BM | dict | list[BM] | list[dict]
            The response in the desired format
        """
        if return_type is None:
            return_type = self.return_type
        if error_response is None:
            error_response = self.error_response

        # Log the request
        self.log_request(request=response.request)

        # Log the response
        self.log_response(response=response)

        # Check for error response
        if response.is_error:
            if error_response == "raise":
                if response.status_code == 400:
                    raise BadRequestException(response.text)
                elif response.status_code // 100 == 5:
                    raise InternalRevolutError(response.text)
                raise PyRevolutAPIException(response.text)
            elif error_response == "raw":
                return response.json()
            elif error_response == "dict":
                return ModelError(**response.json()).model_dump()
            elif error_response == "model":
                return ModelError(**response.json())
            else:
                raise ValueError(f"Invalid error response type: {error_response}")

        # Raw response
        try:
            raw_response = response.json()
        except json.JSONDecodeError:
            raw_response = {}
        if return_type == "raw":
            return raw_response

        # Dict response
        if isinstance(raw_response, list):
            model_response = [response_model(**resp) for resp in raw_response]
        else:
            model_response = response_model(**raw_response)
        if return_type == "dict":
            if isinstance(model_response, list):
                return [resp.model_dump() for resp in model_response]
            return model_response.model_dump()

        # Model response
        if return_type == "model":
            return model_response

    def log_request(self, request: Request):
        """Log the request to the API

        Parameters
        ----------
        request : Request
            The request to log

        Returns
        -------
        None
        """
        logging.info(
            f"Request: {request.method} {request.url} - {request.headers} - {request.read().decode()}"
        )

    def log_response(self, response: Response):
        """Log the response from the API.

        Parameters
        ----------
        response : Response
            The response from the API

        Returns
        -------
        None
        """
        if not response.is_error:
            logging.info(f"Response: {response.status_code} - {response.text}")
        else:
            logging.error(f"Response: {response.status_code} - {response.text}")

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
        solution_msg = (
            "\n\nPlease reauthenticate using the `pyrevolut auth-manual` command."
        )

        try:
            self.credentials = load_creds(location=self.creds_loc)
        except FileNotFoundError as exc:
            raise ValueError(
                f"Credentials file not found: {exc}. {solution_msg}"
            ) from exc
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
            self.credentials.tokens.access_token_expiration_dt = pendulum.now(
                tz="UTC"
            ).add(seconds=resp.expires_in)
            save_creds(creds=self.credentials, location=self.creds_loc, indent=4)
        except Exception as exc:
            raise ValueError(f"Error refreshing access token: {exc}.") from exc

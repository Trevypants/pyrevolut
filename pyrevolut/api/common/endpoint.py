from typing import TYPE_CHECKING, Type, TypeVar, Literal

from pydantic import BaseModel

if TYPE_CHECKING:
    from pyrevolut.client import Client, AsyncClient


BM = TypeVar("BM", bound=Type[BaseModel])


class BaseEndpointBase:
    """Base class for base endpoint classes."""

    def __init__(self, client: "Client | AsyncClient"):
        """Create a new Base endpoint handler

        Parameters
        ----------
        client : Client
            The client to use for the endpoint
        """
        self.client = client

    def process_resp(
        self,
        response: dict | list[dict],
        response_model: BM,
        return_type: Literal["raw", "dict", "model"] | None = None,
    ):
        """Return the response in the desired format

        Parameters
        ----------
        response : BM
            The response to return
        return_type : Literal["raw", "dict", "model"], optional
            The return type for the API responses, by default None.
            If "raw":
                The raw response will be returned
            If "dict":
                The response will be the dictionary representation of the Pydantic model.
                So it will have Decimals, UUIDs, etc instead of the raw string values.
            If "model":
                The response will be a Pydantic model containing all processed response data.
            If None:
                The default return type of the client will be used.

        Returns
        -------
        BM | dict | list[BM] | list[dict]
            The response in the desired format
        """
        if return_type is None:
            return_type = self.client.return_type

        # Raw response
        if return_type == "raw":
            return response

        # Dict response
        elif return_type == "dict":
            if isinstance(response, list):
                return [response_model(**resp).model_dump() for resp in response]
            return response_model(**response).model_dump()

        # Model response
        elif return_type == "model":
            if isinstance(response, list):
                return [response_model(**resp) for resp in response]
            return response_model(**response)


class BaseEndpointSync(BaseEndpointBase):
    """Base class for all endpoints."""

    def __init__(self, client: "Client"):
        """Create a new Base endpoint handler

        Parameters
        ----------
        client : Client
            The client to use for the endpoint
        """
        self.client = client


class BaseEndpointAsync(BaseEndpointBase):
    """Base  class for all async endpoints."""

    def __init__(self, client: "AsyncClient"):
        """Create a new Base endpoint handler

        Parameters
        ----------
        client : AsyncClient
            The async client to use for the endpoint
        """
        self.client = client

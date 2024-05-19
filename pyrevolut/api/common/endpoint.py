from typing import TYPE_CHECKING, Type, TypeVar

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
        response: BM,
        return_dict: bool | None = None,
    ):
        """Return the response in the desired format

        Parameters
        ----------
        response : BM
            The response to return
        return_dict : bool, optional
            If True, return the response as a dictionary.
            If False, return the response as a Pydantic Model.
            If None, will default to the value set in the client.
            Default value: None

        Returns
        -------
        BM | dict
            The response in the desired format
        """
        if return_dict is None:
            return_dict = self.client.return_dict

        if return_dict:
            return response.model_dump()
        return response


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

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyrevolut.client import Client, AsyncClient


class BaseEndpointSync:
    """Base class for all endpoints."""

    def __init__(self, client: "Client"):
        """Create a new Base endpoint handler

        Parameters
        ----------
        client : Client
            The client to use for the endpoint
        """
        self.client = client


class BaseEndpointAsync:
    """Base  class for all async endpoints."""

    def __init__(self, client: "AsyncClient"):
        """Create a new Base endpoint handler

        Parameters
        ----------
        client : AsyncClient
            The async client to use for the endpoint
        """
        self.client = client

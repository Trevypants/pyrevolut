from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyrevolut.client import Client


class BaseEndpoint:
    """Base class for all endpoints."""

    def __init__(self, client: "Client"):
        """Create a new Base endpoint handler

        Parameters
        ----------
        client : Client
            The client to use for the endpoint
        """
        self.client = client

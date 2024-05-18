from pydantic import BaseModel

from pyrevolut.api.accounts.resources import ResourceAccount


class RetrieveAllAccounts:
    """
    Get a list of all your accounts.
    """

    ROUTE = "/1.0/accounts"

    class Params(BaseModel):
        """
        Query parameters for the endpoint.
        """

        pass

    class Response(ResourceAccount):
        """
        Response model for the endpoint.
        """

        pass

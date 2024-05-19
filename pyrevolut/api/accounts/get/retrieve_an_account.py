from pydantic import BaseModel

from pyrevolut.api.accounts.resources import ResourceAccount


class RetrieveAnAccount:
    """
    Get the information about one of your accounts. Specify the account by its ID.
    """

    ROUTE = "/1.0/accounts/{account_id}"

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

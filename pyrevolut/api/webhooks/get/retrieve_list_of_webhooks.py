from pydantic import BaseModel

from pyrevolut.api.webhooks.resources import ResourceWebhook


class RetrieveListOfWebhooks:
    """
    Get the list of all your existing webhooks and their details.
    """

    ROUTE = "/2.0/webhooks"

    class Params(BaseModel):
        """
        The query parameters for the request.
        """

        pass

    class Response(ResourceWebhook):
        """
        The response model for the request.
        """

        pass

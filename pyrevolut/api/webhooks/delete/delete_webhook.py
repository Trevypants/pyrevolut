from pydantic import BaseModel


class DeleteWebhook:
    """
    Delete a specific webhook.

    A successful response does not get any content in return.
    """

    ROUTE = "/2.0/webhooks/{webhook_id}"

    class Params(BaseModel):
        """
        The query params of the request.
        """

        pass

    class Response(BaseModel):
        """
        The response model for the request.
        """

        pass

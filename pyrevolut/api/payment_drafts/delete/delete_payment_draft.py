from pydantic import BaseModel


class DeletePaymentDraft:
    """
    Delete a payment draft with the given ID.
    You can delete a payment draft only if it isn't processed.
    """

    ROUTE = "/1.0/payment-drafts/{payment_draft_id}"

    class Params(BaseModel):
        """
        The parameters for the endpoint.
        """

        pass

    class Response(BaseModel):
        """
        The response model for the endpoint.
        """

        pass

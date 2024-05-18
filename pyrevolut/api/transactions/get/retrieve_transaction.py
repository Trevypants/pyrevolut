from typing import Annotated, Literal

from pydantic import BaseModel, Field

from pyrevolut.api.transactions.resources import ResourceTransaction


class RetrieveTransaction:
    """
    Retrieve the details of a specific transaction.
    The details can include, for example, cardholder details for card payments.

    You can retrieve a transaction with its details either by its transaction ID
    or by the request ID that was provided for this transaction at the time of its
    creation, for example, when you created a payment.

    To retrieve a transaction by its transaction ID, use:

        /transaction/{transaction_id}

    To retrieve a transaction by a request ID provided at transaction creation, use:

        /transaction/{request_id}?id_type=request_id
    """

    ROUTE = "/1.0/transaction/{id}"

    class Params(BaseModel):
        """
        The query parameters for the request.
        """

        id_type: Annotated[
            Literal["request_id"] | None,
            Field(
                description="""
                The type of the ID you're providing for the transaction retrieval.
                The default value is None, which means that the transaction ID is provided.
                """,
            ),
        ] = None

    class Response(ResourceTransaction):
        """
        The response model for the request.
        """

        pass

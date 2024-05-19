from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from pyrevolut.utils import DateTime
from pyrevolut.api.common import EnumTransactionState


class SimulateTransferStateUpdate:
    """
    Simulate a transfer state change in the Sandbox environment.

    For example, after you make a transfer in Sandbox, you can change its
    state to completed.

    The resulting state is final and cannot be changed.
    """

    ROUTE = "/1.0/sandbox/transactions/{transfer_id}/{action}"

    class Body(BaseModel):
        """
        The body of the request.
        """

        pass

    class Response(BaseModel):
        """
        The response model.
        """

        id: Annotated[
            UUID, Field(description="The ID of the transfer whose state was updated.")
        ]
        state: Annotated[
            EnumTransactionState,
            Field(
                description="""
                Indicates the simulated transaction state. Possible values:

                completed:
                    Transaction was successfully processed.
                reverted:
                    Transaction was reverted by the system or company, but not the user. 
                    This can happen for a variety of reasons, for example, the receiver being inaccessible.
                declined:
                    Transaction was declined to the user for a good reason, such as insufficient 
                    account balance, wrong receiver information, etc.
                failed:
                    Transaction failed during initiation or completion. 
                    This can happen for a variety of reasons, for example, 
                    invalid API calls, blocked payments, etc.
                """
            ),
        ]
        created_at: Annotated[
            DateTime,
            Field(
                description="The date and time the transfer was created in ISO 8601 format."
            ),
        ]
        completed_at: Annotated[
            DateTime | None,
            Field(
                description="The date and time the transfer was completed in ISO 8601 format."
            ),
        ] = None

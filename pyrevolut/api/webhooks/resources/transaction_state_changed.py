from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from pyrevolut.api.common import EnumTransactionState


class ResourceTransactionStateChanged(BaseModel):
    """
    Transaction state changed resource model.
    """

    id: Annotated[
        UUID,
        Field(description="The ID of the transaction."),
    ]
    request_id: Annotated[
        str | None,
        Field(description="The request ID provided by the client."),
    ] = None
    old_state: Annotated[
        EnumTransactionState,
        Field(description="The old state of the transaction."),
    ]
    new_state: Annotated[
        EnumTransactionState,
        Field(description="The new state of the transaction."),
    ]

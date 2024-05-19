from typing import Annotated

from pydantic import BaseModel, Field

from pyrevolut.utils import DateTime
from pyrevolut.api.common import EnumTransactionState


class ResourceTransfer(BaseModel):
    """
    Transfer resource model.
    """

    id: Annotated[str, Field(description="The ID of the transaction created.")]
    state: Annotated[
        EnumTransactionState,
        Field(
            description="""
            Indicates the transaction state. Possible values:

            created:
                The transaction has been created and is either processed asynchronously
                or scheduled for a later time.
            pending:
                The transaction is pending until it's being processed.
                If the transfer is made between Revolut accounts,
                this state is skipped and the transaction is executed instantly.
            completed:
                The transaction was successful.
            declined:
                The transaction was unsuccessful. This can happen for a variety of reasons,
                for example, insufficient account balance, wrong receiver information, etc.
            failed:
                The transaction was unsuccessful. This can happen for a variety of reasons,
                for example, invalid API calls, blocked payments, etc.
            reverted:
                The transaction was reverted. This can happen for a variety of reasons,
                for example, the receiver being inaccessible.
            """
        ),
    ]
    created_at: Annotated[
        DateTime,
        Field(
            description="The date and time the transaction was created in ISO 8601 format."
        ),
    ]
    completed_at: Annotated[
        DateTime | None,
        Field(
            description="The date and time the transaction was completed in ISO 8601 format."
        ),
    ] = None

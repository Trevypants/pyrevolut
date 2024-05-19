from uuid import UUID
from datetime import date

from pyrevolut.utils import Date
from pyrevolut.api.common import BaseEndpointAsync

from pyrevolut.api.payment_drafts.get import (
    RetrieveAllPaymentDrafts,
    RetrievePaymentDraft,
)
from pyrevolut.api.payment_drafts.post import CreatePaymentDraft
from pyrevolut.api.payment_drafts.delete import DeletePaymentDraft


class EndpointPaymentDraftsAsync(BaseEndpointAsync):
    """The async Payment Drafts API

    Create a payment draft to request an approval for a payment from a
    business owner or admin before the payment is executed.
    The business owner or admin must manually approve it in the
    Revolut Business User Interface.

    You can also retrieve one or all payment drafts, and delete a payment draft.
    """

    async def get_all_payment_drafts(
        self,
        **kwargs,
    ) -> dict | RetrieveAllPaymentDrafts.Response:
        """
        Get a list of all the payment drafts that aren't processed.

        Parameters
        ----------
        None

        Returns
        -------
        dict | RetrieveAllPaymentDrafts.Response
            A dict with the information about the payment drafts.
        """
        endpoint = RetrieveAllPaymentDrafts
        path = endpoint.ROUTE
        params = endpoint.Params()

        return await self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    async def get_payment_draft(
        self,
        payment_draft_id: UUID,
        **kwargs,
    ) -> dict | RetrievePaymentDraft.Response:
        """
        Get the information about a specific payment draft by ID.

        Parameters
        ----------
        payment_draft_id : UUID
            The ID of the payment draft.

        Returns
        -------
        dict | RetrievePaymentDraft.Response
            A dict with the information about the payment draft.
        """
        endpoint = RetrievePaymentDraft
        path = endpoint.ROUTE.format(payment_draft_id=payment_draft_id)
        params = endpoint.Params()

        return await self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    async def create_payment_draft(
        self,
        account_id: UUID,
        counterparty_ids: list[UUID] = [],
        counterparty_account_ids: list[UUID | None] = [],
        counterparty_card_ids: list[UUID | None] = [],
        amounts: list[float] = [],
        currencies: list[str] = [],
        references: list[str] = [],
        title: str | None = None,
        schedule_for: date | Date | str | None = None,
        **kwargs,
    ) -> dict | CreatePaymentDraft.Response:
        """
        Create a payment draft.

        Parameters
        ----------
        account_id : UUID
            The ID of the account to pay from.
        counterparty_ids : list[UUID]
            The IDs of the counterparty accounts. Each ID corresponds to a payment.
        counterparty_account_ids : list[UUID | None]
            The IDs of the counterparty accounts. Each ID corresponds to a payment.
            If the counterparty has multiple payment methods available, use it to
            specify the account to which you want to send the money. Otherwise, use None.
        counterparty_card_ids : list[UUID | None]
            The IDs of the counterparty cards. Each ID corresponds to a payment.
            If the counterparty has multiple payment methods available, use it to
            specify the card to which you want to send the money. Otherwise, use None.
        amounts : list[float]
            The amounts of the payments.
        currencies : list[str]
            The ISO 4217 currency codes in upper case.
        references : list[str]
            The references for the payments.
        title : str, optional
            The title of the payment draft.
        schedule_for : date | Date | str, optional
            The scheduled date of the payment draft in ISO 8601 format.

        Returns
        -------
        dict | CreatePaymentDraft.Response
            A dict with the information about the payment draft created.
        """
        assert (
            len(counterparty_ids)
            == len(counterparty_account_ids)
            == len(counterparty_card_ids)
            == len(amounts)
            == len(currencies)
            == len(references)
        ), (
            "The number of elements in the lists must be equal. "
            f"Got {len(counterparty_ids)} counterparty_ids, "
            f"{len(counterparty_account_ids)} counterparty_account_ids, "
            f"{len(counterparty_card_ids)} counterparty_card_ids, "
            f"{len(amounts)} amounts, "
            f"{len(currencies)} currencies, "
            f"and {len(references)} references."
        )

        endpoint = CreatePaymentDraft
        path = endpoint.ROUTE
        body = endpoint.Body(
            title=title,
            schedule_for=schedule_for,
            payments=[
                endpoint.Body.ModelPayment(
                    account_id=account_id,
                    receiver=endpoint.Body.ModelPayment.ModelReceiver(
                        counterparty_id=counterparty_id,
                        account_id=counterparty_account_id,
                        card_id=counterparty_card_id,
                    ),
                    amount=amount,
                    currency=currency,
                    reference=reference,
                )
                for counterparty_id, counterparty_account_id, counterparty_card_id, amount, currency, reference in zip(
                    counterparty_ids,
                    counterparty_account_ids,
                    counterparty_card_ids,
                    amounts,
                    currencies,
                    references,
                )
            ],
        )

        return await self.client.post(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

    async def delete_payment_draft(
        self,
        payment_draft_id: UUID,
        **kwargs,
    ) -> dict | DeletePaymentDraft.Response:
        """
        Delete a payment draft with the given ID.
        You can delete a payment draft only if it isn't processed.

        Parameters
        ----------
        payment_draft_id : UUID
            The ID of the payment draft.

        Returns
        -------
        dict | DeletePaymentDraft.Response
            A dict with the information about the payment draft deleted.
        """
        endpoint = DeletePaymentDraft
        path = endpoint.ROUTE.format(payment_draft_id=payment_draft_id)
        params = endpoint.Params()

        return await self.client.delete(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

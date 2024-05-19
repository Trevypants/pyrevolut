from uuid import UUID
from decimal import Decimal
from datetime import datetime

from pydantic_extra_types.pendulum_dt import Duration
from pyrevolut.utils import DateTime
from pyrevolut.api.common import (
    BaseEndpointSync,
    EnumPayoutLinkState,
    EnumPayoutLinkPaymentMethod,
    EnumTransferReasonCode,
)

from pyrevolut.api.payout_links.get import RetrieveListOfPayoutLinks, RetrievePayoutLink
from pyrevolut.api.payout_links.post import CreatePayoutLink, CancelPayoutLink


class EndpointPayoutLinksSync(BaseEndpointSync):
    """The Payout Links API

    Use payout links to send money without having to request full
    banking details of the recipient.
    The recipient must claim the money before the link expires.
    """

    def get_all_payout_links(
        self,
        state: EnumPayoutLinkState | None = None,
        created_before: datetime | DateTime | str | int | float | None = None,
        limit: int | None = None,
        **kwargs,
    ) -> list[dict] | list[RetrieveListOfPayoutLinks.Response]:
        """
        Get all the links that you have created, or use the query parameters to filter the results.

        The links are sorted by the created_at date in reverse chronological order.

        The returned links are paginated. The maximum number of payout links returned per
        page is specified by the limit parameter. To get to the next page, make a
        new request and use the created_at date of the last payout link returned in the previous response.

        Note
        ----
        This feature is available in the UK and the EEA.

        Parameters
        ----------
        state : EnumPayoutLinkState, optional
            The state that the payout link is in. Possible states are:

                created:
                    The payout link has been created, but the amount has not yet been blocked.
                failed:
                    The payout link couldn't be generated due to a failure during transaction booking.
                awaiting:
                    The payout link is awaiting approval.
                active:
                    The payout link can be redeemed.
                expired:
                    The payout link cannot be redeemed because it wasn't claimed before its expiry date.
                cancelled:
                    The payout link cannot be redeemed because it was cancelled.
                processing:
                    The payout link has been redeemed and is being processed.
                processed:
                    The payout link has been redeemed and the money has been transferred to the recipient.
        created_before : datetime | DateTime | str | int | float, optional
            Retrieves links with created_at < created_before.
            The default value is the current date and time at which you are calling the endpoint.

            Provided in ISO 8601 format.
        limit : int, optional
            The maximum number of links returned per page.
            To get to the next page, make a new request and use the
            created_at date of the last payout link returned in the previous
            response as the value for created_before.

            If not provided, the default value is 100.

        Returns
        -------
        list[dict] | list[RetrieveListOfPayoutLinks.Response]
            A list of payout links.
        """
        endpoint = RetrieveListOfPayoutLinks
        path = endpoint.ROUTE
        params = endpoint.Params(
            state=state,
            created_before=created_before,
            limit=limit,
        )

        return self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    def get_payout_link(
        self,
        payout_link_id: UUID,
        **kwargs,
    ) -> dict | RetrievePayoutLink.Response:
        """
        Get the information about a specific link by its ID.

        Note
        ----
        This feature is available in the UK and the EEA.

        Parameters
        ----------
        payout_link_id : UUID
            The ID of the payout link.

        Returns
        -------
        dict | RetrievePayoutLink.Response
            The payout link information.
        """
        endpoint = RetrievePayoutLink
        path = endpoint.ROUTE.format(payout_link_id=payout_link_id)
        params = endpoint.Params()

        return self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    def create_payout_link(
        self,
        counterparty_name: str,
        request_id: str,
        account_id: UUID,
        amount: Decimal,
        currency: str,
        reference: str,
        payout_methods: list[EnumPayoutLinkPaymentMethod],
        save_counterparty: bool | None = None,
        expiry_period: Duration | str | None = None,
        transfer_reason_code: EnumTransferReasonCode | None = None,
        **kwargs,
    ) -> dict | CreatePayoutLink.Response:
        """
        Create a payout link to send money even when you don't have the full
        banking details of the counterparty.
        After you have created the link, send it to the recipient so that
        they can claim the payment.

        Note
        ----
        This feature is available in the UK and the EEA.

        Parameters
        ----------
        counterparty_name : str
            The name of the counterparty provided by the sender.
        request_id : str
            The ID of the request, provided by the sender.

            To ensure that a link payment is not processed multiple times if there
            are network or system errors, the same request_id should be used for
            requests related to the same link.
        account_id : UUID
            The ID of the sender's account.
        amount : Decimal
            The amount of money to be sent.
        currency : str
            The currency of the amount to be sent.
        reference : str
            A reference for the payment.
        payout_methods : list[EnumPayoutLinkPaymentMethod]
            The payout methods that the recipient can use to claim the payment.
            If not provided, the default value is
            [EnumPayoutLinkPaymentMethod.REVOLUT, EnumPayoutLinkPaymentMethod.BANK_ACCOUNT].
        save_counterparty : bool, optional
            Indicates whether to save the recipient as your counterparty upon link claim.
            If false then the counterparty will not show up on your counterparties list,
            for example, when you retrieve your counterparties.
            However, you will still be able to retrieve this counterparty by its ID.

            If you don't choose to save the counterparty on link creation, you can do it later
            from your transactions list in the Business app.

            If not provided, the default value is false.
        expiry_period : Duration | str, optional
            Possible values: >= P1D and <= P7D

            Default value: P7D

            The period after which the payout link expires if not claimed before,
            provided in ISO 8601 format.

            The default and maximum value is 7 days from the link creation.
        transfer_reason_code : EnumTransferReasonCode, optional
            The reason code for the transaction.
            Transactions to certain countries and currencies might require you to
            provide a transfer reason.
            You can check available reason codes with the getTransferReasons operation.

            If a transfer reason is not required for the given currency and country,
            this field is ignored.

        Returns
        -------
        dict | CreatePayoutLink.Response
            The payout link information.
        """
        endpoint = CreatePayoutLink
        path = endpoint.ROUTE
        body = endpoint.Body(
            counterparty_name=counterparty_name,
            save_counterparty=save_counterparty,
            request_id=request_id,
            account_id=account_id,
            amount=amount,
            currency=currency,
            reference=reference,
            payout_methods=payout_methods,
            expiry_period=expiry_period,
            transfer_reasion_code=transfer_reason_code,
        )

        return self.client.post(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

    def cancel_payout_link(
        self,
        payout_link_id: UUID,
        **kwargs,
    ) -> dict | CancelPayoutLink.Response:
        """
        Cancel a payout link.
        You can only cancel a link that hasn't been claimed yet.
        A successful request does not get any content in response.

        Note
        ----
        This feature is available in the UK and the EEA.

        Parameters
        ----------
        payout_link_id : UUID
            The ID of the payout link.

        Returns
        -------
        dict | CancelPayoutLink.Response
            An empty dictionary.
        """
        endpoint = CancelPayoutLink
        path = endpoint.ROUTE.format(payout_link_id=payout_link_id)
        body = endpoint.Body()

        return self.client.post(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

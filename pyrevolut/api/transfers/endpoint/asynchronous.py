from uuid import UUID
from decimal import Decimal

from pyrevolut.api.common import (
    BaseEndpointAsync,
    EnumChargeBearer,
    EnumTransferReasonCode,
)

from pyrevolut.api.transfers.get import GetTransferReasons
from pyrevolut.api.transfers.post import (
    CreateTransferToAnotherAccount,
    MoveMoneyBetweenAccounts,
)


class EndpointTransfersAsync(BaseEndpointAsync):
    """The async Transfers API

    Move funds in the same currency between accounts of your business,
    or make payments to your counterparties.
    """

    async def get_transfer_reasons(
        self,
        **kwargs,
    ) -> list[dict] | list[GetTransferReasons.Response]:
        """
        In order to initiate a transfer in certain currencies and countries,
        you must provide a transfer reason.
        With this endpoint you can retrieve all transfer reasons available to your business account
        per country and currency.

        After you retrieve the results, use the appropriate reason code in the transfer_reason_code
        field when making a transfer to a counterparty or creating a payout link.

        Parameters
        ----------
        None

        Returns
        -------
        list[dict] | list[GetTransferReasons.Response]
            A list of transfer reasons.
        """
        endpoint = GetTransferReasons
        path = endpoint.ROUTE
        params = endpoint.Params()

        return await self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    async def create_transfer_to_another_account(
        self,
        request_id: str,
        account_id: UUID,
        counterparty_id: UUID,
        amount: Decimal,
        currency: str,
        counterparty_account_id: UUID | None = None,
        counterparty_card_id: UUID | None = None,
        reference: str | None = None,
        charge_bearer: EnumChargeBearer | None = None,
        transfer_reason_code: EnumTransferReasonCode | None = None,
        **kwargs,
    ) -> dict | CreateTransferToAnotherAccount.Response:
        """
        Make a payment to a counterparty.
        The resulting transaction has the type transfer.

        If you make the payment to another Revolut account, either business or personal,
        the transaction is executed instantly.

        If the counterparty has multiple payment methods available, for example, 2 accounts,
        or 1 account and 1 card, you must specify the account or card to which you want to
        transfer the money (receiver.account_id or receiver.card_id respectively).

        Caution
        -------
        Due to PSD2 Strong Customer Authentication regulations, this endpoint is
        only available for customers on Revolut Business Company plans. If you're a
        freelancer and wish to make payments via our API, we advise that you instead
        leverage our Payment drafts (/payment-drafts) endpoint.

        Parameters
        ----------
        request_id : str
            The ID of the request, provided by you.
            It helps you identify the transaction in your system.
            To ensure that a transfer is not processed multiple times if
            there are network or system errors, the same request_id should be used
            for requests related to the same transfer.
        account_id : UUID
            The ID of the account that you transfer the funds from.
        counterparty_id : UUID
            The ID of the receiving counterparty.
        amount : Decimal
            The amount of money to transfer.
        currency : str
            The currency of the transfer.
        counterparty_account_id : UUID, optional
            The ID of the receiving counterparty's account, which can be own account.
            Used for bank transfers.
            If the counterparty has multiple payment methods available, use it to
            specify the account to which you want to send the money.
        counterparty_card_id : UUID, optional
            The ID of the receiving counterparty's card. Used for card transfers.
            If the counterparty has multiple payment methods available, use it to
            specify the card to which you want to send the money.
        reference : str, optional
            A reference for the transfer.
        charge_bearer : EnumChargeBearer, optional
            The party to which any transaction fees are charged if the resulting
            transaction route has associated fees. Some transactions with fees might
            not be possible with the specified option, in which case error 3287 is returned.

            Possible values:
            - shared: The transaction fees are shared between the sender and the receiver.
            - debtor: The sender pays the transaction fees.
        transfer_reason_code : EnumTransferReasonCode, optional
            The reason code for the transaction.
            Transactions to certain countries and currencies might require
            you to provide a transfer reason.
            You can check available reason codes with the getTransferReasons operation.

            If a transfer reason is not required for the given currency and country,
            this field is ignored.

        Returns
        -------
        dict | CreateTransferToAnotherAccount.Response
            The details of the transfer.
        """
        endpoint = CreateTransferToAnotherAccount
        path = endpoint.ROUTE
        body = endpoint.Body(
            request_id=request_id,
            account_id=account_id,
            receiver=endpoint.Body.ModelReceiver(
                counterparty_id=counterparty_id,
                account_id=counterparty_account_id,
                card_id=counterparty_card_id,
            ),
            amount=amount,
            currency=currency,
            reference=reference,
            charge_bearer=charge_bearer,
            transfer_reason_code=transfer_reason_code,
        )

        return await self.client.post(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

    async def move_money_between_accounts(
        self,
        request_id: str,
        source_account_id: UUID,
        target_account_id: UUID,
        amount: Decimal,
        currency: str,
        reference: str | None = None,
        **kwargs,
    ) -> dict | MoveMoneyBetweenAccounts.Response:
        """
        Move money between the Revolut accounts of the business in the same currency.

        The resulting transaction has the type transfer.

        Parameters
        ----------
        request_id : str
            The ID of the request, provided by you.
            It helps you identify the transaction in your system.
            To ensure that a transfer is not processed multiple times if
            there are network or system errors, the same request_id should be used
            for requests related to the same transfer.
        source_account_id : UUID
            The ID of the source account that you transfer the funds from.
        target_account_id : UUID
            The ID of the target account that you transfer the funds to.
        amount : Decimal
            The amount of the funds to be transferred.
        currency : str
            The ISO 4217 currency of the funds to be transferred.
        reference : str, optional
            The reference for the funds transfer.

        Returns
        -------
        dict | MoveMoneyBetweenAccounts.Response
            The details of the transfer.
        """
        endpoint = MoveMoneyBetweenAccounts
        path = endpoint.ROUTE
        body = endpoint.Body(
            request_id=request_id,
            source_account_id=source_account_id,
            target_account_id=target_account_id,
            amount=amount,
            currency=currency,
            reference=reference,
        )

        return await self.client.post(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

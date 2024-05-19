from uuid import UUID

from pyrevolut.exceptions import InvalidEnvironmentException
from pyrevolut.api.common import (
    BaseEndpointAsync,
    EnumTransactionState,
    EnumSimulateTransferStateAction,
)
from pyrevolut.api.simulations.post import (
    SimulateAccountTopup,
    SimulateTransferStateUpdate,
)


class EndpointSimulationsAsync(BaseEndpointAsync):
    """The async Simulations API

    The Simulations API is only available in the Sandbox environment.
    It lets you simulate certain events that are otherwise only possible in the production environment,
    such as your account's top-up and transfer state changes.
    """

    async def simulate_account_topup(
        self,
        account_id: UUID,
        amount: float,
        currency: str,
        reference: str | None = None,
        state: EnumTransactionState | None = None,
        **kwargs,
    ) -> dict | SimulateAccountTopup.Response:
        """
        Simulate a top-up of your account in the Sandbox environment.

        This is useful during testing, when you run out of money in your test account
        and need to add more.

        Parameters
        ----------
        account_id : UUID
            The ID of the account that you want to top up.
        amount : float
            The amount with which you want to top up the account. Must be <= 10000
        currency : str
            The currency of the top-up amount. Must be a valid ISO 4217 currency code.
        reference : str, optional
            A short description for your top up.
            Default value: 'Test Top-up' if not provided.
        state : EnumTransactionState, optional
            The state to which you want to set the top-up transaction.

            If not provided, the default value is 'completed'.

            Possible values:

                pending:
                    The transaction is pending until it's being processed.
                    If the transfer is made between Revolut accounts,
                    this state is skipped and the transaction is executed instantly.
                completed:
                    The transaction was successful.
                failed:
                    The transaction was unsuccessful. This can happen for a variety of reasons,
                    for example, invalid API calls, blocked payments, etc.
                reverted:
                    The transaction was reverted. This can happen for a variety of reasons,
                    for example, the receiver being inaccessible.

        Returns
        -------
        dict | SimulateAccountTopup.Response
            The top-up transaction information.
        """
        self.__check_sandbox()
        endpoint = SimulateAccountTopup
        path = endpoint.ROUTE
        body = endpoint.Body(
            account_id=account_id,
            amount=amount,
            currency=currency,
            reference=reference,
            state=state,
        )

        return await self.client.post(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

    async def simulate_transfer_state_update(
        self,
        transfer_id: UUID,
        action: EnumSimulateTransferStateAction,
        **kwargs,
    ) -> dict | SimulateTransferStateUpdate.Response:
        """
        Simulate a transfer state change in the Sandbox environment.

        For example, after you make a transfer in Sandbox, you can change its
        state to completed.

        The resulting state is final and cannot be changed.

        Parameters
        ----------
        transfer_id : UUID
            The ID of the transfer whose state you want to update.
        action : EnumSimulateTransferStateAction
            The action you want to perform on the transfer. Possible values:

                complete:
                    Simulate a completed transfer.
                revert:
                    Simulate a reverted transfer.
                decline:
                    Simulate a declined transfer.
                fail:
                    Simulate a failed transfer.

        Returns
        -------
        dict | SimulateTransferStateUpdate.Response
            The updated transfer information.
        """
        self.__check_sandbox()
        endpoint = SimulateTransferStateUpdate
        path = endpoint.ROUTE.format(transfer_id=transfer_id, action=action)
        body = endpoint.Body()

        return await self.client.post(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

    def __check_sandbox(self):
        """
        Check if the sandbox is enabled.

        Raises
        ------
        InvalidEnvironmentException
            If the sandbox is enabled.
        """
        if not self.client.sandbox:
            raise InvalidEnvironmentException(
                "This feature is only available in the Sandbox."
            )

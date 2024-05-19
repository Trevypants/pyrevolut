from uuid import UUID

from pyrevolut.api.common import BaseEndpointSync

from pyrevolut.api.accounts.get import (
    RetrieveAllAccounts,
    RetrieveAnAccount,
    RetrieveFullBankDetails,
)


class EndpointAccountsSync(BaseEndpointSync):
    """The Accounts API
    Get the balances, full banking details, and other details of your business accounts.
    """

    def get_all_accounts(
        self,
        **kwargs,
    ) -> list[dict] | list[RetrieveAllAccounts.Response]:
        """
        Get a list of all your accounts.

        Parameters
        ----------
        None

        Returns
        -------
        list[dict] | list[RetrieveAllAccounts.Response]
            The list of all your accounts
        """
        endpoint = RetrieveAllAccounts
        path = endpoint.ROUTE
        params = endpoint.Params()

        return self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    def get_account(
        self,
        account_id: UUID,
        **kwargs,
    ) -> dict | RetrieveAnAccount.Response:
        """
        Get the information about one of your accounts. Specify the account by its ID.

        Parameters
        ----------
        account_id : UUID
            The account ID.

        Returns
        -------
        dict | RetrieveAnAccount.Response
            The information about the account
        """
        endpoint = RetrieveAnAccount
        path = endpoint.ROUTE.format(account_id=account_id)
        params = endpoint.Params()

        return self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    def get_full_bank_details(
        self,
        account_id: UUID,
        **kwargs,
    ) -> dict | RetrieveFullBankDetails.Response:
        """
        Get all the bank details of one of your accounts. Specify the account by its ID.

        Parameters
        ----------
        account_id : UUID
            The account ID.

        Returns
        -------
        dict | RetrieveFullBankDetails.Response
            The bank details of the account
        """
        endpoint = RetrieveFullBankDetails
        path = endpoint.ROUTE.format(account_id=account_id)
        params = endpoint.Params()

        return self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

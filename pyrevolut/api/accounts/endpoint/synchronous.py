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
    ):
        """
        Get a list of all your accounts.

        Parameters
        ----------
        None

        Returns
        -------
        list
            The list of all your accounts
        """
        endpoint = RetrieveAllAccounts
        path = endpoint.ROUTE
        params = endpoint.Params()

        response = self.client.get(
            path=path,
            params=params,
            **kwargs,
        )

        return [endpoint.Response(**resp).model_dump() for resp in response.json()]

    def get_account(
        self,
        account_id: UUID,
        **kwargs,
    ):
        """
        Get the information about one of your accounts. Specify the account by its ID.

        Parameters
        ----------
        account_id : UUID
            The account ID.

        Returns
        -------
        dict
            The information about the account
        """
        endpoint = RetrieveAnAccount
        path = endpoint.ROUTE.format(account_id=account_id)
        params = endpoint.Params()

        response = self.client.get(
            path=path,
            params=params,
            **kwargs,
        )

        return endpoint.Response(**response.json()).model_dump()

    def get_full_bank_details(
        self,
        account_id: UUID,
        **kwargs,
    ):
        """
        Get all the bank details of one of your accounts. Specify the account by its ID.

        Parameters
        ----------
        account_id : UUID
            The account ID.

        Returns
        -------
        dict
            The bank details of the account
        """
        endpoint = RetrieveFullBankDetails
        path = endpoint.ROUTE.format(account_id=account_id)
        params = endpoint.Params()

        response = self.client.get(
            path=path,
            params=params,
            **kwargs,
        )

        return endpoint.Response(**response.json()[0]).model_dump()

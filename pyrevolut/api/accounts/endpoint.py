from uuid import UUID
from httpx import Response

from pyrevolut.api.common import BaseEndpoint

from .get import RetrieveAllAccounts, RetrieveAnAccount, RetrieveFullBankDetails


class EndpointAccounts(BaseEndpoint):
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

        return [endpoint.Response(**resp) for resp in response.json()]

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

        response: Response = self.client.get(
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

        response: Response = self.client.get(
            path=path,
            params=params,
            **kwargs,
        )

        return endpoint.Response(**response.json()).model_dump()

    async def aget_all_accounts(
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

        response = await self.client.aget(
            path=path,
            params=params,
            **kwargs,
        )

        return [endpoint.Response(**resp) for resp in response.json()]

    async def aget_account(
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

        response: Response = await self.client.aget(
            path=path,
            params=params,
            **kwargs,
        )

        return endpoint.Response(**response.json()).model_dump()

    async def aget_full_bank_details(
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

        response: Response = await self.client.aget(
            path=path,
            params=params,
            **kwargs,
        )

        return endpoint.Response(**response.json()).model_dump()

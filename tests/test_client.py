import time
import asyncio
import pytest
import random

from pyrevolut.client import Client, AsyncClient
from pyrevolut.api.accounts.get import RetrieveAllAccounts, RetrieveAnAccount


def test_sync_return_dict(sync_client: Client):
    """Test the sync `return_dict` argument"""

    # By default return_dict is True
    accounts_all = sync_client.Accounts.get_all_accounts()
    time.sleep(random.randint(1, 3))
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, dict)

    # Set return_dict to False
    sync_client.return_dict = False
    accounts_all = sync_client.Accounts.get_all_accounts()
    time.sleep(random.randint(1, 3))
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, RetrieveAllAccounts.Response)

    # Get Account
    for account in accounts_all:
        account_id = account.id
        account = sync_client.Accounts.get_account(account_id)
        time.sleep(random.randint(1, 3))
        assert isinstance(account, RetrieveAnAccount.Response)
        assert account.id == account_id

    # Set return_dict back to True
    sync_client.return_dict = True


@pytest.mark.asyncio
async def test_async_return_dict(async_client: AsyncClient):
    """Test the async `return_dict` argument"""

    # By default return_dict is True
    accounts_all = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, dict)

    # Set return_dict to False
    async_client.return_dict = False
    accounts_all = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, RetrieveAllAccounts.Response)

    # Get Account
    for account in accounts_all:
        account_id = account.id
        account = await async_client.Accounts.get_account(account_id)
        await asyncio.sleep(random.randint(1, 3))
        assert isinstance(account, RetrieveAnAccount.Response)
        assert account.id == account_id

    # Set return_dict back to True
    async_client.return_dict = True

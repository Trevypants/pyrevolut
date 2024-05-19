import time
import asyncio
import pytest
import random

from pyrevolut.client import Client, AsyncClient
from pyrevolut.api.accounts.get import RetrieveAllAccounts, RetrieveAnAccount


def test_sync_return_type(sync_client: Client):
    """Test the sync `return_type` argument"""

    # By default return_type is 'dict'
    accounts_all = sync_client.Accounts.get_all_accounts()
    time.sleep(random.randint(1, 3))
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, dict)
        account_id = account["id"]
        account = sync_client.Accounts.get_account(account_id)
        time.sleep(random.randint(1, 3))
        assert isinstance(account, dict)
        assert account["id"] == account_id

    # Set return_dict to 'model'
    sync_client.return_type = "model"
    accounts_all = sync_client.Accounts.get_all_accounts()
    time.sleep(random.randint(1, 3))
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, RetrieveAllAccounts.Response)
        account_id = account.id
        account = sync_client.Accounts.get_account(account_id)
        time.sleep(random.randint(1, 3))
        assert isinstance(account, RetrieveAnAccount.Response)
        assert account.id == account_id

    # Set return_type to 'raw'
    sync_client.return_type = "raw"
    accounts_all = sync_client.Accounts.get_all_accounts()
    time.sleep(random.randint(1, 3))
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, dict)
        account_id = account["id"]
        account = sync_client.Accounts.get_account(account_id)
        time.sleep(random.randint(1, 3))
        assert isinstance(account, dict)
        assert account["id"] == account_id

    # Set return_type back to 'dict'
    sync_client.return_type = "dict"


@pytest.mark.asyncio
async def test_async_return_type(async_client: AsyncClient):
    """Test the async `return_type` argument"""

    # By default return_type is 'dict'
    accounts_all = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, dict)
        account_id = account["id"]
        account = await async_client.Accounts.get_account(account_id)
        await asyncio.sleep(random.randint(1, 3))
        assert isinstance(account, dict)
        assert account["id"] == account_id

    # Set return_dict to 'model'
    async_client.return_type = "model"
    accounts_all = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, RetrieveAllAccounts.Response)
        account_id = account.id
        account = await async_client.Accounts.get_account(account_id)
        await asyncio.sleep(random.randint(1, 3))
        assert isinstance(account, RetrieveAnAccount.Response)
        assert account.id == account_id

    # Set return_type to 'raw'
    async_client.return_type = "raw"
    accounts_all = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, dict)
        account_id = account["id"]
        account = await async_client.Accounts.get_account(account_id)
        await asyncio.sleep(random.randint(1, 3))
        assert isinstance(account, dict)
        assert account["id"] == account_id

    # Set return_type back to 'dict'
    async_client.return_type = "dict"

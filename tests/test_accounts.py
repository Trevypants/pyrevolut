import pytest

from pyrevolut.client import Client, AsyncClient


@pytest.mark.asyncio
async def test_async_get_all_accounts(async_client: AsyncClient):
    """Test the async `get_all_accounts` accounts method"""
    # Get Accounts
    accounts_all = await async_client.Accounts.get_all_accounts()
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, dict)


def test_sync_get_all_accounts(sync_client: Client):
    """Test the sync `get_all_accounts` accounts method"""
    # Get Accounts
    accounts_all = sync_client.Accounts.get_all_accounts()
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, dict)

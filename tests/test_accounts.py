import time
import asyncio
import pytest

from pyrevolut.client import Client, AsyncClient


def test_sync_get_all_accounts(sync_client: Client):
    """Test the sync `get_all_accounts` accounts method"""
    # Get Accounts
    accounts_all = sync_client.Accounts.get_all_accounts()
    time.sleep(1)
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, dict)


def test_sync_get_account(sync_client: Client):
    """Test the sync `get_account` accounts method"""
    # Get Accounts
    accounts_all = sync_client.Accounts.get_all_accounts()
    time.sleep(1)
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, dict)

    # Get Account
    for account in accounts_all:
        account_id = account["id"]
        account = sync_client.Accounts.get_account(account_id)
        time.sleep(1)
        assert isinstance(account, dict)
        assert account["id"] == account_id


def test_sync_get_full_bank_details(sync_client: Client):
    """Test the sync `get_full_bank_details` accounts method"""
    # Get Accounts
    accounts_all = sync_client.Accounts.get_all_accounts()
    time.sleep(1)
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, dict)

    # Get Full Bank Details
    for account in accounts_all:
        account_id = account["id"]
        bank_details = sync_client.Accounts.get_full_bank_details(account_id)
        time.sleep(1)
        assert isinstance(bank_details, dict)


@pytest.mark.asyncio
async def test_async_get_all_accounts(async_client: AsyncClient):
    """Test the async `get_all_accounts` accounts method"""
    # Get Accounts
    accounts_all = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(1)
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, dict)


@pytest.mark.asyncio
async def test_async_get_account(async_client: AsyncClient):
    """Test the async `get_account` accounts method"""
    # Get Accounts
    accounts_all = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(1)
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, dict)

    # Get Account
    for account in accounts_all:
        account_id = account["id"]
        account = await async_client.Accounts.get_account(account_id)
        await asyncio.sleep(1)
        assert isinstance(account, dict)
        assert account["id"] == account_id


@pytest.mark.asyncio
async def test_async_get_full_bank_details(async_client: AsyncClient):
    """Test the async `get_full_bank_details` accounts method"""
    # Get Accounts
    accounts_all = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(1)
    assert isinstance(accounts_all, list)
    for account in accounts_all:
        assert isinstance(account, dict)

    # Get Full Bank Details
    for account in accounts_all:
        account_id = account["id"]
        bank_details = await async_client.Accounts.get_full_bank_details(account_id)
        await asyncio.sleep(1)
        assert isinstance(bank_details, dict)

import time
import asyncio
import pytest
import random

from pyrevolut.client import Client, AsyncClient
from pyrevolut.api.accounts.get import RetrieveAllAccounts, RetrieveAnAccount
from pyrevolut.utils.auth.creds import ModelCreds


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


def test_custom_save_and_load_functions():
    # Create a temporary file for testing
    fake_creds = {
        "certificate": {
            "public": "some-public-key",
            "private": "some-private-key",
            "expiration_dt": "2500-01-01T00:00:00Z",
        },
        "client_assert_jwt": {
            "jwt": "some-jwt",
            "expiration_dt": "2500-01-01T00:00:00Z",
        },
        "tokens": {
            "access_token": "some-access-token",
            "refresh_token": "some-refresh-token",
            "token_type": "bearer",
            "access_token_expiration_dt": "2500-01-01T00:00:00Z",
            "refresh_token_expiration_dt": "2500-01-01T00:00:00Z",
        },
    }

    # Define the custom save function
    def custom_save_fn(model: ModelCreds):
        return True

    # Define the custom load function
    def custom_load_fn():
        return ModelCreds(**fake_creds)

    # Create a new Client instance with the custom save and load functions
    client = Client(custom_save_fn=custom_save_fn, custom_load_fn=custom_load_fn)

    # Save the credentials
    client.save_credentials()

    # Load the credentials
    client.load_credentials()

    # Assert that the loaded credentials match the saved credentials
    assert client.credentials == custom_load_fn()

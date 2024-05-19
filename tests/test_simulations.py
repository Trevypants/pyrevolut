import time
import asyncio
from decimal import Decimal
import pytest
import random

from pyrevolut.client import Client
from pyrevolut.api import (
    EnumAccountState,
    EnumTransactionState,
)


def test_sync_simulate_account_topup(sync_client: Client):
    """Test the sync `simulate_account_topup` simulations method"""

    # Get all accounts
    accounts = sync_client.Accounts.get_all_accounts()
    time.sleep(random.randint(1, 3))

    # Get GBP account
    gbp_account = next(
        account
        for account in accounts
        if account["currency"] == "GBP" and account["state"] == EnumAccountState.ACTIVE
    )

    # Get EUR account
    eur_account = next(
        account
        for account in accounts
        if account["currency"] == "EUR" and account["state"] == EnumAccountState.ACTIVE
    )

    # Simulate a top-up of the GBP account
    response = sync_client.Simulations.simulate_account_topup(
        account_id=gbp_account["id"],
        amount=Decimal("1.00"),
        currency="GBP",
        reference="Sugar Daddy <3",
        state=EnumTransactionState.COMPLETED,
    )
    time.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.COMPLETED

    # Get the GBP account by ID
    account = sync_client.Accounts.get_account(account_id=gbp_account["id"])
    time.sleep(random.randint(1, 3))
    assert account["balance"] == gbp_account["balance"] + Decimal("1.00")

    # Simulate a top-up of the EUR account
    response = sync_client.Simulations.simulate_account_topup(
        account_id=eur_account["id"],
        amount=Decimal("1.00"),
        currency="EUR",
        reference="Sugar Daddy <3",
        state=EnumTransactionState.COMPLETED,
    )
    time.sleep(random.randint(1, 3))

    # Get the EUR account by ID
    account = sync_client.Accounts.get_account(account_id=eur_account["id"])
    time.sleep(random.randint(1, 3))
    assert account["balance"] == eur_account["balance"] + Decimal("1.00")


def test_sync_simulate_transfer_state_update(sync_client: Client):
    """Test the sync `simulate_transfer_state_update` simulations method"""

    # TODO: Implement the test


@pytest.mark.asyncio
async def test_async_simulate_account_topup(async_client: Client):
    """Test the async `simulate_account_topup` simulations method"""

    # Get all accounts
    accounts = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(random.randint(1, 3))

    # Get GBP account
    gbp_account = next(
        account
        for account in accounts
        if account["currency"] == "GBP" and account["state"] == EnumAccountState.ACTIVE
    )

    # Get EUR account
    eur_account = next(
        account
        for account in accounts
        if account["currency"] == "EUR" and account["state"] == EnumAccountState.ACTIVE
    )

    # Simulate a top-up of the GBP account
    response = await async_client.Simulations.simulate_account_topup(
        account_id=gbp_account["id"],
        amount=Decimal("1.00"),
        currency="GBP",
        reference="Sugar Daddy <3",
        state=EnumTransactionState.COMPLETED,
    )
    await asyncio.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.COMPLETED

    # Get the GBP account by ID
    account = await async_client.Accounts.get_account(account_id=gbp_account["id"])
    await asyncio.sleep(random.randint(1, 3))
    assert account["balance"] == gbp_account["balance"] + Decimal("1.00")

    # Simulate a top-up of the EUR account
    response = await async_client.Simulations.simulate_account_topup(
        account_id=eur_account["id"],
        amount=Decimal("1.00"),
        currency="EUR",
        reference="Sugar Daddy <3",
        state=EnumTransactionState.COMPLETED,
    )

    # Get the EUR account by ID
    account = await async_client.Accounts.get_account(account_id=eur_account["id"])
    await asyncio.sleep(random.randint(1, 3))
    assert account["balance"] == eur_account["balance"] + Decimal("1.00")


@pytest.mark.asyncio
async def test_async_simulate_transfer_state_update(async_client: Client):
    """Test the async `simulate_transfer_state_update` simulations method"""

    # TODO: Implement the test

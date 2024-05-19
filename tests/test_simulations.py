import time
import asyncio
from uuid import uuid4
from decimal import Decimal
import pytest
import random

from pyrevolut.client import Client
from pyrevolut.api import (
    EnumAccountState,
    EnumTransactionState,
    EnumTransferReasonCode,
    EnumSimulateTransferStateAction,
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

    # Get all accounts
    accounts = sync_client.Accounts.get_all_accounts()
    time.sleep(random.randint(1, 3))

    # Get EUR account
    eur_account = next(
        account
        for account in accounts
        if account["currency"] == "EUR"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"]
    )
    eur_balance = eur_account["balance"]

    # If there is no EUR balance, simulate a top up
    if eur_balance < Decimal("1"):
        response = sync_client.Simulations.simulate_account_topup(
            account_id=eur_account["id"],
            amount=Decimal("1"),
            currency="EUR",
            reference="PyRevolut Test",
            state=EnumTransactionState.COMPLETED,
        )
        time.sleep(random.randint(1, 3))
        assert response["state"] == EnumTransactionState.COMPLETED

    # Get all counterparties
    counterparties = sync_client.Counterparties.get_all_counterparties()

    # Get a EUR counterparty with an IBAN
    eur_counterparties = []
    for counterparty in counterparties:
        counterparty_accounts = counterparty.get("accounts") or []
        for account in counterparty_accounts:
            if account.get("currency") == "EUR" and account.get("iban") is not None:
                eur_counterparties.append(counterparty)

    # Get the first EUR counterparty
    eur_counterparty = eur_counterparties[0]
    eur_counterparty_account = [
        acc
        for acc in eur_counterparty.get("accounts") or []
        if acc["currency"] == "EUR" and acc["iban"] is not None
    ][0]

    # Create a transfer to the EUR counterparty
    response = sync_client.Transfers.create_transfer_to_another_account(
        request_id=str(uuid4()),
        account_id=eur_account["id"],
        counterparty_id=eur_counterparty["id"],
        amount=Decimal("1"),
        currency="EUR",
        counterparty_account_id=eur_counterparty_account["id"],
        reference="PyRevolut Test",
        transfer_reason_code=EnumTransferReasonCode.FAMILY_SUPPORT,
    )
    time.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.PENDING

    # Check balance
    account = sync_client.Accounts.get_account(account_id=eur_account["id"])
    time.sleep(random.randint(1, 3))
    assert account["balance"] == eur_balance - Decimal("1")

    # Decline the transfer
    response = sync_client.Simulations.simulate_transfer_state_update(
        transfer_id=response["id"],
        action=EnumSimulateTransferStateAction.DECLINE,
    )
    time.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.DECLINED

    # Check balance
    account = sync_client.Accounts.get_account(account_id=eur_account["id"])
    time.sleep(random.randint(1, 3))
    assert account["balance"] == eur_balance


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

    # Get all accounts
    accounts = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(random.randint(1, 3))

    # Get EUR account
    eur_account = next(
        account
        for account in accounts
        if account["currency"] == "EUR"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"]
    )
    eur_balance = eur_account["balance"]

    # If there is no EUR balance, simulate a top up
    if eur_balance < Decimal("1"):
        response = await async_client.Simulations.simulate_account_topup(
            account_id=eur_account["id"],
            amount=Decimal("1"),
            currency="EUR",
            reference="PyRevolut Test",
            state=EnumTransactionState.COMPLETED,
        )
        await asyncio.sleep(random.randint(1, 3))
        assert response["state"] == EnumTransactionState.COMPLETED

    # Get all counterparties
    counterparties = await async_client.Counterparties.get_all_counterparties()

    # Get a EUR counterparty with an IBAN
    eur_counterparties = []
    for counterparty in counterparties:
        counterparty_accounts = counterparty.get("accounts") or []
        for account in counterparty_accounts:
            if account.get("currency") == "EUR" and account.get("iban") is not None:
                eur_counterparties.append(counterparty)

    # Get the first EUR counterparty
    eur_counterparty = eur_counterparties[0]
    eur_counterparty_account = [
        acc
        for acc in eur_counterparty.get("accounts") or []
        if acc["currency"] == "EUR" and acc["iban"] is not None
    ][0]

    # Create a transfer to the EUR counterparty
    response = await async_client.Transfers.create_transfer_to_another_account(
        request_id=str(uuid4()),
        account_id=eur_account["id"],
        counterparty_id=eur_counterparty["id"],
        amount=Decimal("1"),
        currency="EUR",
        counterparty_account_id=eur_counterparty_account["id"],
        reference="PyRevolut Test",
        transfer_reason_code=EnumTransferReasonCode.FAMILY_SUPPORT,
    )
    await asyncio.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.PENDING

    # Check balance
    account = await async_client.Accounts.get_account(account_id=eur_account["id"])
    await asyncio.sleep(random.randint(1, 3))
    assert account["balance"] == eur_balance - Decimal("1")

    # Decline the transfer
    response = await async_client.Simulations.simulate_transfer_state_update(
        transfer_id=response["id"],
        action=EnumSimulateTransferStateAction.DECLINE,
    )
    await asyncio.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.DECLINED

    # Check balance
    account = await async_client.Accounts.get_account(account_id=eur_account["id"])
    await asyncio.sleep(random.randint(1, 3))
    assert account["balance"] == eur_balance

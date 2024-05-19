import time
import asyncio
from uuid import uuid4
import random

import pytest

from pyrevolut.client import Client
from pyrevolut.api import (
    EnumAccountState,
    EnumTransactionState,
    EnumTransferReasonCode,
    EnumSimulateTransferStateAction,
)


def test_sync_get_transfer_reasons(sync_client: Client):
    """Test the sync `get_transfer_reasons` transfers method"""
    # Get all transfer reasons
    transfer_reasons = sync_client.Transfers.get_transfer_reasons()
    time.sleep(random.randint(1, 3))
    assert isinstance(transfer_reasons, list)
    for transfer_reason in transfer_reasons:
        assert isinstance(transfer_reason, dict)


def test_sync_move_money_between_accounts(sync_client: Client):
    """Test the sync `move_money_between_accounts` transfers method"""

    # Get all accounts
    accounts = sync_client.Accounts.get_all_accounts()
    time.sleep(random.randint(1, 3))

    # Get both GBP
    gbp_account1 = next(
        account
        for account in accounts
        if account["currency"] == "GBP"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"] > 0.0
    )
    gbp_balance1 = gbp_account1["balance"]
    gbp_account2 = next(
        account
        for account in accounts
        if account["currency"] == "GBP"
        and account["state"] == EnumAccountState.ACTIVE
        and account["id"] != gbp_account1["id"]
    )
    gbp_balance2 = gbp_account2["balance"]

    # Move 1 GBP from Account 1 to Account 2
    response = sync_client.Transfers.move_money_between_accounts(
        request_id=str(uuid4()),
        source_account_id=gbp_account1["id"],
        target_account_id=gbp_account2["id"],
        amount=1.0,
        currency="GBP",
        reference="PyRevolut Test",
    )
    time.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.COMPLETED

    # Check balances
    accounts = sync_client.Accounts.get_all_accounts()
    time.sleep(random.randint(1, 3))
    gbp_balance1_new = next(
        account["balance"]
        for account in accounts
        if account["id"] == gbp_account1["id"]
    )
    gbp_balance2_new = next(
        account["balance"]
        for account in accounts
        if account["id"] == gbp_account2["id"]
    )
    assert gbp_balance2_new == gbp_balance2 + 1.0
    assert gbp_balance1_new == gbp_balance1 - 1.0

    # Move 1 GBP from Account 2 to Account 1
    response = sync_client.Transfers.move_money_between_accounts(
        request_id=str(uuid4()),
        source_account_id=gbp_account2["id"],
        target_account_id=gbp_account1["id"],
        amount=1.0,
        currency="GBP",
        reference="PyRevolut Test",
    )
    time.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.COMPLETED

    # Check balances
    accounts = sync_client.Accounts.get_all_accounts()
    time.sleep(random.randint(1, 3))
    gbp_balance1_new = next(
        account["balance"]
        for account in accounts
        if account["id"] == gbp_account1["id"]
    )
    gbp_balance2_new = next(
        account["balance"]
        for account in accounts
        if account["id"] == gbp_account2["id"]
    )
    assert gbp_balance2_new == gbp_balance2
    assert gbp_balance1_new == gbp_balance1


def test_sync_create_transfer_to_another_account(sync_client: Client):
    """Test the sync `create_transfer_to_another_account` transfers method"""

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

    # Get GBP account
    gbp_account = next(
        account
        for account in accounts
        if account["currency"] == "GBP"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"]
    )
    gbp_balance = gbp_account["balance"]

    # If there is no EUR balance, simulate a top up
    if eur_balance < 1.0:
        response = sync_client.Simulations.simulate_account_topup(
            account_id=eur_account["id"],
            amount=1.0,
            currency="EUR",
            reference="PyRevolut Test",
            state=EnumTransactionState.COMPLETED,
        )
        time.sleep(random.randint(1, 3))
        assert response["state"] == EnumTransactionState.COMPLETED

    # If there is no GBP balance, simulate a top up
    if gbp_balance < 1.0:
        response = sync_client.Simulations.simulate_account_topup(
            account_id=gbp_account["id"],
            amount=1.0,
            currency="GBP",
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

    # Create a transfer from the EUR account to the EUR counterparty
    response = sync_client.Transfers.create_transfer_to_another_account(
        request_id=str(uuid4()),
        account_id=eur_account["id"],
        counterparty_id=eur_counterparty["id"],
        amount=1.0,
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
    assert account["balance"] == eur_balance - 1.0

    # Complete the transfer via simulation
    response = sync_client.Simulations.simulate_transfer_state_update(
        transfer_id=response["id"],
        action=EnumSimulateTransferStateAction.COMPLETE,
    )
    time.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.COMPLETED

    # Create a transfer from the GBP account to the EUR counterparty
    response = sync_client.Transfers.create_transfer_to_another_account(
        request_id=str(uuid4()),
        account_id=gbp_account["id"],
        counterparty_id=eur_counterparty["id"],
        amount=1.0,
        currency="EUR",
        counterparty_account_id=eur_counterparty_account["id"],
        reference="PyRevolut Test",
        transfer_reason_code=EnumTransferReasonCode.FAMILY_SUPPORT,
    )
    time.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.PENDING

    # Check balance
    account = sync_client.Accounts.get_account(account_id=gbp_account["id"])
    time.sleep(random.randint(1, 3))
    assert account["balance"] < gbp_balance  # Not exact because of the exchange rate

    # Complete the transfer via simulation
    response = sync_client.Simulations.simulate_transfer_state_update(
        transfer_id=response["id"],
        action=EnumSimulateTransferStateAction.COMPLETE,
    )
    time.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.COMPLETED


@pytest.mark.asyncio
async def test_async_get_transfer_reasons(async_client: Client):
    """Test the async `get_transfer_reasons` transfers method"""
    # Get all transfer reasons
    transfer_reasons = await async_client.Transfers.get_transfer_reasons()
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(transfer_reasons, list)
    for transfer_reason in transfer_reasons:
        assert isinstance(transfer_reason, dict)


@pytest.mark.asyncio
async def test_async_move_money_between_accounts(async_client: Client):
    """Test the async `move_money_between_accounts` transfers method"""

    # Get all accounts
    accounts = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(random.randint(1, 3))

    # Get both GBP
    gbp_account1 = next(
        account
        for account in accounts
        if account["currency"] == "GBP"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"] > 0.0
    )
    gbp_balance1 = gbp_account1["balance"]
    gbp_account2 = next(
        account
        for account in accounts
        if account["currency"] == "GBP"
        and account["state"] == EnumAccountState.ACTIVE
        and account["id"] != gbp_account1["id"]
    )
    gbp_balance2 = gbp_account2["balance"]

    # Move 1 GBP from Account 1 to Account 2
    response = await async_client.Transfers.move_money_between_accounts(
        request_id=str(uuid4()),
        source_account_id=gbp_account1["id"],
        target_account_id=gbp_account2["id"],
        amount=1.0,
        currency="GBP",
        reference="PyRevolut Test",
    )
    await asyncio.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.COMPLETED

    # Check balances
    accounts = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(random.randint(1, 3))
    gbp_balance1_new = next(
        account["balance"]
        for account in accounts
        if account["id"] == gbp_account1["id"]
    )
    gbp_balance2_new = next(
        account["balance"]
        for account in accounts
        if account["id"] == gbp_account2["id"]
    )
    assert gbp_balance2_new == gbp_balance2 + 1.0
    assert gbp_balance1_new == gbp_balance1 - 1.0

    # Move 1 GBP from Account 2 to Account 1
    response = await async_client.Transfers.move_money_between_accounts(
        request_id=str(uuid4()),
        source_account_id=gbp_account2["id"],
        target_account_id=gbp_account1["id"],
        amount=1.0,
        currency="GBP",
        reference="PyRevolut Test",
    )
    await asyncio.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.COMPLETED

    # Check balances
    accounts = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(random.randint(1, 3))
    gbp_balance1_new = next(
        account["balance"]
        for account in accounts
        if account["id"] == gbp_account1["id"]
    )
    gbp_balance2_new = next(
        account["balance"]
        for account in accounts
        if account["id"] == gbp_account2["id"]
    )
    assert gbp_balance2_new == gbp_balance2
    assert gbp_balance1_new == gbp_balance1


@pytest.mark.asyncio
async def test_async_create_transfer_to_another_account(async_client: Client):
    """Test the async `create_transfer_to_another_account` transfers method"""

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

    # Get GBP account
    gbp_account = next(
        account
        for account in accounts
        if account["currency"] == "GBP"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"]
    )
    gbp_balance = gbp_account["balance"]

    # If there is no EUR balance, simulate a top up
    if eur_balance < 1.0:
        response = await async_client.Simulations.simulate_account_topup(
            account_id=eur_account["id"],
            amount=1.0,
            currency="EUR",
            reference="PyRevolut Test",
            state=EnumTransactionState.COMPLETED,
        )
        await asyncio.sleep(random.randint(1, 3))
        assert response["state"] == EnumTransactionState.COMPLETED

    # If there is no GBP balance, simulate a top up
    if gbp_balance < 1.0:
        response = await async_client.Simulations.simulate_account_topup(
            account_id=gbp_account["id"],
            amount=1.0,
            currency="GBP",
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
        amount=1.0,
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
    assert account["balance"] == eur_balance - 1.0

    # Complete the transfer via simulation
    response = await async_client.Simulations.simulate_transfer_state_update(
        transfer_id=response["id"],
        action=EnumSimulateTransferStateAction.COMPLETE,
    )
    await asyncio.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.COMPLETED

    # Create a transfer from the GBP account to the EUR counterparty
    response = await async_client.Transfers.create_transfer_to_another_account(
        request_id=str(uuid4()),
        account_id=gbp_account["id"],
        counterparty_id=eur_counterparty["id"],
        amount=1.0,
        currency="EUR",
        counterparty_account_id=eur_counterparty_account["id"],
        reference="PyRevolut Test",
        transfer_reason_code=EnumTransferReasonCode.FAMILY_SUPPORT,
    )
    await asyncio.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.PENDING

    # Check balance
    account = await async_client.Accounts.get_account(account_id=gbp_account["id"])
    await asyncio.sleep(random.randint(1, 3))
    assert account["balance"] < gbp_balance  # Not exact because of the exchange rate

    # Complete the transfer via simulation
    response = await async_client.Simulations.simulate_transfer_state_update(
        transfer_id=response["id"],
        action=EnumSimulateTransferStateAction.COMPLETE,
    )
    await asyncio.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.COMPLETED

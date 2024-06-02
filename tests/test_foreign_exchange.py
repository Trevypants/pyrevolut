import time
import asyncio
from uuid import uuid4
import pytest
import random

from pyrevolut.client import Client, AsyncClient
from pyrevolut.api import EnumAccountState, EnumTransactionState
from pyrevolut.exceptions import PyRevolutInternalServerError


def test_sync_get_exchange_rate(sync_client: Client):
    """Test the sync `get_exchange_rate` foreign exchange method"""
    # Get Exchange Rate EUR to USD
    sync_client.ForeignExchange.get_exchange_rate(
        from_currency="EUR",
        to_currency="USD",
    )
    time.sleep(random.randint(1, 3))

    # Get Exchange Rate USD to EUR
    sync_client.ForeignExchange.get_exchange_rate(
        from_currency="USD",
        to_currency="EUR",
    )
    time.sleep(random.randint(1, 3))

    # Get Exchange Rate EUR to GBP
    sync_client.ForeignExchange.get_exchange_rate(
        from_currency="EUR",
        to_currency="GBP",
    )
    time.sleep(random.randint(1, 3))


def test_sync_exchange_money(sync_client: Client):
    """Test the sync `exchange_money` foreign exchange method"""

    # Get all accounts
    accounts = sync_client.Accounts.get_all_accounts()
    time.sleep(random.randint(1, 3))

    # Get GBP and EUR accounts
    gbp_account = next(
        account
        for account in accounts
        if account["currency"] == "GBP"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"] > 0.0
    )
    gbp_balance = gbp_account["balance"]
    eur_account = next(
        account
        for account in accounts
        if account["currency"] == "EUR"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"] > 0.0
    )
    eur_balance = eur_account["balance"]

    # Exchange 1 EUR from EUR to GBP
    response = sync_client.ForeignExchange.exchange_money(
        request_id=str(uuid4()),
        from_account_id=eur_account["id"],
        from_currency="EUR",
        to_account_id=gbp_account["id"],
        to_currency="GBP",
        from_amount=1.0,
        to_amount=None,
        reference="PyRevolut Test",
    )
    time.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.COMPLETED

    # Check balances
    accounts = sync_client.Accounts.get_all_accounts()
    time.sleep(random.randint(1, 3))
    gbp_balance2 = next(
        account["balance"]
        for account in accounts
        if account["currency"] == "GBP"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"] > 0.0
    )
    eur_balance2 = next(
        account["balance"]
        for account in accounts
        if account["currency"] == "EUR"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"] > 0.0
    )
    assert gbp_balance2 > gbp_balance
    assert eur_balance2 == eur_balance - 1.0

    try:
        # Exchange 1 EUR from GBP to EUR
        response = sync_client.ForeignExchange.exchange_money(
            request_id=str(uuid4()),
            from_account_id=gbp_account["id"],
            from_currency="GBP",
            to_account_id=eur_account["id"],
            to_currency="EUR",
            from_amount=None,
            to_amount=1.0,
            reference="PyRevolut Test",
        )
        time.sleep(random.randint(1, 3))
        assert response["state"] == EnumTransactionState.COMPLETED

        # Check balances
        accounts = sync_client.Accounts.get_all_accounts()
        time.sleep(random.randint(1, 3))
        gbp_balance3 = next(
            account["balance"]
            for account in accounts
            if account["currency"] == "GBP"
            and account["state"] == EnumAccountState.ACTIVE
        )
        eur_balance3 = next(
            account["balance"]
            for account in accounts
            if account["currency"] == "EUR"
            and account["state"] == EnumAccountState.ACTIVE
        )
        assert gbp_balance3 < gbp_balance2
        assert eur_balance3 == eur_balance
        assert eur_balance3 > eur_balance2
    except PyRevolutInternalServerError:
        # This error occurs randomly in the sandbox environment
        pass


@pytest.mark.asyncio
async def test_async_get_exchange_rate(async_client: AsyncClient):
    """Test the async `get_exchange_rate` foreign exchange method"""
    # Get Exchange Rate EUR to USD
    await async_client.ForeignExchange.get_exchange_rate(
        from_currency="EUR",
        to_currency="USD",
    )
    await asyncio.sleep(random.randint(1, 3))

    # Get Exchange Rate USD to EUR
    await async_client.ForeignExchange.get_exchange_rate(
        from_currency="USD",
        to_currency="EUR",
    )
    await asyncio.sleep(random.randint(1, 3))

    # Get Exchange Rate EUR to GBP
    await async_client.ForeignExchange.get_exchange_rate(
        from_currency="EUR",
        to_currency="GBP",
    )
    await asyncio.sleep(random.randint(1, 3))


@pytest.mark.asyncio
async def test_async_exchange_money(async_client: AsyncClient):
    """Test the async `exchange_money` foreign exchange method"""

    # Get all accounts
    accounts = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(random.randint(1, 3))

    # Get GBP and EUR accounts
    gbp_account = next(
        account
        for account in accounts
        if account["currency"] == "GBP"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"] > 0.0
    )
    gbp_balance = gbp_account["balance"]
    eur_account = next(
        account
        for account in accounts
        if account["currency"] == "EUR"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"] > 0.0
    )
    eur_balance = eur_account["balance"]

    # Exchange 1 EUR from EUR to GBP
    response = await async_client.ForeignExchange.exchange_money(
        request_id=str(uuid4()),
        from_account_id=eur_account["id"],
        from_currency="EUR",
        to_account_id=gbp_account["id"],
        to_currency="GBP",
        from_amount=1.0,
        to_amount=None,
        reference="PyRevolut Test",
    )
    await asyncio.sleep(random.randint(1, 3))
    assert response["state"] == EnumTransactionState.COMPLETED

    # Check balances
    accounts = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(random.randint(1, 3))
    gbp_balance2 = next(
        account["balance"]
        for account in accounts
        if account["currency"] == "GBP"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"] > 0.0
    )
    eur_balance2 = next(
        account["balance"]
        for account in accounts
        if account["currency"] == "EUR"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"] > 0.0
    )
    assert gbp_balance2 > gbp_balance
    assert eur_balance2 == eur_balance - 1.0

    try:
        # Exchange 1 EUR from GBP to EUR
        response = await async_client.ForeignExchange.exchange_money(
            request_id=str(uuid4()),
            from_account_id=gbp_account["id"],
            from_currency="GBP",
            to_account_id=eur_account["id"],
            to_currency="EUR",
            from_amount=None,
            to_amount=1.0,
            reference="PyRevolut Test",
        )
        await asyncio.sleep(random.randint(1, 3))
        assert response["state"] == EnumTransactionState.COMPLETED

        # Check balances
        accounts = await async_client.Accounts.get_all_accounts()
        await asyncio.sleep(random.randint(1, 3))
        gbp_balance3 = next(
            account["balance"]
            for account in accounts
            if account["currency"] == "GBP"
            and account["state"] == EnumAccountState.ACTIVE
        )
        eur_balance3 = next(
            account["balance"]
            for account in accounts
            if account["currency"] == "EUR"
            and account["state"] == EnumAccountState.ACTIVE
        )
        assert gbp_balance3 < gbp_balance2
        assert eur_balance3 == eur_balance
        assert eur_balance3 > eur_balance2
    except PyRevolutInternalServerError:
        # This error occurs randomly in the sandbox environment
        pass

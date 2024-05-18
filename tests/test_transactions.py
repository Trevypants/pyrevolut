import time
import asyncio

import pendulum
import pytest

from pyrevolut.client import Client
from pyrevolut.api import EnumTransactionType


def test_sync_get_all_transactions(sync_client: Client):
    """Test the sync `get_all_transactions` transactions method"""
    # Get all transactions (no params)
    transactions = sync_client.Transactions.get_all_transactions()
    time.sleep(1)
    assert isinstance(transactions, list)
    for transaction in transactions:
        assert isinstance(transaction, dict)

    # Get all transactions (with params)
    transactions = sync_client.Transactions.get_all_transactions(
        from_datetime=pendulum.now().subtract(days=1),
        to_datetime=pendulum.now(),
        limit=10,
        transaction_type=EnumTransactionType.TOPUP,
    )
    time.sleep(1)
    assert isinstance(transactions, list)
    for transaction in transactions:
        assert isinstance(transaction, dict)
        assert transaction["type"] == EnumTransactionType.TOPUP


def test_sync_get_transaction(sync_client: Client):
    """Test the sync `get_transaction` transactions method"""
    # Get all transactions (no params)
    transactions = sync_client.Transactions.get_all_transactions(limit=3)
    time.sleep(1)
    assert isinstance(transactions, list)
    for transaction in transactions:
        assert isinstance(transaction, dict)

    # Get the transactions by id
    for transaction in transactions:
        transaction_id = transaction["id"]
        transaction = sync_client.Transactions.get_transaction(transaction_id=transaction_id)
        time.sleep(1)
        assert isinstance(transaction, dict)
        assert transaction["id"] == transaction_id

    # Get the transactions by request id
    for transaction in transactions:
        request_id = transaction["request_id"]
        transaction = sync_client.Transactions.get_transaction(request_id=request_id)
        time.sleep(1)
        assert isinstance(transaction, dict)
        assert transaction["request_id"] == request_id


@pytest.mark.asyncio
async def test_async_get_all_transactions(async_client: Client):
    """Test the async `get_all_transactions` transactions method"""
    # Get all transactions (no params)
    transactions = await async_client.Transactions.get_all_transactions()
    await asyncio.sleep(1)
    assert isinstance(transactions, list)
    for transaction in transactions:
        assert isinstance(transaction, dict)

    # Get all transactions (with params)
    transactions = await async_client.Transactions.get_all_transactions(
        from_datetime=pendulum.now().subtract(days=1),
        to_datetime=pendulum.now(),
        limit=10,
        transaction_type=EnumTransactionType.TOPUP,
    )
    await asyncio.sleep(1)
    assert isinstance(transactions, list)
    for transaction in transactions:
        assert isinstance(transaction, dict)
        assert transaction["type"] == EnumTransactionType.TOPUP


@pytest.mark.asyncio
async def test_async_get_transaction(async_client: Client):
    """Test the async `get_transaction` transactions method"""
    # Get all transactions (no params)
    transactions = await async_client.Transactions.get_all_transactions(limit=3)
    await asyncio.sleep(1)
    assert isinstance(transactions, list)
    for transaction in transactions:
        assert isinstance(transaction, dict)

    # Get the transactions by id
    for transaction in transactions:
        transaction_id = transaction["id"]
        transaction = await async_client.Transactions.get_transaction(transaction_id=transaction_id)
        await asyncio.sleep(1)
        assert isinstance(transaction, dict)
        assert transaction["id"] == transaction_id

    # Get the transactions by request id
    for transaction in transactions:
        request_id = transaction["request_id"]
        transaction = await async_client.Transactions.get_transaction(request_id=request_id)
        await asyncio.sleep(1)
        assert isinstance(transaction, dict)
        assert transaction["request_id"] == request_id

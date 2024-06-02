import time
import asyncio
import pytest
import random

from pyrevolut.client import Client
from pyrevolut.api import EnumAccountState
from pyrevolut.exceptions import PyRevolutInternalServerError


def test_sync_get_all_payment_drafts(sync_client: Client):
    """Test the sync `get_all_payment_drafts` payment drafts method"""
    # Get all payment drafts
    drafts = sync_client.PaymentDrafts.get_all_payment_drafts()
    time.sleep(random.randint(1, 3))
    assert isinstance(drafts, dict)
    for draft in drafts["payment_orders"]:
        assert isinstance(draft, dict)


def test_sync_get_payment_draft(sync_client: Client):
    """Test the sync `get_payment_draft` payment drafts method"""
    # Get all payment drafts
    drafts = sync_client.PaymentDrafts.get_all_payment_drafts()
    time.sleep(random.randint(1, 3))
    assert isinstance(drafts, dict)
    for draft in drafts["payment_orders"]:
        assert isinstance(draft, dict)
        draft_id = draft["id"]

        # Get the payment draft by ID
        response = sync_client.PaymentDrafts.get_payment_draft(
            payment_draft_id=draft_id
        )
        time.sleep(random.randint(1, 3))
        assert isinstance(response, dict)
        assert response["id"] == draft_id


def test_sync_create_delete_payment_draft(sync_client: Client):
    """Test the sync `create_payment_draft` and `delete_payment_draft` payment drafts methods"""
    # Get all accounts
    accounts = sync_client.Accounts.get_all_accounts()
    time.sleep(random.randint(1, 3))

    # Get GBP account
    gbp_account = next(
        account
        for account in accounts
        if account["currency"] == "GBP"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"] > 0.0
    )

    # Get recipients
    recipients = sync_client.Counterparties.get_all_counterparties()
    time.sleep(random.randint(1, 3))

    # Get the first recipient in the UK (GB)
    recipient = next(
        recipient for recipient in recipients if recipient["country"] == "GB"
    )

    try:
        # Create a payment draft
        response = sync_client.PaymentDrafts.create_payment_draft(
            account_id=gbp_account["id"],
            counterparty_ids=[recipient["id"]],
            counterparty_account_ids=[None],
            counterparty_card_ids=[None],
            amounts=[1.0],
            currencies=["GBP"],
            references=["test"],
            title="Test payment draft",
            schedule_for="2025-01-01",
        )
        time.sleep(random.randint(1, 3))

        # Delete the payment draft
        sync_client.PaymentDrafts.delete_payment_draft(payment_draft_id=response["id"])
        time.sleep(random.randint(1, 3))
    except PyRevolutInternalServerError:
        # This error occurs randomly in the sandbox environment
        pass


@pytest.mark.asyncio
async def test_async_get_all_payment_drafts(async_client: Client):
    """Test the async `get_all_payment_drafts` payment drafts method"""
    # Get all payment drafts
    drafts = await async_client.PaymentDrafts.get_all_payment_drafts()
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(drafts, dict)
    for draft in drafts["payment_orders"]:
        assert isinstance(draft, dict)


@pytest.mark.asyncio
async def test_async_get_payment_draft(async_client: Client):
    """Test the async `get_payment_draft` payment drafts method"""
    # Get all payment drafts
    drafts = await async_client.PaymentDrafts.get_all_payment_drafts()
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(drafts, dict)
    for draft in drafts["payment_orders"]:
        assert isinstance(draft, dict)
        draft_id = draft["id"]

        # Get the payment draft by ID
        response = await async_client.PaymentDrafts.get_payment_draft(
            payment_draft_id=draft_id
        )
        await asyncio.sleep(random.randint(1, 3))
        assert isinstance(response, dict)
        assert response["id"] == draft_id


@pytest.mark.asyncio
async def test_async_create_delete_payment_draft(async_client: Client):
    """Test the async `create_payment_draft` and `delete_payment_draft` payment drafts methods"""
    # Get all accounts
    accounts = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(random.randint(1, 3))

    # Get GBP account
    gbp_account = next(
        account
        for account in accounts
        if account["currency"] == "GBP"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"] > 0.0
    )

    # Get recipients
    recipients = await async_client.Counterparties.get_all_counterparties()
    await asyncio.sleep(random.randint(1, 3))

    # Get the first recipient in the UK (GB)
    recipient = next(
        recipient for recipient in recipients if recipient["country"] == "GB"
    )

    try:
        # Create a payment draft
        response = await async_client.PaymentDrafts.create_payment_draft(
            account_id=gbp_account["id"],
            counterparty_ids=[recipient["id"]],
            counterparty_account_ids=[None],
            counterparty_card_ids=[None],
            amounts=[1.0],
            currencies=["GBP"],
            references=["test"],
            title="Test payment draft",
            schedule_for="2025-01-01",
        )
        await asyncio.sleep(random.randint(1, 3))

        # Delete the payment draft
        await async_client.PaymentDrafts.delete_payment_draft(
            payment_draft_id=response["id"]
        )
        await asyncio.sleep(random.randint(1, 3))
    except PyRevolutInternalServerError:
        # This error occurs randomly in the sandbox environment
        pass

import time
import asyncio
from decimal import Decimal
from uuid import uuid4
import pytest

from pyrevolut.client import Client
from pyrevolut.api import (
    EnumPayoutLinkState,
    EnumAccountState,
    EnumPayoutLinkPaymentMethod,
    EnumTransferReasonCode,
)


def test_sync_get_all_payout_links(sync_client: Client):
    """Test the sync `get_all_payout_links` payout links method"""
    # Get all payout links (no params)
    links = sync_client.PayoutLinks.get_all_payout_links()
    time.sleep(1)
    assert isinstance(links, list)
    for link in links:
        assert isinstance(link, dict)

    # Get all payout links (with params)
    links = sync_client.PayoutLinks.get_all_payout_links(
        state=EnumPayoutLinkState.ACTIVE,
        created_before="2020-01-01",
        limit=1,
    )
    time.sleep(1)
    assert isinstance(links, list)
    assert len(links) == 0


def test_sync_get_payout_link(sync_client: Client):
    """Test the sync `get_payout_link` payout links method"""
    # Get all payout links
    links = sync_client.PayoutLinks.get_all_payout_links()
    time.sleep(1)
    assert isinstance(links, list)
    for link in links:
        assert isinstance(link, dict)
        link_id = link["id"]

        # Get the payout link by ID
        response = sync_client.PayoutLinks.get_payout_link(payout_link_id=link_id)
        time.sleep(1)
        assert isinstance(response, dict)
        assert response["id"] == link_id


def test_sync_create_cancel_payout_link(sync_client: Client):
    """Test the sync `create_payout_link` and `cancel_payout_link` payout links methods"""
    # Get all accounts
    accounts = sync_client.Accounts.get_all_accounts()
    time.sleep(1)

    # Get GBP account
    gbp_account = next(
        account
        for account in accounts
        if account["currency"] == "GBP"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"] > Decimal("0")
    )

    # Create a payout link
    response = sync_client.PayoutLinks.create_payout_link(
        counterparty_name="John Doe",
        request_id=str(uuid4()),
        account_id=gbp_account["id"],
        amount=Decimal("1.00"),
        currency="GBP",
        reference="test payout link",
        payout_methods=[
            EnumPayoutLinkPaymentMethod.REVOLUT,
            EnumPayoutLinkPaymentMethod.BANK_ACCOUNT,
        ],
        expiry_period="P3D",  # 3 days
        transfer_reason_code=EnumTransferReasonCode.FAMILY,
    )
    time.sleep(1)
    assert isinstance(response, dict)
    assert response["state"] == EnumPayoutLinkState.ACTIVE

    # Get the payout link by ID
    response = sync_client.PayoutLinks.get_payout_link(payout_link_id=response["id"])
    time.sleep(1)
    assert isinstance(response, dict)
    assert response["id"] == response["id"]
    assert response["state"] == EnumPayoutLinkState.ACTIVE

    # Cancel the payout link
    sync_client.PayoutLinks.cancel_payout_link(payout_link_id=response["id"])
    time.sleep(1)

    # Get the payout link by ID
    response = sync_client.PayoutLinks.get_payout_link(payout_link_id=response["id"])
    time.sleep(1)
    assert isinstance(response, dict)
    assert response["id"] == response["id"]
    assert response["state"] == EnumPayoutLinkState.CANCELLED


@pytest.mark.asyncio
async def test_async_get_all_payout_links(async_client: Client):
    """Test the async `get_all_payout_links` payout links method"""
    # Get all payout links (no params)
    links = await async_client.PayoutLinks.get_all_payout_links()
    await asyncio.sleep(1)
    assert isinstance(links, list)
    for link in links:
        assert isinstance(link, dict)

    # Get all payout links (with params)
    links = await async_client.PayoutLinks.get_all_payout_links(
        state=EnumPayoutLinkState.ACTIVE,
        created_before="2020-01-01",
        limit=1,
    )
    await asyncio.sleep(1)
    assert isinstance(links, list)
    assert len(links) == 0


@pytest.mark.asyncio
async def test_async_get_payout_link(async_client: Client):
    """Test the async `get_payout_link` payout links method"""
    # Get all payout links
    links = await async_client.PayoutLinks.get_all_payout_links()
    await asyncio.sleep(1)
    assert isinstance(links, list)
    for link in links:
        assert isinstance(link, dict)
        link_id = link["id"]

        # Get the payout link by ID
        response = await async_client.PayoutLinks.get_payout_link(payout_link_id=link_id)
        await asyncio.sleep(1)
        assert isinstance(response, dict)
        assert response["id"] == link_id


@pytest.mark.asyncio
async def test_async_create_cancel_payout_link(async_client: Client):
    """Test the async `create_payout_link` and `cancel_payout_link` payout links methods"""
    # Get all accounts
    accounts = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(1)

    # Get GBP account
    gbp_account = next(
        account
        for account in accounts
        if account["currency"] == "GBP"
        and account["state"] == EnumAccountState.ACTIVE
        and account["balance"] > Decimal("0")
    )

    # Create a payout link
    response = await async_client.PayoutLinks.create_payout_link(
        counterparty_name="John Doe",
        request_id=str(uuid4()),
        account_id=gbp_account["id"],
        amount=Decimal("1.00"),
        currency="GBP",
        reference="test payout link",
        payout_methods=[
            EnumPayoutLinkPaymentMethod.REVOLUT,
            EnumPayoutLinkPaymentMethod.BANK_ACCOUNT,
        ],
        expiry_period="P3D",  # 3 days
        transfer_reason_code=EnumTransferReasonCode.FAMILY,
    )
    await asyncio.sleep(1)
    assert isinstance(response, dict)
    assert response["state"] == EnumPayoutLinkState.ACTIVE

    # Get the payout link by ID
    response = await async_client.PayoutLinks.get_payout_link(payout_link_id=response["id"])
    await asyncio.sleep(1)
    assert isinstance(response, dict)
    assert response["id"] == response["id"]
    assert response["state"] == EnumPayoutLinkState.ACTIVE

    # Cancel the payout link
    await async_client.PayoutLinks.cancel_payout_link(payout_link_id=response["id"])
    await asyncio.sleep(1)

    # Get the payout link by ID
    response = await async_client.PayoutLinks.get_payout_link(payout_link_id=response["id"])
    await asyncio.sleep(1)
    assert isinstance(response, dict)
    assert response["id"] == response["id"]
    assert response["state"] == EnumPayoutLinkState.CANCELLED

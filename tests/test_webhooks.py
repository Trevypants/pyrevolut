import time
import asyncio
import random

import pytest

from pyrevolut.client import Client
from pyrevolut.api import EnumWebhookEvent


def test_sync_get_all_webhooks(sync_client: Client):
    """Test the sync `get_all_webhooks` webhooks method"""
    # Get all webhooks
    webhooks = sync_client.Webhooks.get_all_webhooks()
    time.sleep(random.randint(1, 3))
    assert isinstance(webhooks, list)
    for webhook in webhooks:
        assert isinstance(webhook, dict)


def test_sync_get_webhook(sync_client: Client):
    """Test the sync `get_webhook` webhooks method"""
    # Get all webhooks
    webhooks = sync_client.Webhooks.get_all_webhooks()

    # For each webhook, get the webhook
    for webhook in webhooks:
        webhook = sync_client.Webhooks.get_webhook(webhook_id=webhook["id"])
        time.sleep(random.randint(1, 3))
        assert isinstance(webhook, dict)
        assert webhook["id"] == webhook["id"]


def test_sync_get_failed_webhook_events(sync_client: Client):
    """Test the sync `get_failed_webhook_events` webhooks method"""
    # Get all webhooks
    webhooks = sync_client.Webhooks.get_all_webhooks()

    # For each webhook, get all failed webhooks
    for webhook in webhooks:
        failed_webhooks = sync_client.Webhooks.get_failed_webhook_events(
            webhook_id=webhook["id"], limit=10
        )
        time.sleep(random.randint(1, 3))
        assert isinstance(failed_webhooks, list)
        for failed_webhook in failed_webhooks:
            assert isinstance(failed_webhook, dict)


def test_sync_create_update_rotate_delete_webhook(sync_client: Client):
    """Test the sync `create`, `update`, `rotate` and `delete` webhooks methods"""
    # Create a new webhook
    webhook = sync_client.Webhooks.create_webhook(
        url="https://example.com",
        events=[
            EnumWebhookEvent.PAYOUT_LINK_CREATED,
        ],
    )
    time.sleep(random.randint(1, 3))
    assert isinstance(webhook, dict)

    # Get the webhook
    webhook = sync_client.Webhooks.get_webhook(webhook_id=webhook["id"])
    time.sleep(random.randint(1, 3))
    assert isinstance(webhook, dict)
    assert webhook["id"] == webhook["id"]
    assert webhook["url"] is not None
    assert EnumWebhookEvent.PAYOUT_LINK_CREATED in webhook["events"]

    # Update the webhook
    updated_webhook = sync_client.Webhooks.update_webhook(
        webhook_id=webhook["id"],
        url=None,
        events=[
            EnumWebhookEvent.PAYOUT_LINK_CREATED,
            EnumWebhookEvent.PAYOUT_LINK_STATE_CHANGED,
        ],
    )
    time.sleep(random.randint(1, 3))
    assert isinstance(updated_webhook, dict)

    # Get the webhook
    webhook = sync_client.Webhooks.get_webhook(webhook_id=webhook["id"])
    time.sleep(random.randint(1, 3))
    assert isinstance(webhook, dict)
    assert webhook["id"] == webhook["id"]
    assert webhook["url"] is not None
    assert EnumWebhookEvent.PAYOUT_LINK_CREATED in webhook["events"]
    assert EnumWebhookEvent.PAYOUT_LINK_STATE_CHANGED in webhook["events"]

    # Rotate the webhook
    rotated_webhook = sync_client.Webhooks.rotate_webhook_secret(
        webhook_id=webhook["id"], expiration_period="P1D"
    )
    time.sleep(random.randint(1, 3))
    assert isinstance(rotated_webhook, dict)

    # Delete the webhook
    sync_client.Webhooks.delete_webhook(webhook_id=webhook["id"])
    time.sleep(random.randint(1, 3))

    # Get all webhooks
    webhooks = sync_client.Webhooks.get_all_webhooks()
    time.sleep(random.randint(1, 3))
    assert webhook["id"] not in [webhook["id"] for webhook in webhooks]


@pytest.mark.asyncio
async def test_async_get_all_webhooks(async_client: Client):
    """Test the async `get_all_webhooks` webhooks method"""
    # Get all webhooks
    webhooks = await async_client.Webhooks.get_all_webhooks()
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(webhooks, list)
    for webhook in webhooks:
        assert isinstance(webhook, dict)


@pytest.mark.asyncio
async def test_async_get_webhook(async_client: Client):
    """Test the async `get_webhook` webhooks method"""
    # Get all webhooks
    webhooks = await async_client.Webhooks.get_all_webhooks()

    # For each webhook, get the webhook
    for webhook in webhooks:
        webhook = await async_client.Webhooks.get_webhook(webhook_id=webhook["id"])
        await asyncio.sleep(random.randint(1, 3))
        assert isinstance(webhook, dict)
        assert webhook["id"] == webhook["id"]


@pytest.mark.asyncio
async def test_async_get_failed_webhook_events(async_client: Client):
    """Test the async `get_failed_webhook_events` webhooks method"""
    # Get all webhooks
    webhooks = await async_client.Webhooks.get_all_webhooks()

    # For each webhook, get all failed webhooks
    for webhook in webhooks:
        failed_webhooks = await async_client.Webhooks.get_failed_webhook_events(
            webhook_id=webhook["id"], limit=10
        )
        await asyncio.sleep(random.randint(1, 3))
        assert isinstance(failed_webhooks, list)
        for failed_webhook in failed_webhooks:
            assert isinstance(failed_webhook, dict)


@pytest.mark.asyncio
async def test_async_create_update_rotate_delete_webhook(async_client: Client):
    """Test the async `create`, `update`, `rotate` and `delete` webhooks methods"""
    # Create a new webhook
    webhook = await async_client.Webhooks.create_webhook(
        url="https://example.com",
        events=[
            EnumWebhookEvent.PAYOUT_LINK_CREATED,
        ],
    )
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(webhook, dict)

    # Get the webhook
    webhook = await async_client.Webhooks.get_webhook(webhook_id=webhook["id"])
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(webhook, dict)
    assert webhook["id"] == webhook["id"]
    assert webhook["url"] is not None
    assert EnumWebhookEvent.PAYOUT_LINK_CREATED in webhook["events"]

    # Update the webhook
    updated_webhook = await async_client.Webhooks.update_webhook(
        webhook_id=webhook["id"],
        url=None,
        events=[
            EnumWebhookEvent.PAYOUT_LINK_CREATED,
            EnumWebhookEvent.PAYOUT_LINK_STATE_CHANGED,
        ],
    )
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(updated_webhook, dict)

    # Get the webhook
    webhook = await async_client.Webhooks.get_webhook(webhook_id=webhook["id"])
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(webhook, dict)
    assert webhook["id"] == webhook["id"]
    assert webhook["url"] is not None
    assert EnumWebhookEvent.PAYOUT_LINK_CREATED in webhook["events"]
    assert EnumWebhookEvent.PAYOUT_LINK_STATE_CHANGED in webhook["events"]

    # Rotate the webhook
    rotated_webhook = await async_client.Webhooks.rotate_webhook_secret(
        webhook_id=webhook["id"], expiration_period="P1D"
    )
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(rotated_webhook, dict)

    # Delete the webhook
    await async_client.Webhooks.delete_webhook(webhook_id=webhook["id"])
    await asyncio.sleep(random.randint(1, 3))

    # Get all webhooks
    webhooks = await async_client.Webhooks.get_all_webhooks()
    await asyncio.sleep(random.randint(1, 3))
    assert webhook["id"] not in [webhook["id"] for webhook in webhooks]

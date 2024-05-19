import time
import asyncio
import pytest
import random

from pyrevolut.client import Client, AsyncClient
from pyrevolut.exceptions import InvalidEnvironmentException


def test_sync_get_all_cards(sync_client: Client):
    """Test the sync `get_all_cards` cards method"""
    # Get Cards (no params)
    with pytest.raises(
        InvalidEnvironmentException, match="This feature is not available in Sandbox."
    ):
        cards_all = sync_client.Cards.get_all_cards()
        time.sleep(random.randint(1, 3))
        assert isinstance(cards_all, list)
        for card in cards_all:
            assert isinstance(card, dict)

    # Get Cards (with params)
    with pytest.raises(
        InvalidEnvironmentException, match="This feature is not available in Sandbox."
    ):
        cards_all = sync_client.Cards.get_all_cards(
            created_before="2020-01-01",
            limit=10,
        )
        time.sleep(random.randint(1, 3))
        assert isinstance(cards_all, list)
        assert len(cards_all) == 0


def test_sync_get_card(sync_client: Client):
    """Test the sync `get_card` cards method"""
    with pytest.raises(
        InvalidEnvironmentException, match="This feature is not available in Sandbox."
    ):
        # Get all cards
        cards_all = sync_client.Cards.get_all_cards()
        time.sleep(random.randint(1, 3))
        assert isinstance(cards_all, list)
        assert len(cards_all) > 0

        # Get Card
        for card in cards_all:
            card_id = card["id"]
            card = sync_client.Cards.get_card(card_id=card_id)
            time.sleep(random.randint(1, 3))
            assert isinstance(card, dict)


def test_get_card_sensitive_details(sync_client: Client):
    """Test the sync `get_card_sensitive_details` cards method"""
    with pytest.raises(
        InvalidEnvironmentException, match="This feature is not available in Sandbox."
    ):
        # Get all cards
        cards_all = sync_client.Cards.get_all_cards()
        time.sleep(random.randint(1, 3))
        assert isinstance(cards_all, list)
        assert len(cards_all) > 0

        # Get Card
        for card in cards_all:
            card_id = card["id"]
            card = sync_client.Cards.get_card_sensitive_details(card_id=card_id)
            time.sleep(random.randint(1, 3))
            assert isinstance(card, dict)


def test_create_card(sync_client: Client):
    """Test the sync `create_card` cards method"""
    # TODO: Implement this test


def test_freeze_card(sync_client: Client):
    """Test the sync `freeze_card` cards method"""
    # TODO: Implement this test


def test_unfreeze_card(sync_client: Client):
    """Test the sync `unfreeze_card` cards method"""
    # TODO: Implement this test


def test_update_card(sync_client: Client):
    """Test the sync `update_card` cards method"""
    # TODO: Implement this test


def test_delete_card(sync_client: Client):
    """Test the sync `delete_card` cards method"""
    # TODO: Implement this test


@pytest.mark.asyncio
async def test_async_get_all_cards(async_client: AsyncClient):
    """Test the async `get_all_cards` cards method"""
    # Get Cards (no params)
    with pytest.raises(
        InvalidEnvironmentException, match="This feature is not available in Sandbox."
    ):
        cards_all = await async_client.Cards.get_all_cards()
        await asyncio.sleep(random.randint(1, 3))
        assert isinstance(cards_all, list)
        for card in cards_all:
            assert isinstance(card, dict)

    # Get Cards (with params)
    with pytest.raises(
        InvalidEnvironmentException, match="This feature is not available in Sandbox."
    ):
        cards_all = await async_client.Cards.get_all_cards(
            created_before="2020-01-01",
            limit=10,
        )
        await asyncio.sleep(random.randint(1, 3))
        assert isinstance(cards_all, list)
        assert len(cards_all) == 0


@pytest.mark.asyncio
async def test_async_get_card(async_client: AsyncClient):
    """Test the async `get_card` cards method"""
    with pytest.raises(
        InvalidEnvironmentException, match="This feature is not available in Sandbox."
    ):
        # Get all cards
        cards_all = await async_client.Cards.get_all_cards()
        await asyncio.sleep(random.randint(1, 3))
        assert isinstance(cards_all, list)
        assert len(cards_all) > 0

        # Get Card
        for card in cards_all:
            card_id = card["id"]
            card = await async_client.Cards.get_card(card_id=card_id)
            await asyncio.sleep(random.randint(1, 3))
            assert isinstance(card, dict)


@pytest.mark.asyncio
async def test_async_get_card_sensitive_details(async_client: AsyncClient):
    """Test the async `get_card_sensitive_details` cards method"""
    with pytest.raises(
        InvalidEnvironmentException, match="This feature is not available in Sandbox."
    ):
        # Get all cards
        cards_all = await async_client.Cards.get_all_cards()
        await asyncio.sleep(random.randint(1, 3))
        assert isinstance(cards_all, list)
        assert len(cards_all) > 0

        # Get Card
        for card in cards_all:
            card_id = card["id"]
            card = await async_client.Cards.get_card_sensitive_details(card_id=card_id)
            await asyncio.sleep(random.randint(1, 3))
            assert isinstance(card, dict)


@pytest.mark.asyncio
async def test_async_create_card(async_client: AsyncClient):
    """Test the async `create_card` cards method"""
    # TODO: Implement this test


@pytest.mark.asyncio
async def test_async_freeze_card(async_client: AsyncClient):
    """Test the async `freeze_card` cards method"""
    # TODO: Implement this test


@pytest.mark.asyncio
async def test_async_unfreeze_card(async_client: AsyncClient):
    """Test the async `unfreeze_card` cards method"""
    # TODO: Implement this test


@pytest.mark.asyncio
async def test_async_update_card(async_client: AsyncClient):
    """Test the async `update_card` cards method"""
    # TODO: Implement this test


@pytest.mark.asyncio
async def test_async_delete_card(async_client: AsyncClient):
    """Test the async `delete_card` cards method"""
    # TODO: Implement this test

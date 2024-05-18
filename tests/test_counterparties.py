import time
import asyncio
import pytest
import random

from pyrevolut.client import Client, AsyncClient
from pyrevolut.api import EnumProfileType


def test_sync_get_all_counterparties(sync_client: Client):
    """Test the sync `get_all_counterparties` counterparties method"""
    # Get Counterparties (no params)
    counterparties_all = sync_client.Counterparties.get_all_counterparties()
    time.sleep(random.randint(1, 3))
    assert isinstance(counterparties_all, list)
    for counterparty in counterparties_all:
        assert isinstance(counterparty, dict)

    # Get Counterparties (with params)
    counterparties_all = sync_client.Counterparties.get_all_counterparties(
        name="Testing",
        account_no="12345678",
        created_before="2020-01-01",
        limit=10,
    )
    time.sleep(random.randint(1, 3))
    assert isinstance(counterparties_all, list)
    assert len(counterparties_all) == 0


def test_sync_get_counterparty(sync_client: Client):
    """Test the sync `get_counterparty` counterparties method"""
    # Get all counterparties
    counterparties_all = sync_client.Counterparties.get_all_counterparties()
    time.sleep(random.randint(1, 3))
    assert isinstance(counterparties_all, list)
    assert len(counterparties_all) > 0

    # Get Counterparty
    for counterparty in counterparties_all:
        counterparty_id = counterparty["id"]
        counterparty = sync_client.Counterparties.get_counterparty(counterparty_id=counterparty_id)
        time.sleep(random.randint(1, 3))
        assert isinstance(counterparty, dict)


def test_sync_validate_account_name(sync_client: Client):
    """Test the sync `validate_account_name` counterparties method"""
    # Validate UK individual counterparty (personal account)
    response = sync_client.Counterparties.validate_account_name(
        sort_code="54-01-05",
        account_no="12345678",
        individual_first_name="John",
        individual_last_name="Doe",
    )
    time.sleep(random.randint(1, 3))
    assert response["result_code"] == "cannot_be_checked"

    # Validate UK company counterparty (business account)
    response = sync_client.Counterparties.validate_account_name(
        sort_code="54-01-05",
        account_no="12345678",
        company_name="John Smith Co.",
    )
    time.sleep(random.randint(1, 3))
    assert response["result_code"] == "cannot_be_checked"


def test_create_delete_counterparty(sync_client: Client):
    """Test the sync `create_counterparty` and `delete_counterparty` counterparties methods"""

    counterparty_ids = []

    # Create Personal Revolut Counterparty
    counterparty = sync_client.Counterparties.create_counterparty(
        profile_type=EnumProfileType.PERSONAL,
        name="Test User 2",
        revtag="john2pvki",
    )
    time.sleep(random.randint(1, 3))
    counterparty_ids.append(counterparty["id"])

    # Create UK Individual Counterparty
    counterparty = sync_client.Counterparties.create_counterparty(
        individual_first_name="John",
        individual_last_name="Doe",
        bank_country="GB",
        currency="GBP",
        sort_code="54-01-05",
        account_no="12345678",
    )
    time.sleep(random.randint(1, 3))
    counterparty_ids.append(counterparty["id"])

    # Create UK Company Counterparty
    counterparty = sync_client.Counterparties.create_counterparty(
        company_name="John Smith Co.",
        bank_country="GB",
        currency="GBP",
        sort_code="54-01-05",
        account_no="12345678",
    )
    time.sleep(random.randint(1, 3))
    counterparty_ids.append(counterparty["id"])

    # Create International Business Counterparty (eurozone with EUR)
    counterparty = sync_client.Counterparties.create_counterparty(
        company_name="John Smith Co.",
        bank_country="FR",
        currency="EUR",
        iban="FR1420041010050500013M02606",
    )
    time.sleep(random.randint(1, 3))
    counterparty_ids.append(counterparty["id"])

    # Create International Business Counterparty (outside eurozone)
    counterparty = sync_client.Counterparties.create_counterparty(
        company_name="Johann Meier Co.",
        bank_country="CH",
        currency="EUR",
        iban="CH5604835012345678009",
        address_street_line1="Bahnhofstrasse 4a/8",
        address_city="Zurich",
        address_country="CH",
        address_postcode="8001",
    )
    time.sleep(random.randint(1, 3))
    counterparty_ids.append(counterparty["id"])

    # Fetch all counterparties
    counterparties_all = sync_client.Counterparties.get_all_counterparties()
    time.sleep(random.randint(1, 3))
    for counterparty_id in counterparty_ids:
        assert counterparty_id in [counterparty["id"] for counterparty in counterparties_all]

    # Delete all created counterparties
    for counterparty_id in counterparty_ids:
        sync_client.Counterparties.delete_counterparty(counterparty_id=counterparty_id)
        time.sleep(random.randint(1, 3))

    # Fetch all counterparties
    counterparties_all = sync_client.Counterparties.get_all_counterparties()
    time.sleep(random.randint(1, 3))
    for counterparty_id in counterparty_ids:
        assert counterparty_id not in [counterparty["id"] for counterparty in counterparties_all]


@pytest.mark.asyncio
async def test_async_get_all_counterparties(async_client: AsyncClient):
    """Test the async `get_all_counterparties` counterparties method"""
    # Get Counterparties (no params)
    counterparties_all = await async_client.Counterparties.get_all_counterparties()
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(counterparties_all, list)
    for counterparty in counterparties_all:
        assert isinstance(counterparty, dict)

    # Get Counterparties (with params)
    counterparties_all = await async_client.Counterparties.get_all_counterparties(
        name="Testing",
        account_no="12345678",
        created_before="2020-01-01",
        limit=10,
    )
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(counterparties_all, list)
    assert len(counterparties_all) == 0


@pytest.mark.asyncio
async def test_async_get_counterparty(async_client: AsyncClient):
    """Test the async `get_counterparty` counterparties method"""
    # Get all counterparties
    counterparties_all = await async_client.Counterparties.get_all_counterparties()
    await asyncio.sleep(random.randint(1, 3))
    assert isinstance(counterparties_all, list)
    assert len(counterparties_all) > 0

    # Get Counterparty
    for counterparty in counterparties_all:
        counterparty_id = counterparty["id"]
        counterparty = await async_client.Counterparties.get_counterparty(
            counterparty_id=counterparty_id
        )
        await asyncio.sleep(random.randint(1, 3))
        assert isinstance(counterparty, dict)


@pytest.mark.asyncio
async def test_async_validate_account_name(async_client: AsyncClient):
    """Test the async `validate_account_name` counterparties method"""
    # Validate UK individual counterparty (personal account)
    response = await async_client.Counterparties.validate_account_name(
        sort_code="54-01-05",
        account_no="12345678",
        individual_first_name="John",
        individual_last_name="Doe",
    )
    await asyncio.sleep(random.randint(1, 3))
    assert response["result_code"] == "cannot_be_checked"

    # Validate UK company counterparty (business account)
    response = await async_client.Counterparties.validate_account_name(
        sort_code="54-01-05",
        account_no="12345678",
        company_name="John Smith Co.",
    )
    await asyncio.sleep(random.randint(1, 3))
    assert response["result_code"] == "cannot_be_checked"


@pytest.mark.asyncio
async def test_async_create_delete_counterparty(async_client: AsyncClient):
    """Test the async `create_counterparty` and `delete_counterparty` counterparties methods"""

    counterparty_ids = []

    # Create Personal Revolut Counterparty
    counterparty = await async_client.Counterparties.create_counterparty(
        profile_type=EnumProfileType.PERSONAL,
        name="Test User 1",
        revtag="john1pvki",
    )
    await asyncio.sleep(random.randint(1, 3))
    counterparty_ids.append(counterparty["id"])

    # Create UK Individual Counterparty
    counterparty = await async_client.Counterparties.create_counterparty(
        individual_first_name="John",
        individual_last_name="Doe",
        bank_country="GB",
        currency="GBP",
        sort_code="54-01-05",
        account_no="12345678",
    )
    await asyncio.sleep(random.randint(1, 3))
    counterparty_ids.append(counterparty["id"])

    # Create UK Company Counterparty
    counterparty = await async_client.Counterparties.create_counterparty(
        company_name="John Smith Co.",
        bank_country="GB",
        currency="GBP",
        sort_code="54-01-05",
        account_no="12345678",
    )
    await asyncio.sleep(random.randint(1, 3))
    counterparty_ids.append(counterparty["id"])

    # Create International Business Counterparty (eurozone with EUR)
    counterparty = await async_client.Counterparties.create_counterparty(
        company_name="John Smith Co.",
        bank_country="FR",
        currency="EUR",
        iban="FR1420041010050500013M02606",
    )
    await asyncio.sleep(random.randint(1, 3))
    counterparty_ids.append(counterparty["id"])

    # Create International Business Counterparty (outside eurozone)
    counterparty = await async_client.Counterparties.create_counterparty(
        company_name="Johann Meier Co.",
        bank_country="CH",
        currency="EUR",
        iban="CH5604835012345678009",
        address_street_line1="Bahnhofstrasse 4a/8",
        address_city="Zurich",
        address_country="CH",
        address_postcode="8001",
    )
    await asyncio.sleep(random.randint(1, 3))
    counterparty_ids.append(counterparty["id"])

    # Fetch all counterparties
    counterparties_all = await async_client.Counterparties.get_all_counterparties()
    await asyncio.sleep(random.randint(1, 3))
    for counterparty_id in counterparty_ids:
        assert counterparty_id in [counterparty["id"] for counterparty in counterparties_all]

    # Delete all created counterparties
    for counterparty_id in counterparty_ids:
        await async_client.Counterparties.delete_counterparty(counterparty_id=counterparty_id)
        await asyncio.sleep(random.randint(1, 3))

    # Fetch all counterparties
    counterparties_all = await async_client.Counterparties.get_all_counterparties()
    await asyncio.sleep(random.randint(1, 3))
    for counterparty_id in counterparty_ids:
        assert counterparty_id not in [counterparty["id"] for counterparty in counterparties_all]

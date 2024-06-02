import time
import asyncio
import random
from uuid import UUID, uuid4
import platform

import pytest
import pendulum
from httpx import AsyncClient as TestHTTPClient

from pyrevolut.client import Client
from pyrevolut.api import (
    EnumWebhookEvent,
    EnumAccountState,
    EnumTransactionState,
    EnumTransferReasonCode,
)
from pyrevolut.api.webhooks.post import CreateWebhook
from pyrevolut.api.webhooks.resources import (
    ResourceWebhookPayload,
    ResourceTransactionCreated,
    ResourceTransactionStateChanged,
)
from pyrevolut.api.accounts.get import RetrieveAllAccounts
from pyrevolut.api.simulations.post import SimulateAccountTopup
from pyrevolut.api.counterparties.get import RetrieveListOfCounterparties
from pyrevolut.api.transfers.post import CreateTransferToAnotherAccount
from pyrevolut.exceptions import PyRevolutInvalidPayload


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


def test_webhook_sign_payload(sync_client: Client):
    """Test that the webhook payload signing works"""
    # Params
    revolut_signature_header = (
        "v1=bca326fb378d0da7f7c490ad584a8106bab9723d8d9cdd0d50b4c5b3be3837c0"
    )
    revolut_request_timestamp = 1683650202360
    signing_secret = "wsk_r59a4HfWVAKycbCaNO1RvgCJec02gRd8"
    raw_payload = '{"data":{"id":"645a7696-22f3-aa47-9c74-cbae0449cc46","new_state":"completed","old_state":"pending","request_id":"app_charges-9f5d5eb3-1e06-46c5-b1c0-3914763e0bcb"},"event":"TransactionStateChanged","timestamp":"2023-05-09T16:36:38.028960Z"}'

    # Sign the payload
    payload_signed = sync_client.Webhooks.sign_payload(
        raw_payload=raw_payload,
        signing_secret=signing_secret,
        header_timestamp=revolut_request_timestamp,
        signature_version="v1",
    )

    # Check the signature
    assert payload_signed == revolut_signature_header


def test_webhook_verify_payload_signature_valid(sync_client: Client):
    raw_payload = '{"event": "TransactionCreated"}'
    signing_secret = "my_signing_secret"
    header_timestamp = pendulum.now(tz="UTC").int_timestamp * 1000
    header_signature = sync_client.Webhooks.sign_payload(
        raw_payload=raw_payload,
        signing_secret=signing_secret,
        header_timestamp=header_timestamp,
        signature_version="v1",
    )

    # No exception should be raised
    sync_client.Webhooks.verify_payload_signature(
        raw_payload=raw_payload,
        signing_secret=signing_secret,
        header_timestamp=header_timestamp,
        header_signature=header_signature,
    )


def test_webhook_verify_payload_signature_invalid_signature(sync_client: Client):
    raw_payload = '{"event": "TransactionCreated"}'
    signing_secret = "my_signing_secret"
    header_timestamp = pendulum.now(tz="UTC").int_timestamp * 1000
    header_signature = "v1=invalid_signature"

    # PyRevolutInvalidPayload exception should be raised
    with pytest.raises(
        PyRevolutInvalidPayload, match="The webhook payload signature is invalid."
    ):
        sync_client.Webhooks.verify_payload_signature(
            raw_payload=raw_payload,
            signing_secret=signing_secret,
            header_timestamp=header_timestamp,
            header_signature=header_signature,
        )


def test_webhook_verify_payload_signature_invalid_timestamp(sync_client: Client):
    raw_payload = '{"event": "TransactionCreated"}'
    signing_secret = "my_signing_secret"
    header_timestamp = 1683650200000  # Older timestamp
    header_signature = sync_client.Webhooks.sign_payload(
        raw_payload=raw_payload,
        signing_secret=signing_secret,
        header_timestamp=header_timestamp,
        signature_version="v1",
    )

    # PyRevolutInvalidPayload exception should be raised
    with pytest.raises(
        PyRevolutInvalidPayload, match="The webhook payload timestamp is too old."
    ):
        sync_client.Webhooks.verify_payload_signature(
            raw_payload=raw_payload,
            signing_secret=signing_secret,
            header_timestamp=header_timestamp,
            header_signature=header_signature,
        )


@pytest.mark.asyncio
@pytest.mark.skipif(
    condition=platform.system() != "Darwin",
    reason="Only one ngrok tunnel allowed at a time",
)
async def test_webhook_app(async_client: Client, litestar_client_url: str):
    """Test the webhook when receiving a webhook"""
    # Set the async client to return pydantic models
    async_client.return_type = "model"

    # Create a new webhook
    webhook: CreateWebhook.Response = await async_client.Webhooks.create_webhook(
        url=litestar_client_url + "/webhook",
        events=[
            EnumWebhookEvent.TRANSACTION_CREATED,
            EnumWebhookEvent.TRANSACTION_STATE_CHANGED,
            EnumWebhookEvent.PAYOUT_LINK_CREATED,
            EnumWebhookEvent.PAYOUT_LINK_STATE_CHANGED,
        ],
    )
    await asyncio.sleep(random.randint(1, 3))

    async with TestHTTPClient() as http_client:
        # Set the signing secret
        resp = await http_client.post(
            url=f"{litestar_client_url}/signing-secret",
            json={"signing_secret": webhook.signing_secret},
        )
        assert resp.status_code == 201
        assert resp.json() == {"message": "Signing secret set!"}

        # Get the signing secret
        resp = await http_client.get(url=f"{litestar_client_url}/signing-secret")
        assert resp.status_code == 200
        assert resp.json() == {"signing_secret": webhook.signing_secret}

    ### Create a transaction ###

    # Get all accounts
    accounts: list[
        RetrieveAllAccounts.Response
    ] = await async_client.Accounts.get_all_accounts()
    await asyncio.sleep(random.randint(1, 3))

    # Get EUR account
    eur_account = next(
        account
        for account in accounts
        if account.currency == "EUR"
        and account.state == EnumAccountState.ACTIVE
        and account.balance > 0.0
    )
    eur_balance = eur_account.balance

    # If there is no EUR balance, simulate a top up
    if eur_balance < 1.0:
        response: SimulateAccountTopup.Response = (
            await async_client.Simulations.simulate_account_topup(
                account_id=eur_account.id,
                amount=1.0,
                currency="EUR",
                reference="PyRevolut Test",
                state=EnumTransactionState.COMPLETED,
            )
        )
        await asyncio.sleep(random.randint(1, 3))
        assert response.state == EnumTransactionState.COMPLETED

    # Get all counterparties
    counterparties: list[
        RetrieveListOfCounterparties.Response
    ] = await async_client.Counterparties.get_all_counterparties()

    # Get a EUR counterparty with an IBAN
    eur_counterparties: list[RetrieveListOfCounterparties.Response] = []
    for counterparty in counterparties:
        counterparty_accounts = counterparty.accounts or []
        for account in counterparty_accounts:
            if account.currency == "EUR" and account.iban is not None:
                eur_counterparties.append(counterparty)

    # Get the first EUR counterparty
    eur_counterparty = eur_counterparties[0]
    eur_counterparty_account = [
        acc
        for acc in eur_counterparty.accounts or []
        if acc.currency == "EUR" and acc.iban is not None
    ][0]

    # Create a transfer to the EUR counterparty
    response: CreateTransferToAnotherAccount.Response = (
        await async_client.Transfers.create_transfer_to_another_account(
            request_id=str(uuid4()),
            account_id=eur_account.id,
            counterparty_id=eur_counterparty.id,
            amount=1.0,
            currency="EUR",
            counterparty_account_id=eur_counterparty_account.id,
            reference="PyRevolut Test",
            transfer_reason_code=EnumTransferReasonCode.FAMILY_SUPPORT,
        )
    )
    await asyncio.sleep(3)
    assert response.state == EnumTransactionState.PENDING

    # Check that the webhook was received
    async with TestHTTPClient() as http_client:
        resp = await http_client.get(url=f"{litestar_client_url}/webhook")
        assert resp.status_code == 200
        response_data = ResourceWebhookPayload(**resp.json())
        assert response_data.event == EnumWebhookEvent.TRANSACTION_CREATED
        assert isinstance(response_data.data, ResourceTransactionCreated)
        assert response_data.data.id == UUID(response.id)
        assert response_data.data.state == EnumTransactionState.PENDING

    # Simulate a transfer state change
    await async_client.Simulations.simulate_transfer_state_update(
        transfer_id=response.id,
        action="complete",
    )
    await asyncio.sleep(3)

    # Check that the webhook was received
    async with TestHTTPClient() as http_client:
        resp = await http_client.get(url=f"{litestar_client_url}/webhook")
        assert resp.status_code == 200
        response_data = ResourceWebhookPayload(**resp.json())
        assert response_data.event == EnumWebhookEvent.TRANSACTION_STATE_CHANGED
        assert isinstance(response_data.data, ResourceTransactionStateChanged)
        assert response_data.data.id == UUID(response.id)
        assert response_data.data.new_state == EnumTransactionState.COMPLETED
        assert response_data.data.old_state == EnumTransactionState.PENDING

    # Delete the webhook
    await async_client.Webhooks.delete_webhook(webhook_id=webhook.id)
    await asyncio.sleep(random.randint(1, 3))

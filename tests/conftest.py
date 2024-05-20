import os
import glob
import asyncio
import time
import random
import itertools

import pytest
import pytest_asyncio

from pyrevolut.client import Client, AsyncClient
from pyrevolut.api import EnumTransactionState

""" Pytest Fixture Scopes

1. function: the default scope, the fixture is destroyed at the end of the test.
2. class: the fixture is destroyed during teardown of the last test in the class.
3. module: the fixture is destroyed during teardown of the last test in the module.
4. package: the fixture is destroyed during teardown of the last test in the package.
5. session: the fixture is destroyed at the end of the test session.
"""

# All the JSON files in the credentials folder
CREDENTIALS_LOC = glob.glob(os.path.join("tests/credentials", "*.json"))
CREDENTIALS_LOC_ITER = itertools.cycle(CREDENTIALS_LOC)


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def random_creds_file():
    """Context manager that selects a random credentials file

    Yields
    ------
    str
        The path to the credentials file
    """
    # Select a random credentials file
    creds_loc = next(CREDENTIALS_LOC_ITER)

    # Yield for test
    yield creds_loc


@pytest.fixture(scope="function")
def base_sync_client(random_creds_file: str):
    """Context manager that initializes the sync client

    Yields
    ------
    None
    """
    # Initialize the client
    client = Client(
        creds_loc=random_creds_file,
        sandbox=True,
        return_type="dict",
    )

    # Yield for test
    yield client


@pytest.fixture(scope="function")
def base_async_client(random_creds_file: str):
    """Context manager that initializes the async client

    Yields
    ------
    None
    """
    # Initialize the client
    client = AsyncClient(
        creds_loc=random_creds_file,
        sandbox=True,
        return_type="dict",
    )

    # Yield for test
    yield client


@pytest.fixture(scope="function")
def sync_client(base_sync_client: Client):
    """Context manager that initializes the sync client

    Parameters
    ----------
    base_client : Client
        The client to use for the endpoint

    Yields
    ------
    Client
        The client to use for the endpoint
    """
    # Initialize the sync client
    base_sync_client.open()

    # Check that all accounts have funds, otherwise top them up
    accounts = base_sync_client.Accounts.get_all_accounts()
    time.sleep(random.randint(1, 3))
    for account in accounts:
        if account["balance"] == 0.0:
            base_sync_client.Simulations.simulate_account_topup(
                account_id=account["id"],
                amount=100.0,
                currency=account["currency"],
                reference="Sugar Daddy <3",
                state=EnumTransactionState.COMPLETED,
            )
            time.sleep(random.randint(1, 3))

    # Yield for test
    yield base_sync_client

    # Close the sync client
    base_sync_client.close()


@pytest_asyncio.fixture(scope="function")
async def async_client(base_async_client: AsyncClient):
    """Context manager that initializes the async client

    Parameters
    ----------
    base_async_client : AsyncClient
        The async client to use for the endpoint

    Yields
    ------
    AsyncClient
        The async client to use for the endpoint
    """
    # Initialize the async client
    await base_async_client.open()

    # Check that all accounts have funds, otherwise top them up
    accounts = await base_async_client.Accounts.get_all_accounts()
    await asyncio.sleep(random.randint(1, 3))
    for account in accounts:
        if account["balance"] == 0.0:
            await base_async_client.Simulations.simulate_account_topup(
                account_id=account["id"],
                amount=100.0,
                currency=account["currency"],
                reference="Sugar Daddy <3",
                state=EnumTransactionState.COMPLETED,
            )
            await asyncio.sleep(random.randint(1, 3))

    # Yield for test
    yield base_async_client

    # Close the async client
    await base_async_client.close()

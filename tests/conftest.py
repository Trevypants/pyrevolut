import asyncio

import pytest
import pytest_asyncio

from pyrevolut.client import Client, AsyncClient, EnumEnvironment

""" Pytest Fixture Scopes

1. function: the default scope, the fixture is destroyed at the end of the test.
2. class: the fixture is destroyed during teardown of the last test in the class.
3. module: the fixture is destroyed during teardown of the last test in the module.
4. package: the fixture is destroyed during teardown of the last test in the package.
5. session: the fixture is destroyed at the end of the test session.
"""

ACCESS_TOKEN = "TO BE FILLED"
REFRESH_TOKEN = "TO BE FILLED"


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def base_sync_client():
    """Context manager that initializes the sync client

    Yields
    ------
    None
    """
    # Initialize the client
    client = Client(
        access_token=ACCESS_TOKEN,
        refresh_token=REFRESH_TOKEN,
        environment=EnumEnvironment.SANDBOX,
    )

    # Yield for test
    yield client


@pytest.fixture(scope="session")
def base_async_client():
    """Context manager that initializes the async client

    Yields
    ------
    None
    """
    # Initialize the client
    client = AsyncClient(
        access_token=ACCESS_TOKEN,
        refresh_token=REFRESH_TOKEN,
        environment=EnumEnvironment.SANDBOX,
    )

    # Yield for test
    yield client


@pytest.fixture(scope="session")
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

    # Yield for test
    yield base_sync_client

    # Close the sync client
    base_sync_client.close()


@pytest_asyncio.fixture(scope="session")
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

    # Yield for test
    yield base_async_client

    # Close the async client
    await base_async_client.close()

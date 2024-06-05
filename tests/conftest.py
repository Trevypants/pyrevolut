import os
import glob
import asyncio
import time
import random
import itertools
import json
import base64

import pytest
import pytest_asyncio
from dotenv import load_dotenv
import uvicorn

from litestar import Litestar, status_codes
from litestar.config.cors import CORSConfig
from litestar.datastructures import State
from pyngrok import ngrok
from pyngrok.conf import PyngrokConfig

from pyrevolut.client import Client, AsyncClient
from pyrevolut.api import EnumTransactionState

from tests.app import (
    UvicornServer,
    index,
    webhook,
    test_raw_payload,
    set_signing_secret,
    get_signing_secret,
    get_webhook_payload,
    internal_server_error_handler,
)

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
CREDENTIALS_CHOICE_ITER = itertools.cycle(["creds_loc", "creds", "creds_base64"])


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def random_creds():
    """Context manager that selects a random credentials file

    Yields
    ------
    dict[str, str | dict]
        A dictionary containing the credentials location, credentials, or base64 encoded credentials.
        Will randomly choose between providing the creds_loc, creds, or creds_base64.
        For example: {
            "creds_loc": "tests/credentials/creds_1.json",
            "creds": None,
        }
        or {
            "creds_loc": None,
            "creds": {
                "client_id": "12345678-abcd-1234-abcd-1234567890ab",
                "client_secret": "123"
            }
        }
        or {
            "creds_loc": None,
            "creds": "eyJjbGllbnRfa"  # Base64 encoded credentials
        }
    """
    # Select a random credentials file
    creds_loc = next(CREDENTIALS_LOC_ITER)

    # Select a random credentials loading choice
    choice = next(CREDENTIALS_CHOICE_ITER)

    # Load the credentials file
    with open(creds_loc, "r") as file:
        creds = json.load(file)

    # Base64 encode the credentials dict
    creds_base64 = base64.b64encode(json.dumps(creds).encode(encoding="utf-8")).decode(
        encoding="utf-8"
    )

    # Randomly choose between providing the creds_loc, creds, or creds_base64
    if choice == "creds_loc":
        yield {"creds_loc": creds_loc, "creds": None}
    elif choice == "creds":
        yield {"creds_loc": creds_loc, "creds": creds}
    else:
        yield {"creds_loc": creds_loc, "creds": creds_base64}


@pytest.fixture(scope="function")
def base_sync_client(random_creds: dict[str, str | dict]):
    """Context manager that initializes the sync client

    Yields
    ------
    None
    """
    # Initialize the client
    client = Client(
        creds_loc=random_creds["creds_loc"],
        creds=random_creds["creds"],
        sandbox=True,
        return_type="dict",
    )

    # Yield for test
    yield client


@pytest.fixture(scope="function")
def base_async_client(random_creds: dict[str, str | dict]):
    """Context manager that initializes the async client

    Yields
    ------
    None
    """

    # Initialize the client
    client = AsyncClient(
        creds_loc=random_creds["creds_loc"],
        creds=random_creds["creds"],
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


@pytest_asyncio.fixture(scope="function")
async def litestar_client_url(async_client: AsyncClient):
    """Context manager that initializes the Litestar client

    Parameters
    ----------
    async_client : AsyncClient
        The async client to use for the endpoint

    Yields
    ------
    str
        The url of the Litestar client
    """
    # Create the Litestar app
    app = Litestar(
        route_handlers=[
            index,
            webhook,
            set_signing_secret,
            test_raw_payload,
            get_signing_secret,
            get_webhook_payload,
        ],
        cors_config=CORSConfig(allow_origins=["*"]),
        state=State({"client": async_client}),
        exception_handlers={
            status_codes.HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler,
        },
    )

    # Get the Environment variables
    dotenv_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "tests/.env",
    )

    # Load .env file variables
    load_dotenv(dotenv_path=dotenv_path)

    # Initialize the ngrok tunnel
    ngrok_config = PyngrokConfig(auth_token=os.getenv("NGROK_AUTH_TOKEN"))
    ngrok_tunnel = ngrok.connect(
        addr="8000",
        pyngrok_config=ngrok_config,
    )
    public_url = ngrok_tunnel.public_url

    # Start the Litestar app in a seaparate thread
    uvicorn_config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8000,
        log_level="error",
    )
    with UvicornServer(config=uvicorn_config).run_in_thread():
        # Wait a few seconds for startup
        await asyncio.sleep(3)

        # Yield public URL for test
        yield public_url

    # Shutdown the ngrok tunnel
    ngrok.disconnect(public_url=public_url)
    ngrok.kill()

import os
from typing import Annotated

import typer

from pydantic import BaseModel
from pyrevolut.utils.auth import EnumAuthScope, auth_manual_flow

app = typer.Typer()


class AuthManualParams(BaseModel):
    """Pydantic model for the auth_manual CLI command."""

    credentials_json: str
    sandbox: bool = True
    scopes: list[EnumAuthScope] | None = None


@app.callback()
def callback():
    """
    pyrevolut CLI tool to interact with the Revolut Business API. Primarily
    used for authentication and authorization.
    """


@app.command(name="auth-manual")
def auth_manual(
    credentials_json: str = "credentials/creds.json",
    sandbox: bool = True,
    scopes: Annotated[list[str], typer.Option()] = None,
):
    """
    Method to run the manual authorization flow to get the client assertion JWT and the access and refresh tokens.

    Parameters
    ----------
    credentials_json : str, optional
        The location to save the credentials JSON file.
        Will overwrite the file if it already exists.
        Default is "credentials/creds.json".
    sandbox : bool, optional
        Whether to use the sandbox environment.
        Default is True.
    scopes : list[str] | None, optional
        The list of scopes to request. If not provided, the default scopes will be used.

        Access tokens can be issued with four security scopes and require a JWT (JSON Web Token)
        signature to be obtained:

            READ: Permissions for GET operations.

            WRITE: Permissions to update counterparties, webhooks, and issue payment drafts.

            PAY: Permissions to initiate or cancel transactions and currency exchanges.

            READ_SENSITIVE_CARD_DATA: Permissions to retrieve sensitive card details.

        Caution
        -------
        If you enable the READ_SENSITIVE_CARD_DATA scope for your access token, you must
        set up IP whitelisting.
        Failing to do so will prevent you from accessing any Business API endpoint.

        Default is None.

    Returns
    -------
    None
    """
    params = AuthManualParams(
        credentials_json=credentials_json,
        sandbox=sandbox,
        scopes=scopes,
    )

    # Create the directories if they do not exist
    os.makedirs(os.path.dirname(params.credentials_json), exist_ok=True)

    # Run the manual authorization flow
    auth_manual_flow(
        credentials_json=params.credentials_json,
        sandbox=params.sandbox,
        scopes=params.scopes,
    )

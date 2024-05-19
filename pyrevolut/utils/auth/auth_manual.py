import base64
import json

import pendulum
from httpx import Client
import typer
from rich import print as console

from pyrevolut.utils.datetime import to_datetime

from .enum_auth_scope import EnumAuthScope
from .creds import ModelCreds, save_creds
from .gen_public_private_cert import gen_public_private_cert
from .create_client_assert_jwt import create_client_assert_jwt
from .get_auth_tokens import get_auth_tokens


def auth_manual_flow(
    credentials_json: str = "credentials/creds.json",
    sandbox: bool = True,
    scopes: list[EnumAuthScope] | None = None,
):
    """
    Method to run the manual authorization flow to get the client assertion JWT and the access and refresh tokens.

    Parameters
    ----------
    credentials_json : str, optional
        The location to save the credentials JSON file.
        Default is "credentials/creds.json".
    sandbox : bool, optional
        Whether to use the sandbox environment.
        Default is True.
    scopes : list[EnumAuthScope] | None, optional
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

    # Final credentials dictionary to be saved to a JSON file
    creds = {}

    console("======================================================================")
    console("=                    Revolut Client from Manual Flow                 =")
    console("======================================================================")

    # Check if the credentials file already exists
    try:
        with open(credentials_json, "r") as f:
            creds = json.load(f)
            console("Credentials file found. Loading credentials...")

        # Check if the credentials file is valid
        try:
            creds_model = ModelCreds(**creds)

            # Check for any expired fields
            if not creds_model.credentials_expired:
                console("Credentials loaded successfully.")
                console("To re-authenticate, please delete the credentials file.")
                return
            else:
                console("Credentials have expired. Re-authenticating...")
        except Exception as exc:
            console(f"An error occurred: {exc}")
            console(
                "Credentials file is invalid. Please delete the credentials file and re-authenticate."
            )
            return
    except FileNotFoundError:
        pass

    # Generate the Public and Private Certificates
    console("\n-----------------------------------------------------------")
    console("--- Step (1/4) Generate Public and Private Certificates ---")
    console("-----------------------------------------------------------")
    while True:
        expiration_dt = to_datetime(
            typer.prompt("Expiration datetime of the certificates (UTC)")
        )
        country = typer.prompt("Country (2-letter code)")
        email_address = typer.prompt(
            text="Email Address (can be left blank)", default=""
        )
        common_name = typer.prompt(
            text="Common Name (fully qualified host name, can be left blank)",
            default="",
        )
        state = typer.prompt(
            text="State or Province (full name, can be left blank)", default=""
        )
        locality = typer.prompt(text="Locality (city, can be left blank)", default="")
        organization = typer.prompt(
            text="Organization (company, can be left blank)", default=""
        )
        organization_unit = typer.prompt(
            text="Organization Unit (section, can be left blank)", default=""
        )

        try:
            keys = gen_public_private_cert(
                expiration_dt=expiration_dt,
                country=country,
                email_address=email_address,
                common_name=common_name,
                state=state,
                locality=locality,
                organization=organization,
                organization_unit=organization_unit,
                save_location_private=None,
                save_location_public=None,
            )
            public_key = keys["public"]
            private_key = keys["private"]

            # Store in the creds dictionary as base64 encoded strings
            creds["certificate"] = {
                "public": base64.b64encode(public_key).decode("utf-8"),
                "private": base64.b64encode(private_key).decode("utf-8"),
                "expiration_dt": expiration_dt.to_iso8601_string(),
            }
            break
        except Exception as exc:
            console(f"An error occurred: {exc}")

    console("\n-------------------------------------------------------")
    console("--- Step (2/4) Upload Public Certificate to Revolut ---")
    console("-------------------------------------------------------")
    upload_url = (
        "https://sandbox-business.revolut.com/settings/api"
        if sandbox
        else "https://business.revolut.com/settings/api"
    )
    public_key_string = public_key.decode("utf-8").replace("\\n", "")
    console(
        "Please specify your OAuth redirect URI. "
        "This is the URL where you are redirected after you consent for "
        "the application to access your Revolut Business account."
    )
    while True:
        try:
            redirect_url: str = typer.prompt(
                "OAuth redirect URI (e.g: https://example.com)",
                default="https://example.com",
            )
            if redirect_url.startswith("http://"):
                raise ValueError(
                    f"WARNING: Your redirect URL ({redirect_url}) is not secure."
                )
            break
        except ValueError:
            pass

    console("\nPlease follow the instructions exactly:")
    console(f"Step (2.1) Navigate to the following URL: {upload_url}")
    console(
        "Step (2.2) In the [bold red]API Certificates[/bold red] section, "
        "click [bold red]Add API certificate[/bold red]. "
        "If you already have other certificates added, click [bold red]Add new[/bold red]."
    )
    console(
        "Step (2.3) Give your certificate a meaningful title. It will help you later to distinguish "
        "it from other certificates."
    )
    console(
        "Step (2.4) Copy and paste the following url to the OAuth redirect URI field: "
        f"\n\n[bold]{redirect_url}[/bold]\n"
    )
    console(
        "Step (2.5) Copy and paste the following public key to the X509 public key field "
        "(including the -----BEGIN CERTIFICATE----- and -----END CERTIFICATE----- lines): "
        f"\n\n[bold]{public_key_string}[/bold]\n",
        end="",
    )
    console(
        "Step (2.6) Click [bold red]Continue[/bold red]. "
        "This takes you to the [bold red]API Certificate[/bold red] page with the parameters "
        "of your application."
    )
    console("Step (2.7) Copy the [bold red]Client ID[/bold red] provided by Revolut.")
    client_id = typer.prompt(text="Client ID")

    console("\n------------------------------------------------------")
    console("--- Step (3/4) Generate Client Assertion JWT Token ---")
    console("------------------------------------------------------")
    client_assert_jwt = create_client_assert_jwt(
        client_id=client_id,
        expiration_dt=expiration_dt,
        private_credentials_key=private_key,
        issuer_url=redirect_url,
        save_location=None,
    )
    creds["client_assert_jwt"] = {
        "jwt": client_assert_jwt,
        "expiration_dt": expiration_dt.to_iso8601_string(),
    }

    console("\n---------------------------------------------")
    console("--- Step (4/4) Consent to the application ---")
    console("---------------------------------------------")
    suffix = f"app-confirm?client_id={client_id}&redirect_uri={redirect_url}&response_type=code"
    if scopes is not None:
        suffix += f"&scope={','.join([scope for scope in scopes])}"
    suffix += "#authorize"
    consent_url = (
        "https://sandbox-business.revolut.com/"
        if sandbox
        else "https://business.revolut.com/"
    ) + suffix

    console("\nPlease follow the instructions exactly:")
    console(f"Step (4.1) Navigate to the following URL: {consent_url}")
    console(
        "Step (4.2) Click on [bold red]Authorize[/bold red] and upon success, "
        "you will be redirected to your OAuth redirect URI."
    )
    console("Step (4.3) Copy the entire redirect URI and paste it below.")
    auth_url: str = typer.prompt("OAuth redirect URI")
    auth_code = auth_url.split("code=")[1]

    console("\n-----------------------------------------------")
    console("--- Step (5/5) Get Access and Refresh Token ---")
    console("-----------------------------------------------")
    resp = get_auth_tokens(
        client=Client(),
        auth_code=auth_code,
        client_assert_jwt=client_assert_jwt,
        sandbox=sandbox,
    )
    dt_now = pendulum.now(tz="UTC")
    creds["tokens"] = {
        "access_token": resp.access_token.get_secret_value(),
        "refresh_token": resp.refresh_token.get_secret_value(),
        "token_type": resp.token_type,
        "access_token_expiration_dt": dt_now.add(
            seconds=resp.expires_in
        ).to_iso8601_string(),
        # To comply with PSD2 SCA regulations, refresh tokens expire after 90 days
        "refresh_token_expiration_dt": dt_now.add(days=90).to_iso8601_string(),
    }

    # Store the credentials to a JSON file
    creds_model = ModelCreds(**creds)
    save_creds(creds=creds_model, location=credentials_json, indent=4)

    console(
        "\n====================================================================================="
    )
    console(
        f"=                      Credentials Saved to {credentials_json}                  ="
    )
    console(
        "====================================================================================="
    )

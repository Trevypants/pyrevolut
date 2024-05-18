from typing import Annotated

from httpx import Client, AsyncClient
from pydantic import BaseModel, Field, SecretStr


class ModelRefreshAccessTokenResponse(BaseModel):
    """The model that represents the response from the refresh access token endpoint."""

    access_token: Annotated[SecretStr, Field(description="The access token")]
    token_type: Annotated[str, Field(description="The token type")]
    expires_in: Annotated[int, Field(description="The expiration time in seconds")]


def refresh_access_token(
    client: Client,
    refresh_token: str,
    client_assert_jwt: str,
    sandbox: bool = True,
):
    """
    Method to get a new access token via the refresh token.

    Parameters
    ----------
    client : Client
        The HTTPX client.
    refresh_token : str
        The refresh token.
    client_assert_jwt : str
        The client assertion JWT.
    sandbox : bool, optional
        Whether to use the sandbox environment.
        Default is True.

    Returns
    -------
    dict
        The new access token response.
    """
    response = client.post(
        **prep_refresh_access_token(
            refresh_token=refresh_token,
            client_assert_jwt=client_assert_jwt,
            sandbox=sandbox,
        )
    )
    return ModelRefreshAccessTokenResponse(**response.json())


async def arefresh_access_token(
    client: AsyncClient,
    refresh_token: str,
    client_assert_jwt: str,
    sandbox: bool = True,
):
    """
    Method to get a new access token via the refresh token.

    Parameters
    ----------
    client : Client
        The HTTPX client.
    refresh_token : str
        The refresh token.
    client_assert_jwt : str
        The client assertion JWT.
    sandbox : bool, optional
        Whether to use the sandbox environment.
        Default is True.

    Returns
    -------
    dict
        The new access token response.
    """
    response = await client.post(
        **prep_refresh_access_token(
            refresh_token=refresh_token,
            client_assert_jwt=client_assert_jwt,
            sandbox=sandbox,
        )
    )
    return ModelRefreshAccessTokenResponse(**response.json())


def prep_refresh_access_token(
    refresh_token: str,
    client_assert_jwt: str,
    sandbox: bool = True,
):
    """
    Method to prepare the arguments for refreshing the access token functions.

    Parameters
    ----------
    refresh_token : str
        The refresh token.
    client_assert_jwt : str
        The client assertion JWT.
    sandbox : bool, optional
        Whether to use the sandbox environment.
        Default is True.

    Returns
    -------
    dict
        The arguments to be passed to the HTTPX client POST method.
    """
    if sandbox:
        url = "https://sandbox-b2b.revolut.com/api/1.0/auth/token"
    else:
        url = "https://b2b.revolut.com/api/1.0/auth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": client_assert_jwt,
    }
    return {
        "url": url,
        "headers": headers,
        "data": data,
    }

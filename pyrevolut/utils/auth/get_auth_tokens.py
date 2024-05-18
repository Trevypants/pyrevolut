from typing import Annotated

from httpx import Client, AsyncClient
from pydantic import BaseModel, Field, SecretStr


class ModelGetAuthTokensResponse(BaseModel):
    """The model that represents the response from the get auth tokens endpoint."""

    access_token: Annotated[SecretStr, Field(description="The access token")]
    refresh_token: Annotated[SecretStr, Field(description="The refresh token")]
    token_type: Annotated[str, Field(description="The token type")]
    expires_in: Annotated[int, Field(description="The expiration time in seconds")]


def get_auth_tokens(
    client: Client,
    auth_code: str,
    client_assert_jwt: str,
    sandbox: bool = True,
):
    """
    Method to get the access and refresh token from the Revolut API.

    Parameters
    ----------
    client : Client
        The HTTPX client.
    auth_code : str
        The authorization code.
    client_assert_jwt : str
        The client assertion JWT.
    sandbox : bool, optional
        Whether to use the sandbox environment.
        Default is True.

    Returns
    -------
    dict
        The access and refresh token response.
    """
    response = client.post(
        **prep_get_auth_tokens(
            auth_code=auth_code,
            client_assert_jwt=client_assert_jwt,
            sandbox=sandbox,
        ),
    )
    return ModelGetAuthTokensResponse(**response.json())


async def aget_auth_tokens(
    client: AsyncClient,
    auth_code: str,
    client_assert_jwt: str,
    sandbox: bool = True,
):
    """
    Method to get the access and refresh token from the Revolut API.

    Parameters
    ----------
    client : Client
        The async HTTPX client.
    auth_code : str
        The authorization code.
    client_assert_jwt : str
        The client assertion JWT.
    sandbox : bool, optional
        Whether to use the sandbox environment.
        Default is True.

    Returns
    -------
    dict
        The access and refresh token response.
    """
    response = await client.post(
        **prep_get_auth_tokens(
            auth_code=auth_code,
            client_assert_jwt=client_assert_jwt,
            sandbox=sandbox,
        ),
    )
    return ModelGetAuthTokensResponse(**response.json())


def prep_get_auth_tokens(
    auth_code: str,
    client_assert_jwt: str,
    sandbox: bool = True,
):
    """
    Method to prepare the arguments for getting the auth token functions.

    Parameters
    ----------
    auth_code : str
        The authorization code.
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
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": "client_id",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": client_assert_jwt,
    }
    return {
        "url": url,
        "headers": headers,
        "data": data,
    }

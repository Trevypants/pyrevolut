from datetime import datetime

import jwt

from pyrevolut.utils.datetime import DateTime, to_datetime


def create_client_assert_jwt(
    client_id: str,
    expiration_dt: datetime | DateTime | str | int | float,
    private_credentials_key: bytes,
    issuer_url: str = "https://example.com",
    save_location: str | None = "client_assertion.jwt",
):
    """
    Method to create a client-assertion JWT for Revolut.
    The JWT is used to authenticate the client to the Revolut API.

    Parameters
    ----------
    client_id : str
        The client ID.
        This is the client ID provided by Revolut when you upload your public key.
    expiration_dt : datetime | DateTime | str | int | float
        The expiration datetime (UTC) of the JWT.
        This can be a datetime object, a DateTime object, a string, an integer, or a float.
    private_credentials_key : bytes
        The private key used to sign the JWT.
    issuer_url : str, optional
        The issuer URL.
        This is the URL of the client.
        When you finalize the authentication using the JWT, Revolut will redirect you to this URL
        with an attached authorization code in the query string.

        For example if the URL is "https://example.com",
        the redirect URL will be https://example.com?code=oa_prod_vYo3mAI9TmJuo2_ukYlHVZMh3OiszmfQdgVqk_gLSkU

        Default is "https://example.com".
    save_location : str | None, optional
        The location to save the JWT assertion.
        If None, the assertion will not be saved.
        Default is "client_assertion.jwt".

    Returns
    -------
    str
        The JWT assertion string.
    """

    # Remove the https:// from the issuer_url if it exists
    issuer_url = issuer_url.replace("https://", "")

    # Convert the expiration_dt to a UNIX timestamp if it is not already
    expiration_dt = to_datetime(dt=expiration_dt)
    expiration_ts = expiration_dt.int_timestamp

    # Create the JWT payload
    payload = {
        "iss": issuer_url,  # The URL of the client
        "sub": client_id,  # The client ID
        "aud": "https://revolut.com",  # The URL of the authorization server
        "exp": expiration_ts,  # UNIX timestamp (integer)
    }

    # Create the JWT assertion using the private key
    assertion_string = jwt.encode(
        payload=payload, key=private_credentials_key, algorithm="RS256"
    )

    # Save the JWT assertion to a file if save_location is provided
    if save_location is not None:
        with open(save_location, "w") as f:
            f.write(assertion_string)

    # Return the JWT assertion
    return assertion_string

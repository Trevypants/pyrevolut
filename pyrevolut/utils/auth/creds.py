from typing import Annotated
import json

import pendulum
from pydantic import BaseModel, Field, SecretStr, field_serializer, ConfigDict

from pyrevolut.utils.datetime import DateTime


class ModelCreds(BaseModel):
    """The model that represents the credentials JSON file."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    class ModelCertificate(BaseModel):
        """The model that represents the certificate information"""

        model_config = ConfigDict(validate_assignment=True, extra="forbid")

        public: Annotated[
            SecretStr,
            Field(description="The public certificate in base64 encoded format"),
        ]
        private: Annotated[
            SecretStr,
            Field(description="The private certificate in base64 encoded format"),
        ]
        expiration_dt: Annotated[
            DateTime, Field(description="The expiration datetime of the certificates")
        ]

        @field_serializer("public", "private", when_used="json")
        def dump_secret(self, value: SecretStr) -> str:
            """Serialize the secret value to a string"""
            return value.get_secret_value()

    class ModelClientAssertJWT(BaseModel):
        """The model that represents the client assertion JWT information"""

        model_config = ConfigDict(validate_assignment=True, extra="forbid")

        jwt: Annotated[SecretStr, Field(description="The JWT assertion string")]
        expiration_dt: Annotated[
            DateTime, Field(description="The expiration datetime of the JWT")
        ]

        @field_serializer("jwt", when_used="json")
        def dump_secret(self, value: SecretStr) -> str:
            """Serialize the secret value to a string"""
            return value.get_secret_value()

    class ModelTokens(BaseModel):
        """The model that represents the tokens information"""

        model_config = ConfigDict(validate_assignment=True, extra="forbid")

        access_token: Annotated[SecretStr, Field(description="The access token")]
        refresh_token: Annotated[SecretStr, Field(description="The refresh token")]
        token_type: Annotated[str, Field(description="The token type")]
        access_token_expiration_dt: Annotated[
            DateTime, Field(description="The expiration datetime of the access token")
        ]
        refresh_token_expiration_dt: Annotated[
            DateTime, Field(description="The expiration datetime of the refresh token")
        ]

        @field_serializer("access_token", "refresh_token", when_used="json")
        def dump_secret(self, value: SecretStr) -> str:
            """Serialize the secret value to a string"""
            return value.get_secret_value()

    certificate: Annotated[
        ModelCertificate, Field(description="The certificate information")
    ]
    client_assert_jwt: Annotated[
        ModelClientAssertJWT, Field(description="The client assertion JWT information")
    ]
    tokens: Annotated[ModelTokens, Field(description="The tokens information")]

    @property
    def access_token_expired(self) -> bool:
        """Check if the access token has expired.
        This means that the token is no longer valid and a new one should be requested.

        Returns
        -------
        bool
        """
        # Subtract 1 minute to ensure that the token still works for a little bit
        return self.tokens.access_token_expiration_dt.subtract(
            minutes=1
        ) < pendulum.now(tz="UTC")

    @property
    def credentials_expired(self) -> bool:
        """Check if any of the long term credentials have expired.
        This means that the certificate, client assertion JWT, or refresh token has expired and
        a new one should be requested.

        Returns
        -------
        bool
            True if any of the credentials have expired, False otherwise.
        """
        dt_now = pendulum.now(tz="UTC")
        if self.certificate.expiration_dt < dt_now:
            return True
        if self.client_assert_jwt.expiration_dt < dt_now:
            return True
        if self.tokens.refresh_token_expiration_dt < dt_now:
            return True
        return False


def save_creds(
    creds: ModelCreds,
    location: str = "credentials.json",
    indent: int = 4,
):
    """Save the credentials to the provided location.

    Parameters
    ----------
    creds : ModelCreds
        The credentials model
    location : str, optional
        The location to save the credentials to, by default "credentials.json"
    indent : int, optional
        The indentation level to use, by default 4

    Returns
    -------
    None
    """
    with open(location, "w") as file:
        json.dump(creds.model_dump(mode="json"), file, indent=indent)


def load_creds(location: str = "credentials.json") -> ModelCreds:
    """Load the credentials from the provided location.

    Parameters
    ----------
    location : str, optional
        The location to load the credentials from, by default "credentials.json"

    Returns
    -------
    ModelCreds
        The credentials model
    """
    with open(location, "r") as file:
        return ModelCreds(**json.load(file))

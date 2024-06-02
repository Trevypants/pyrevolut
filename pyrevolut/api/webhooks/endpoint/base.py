import hmac
import hashlib
import json

import pendulum

from pyrevolut.api.common import BaseEndpointSync
from pyrevolut.exceptions import PyRevolutInvalidPayload
from pyrevolut.api.webhooks.resources import ResourceWebhookPayload


class BaseEndpointWebhooks(BaseEndpointSync):
    """The Webhooks API

    A webhook (also called a web callback) allows your system to receive
    updates about your account to an HTTPS endpoint that you provide.
    When a supported event occurs, a notification is posted via HTTP POST method
    to the specified endpoint.

    If the receiver returns an HTTP error response, Revolut will retry the webhook
    event three more times, each with a 10-minute interval.

    The following events are supported:

    TransactionCreated
    TransactionStateChanged
    PayoutLinkCreated
    PayoutLinkStateChanged
    """

    def receive_webhook_event(
        self,
        raw_payload: str,
        signing_secret: str,
        header_timestamp: int,
        header_signature: str,
        **kwargs,
    ):
        """
        Receive a webhook event notification. Will verify the payload signature and
        raise an exception if the signature is invalid.

        Parameters
        ----------
        raw_payload : str
            The raw payload string received from the webhook event.
        signing_secret : str
            The signing secret provided by Revolut for the webhook endpoint.
        header_timestamp : int
            The timestamp string received from the webhook event. It
            will be in the header of the request under the key `Revolut-Requested-Timestamp`.
            For example: 1683650202360
        header_signature : str
            Signature of the request payload. It will be in the header of the request
            under the key `Revolut-Signature`.
            Contains the current version of the signature generating algorithm,
            and the hexadecimal-encoded signature itself.
            For example: v1=09a9989dd8d9282c1d34974fc730f5cbfc4f4296941247e90ae5256590a11e8c.

            It can be that there are multiple signatures in the header if multiple signing secrets are active at a given moment.
            If that's the case, they are separated by a comma.
            For example:
            Revolut-Signature: v1=4fce70bda66b2e713be09fbb7ab1b31b0c8976ea4eeb01b244db7b99aa6482cb,v1=6ffbb59b2300aae63f272406069a9788598b792a944a07aba816edb039989a39

        Raises
        ------
        PyRevolutInvalidPayload
            If the payload signature is invalid or if the payload timestamp is too old.

        Returns
        -------
        dict | ResourceWebhookPayload
            The webhook event payload.
        """
        # Verify the payload signature
        self.verify_payload_signature(
            raw_payload, signing_secret, header_timestamp, header_signature
        )

        # Parse the raw payload
        raw_payload = json.loads(raw_payload)

        # Raw response
        if self.client.return_type == "raw":
            return raw_payload

        # Dict response
        model_response = ResourceWebhookPayload(**raw_payload)
        if self.client.return_type == "dict":
            return model_response.model_dump()

        # Model response
        if self.client.return_type == "model":
            return model_response

    def verify_payload_signature(
        self,
        raw_payload: str,
        signing_secret: str,
        header_timestamp: int,
        header_signature: str,
    ):
        """Verifies the webhook payload signature.

        Parameters
        ----------
        raw_payload : str
            The raw payload string received from the webhook event.
        signing_secret : str
            The signing secret provided by Revolut for the webhook endpoint.
        header_timestamp : int
            The timestamp string received from the webhook event. It
            will be in the header of the request under the key `Revolut-Requested-Timestamp`.
            For example: 1683650202360
        header_signature : str
            Signature of the request payload. It will be in the header of the request
            under the key `Revolut-Signature`.
            Contains the current version of the signature generating algorithm,
            and the hexadecimal-encoded signature itself.
            For example: v1=09a9989dd8d9282c1d34974fc730f5cbfc4f4296941247e90ae5256590a11e8c.

            It can be that there are multiple signatures in the header if multiple signing secrets are active at a given moment.
            If that's the case, they are separated by a comma.
            For example:
            Revolut-Signature: v1=4fce70bda66b2e713be09fbb7ab1b31b0c8976ea4eeb01b244db7b99aa6482cb,v1=6ffbb59b2300aae63f272406069a9788598b792a944a07aba816edb039989a39

        Raises
        ------
        PyRevolutInvalidPayload
            If the payload signature is invalid or if the payload timestamp is too old.

        Returns
        -------
        None
        """
        # Get the revolut signature version from the signature
        revolut_signature_version = header_signature.split("=")[0]

        # Check the timestamp
        current_dt = pendulum.now(tz="UTC")
        timestamp_dt = pendulum.from_timestamp(header_timestamp / 1000, tz="UTC")

        # Check if the timestamp is too old
        if current_dt.diff(timestamp_dt).in_minutes() > 5:
            raise PyRevolutInvalidPayload("The webhook payload timestamp is too old.")

        # Sign the payload
        valid_signature = self.sign_payload(
            raw_payload=raw_payload,
            signing_secret=signing_secret,
            header_timestamp=header_timestamp,
            signature_version=revolut_signature_version,
        )

        # Get the multiple signatures
        multiple_signatures = header_signature.split(",")

        # The computed signature must match exactly the signature (or one of the multiple signatures)
        # sent in that header.
        if valid_signature not in multiple_signatures:
            raise PyRevolutInvalidPayload("The webhook payload signature is invalid.")

    def sign_payload(
        self,
        raw_payload: str,
        signing_secret: str,
        header_timestamp: int,
        signature_version: str = "v1",
    ):
        """Signs the webhook payload.

        Parameters
        ----------
        raw_payload : str
            The raw payload string received from the webhook event.
        signing_secret : str
            The signing secret provided by Revolut for the webhook endpoint.
        header_timestamp : int
            The timestamp string received from the webhook event. It
            will be in the header of the request under the key `Revolut-Requested-Timestamp`.
            For example: 1683650202360
        signature_version : str
            The signature version to use. Default is "v1".

        Returns
        -------
        str
            The signature of the request payload.
        """
        # Create the payload to sign
        payload_to_sign = f"{signature_version}.{header_timestamp}.{raw_payload}"

        # Sign the payload
        return (
            f"{signature_version}="
            + hmac.new(
                bytes(signing_secret, "utf-8"),
                msg=bytes(payload_to_sign, "utf-8"),
                digestmod=hashlib.sha256,
            ).hexdigest()
        )

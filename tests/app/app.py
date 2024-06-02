from typing import Annotated, Any
import json
import logging

from litestar import Request, Response, get, post, status_codes
from litestar.params import Body, Parameter
from litestar.datastructures import State
from litestar.exceptions import ValidationException

from pyrevolut.client import AsyncClient
from pyrevolut.api.webhooks.resources import ResourceWebhookPayload


def internal_server_error_handler(request: Request, exc: Exception) -> Response:
    """This function will handle all internal server errors

    Parameters
    ----------
    request: Request
        The request object
    exc: Exception
        The exception that was raised

    Returns
    -------
    Response
        The response object
    """
    logging.error(
        {
            "path": request.url.path,
            "method": request.method,
            "query_params": request.query_params,
            "reason": str(exc),
        }
    )
    return Response(
        status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )


@get("/")
async def index() -> dict[str, str]:
    return {"message": "Hello, World!"}


@post("/test-raw-payload")
async def test_raw_payload(
    request: Request,
    data: Annotated[dict[str, Any], Body(description="The raw payload")],
) -> dict[str, str]:
    raw_payload = json.dumps(await request.json())
    print("Raw payload", raw_payload)
    return {"message": f"Raw payload: {raw_payload}"}


@post("/signing-secret")
async def set_signing_secret(
    state: State,
    data: Annotated[dict[str, str], Body(description="The signing secret")],
) -> dict[str, str]:
    if "signing_secret" not in data:
        raise ValidationException(
            "Signing secret not provided! Make sure to include the 'signing_secret' key in the request body."
        )
    state.signing_secret = data["signing_secret"]
    return {"message": "Signing secret set!"}


@get("/signing-secret")
async def get_signing_secret(state: State) -> dict[str, str]:
    return {"signing_secret": state.signing_secret}


@post("/webhook")
async def webhook(
    state: State,
    request: Request,
    signature: Annotated[str, Parameter(header="Revolut-Signature")],
    timestamp: Annotated[int, Parameter(header="Revolut-Request-Timestamp")],
) -> dict[str, str]:
    client: AsyncClient = state.client
    signing_secret: str = state.signing_secret
    raw_payload = (await request.body()).decode("utf-8")

    logging.info("Webhook received with payload: %s", raw_payload)

    # Validate the webhook payload
    result: ResourceWebhookPayload = client.Webhooks.receive_webhook_event(
        raw_payload=raw_payload,
        signing_secret=signing_secret,
        header_timestamp=timestamp,
        header_signature=signature,
    )

    # Store the webhook payload
    state.webhook_payload = result
    return {"message": "Webhook received successfully!"}


@get("/webhook")
async def get_webhook_payload(state: State) -> ResourceWebhookPayload:
    if not state.webhook_payload:
        raise ValidationException("No webhook payload received yet!")
    return state.webhook_payload

from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.webhook_replay import WebhookReplay
from ...models.webhook_replay_accepted import WebhookReplayAccepted
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: WebhookReplay,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/webhooks/{id}/replay".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, WebhookReplayAccepted]:
    if response.status_code == 202:
        response_202 = WebhookReplayAccepted.from_dict(response.json())

        return response_202

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, WebhookReplayAccepted]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WebhookReplay,
    idempotency_key: str,
) -> Response[Union[Error, WebhookReplayAccepted]]:
    """Send again the events after a cursor of the stream, or one dead letter

    Args:
        id (UUID):
        idempotency_key (str):
        body (WebhookReplay): Send again every event after `after` that the endpoint asks for,
            marked MFX-Delivery-Attempt: replay; or one dead letter by its id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, WebhookReplayAccepted]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WebhookReplay,
    idempotency_key: str,
) -> Optional[Union[Error, WebhookReplayAccepted]]:
    """Send again the events after a cursor of the stream, or one dead letter

    Args:
        id (UUID):
        idempotency_key (str):
        body (WebhookReplay): Send again every event after `after` that the endpoint asks for,
            marked MFX-Delivery-Attempt: replay; or one dead letter by its id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, WebhookReplayAccepted]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WebhookReplay,
    idempotency_key: str,
) -> Response[Union[Error, WebhookReplayAccepted]]:
    """Send again the events after a cursor of the stream, or one dead letter

    Args:
        id (UUID):
        idempotency_key (str):
        body (WebhookReplay): Send again every event after `after` that the endpoint asks for,
            marked MFX-Delivery-Attempt: replay; or one dead letter by its id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, WebhookReplayAccepted]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WebhookReplay,
    idempotency_key: str,
) -> Optional[Union[Error, WebhookReplayAccepted]]:
    """Send again the events after a cursor of the stream, or one dead letter

    Args:
        id (UUID):
        idempotency_key (str):
        body (WebhookReplay): Send again every event after `after` that the endpoint asks for,
            marked MFX-Delivery-Attempt: replay; or one dead letter by its id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, WebhookReplayAccepted]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

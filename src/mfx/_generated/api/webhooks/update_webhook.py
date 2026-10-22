from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.webhook_endpoint import WebhookEndpoint
from ...models.webhook_endpoint_update import WebhookEndpointUpdate
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: WebhookEndpointUpdate,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/webhooks/{id}".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, WebhookEndpoint]:
    if response.status_code == 200:
        response_200 = WebhookEndpoint.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, WebhookEndpoint]]:
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
    body: WebhookEndpointUpdate,
    idempotency_key: str,
) -> Response[Union[Error, WebhookEndpoint]]:
    """Change the address or the event types, pause or resume

    Args:
        id (UUID):
        idempotency_key (str):
        body (WebhookEndpointUpdate): Fields left out keep their value. `status: active` resumes
            an endpoint paused by the tenant, an operator or the platform; `paused` pauses it

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, WebhookEndpoint]]
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
    body: WebhookEndpointUpdate,
    idempotency_key: str,
) -> Optional[Union[Error, WebhookEndpoint]]:
    """Change the address or the event types, pause or resume

    Args:
        id (UUID):
        idempotency_key (str):
        body (WebhookEndpointUpdate): Fields left out keep their value. `status: active` resumes
            an endpoint paused by the tenant, an operator or the platform; `paused` pauses it

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, WebhookEndpoint]
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
    body: WebhookEndpointUpdate,
    idempotency_key: str,
) -> Response[Union[Error, WebhookEndpoint]]:
    """Change the address or the event types, pause or resume

    Args:
        id (UUID):
        idempotency_key (str):
        body (WebhookEndpointUpdate): Fields left out keep their value. `status: active` resumes
            an endpoint paused by the tenant, an operator or the platform; `paused` pauses it

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, WebhookEndpoint]]
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
    body: WebhookEndpointUpdate,
    idempotency_key: str,
) -> Optional[Union[Error, WebhookEndpoint]]:
    """Change the address or the event types, pause or resume

    Args:
        id (UUID):
        idempotency_key (str):
        body (WebhookEndpointUpdate): Fields left out keep their value. `status: active` resumes
            an endpoint paused by the tenant, an operator or the platform; `paused` pauses it

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, WebhookEndpoint]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

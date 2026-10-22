from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.webhook_endpoint_create import WebhookEndpointCreate
from ...models.webhook_endpoint_created import WebhookEndpointCreated
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: WebhookEndpointCreate,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/webhooks",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, WebhookEndpointCreated]:
    if response.status_code == 201:
        response_201 = WebhookEndpointCreated.from_dict(response.json())

        return response_201

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, WebhookEndpointCreated]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: WebhookEndpointCreate,
    idempotency_key: str,
) -> Response[Union[Error, WebhookEndpointCreated]]:
    """Register an endpoint; its signing secret is in this answer and in no other

    Args:
        idempotency_key (str):
        body (WebhookEndpointCreate): An address MFX Hub calls for the tenant's events. `https`
            only, port 443 or 8443, a host name and not an address, no credentials in the URL; a name
            that resolves to a private, loopback, link-local, metadata or MFX Hub address is refused
            with 422. The number of endpoints a tenant may have is limited (409 `quota_exceeded`).
            Each delivery's body is the event as the `events` channel carries its `data`: `type`, the
            fields of the schema `x-event-payloads` on `/stream` names for that type, and `id`, the
            event's cursor (`MFX-Event-Id`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, WebhookEndpointCreated]]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: WebhookEndpointCreate,
    idempotency_key: str,
) -> Optional[Union[Error, WebhookEndpointCreated]]:
    """Register an endpoint; its signing secret is in this answer and in no other

    Args:
        idempotency_key (str):
        body (WebhookEndpointCreate): An address MFX Hub calls for the tenant's events. `https`
            only, port 443 or 8443, a host name and not an address, no credentials in the URL; a name
            that resolves to a private, loopback, link-local, metadata or MFX Hub address is refused
            with 422. The number of endpoints a tenant may have is limited (409 `quota_exceeded`).
            Each delivery's body is the event as the `events` channel carries its `data`: `type`, the
            fields of the schema `x-event-payloads` on `/stream` names for that type, and `id`, the
            event's cursor (`MFX-Event-Id`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, WebhookEndpointCreated]
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: WebhookEndpointCreate,
    idempotency_key: str,
) -> Response[Union[Error, WebhookEndpointCreated]]:
    """Register an endpoint; its signing secret is in this answer and in no other

    Args:
        idempotency_key (str):
        body (WebhookEndpointCreate): An address MFX Hub calls for the tenant's events. `https`
            only, port 443 or 8443, a host name and not an address, no credentials in the URL; a name
            that resolves to a private, loopback, link-local, metadata or MFX Hub address is refused
            with 422. The number of endpoints a tenant may have is limited (409 `quota_exceeded`).
            Each delivery's body is the event as the `events` channel carries its `data`: `type`, the
            fields of the schema `x-event-payloads` on `/stream` names for that type, and `id`, the
            event's cursor (`MFX-Event-Id`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, WebhookEndpointCreated]]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: WebhookEndpointCreate,
    idempotency_key: str,
) -> Optional[Union[Error, WebhookEndpointCreated]]:
    """Register an endpoint; its signing secret is in this answer and in no other

    Args:
        idempotency_key (str):
        body (WebhookEndpointCreate): An address MFX Hub calls for the tenant's events. `https`
            only, port 443 or 8443, a host name and not an address, no credentials in the URL; a name
            that resolves to a private, loopback, link-local, metadata or MFX Hub address is refused
            with 422. The number of endpoints a tenant may have is limited (409 `quota_exceeded`).
            Each delivery's body is the event as the `events` channel carries its `data`: `type`, the
            fields of the schema `x-event-payloads` on `/stream` names for that type, and `id`, the
            event's cursor (`MFX-Event-Id`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, WebhookEndpointCreated]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.md_subscription import MdSubscription
from ...models.md_subscription_create import MdSubscriptionCreate
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: MdSubscriptionCreate,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/md/subscriptions",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, MdSubscription]:
    if response.status_code == 201:
        response_201 = MdSubscription.from_dict(response.json())

        return response_201

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, MdSubscription]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: MdSubscriptionCreate,
    idempotency_key: str,
) -> Response[Union[Error, MdSubscription]]:
    """Streaming subscription (server, symbol, timeframes, delivery ws|redis_push) — state pending until
    first tick

     A resource, not a command: it is created at once and answered as it is, in state `pending` until its
    first tick arrives — a subscription that never ticks stays visibly pending rather than looking live.

    Args:
        idempotency_key (str):
        body (MdSubscriptionCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, MdSubscription]]
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
    body: MdSubscriptionCreate,
    idempotency_key: str,
) -> Optional[Union[Error, MdSubscription]]:
    """Streaming subscription (server, symbol, timeframes, delivery ws|redis_push) — state pending until
    first tick

     A resource, not a command: it is created at once and answered as it is, in state `pending` until its
    first tick arrives — a subscription that never ticks stays visibly pending rather than looking live.

    Args:
        idempotency_key (str):
        body (MdSubscriptionCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, MdSubscription]
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: MdSubscriptionCreate,
    idempotency_key: str,
) -> Response[Union[Error, MdSubscription]]:
    """Streaming subscription (server, symbol, timeframes, delivery ws|redis_push) — state pending until
    first tick

     A resource, not a command: it is created at once and answered as it is, in state `pending` until its
    first tick arrives — a subscription that never ticks stays visibly pending rather than looking live.

    Args:
        idempotency_key (str):
        body (MdSubscriptionCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, MdSubscription]]
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
    body: MdSubscriptionCreate,
    idempotency_key: str,
) -> Optional[Union[Error, MdSubscription]]:
    """Streaming subscription (server, symbol, timeframes, delivery ws|redis_push) — state pending until
    first tick

     A resource, not a command: it is created at once and answered as it is, in state `pending` until its
    first tick arrives — a subscription that never ticks stays visibly pending rather than looking live.

    Args:
        idempotency_key (str):
        body (MdSubscriptionCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, MdSubscription]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

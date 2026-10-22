from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/stream",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, Error]:
    if response.status_code == 101:
        response_101 = cast(Any, None)
        return response_101

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Error]]:
    """WebSocket upgrade (wss://ws.mfxhub.com/v1/stream; dev wss://ws.dev.mfxhub.com/v1/stream) — Ed25519
    signature at upgrade (mfxSignature); channels md · candles · events · results · account · ea · book;
    24 h max lifetime; drop-oldest ticks per slow client

     Control messages are JSON: `StreamClientMessage` in, `StreamServerMessage` out. Channels are keyed
    by id (`StreamChannel`). Results and events carry a per-channel `seq` and are replayed on `resume`
    for up to 15 minutes; ticks and candles are not replayed. Account state travels on the terminal's
    own `account:{terminal_id}` channel, not on `events`: `account.snapshot` on every subscribe and
    resume (a snapshot, never a replay), when the position set changes and every 60 s, and
    `account.marks` in between. Account messages are samples: a slow client loses them before any event,
    and a `seq` gap means resume. `position.*` and `account.profile_changed` stay on `events`; fills
    stay on `results:{terminal_id}`. Market depth travels on `book:{server_id}:{symbol}` as `md.book`:
    the newest book on subscribe, then each change. While a planned maintenance window suspends the
    tenant's market data, its `md:`, `candles:` and `book:` channels carry an `md.status` of
    `maintenance` and no data, then `live` when it ends (`MdStatusMessage`). The upgrade request is
    signed as any call is (`mfxSignature`, Ed25519): over `GET`, the path with its query and an empty
    body. Each event's `data` is described by the schema `x-event-payloads` names for its type; on
    `events` it also carries the `type`. Close codes are listed in `x-close-codes`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Error]]:
    """WebSocket upgrade (wss://ws.mfxhub.com/v1/stream; dev wss://ws.dev.mfxhub.com/v1/stream) — Ed25519
    signature at upgrade (mfxSignature); channels md · candles · events · results · account · ea · book;
    24 h max lifetime; drop-oldest ticks per slow client

     Control messages are JSON: `StreamClientMessage` in, `StreamServerMessage` out. Channels are keyed
    by id (`StreamChannel`). Results and events carry a per-channel `seq` and are replayed on `resume`
    for up to 15 minutes; ticks and candles are not replayed. Account state travels on the terminal's
    own `account:{terminal_id}` channel, not on `events`: `account.snapshot` on every subscribe and
    resume (a snapshot, never a replay), when the position set changes and every 60 s, and
    `account.marks` in between. Account messages are samples: a slow client loses them before any event,
    and a `seq` gap means resume. `position.*` and `account.profile_changed` stay on `events`; fills
    stay on `results:{terminal_id}`. Market depth travels on `book:{server_id}:{symbol}` as `md.book`:
    the newest book on subscribe, then each change. While a planned maintenance window suspends the
    tenant's market data, its `md:`, `candles:` and `book:` channels carry an `md.status` of
    `maintenance` and no data, then `live` when it ends (`MdStatusMessage`). The upgrade request is
    signed as any call is (`mfxSignature`, Ed25519): over `GET`, the path with its query and an empty
    body. Each event's `data` is described by the schema `x-event-payloads` names for its type; on
    `events` it also carries the `type`. Close codes are listed in `x-close-codes`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Error]]:
    """WebSocket upgrade (wss://ws.mfxhub.com/v1/stream; dev wss://ws.dev.mfxhub.com/v1/stream) — Ed25519
    signature at upgrade (mfxSignature); channels md · candles · events · results · account · ea · book;
    24 h max lifetime; drop-oldest ticks per slow client

     Control messages are JSON: `StreamClientMessage` in, `StreamServerMessage` out. Channels are keyed
    by id (`StreamChannel`). Results and events carry a per-channel `seq` and are replayed on `resume`
    for up to 15 minutes; ticks and candles are not replayed. Account state travels on the terminal's
    own `account:{terminal_id}` channel, not on `events`: `account.snapshot` on every subscribe and
    resume (a snapshot, never a replay), when the position set changes and every 60 s, and
    `account.marks` in between. Account messages are samples: a slow client loses them before any event,
    and a `seq` gap means resume. `position.*` and `account.profile_changed` stay on `events`; fills
    stay on `results:{terminal_id}`. Market depth travels on `book:{server_id}:{symbol}` as `md.book`:
    the newest book on subscribe, then each change. While a planned maintenance window suspends the
    tenant's market data, its `md:`, `candles:` and `book:` channels carry an `md.status` of
    `maintenance` and no data, then `live` when it ends (`MdStatusMessage`). The upgrade request is
    signed as any call is (`mfxSignature`, Ed25519): over `GET`, the path with its query and an empty
    body. Each event's `data` is described by the schema `x-event-payloads` names for its type; on
    `events` it also carries the `type`. Close codes are listed in `x-close-codes`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Error]]:
    """WebSocket upgrade (wss://ws.mfxhub.com/v1/stream; dev wss://ws.dev.mfxhub.com/v1/stream) — Ed25519
    signature at upgrade (mfxSignature); channels md · candles · events · results · account · ea · book;
    24 h max lifetime; drop-oldest ticks per slow client

     Control messages are JSON: `StreamClientMessage` in, `StreamServerMessage` out. Channels are keyed
    by id (`StreamChannel`). Results and events carry a per-channel `seq` and are replayed on `resume`
    for up to 15 minutes; ticks and candles are not replayed. Account state travels on the terminal's
    own `account:{terminal_id}` channel, not on `events`: `account.snapshot` on every subscribe and
    resume (a snapshot, never a replay), when the position set changes and every 60 s, and
    `account.marks` in between. Account messages are samples: a slow client loses them before any event,
    and a `seq` gap means resume. `position.*` and `account.profile_changed` stay on `events`; fills
    stay on `results:{terminal_id}`. Market depth travels on `book:{server_id}:{symbol}` as `md.book`:
    the newest book on subscribe, then each change. While a planned maintenance window suspends the
    tenant's market data, its `md:`, `candles:` and `book:` channels carry an `md.status` of
    `maintenance` and no data, then `live` when it ends (`MdStatusMessage`). The upgrade request is
    signed as any call is (`mfxSignature`, Ed25519): over `GET`, the path with its query and an empty
    body. Each event's `data` is described by the schema `x-event-payloads` names for its type; on
    `events` it also carries the `type`. Close codes are listed in `x-close-codes`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed

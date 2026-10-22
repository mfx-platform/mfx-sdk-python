from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.command_accepted import CommandAccepted
from ...models.error import Error
from ...models.trailing_stop_set import TrailingStopSet
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    ticket: int,
    *,
    body: TrailingStopSet,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/terminals/{id}/positions/{ticket}/trailing-stop".format(
            id=id,
            ticket=ticket,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CommandAccepted, Error]:
    if response.status_code == 202:
        response_202 = CommandAccepted.from_dict(response.json())

        return response_202

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CommandAccepted, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    ticket: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: TrailingStopSet,
    idempotency_key: str,
) -> Response[Union[CommandAccepted, Error]]:
    """Set or change a position's trailing stop, kept by the platform

     The platform keeps the record first, then a `TRAILING_STOP_SET` command carries it to the cell. If a
    cell restarts or a terminal moves, the platform sends it again within one account snapshot. A stop
    loss set by anyone else ends it and the tenant is told (`position.trailing_stop_changed`, reason
    `stop_changed`). Refused as any order is on a terminal that may not execute.

    Args:
        id (UUID):
        ticket (int):
        idempotency_key (str):
        body (TrailingStopSet): Keep this position's stop loss `distance` behind the best price it
            reaches. The platform moves the broker's stop, only ever tighter, at most once a second
            and by at least a tenth of the distance. Setting again replaces the distance and keeps
            what the stop has reached. Refused with `invalid_request` when the ticket is not an open
            position of this account, and `invalid_stops` when the distance is inside the symbol's
            stops level.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CommandAccepted, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        ticket=ticket,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    ticket: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: TrailingStopSet,
    idempotency_key: str,
) -> Optional[Union[CommandAccepted, Error]]:
    """Set or change a position's trailing stop, kept by the platform

     The platform keeps the record first, then a `TRAILING_STOP_SET` command carries it to the cell. If a
    cell restarts or a terminal moves, the platform sends it again within one account snapshot. A stop
    loss set by anyone else ends it and the tenant is told (`position.trailing_stop_changed`, reason
    `stop_changed`). Refused as any order is on a terminal that may not execute.

    Args:
        id (UUID):
        ticket (int):
        idempotency_key (str):
        body (TrailingStopSet): Keep this position's stop loss `distance` behind the best price it
            reaches. The platform moves the broker's stop, only ever tighter, at most once a second
            and by at least a tenth of the distance. Setting again replaces the distance and keeps
            what the stop has reached. Refused with `invalid_request` when the ticket is not an open
            position of this account, and `invalid_stops` when the distance is inside the symbol's
            stops level.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CommandAccepted, Error]
    """

    return sync_detailed(
        id=id,
        ticket=ticket,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    ticket: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: TrailingStopSet,
    idempotency_key: str,
) -> Response[Union[CommandAccepted, Error]]:
    """Set or change a position's trailing stop, kept by the platform

     The platform keeps the record first, then a `TRAILING_STOP_SET` command carries it to the cell. If a
    cell restarts or a terminal moves, the platform sends it again within one account snapshot. A stop
    loss set by anyone else ends it and the tenant is told (`position.trailing_stop_changed`, reason
    `stop_changed`). Refused as any order is on a terminal that may not execute.

    Args:
        id (UUID):
        ticket (int):
        idempotency_key (str):
        body (TrailingStopSet): Keep this position's stop loss `distance` behind the best price it
            reaches. The platform moves the broker's stop, only ever tighter, at most once a second
            and by at least a tenth of the distance. Setting again replaces the distance and keeps
            what the stop has reached. Refused with `invalid_request` when the ticket is not an open
            position of this account, and `invalid_stops` when the distance is inside the symbol's
            stops level.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CommandAccepted, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        ticket=ticket,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    ticket: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: TrailingStopSet,
    idempotency_key: str,
) -> Optional[Union[CommandAccepted, Error]]:
    """Set or change a position's trailing stop, kept by the platform

     The platform keeps the record first, then a `TRAILING_STOP_SET` command carries it to the cell. If a
    cell restarts or a terminal moves, the platform sends it again within one account snapshot. A stop
    loss set by anyone else ends it and the tenant is told (`position.trailing_stop_changed`, reason
    `stop_changed`). Refused as any order is on a terminal that may not execute.

    Args:
        id (UUID):
        ticket (int):
        idempotency_key (str):
        body (TrailingStopSet): Keep this position's stop loss `distance` behind the best price it
            reaches. The platform moves the broker's stop, only ever tighter, at most once a second
            and by at least a tenth of the distance. Setting again replaces the distance and keeps
            what the stop has reached. Refused with `invalid_request` when the ticket is not an open
            position of this account, and `invalid_stops` when the distance is inside the symbol's
            stops level.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CommandAccepted, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            ticket=ticket,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_follower import CopyFollower
from ...models.copy_stopout_reset import CopyStopoutReset
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: CopyStopoutReset,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/copy/followers/{id}/stopouts/reset".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopyFollower, Error]:
    if response.status_code == 200:
        response_200 = CopyFollower.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopyFollower, Error]]:
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
    body: CopyStopoutReset,
    idempotency_key: str,
) -> Response[Union[CopyFollower, Error]]:
    """Reset a follower's active stop-outs before their period ends, with a reason

     Every active stop-out of the follower, or only the one for `limit`, becomes `reset`, with who reset
    it, when and why. The follower returns to `copying` once none is active, unless it is paused.
    Positions a stop-out closed stay closed. No active stop-out to reset is 409 `state_error` with
    `details.reason = no_active_stopout`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyStopoutReset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyFollower, Error]]
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
    body: CopyStopoutReset,
    idempotency_key: str,
) -> Optional[Union[CopyFollower, Error]]:
    """Reset a follower's active stop-outs before their period ends, with a reason

     Every active stop-out of the follower, or only the one for `limit`, becomes `reset`, with who reset
    it, when and why. The follower returns to `copying` once none is active, unless it is paused.
    Positions a stop-out closed stay closed. No active stop-out to reset is 409 `state_error` with
    `details.reason = no_active_stopout`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyStopoutReset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyFollower, Error]
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
    body: CopyStopoutReset,
    idempotency_key: str,
) -> Response[Union[CopyFollower, Error]]:
    """Reset a follower's active stop-outs before their period ends, with a reason

     Every active stop-out of the follower, or only the one for `limit`, becomes `reset`, with who reset
    it, when and why. The follower returns to `copying` once none is active, unless it is paused.
    Positions a stop-out closed stay closed. No active stop-out to reset is 409 `state_error` with
    `details.reason = no_active_stopout`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyStopoutReset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyFollower, Error]]
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
    body: CopyStopoutReset,
    idempotency_key: str,
) -> Optional[Union[CopyFollower, Error]]:
    """Reset a follower's active stop-outs before their period ends, with a reason

     Every active stop-out of the follower, or only the one for `limit`, becomes `reset`, with who reset
    it, when and why. The follower returns to `copying` once none is active, unless it is paused.
    Positions a stop-out closed stay closed. No active stop-out to reset is 409 `state_error` with
    `details.reason = no_active_stopout`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyStopoutReset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyFollower, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_leader import CopyLeader
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/copy/leaders/{id}/pause".format(
            id=id,
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopyLeader, Error]:
    if response.status_code == 200:
        response_200 = CopyLeader.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopyLeader, Error]]:
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
    idempotency_key: str,
) -> Response[Union[CopyLeader, Error]]:
    """Stop copying the leader's new entries; its closes and stop changes are still copied

     While a leader is paused its entries and pending orders are not copied, and each follower's log row
    says `refused` with reason `paused`. Its closes, partial closes and stop-loss and take-profit
    changes are still copied, so no follower is left holding a position its leader has closed. An
    external leader's open signals are refused 409 `state_error`; its close signals are taken. A leader
    already paused is answered as it is; a retired one is 409 `state_error`.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyLeader, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
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
    idempotency_key: str,
) -> Optional[Union[CopyLeader, Error]]:
    """Stop copying the leader's new entries; its closes and stop changes are still copied

     While a leader is paused its entries and pending orders are not copied, and each follower's log row
    says `refused` with reason `paused`. Its closes, partial closes and stop-loss and take-profit
    changes are still copied, so no follower is left holding a position its leader has closed. An
    external leader's open signals are refused 409 `state_error`; its close signals are taken. A leader
    already paused is answered as it is; a retired one is 409 `state_error`.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyLeader, Error]
    """

    return sync_detailed(
        id=id,
        client=client,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    idempotency_key: str,
) -> Response[Union[CopyLeader, Error]]:
    """Stop copying the leader's new entries; its closes and stop changes are still copied

     While a leader is paused its entries and pending orders are not copied, and each follower's log row
    says `refused` with reason `paused`. Its closes, partial closes and stop-loss and take-profit
    changes are still copied, so no follower is left holding a position its leader has closed. An
    external leader's open signals are refused 409 `state_error`; its close signals are taken. A leader
    already paused is answered as it is; a retired one is 409 `state_error`.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyLeader, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    idempotency_key: str,
) -> Optional[Union[CopyLeader, Error]]:
    """Stop copying the leader's new entries; its closes and stop changes are still copied

     While a leader is paused its entries and pending orders are not copied, and each follower's log row
    says `refused` with reason `paused`. Its closes, partial closes and stop-loss and take-profit
    changes are still copied, so no follower is left holding a position its leader has closed. An
    external leader's open signals are refused 409 `state_error`; its close signals are taken. A leader
    already paused is answered as it is; a retired one is 409 `state_error`.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyLeader, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            idempotency_key=idempotency_key,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_leader import CopyLeader
from ...models.copy_leader_retire import CopyLeaderRetire
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: CopyLeaderRetire,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/copy/leaders/{id}/retire".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

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
    body: CopyLeaderRetire,
    idempotency_key: str,
) -> Response[Union[CopyLeader, Error]]:
    """Retire a leader; every follow of it ends, and its copied positions are closed only if you ask

     Every follower of the leader that has not unfollowed becomes `unfollowed`, each with
    `copy.state_changed` (`why: leader_retired`). With `close_copied`, each follower's copied volume of
    this leader is closed, from the copied-position ledger, never the account's own positions; without
    it the copied positions stay open and are the account's own from then on. Retired is final: the
    account may lead again as a new leader. A leader already retired is answered as it is.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyLeaderRetire):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyLeader, Error]]
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
    body: CopyLeaderRetire,
    idempotency_key: str,
) -> Optional[Union[CopyLeader, Error]]:
    """Retire a leader; every follow of it ends, and its copied positions are closed only if you ask

     Every follower of the leader that has not unfollowed becomes `unfollowed`, each with
    `copy.state_changed` (`why: leader_retired`). With `close_copied`, each follower's copied volume of
    this leader is closed, from the copied-position ledger, never the account's own positions; without
    it the copied positions stay open and are the account's own from then on. Retired is final: the
    account may lead again as a new leader. A leader already retired is answered as it is.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyLeaderRetire):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyLeader, Error]
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
    body: CopyLeaderRetire,
    idempotency_key: str,
) -> Response[Union[CopyLeader, Error]]:
    """Retire a leader; every follow of it ends, and its copied positions are closed only if you ask

     Every follower of the leader that has not unfollowed becomes `unfollowed`, each with
    `copy.state_changed` (`why: leader_retired`). With `close_copied`, each follower's copied volume of
    this leader is closed, from the copied-position ledger, never the account's own positions; without
    it the copied positions stay open and are the account's own from then on. Retired is final: the
    account may lead again as a new leader. A leader already retired is answered as it is.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyLeaderRetire):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyLeader, Error]]
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
    body: CopyLeaderRetire,
    idempotency_key: str,
) -> Optional[Union[CopyLeader, Error]]:
    """Retire a leader; every follow of it ends, and its copied positions are closed only if you ask

     Every follower of the leader that has not unfollowed becomes `unfollowed`, each with
    `copy.state_changed` (`why: leader_retired`). With `close_copied`, each follower's copied volume of
    this leader is closed, from the copied-position ledger, never the account's own positions; without
    it the copied positions stay open and are the account's own from then on. Retired is final: the
    account may lead again as a new leader. A leader already retired is answered as it is.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyLeaderRetire):

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
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

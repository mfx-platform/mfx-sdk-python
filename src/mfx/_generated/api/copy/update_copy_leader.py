from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_leader import CopyLeader
from ...models.copy_leader_update import CopyLeaderUpdate
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: CopyLeaderUpdate,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/copy/leaders/{id}".format(
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
    body: CopyLeaderUpdate,
    idempotency_key: str,
) -> Response[Union[CopyLeader, Error]]:
    """Change what a leader's followers receive - its filters, what is copied, the signal lifetime, its
    limits and who may join

     Only the fields sent change. The source and the account are not fields here: a leader on another
    account is another leader. Applies to the next deal; a signal already made keeps what it was made
    with. A retired leader is 409 `state_error`. Narrowing who may join does not end a follow already
    made; unfollow it to end it.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyLeaderUpdate):

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
    body: CopyLeaderUpdate,
    idempotency_key: str,
) -> Optional[Union[CopyLeader, Error]]:
    """Change what a leader's followers receive - its filters, what is copied, the signal lifetime, its
    limits and who may join

     Only the fields sent change. The source and the account are not fields here: a leader on another
    account is another leader. Applies to the next deal; a signal already made keeps what it was made
    with. A retired leader is 409 `state_error`. Narrowing who may join does not end a follow already
    made; unfollow it to end it.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyLeaderUpdate):

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
    body: CopyLeaderUpdate,
    idempotency_key: str,
) -> Response[Union[CopyLeader, Error]]:
    """Change what a leader's followers receive - its filters, what is copied, the signal lifetime, its
    limits and who may join

     Only the fields sent change. The source and the account are not fields here: a leader on another
    account is another leader. Applies to the next deal; a signal already made keeps what it was made
    with. A retired leader is 409 `state_error`. Narrowing who may join does not end a follow already
    made; unfollow it to end it.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyLeaderUpdate):

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
    body: CopyLeaderUpdate,
    idempotency_key: str,
) -> Optional[Union[CopyLeader, Error]]:
    """Change what a leader's followers receive - its filters, what is copied, the signal lifetime, its
    limits and who may join

     Only the fields sent change. The source and the account are not fields here: a leader on another
    account is another leader. Applies to the next deal; a signal already made keeps what it was made
    with. A retired leader is 409 `state_error`. Narrowing who may join does not end a follow already
    made; unfollow it to end it.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyLeaderUpdate):

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

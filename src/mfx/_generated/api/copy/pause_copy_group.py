from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_group import CopyGroup
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
        "url": "/copy/groups/{id}/pause".format(
            id=id,
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopyGroup, Error]:
    if response.status_code == 200:
        response_200 = CopyGroup.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopyGroup, Error]]:
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
) -> Response[Union[CopyGroup, Error]]:
    """Stop copying new entries to every follower of the group at once; closes still are

     While the group is paused its followers' entries are logged `refused` with reason `paused`; closes,
    partial closes and stop changes of what they copied are still copied. Each follower keeps its own
    state, so resuming the group restores each one as it was. A group already paused is answered as it
    is.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyGroup, Error]]
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
) -> Optional[Union[CopyGroup, Error]]:
    """Stop copying new entries to every follower of the group at once; closes still are

     While the group is paused its followers' entries are logged `refused` with reason `paused`; closes,
    partial closes and stop changes of what they copied are still copied. Each follower keeps its own
    state, so resuming the group restores each one as it was. A group already paused is answered as it
    is.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyGroup, Error]
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
) -> Response[Union[CopyGroup, Error]]:
    """Stop copying new entries to every follower of the group at once; closes still are

     While the group is paused its followers' entries are logged `refused` with reason `paused`; closes,
    partial closes and stop changes of what they copied are still copied. Each follower keeps its own
    state, so resuming the group restores each one as it was. A group already paused is answered as it
    is.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyGroup, Error]]
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
) -> Optional[Union[CopyGroup, Error]]:
    """Stop copying new entries to every follower of the group at once; closes still are

     While the group is paused its followers' entries are logged `refused` with reason `paused`; closes,
    partial closes and stop changes of what they copied are still copied. Each follower keeps its own
    state, so resuming the group restores each one as it was. A group already paused is answered as it
    is.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyGroup, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            idempotency_key=idempotency_key,
        )
    ).parsed

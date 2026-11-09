from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_group_members import CopyGroupMembers
from ...models.copy_group_members_result import CopyGroupMembersResult
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: CopyGroupMembers,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/copy/groups/{id}/followers/remove".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopyGroupMembersResult, Error]:
    if response.status_code == 200:
        response_200 = CopyGroupMembersResult.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopyGroupMembersResult, Error]]:
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
    body: CopyGroupMembers,
    idempotency_key: str,
) -> Response[Union[CopyGroupMembersResult, Error]]:
    """Take followers out of the group; they keep following with their own mandates

     A follower not in this group is answered unchanged. Its mandate and state are not changed; the
    group's exposure cap and pause no longer apply to it

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyGroupMembers):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyGroupMembersResult, Error]]
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
    body: CopyGroupMembers,
    idempotency_key: str,
) -> Optional[Union[CopyGroupMembersResult, Error]]:
    """Take followers out of the group; they keep following with their own mandates

     A follower not in this group is answered unchanged. Its mandate and state are not changed; the
    group's exposure cap and pause no longer apply to it

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyGroupMembers):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyGroupMembersResult, Error]
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
    body: CopyGroupMembers,
    idempotency_key: str,
) -> Response[Union[CopyGroupMembersResult, Error]]:
    """Take followers out of the group; they keep following with their own mandates

     A follower not in this group is answered unchanged. Its mandate and state are not changed; the
    group's exposure cap and pause no longer apply to it

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyGroupMembers):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyGroupMembersResult, Error]]
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
    body: CopyGroupMembers,
    idempotency_key: str,
) -> Optional[Union[CopyGroupMembersResult, Error]]:
    """Take followers out of the group; they keep following with their own mandates

     A follower not in this group is answered unchanged. Its mandate and state are not changed; the
    group's exposure cap and pause no longer apply to it

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyGroupMembers):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyGroupMembersResult, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

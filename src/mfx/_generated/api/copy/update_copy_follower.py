from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_follower import CopyFollower
from ...models.copy_follower_update import CopyFollowerUpdate
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: CopyFollowerUpdate,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/copy/followers/{id}".format(
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

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

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
    body: CopyFollowerUpdate,
    idempotency_key: str,
) -> Response[Union[CopyFollower, Error]]:
    """Change a follower's scaling, bounds, symbol map, options, limits or close on stop-out; each change
    is a new mandate version

     Only the fields sent change, and the follower's account and leader are not among them. The change is
    checked as a follow is (`not_on_this_venue`, `needs_leader_account`) and, once accepted, is a new
    `mandate_version` sent to the account's copy host; a signal is copied under the version the host
    holds when it arrives. An unfollowed follower is 409 `state_error`. Group membership changes through
    the group's routes.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyFollowerUpdate):

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
    body: CopyFollowerUpdate,
    idempotency_key: str,
) -> Optional[Union[CopyFollower, Error]]:
    """Change a follower's scaling, bounds, symbol map, options, limits or close on stop-out; each change
    is a new mandate version

     Only the fields sent change, and the follower's account and leader are not among them. The change is
    checked as a follow is (`not_on_this_venue`, `needs_leader_account`) and, once accepted, is a new
    `mandate_version` sent to the account's copy host; a signal is copied under the version the host
    holds when it arrives. An unfollowed follower is 409 `state_error`. Group membership changes through
    the group's routes.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyFollowerUpdate):

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
    body: CopyFollowerUpdate,
    idempotency_key: str,
) -> Response[Union[CopyFollower, Error]]:
    """Change a follower's scaling, bounds, symbol map, options, limits or close on stop-out; each change
    is a new mandate version

     Only the fields sent change, and the follower's account and leader are not among them. The change is
    checked as a follow is (`not_on_this_venue`, `needs_leader_account`) and, once accepted, is a new
    `mandate_version` sent to the account's copy host; a signal is copied under the version the host
    holds when it arrives. An unfollowed follower is 409 `state_error`. Group membership changes through
    the group's routes.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyFollowerUpdate):

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
    body: CopyFollowerUpdate,
    idempotency_key: str,
) -> Optional[Union[CopyFollower, Error]]:
    """Change a follower's scaling, bounds, symbol map, options, limits or close on stop-out; each change
    is a new mandate version

     Only the fields sent change, and the follower's account and leader are not among them. The change is
    checked as a follow is (`not_on_this_venue`, `needs_leader_account`) and, once accepted, is a new
    `mandate_version` sent to the account's copy host; a signal is copied under the version the host
    holds when it arrives. An unfollowed follower is 409 `state_error`. Group membership changes through
    the group's routes.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyFollowerUpdate):

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

from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_follower_page import CopyFollowerPage
from ...models.copy_follower_state import CopyFollowerState
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, list[CopyFollowerState]] = UNSET,
    leader_id: Union[Unset, UUID] = UNSET,
    account_id: Union[Unset, UUID] = UNSET,
    group_id: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    json_leader_id: Union[Unset, str] = UNSET
    if not isinstance(leader_id, Unset):
        json_leader_id = str(leader_id)
    params["leader_id"] = json_leader_id

    json_account_id: Union[Unset, str] = UNSET
    if not isinstance(account_id, Unset):
        json_account_id = str(account_id)
    params["account_id"] = json_account_id

    json_group_id: Union[Unset, str] = UNSET
    if not isinstance(group_id, Unset):
        json_group_id = str(group_id)
    params["group_id"] = json_group_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/copy/followers",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopyFollowerPage, Error]:
    if response.status_code == 200:
        response_200 = CopyFollowerPage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopyFollowerPage, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, list[CopyFollowerState]] = UNSET,
    leader_id: Union[Unset, UUID] = UNSET,
    account_id: Union[Unset, UUID] = UNSET,
    group_id: Union[Unset, UUID] = UNSET,
) -> Response[Union[CopyFollowerPage, Error]]:
    """Your followers, newest first, with a count of each state

     `state`, `leader_id`, `account_id` and `group_id` narrow the list in the query, before the page is
    cut. The stats row counts the followers the filters match, on every page.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, list[CopyFollowerState]]):
        leader_id (Union[Unset, UUID]):
        account_id (Union[Unset, UUID]):
        group_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyFollowerPage, Error]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        state=state,
        leader_id=leader_id,
        account_id=account_id,
        group_id=group_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, list[CopyFollowerState]] = UNSET,
    leader_id: Union[Unset, UUID] = UNSET,
    account_id: Union[Unset, UUID] = UNSET,
    group_id: Union[Unset, UUID] = UNSET,
) -> Optional[Union[CopyFollowerPage, Error]]:
    """Your followers, newest first, with a count of each state

     `state`, `leader_id`, `account_id` and `group_id` narrow the list in the query, before the page is
    cut. The stats row counts the followers the filters match, on every page.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, list[CopyFollowerState]]):
        leader_id (Union[Unset, UUID]):
        account_id (Union[Unset, UUID]):
        group_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyFollowerPage, Error]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        state=state,
        leader_id=leader_id,
        account_id=account_id,
        group_id=group_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, list[CopyFollowerState]] = UNSET,
    leader_id: Union[Unset, UUID] = UNSET,
    account_id: Union[Unset, UUID] = UNSET,
    group_id: Union[Unset, UUID] = UNSET,
) -> Response[Union[CopyFollowerPage, Error]]:
    """Your followers, newest first, with a count of each state

     `state`, `leader_id`, `account_id` and `group_id` narrow the list in the query, before the page is
    cut. The stats row counts the followers the filters match, on every page.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, list[CopyFollowerState]]):
        leader_id (Union[Unset, UUID]):
        account_id (Union[Unset, UUID]):
        group_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyFollowerPage, Error]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        state=state,
        leader_id=leader_id,
        account_id=account_id,
        group_id=group_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, list[CopyFollowerState]] = UNSET,
    leader_id: Union[Unset, UUID] = UNSET,
    account_id: Union[Unset, UUID] = UNSET,
    group_id: Union[Unset, UUID] = UNSET,
) -> Optional[Union[CopyFollowerPage, Error]]:
    """Your followers, newest first, with a count of each state

     `state`, `leader_id`, `account_id` and `group_id` narrow the list in the query, before the page is
    cut. The stats row counts the followers the filters match, on every page.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, list[CopyFollowerState]]):
        leader_id (Union[Unset, UUID]):
        account_id (Union[Unset, UUID]):
        group_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyFollowerPage, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            state=state,
            leader_id=leader_id,
            account_id=account_id,
            group_id=group_id,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_leader_page import CopyLeaderPage
from ...models.copy_leader_source import CopyLeaderSource
from ...models.copy_leader_state import CopyLeaderState
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, list[CopyLeaderState]] = UNSET,
    source: Union[Unset, CopyLeaderSource] = UNSET,
    account_id: Union[Unset, UUID] = UNSET,
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

    json_source: Union[Unset, str] = UNSET
    if not isinstance(source, Unset):
        json_source = source.value

    params["source"] = json_source

    json_account_id: Union[Unset, str] = UNSET
    if not isinstance(account_id, Unset):
        json_account_id = str(account_id)
    params["account_id"] = json_account_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/copy/leaders",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopyLeaderPage, Error]:
    if response.status_code == 200:
        response_200 = CopyLeaderPage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopyLeaderPage, Error]]:
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
    state: Union[Unset, list[CopyLeaderState]] = UNSET,
    source: Union[Unset, CopyLeaderSource] = UNSET,
    account_id: Union[Unset, UUID] = UNSET,
) -> Response[Union[CopyLeaderPage, Error]]:
    """Your leaders, newest first, with a count of each state

     `state`, `source` and `account_id` narrow the list in the query, before the page is cut. The stats
    row counts the leaders the filters match, on every page.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, list[CopyLeaderState]]):
        source (Union[Unset, CopyLeaderSource]): account: one of your accounts, whose fills are
            seen as they happen. external: a source that sends signals to the signals route
        account_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyLeaderPage, Error]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        state=state,
        source=source,
        account_id=account_id,
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
    state: Union[Unset, list[CopyLeaderState]] = UNSET,
    source: Union[Unset, CopyLeaderSource] = UNSET,
    account_id: Union[Unset, UUID] = UNSET,
) -> Optional[Union[CopyLeaderPage, Error]]:
    """Your leaders, newest first, with a count of each state

     `state`, `source` and `account_id` narrow the list in the query, before the page is cut. The stats
    row counts the leaders the filters match, on every page.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, list[CopyLeaderState]]):
        source (Union[Unset, CopyLeaderSource]): account: one of your accounts, whose fills are
            seen as they happen. external: a source that sends signals to the signals route
        account_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyLeaderPage, Error]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        state=state,
        source=source,
        account_id=account_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, list[CopyLeaderState]] = UNSET,
    source: Union[Unset, CopyLeaderSource] = UNSET,
    account_id: Union[Unset, UUID] = UNSET,
) -> Response[Union[CopyLeaderPage, Error]]:
    """Your leaders, newest first, with a count of each state

     `state`, `source` and `account_id` narrow the list in the query, before the page is cut. The stats
    row counts the leaders the filters match, on every page.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, list[CopyLeaderState]]):
        source (Union[Unset, CopyLeaderSource]): account: one of your accounts, whose fills are
            seen as they happen. external: a source that sends signals to the signals route
        account_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyLeaderPage, Error]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        state=state,
        source=source,
        account_id=account_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, list[CopyLeaderState]] = UNSET,
    source: Union[Unset, CopyLeaderSource] = UNSET,
    account_id: Union[Unset, UUID] = UNSET,
) -> Optional[Union[CopyLeaderPage, Error]]:
    """Your leaders, newest first, with a count of each state

     `state`, `source` and `account_id` narrow the list in the query, before the page is cut. The stats
    row counts the leaders the filters match, on every page.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, list[CopyLeaderState]]):
        source (Union[Unset, CopyLeaderSource]): account: one of your accounts, whose fills are
            seen as they happen. external: a source that sends signals to the signals route
        account_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyLeaderPage, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            state=state,
            source=source,
            account_id=account_id,
        )
    ).parsed

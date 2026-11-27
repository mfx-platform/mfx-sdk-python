import datetime
from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_stopout_state import CopyStopoutState
from ...models.copy_tenant_stopout_page import CopyTenantStopoutPage
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    state: Union[Unset, list[CopyStopoutState]] = UNSET,
    follower_id: Union[Unset, UUID] = UNSET,
    group_id: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_from_: Union[Unset, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to: Union[Unset, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    json_follower_id: Union[Unset, str] = UNSET
    if not isinstance(follower_id, Unset):
        json_follower_id = str(follower_id)
    params["follower_id"] = json_follower_id

    json_group_id: Union[Unset, str] = UNSET
    if not isinstance(group_id, Unset):
        json_group_id = str(group_id)
    params["group_id"] = json_group_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/copy/stopouts",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopyTenantStopoutPage, Error]:
    if response.status_code == 200:
        response_200 = CopyTenantStopoutPage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopyTenantStopoutPage, Error]]:
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
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    state: Union[Unset, list[CopyStopoutState]] = UNSET,
    follower_id: Union[Unset, UUID] = UNSET,
    group_id: Union[Unset, UUID] = UNSET,
) -> Response[Union[CopyTenantStopoutPage, Error]]:
    """Every stop-out of your followers over a window, newest first, with a count of each state

     Each stop-out as `listCopyStopouts` shows it, across every follower. Every filter narrows the rows
    in the query, before the page is cut, and the stats row counts every stop-out the window and the
    filters match, by state, on every page. The window is `from` to `to` on the stop-out's `created_at`,
    each inclusive, at most 31 days (422 `window_too_wide`); without `from` it is the last 24 hours, and
    a day is its two ends. `group_id` is the group's followers now. Another tenant's follower or group
    matches none.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        state (Union[Unset, list[CopyStopoutState]]):
        follower_id (Union[Unset, UUID]):
        group_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyTenantStopoutPage, Error]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        from_=from_,
        to=to,
        state=state,
        follower_id=follower_id,
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
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    state: Union[Unset, list[CopyStopoutState]] = UNSET,
    follower_id: Union[Unset, UUID] = UNSET,
    group_id: Union[Unset, UUID] = UNSET,
) -> Optional[Union[CopyTenantStopoutPage, Error]]:
    """Every stop-out of your followers over a window, newest first, with a count of each state

     Each stop-out as `listCopyStopouts` shows it, across every follower. Every filter narrows the rows
    in the query, before the page is cut, and the stats row counts every stop-out the window and the
    filters match, by state, on every page. The window is `from` to `to` on the stop-out's `created_at`,
    each inclusive, at most 31 days (422 `window_too_wide`); without `from` it is the last 24 hours, and
    a day is its two ends. `group_id` is the group's followers now. Another tenant's follower or group
    matches none.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        state (Union[Unset, list[CopyStopoutState]]):
        follower_id (Union[Unset, UUID]):
        group_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyTenantStopoutPage, Error]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        from_=from_,
        to=to,
        state=state,
        follower_id=follower_id,
        group_id=group_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    state: Union[Unset, list[CopyStopoutState]] = UNSET,
    follower_id: Union[Unset, UUID] = UNSET,
    group_id: Union[Unset, UUID] = UNSET,
) -> Response[Union[CopyTenantStopoutPage, Error]]:
    """Every stop-out of your followers over a window, newest first, with a count of each state

     Each stop-out as `listCopyStopouts` shows it, across every follower. Every filter narrows the rows
    in the query, before the page is cut, and the stats row counts every stop-out the window and the
    filters match, by state, on every page. The window is `from` to `to` on the stop-out's `created_at`,
    each inclusive, at most 31 days (422 `window_too_wide`); without `from` it is the last 24 hours, and
    a day is its two ends. `group_id` is the group's followers now. Another tenant's follower or group
    matches none.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        state (Union[Unset, list[CopyStopoutState]]):
        follower_id (Union[Unset, UUID]):
        group_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyTenantStopoutPage, Error]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        from_=from_,
        to=to,
        state=state,
        follower_id=follower_id,
        group_id=group_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    state: Union[Unset, list[CopyStopoutState]] = UNSET,
    follower_id: Union[Unset, UUID] = UNSET,
    group_id: Union[Unset, UUID] = UNSET,
) -> Optional[Union[CopyTenantStopoutPage, Error]]:
    """Every stop-out of your followers over a window, newest first, with a count of each state

     Each stop-out as `listCopyStopouts` shows it, across every follower. Every filter narrows the rows
    in the query, before the page is cut, and the stats row counts every stop-out the window and the
    filters match, by state, on every page. The window is `from` to `to` on the stop-out's `created_at`,
    each inclusive, at most 31 days (422 `window_too_wide`); without `from` it is the last 24 hours, and
    a day is its two ends. `group_id` is the group's followers now. Another tenant's follower or group
    matches none.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        state (Union[Unset, list[CopyStopoutState]]):
        follower_id (Union[Unset, UUID]):
        group_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyTenantStopoutPage, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            from_=from_,
            to=to,
            state=state,
            follower_id=follower_id,
            group_id=group_id,
        )
    ).parsed

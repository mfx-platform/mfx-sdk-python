import datetime
from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_log_page import CopyLogPage
from ...models.copy_outcome import CopyOutcome
from ...models.copy_reason import CopyReason
from ...models.error import Error
from ...models.list_copy_log_sort import ListCopyLogSort
from ...models.venue import Venue
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    leader_id: Union[Unset, UUID] = UNSET,
    follower_id: Union[Unset, UUID] = UNSET,
    account_id: Union[Unset, UUID] = UNSET,
    signal_id: Union[Unset, UUID] = UNSET,
    outcome: Union[Unset, list[CopyOutcome]] = UNSET,
    reason: Union[Unset, list[CopyReason]] = UNSET,
    venue: Union[Unset, list[Venue]] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    sort: Union[Unset, ListCopyLogSort] = ListCopyLogSort.CREATED_AT,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_leader_id: Union[Unset, str] = UNSET
    if not isinstance(leader_id, Unset):
        json_leader_id = str(leader_id)
    params["leader_id"] = json_leader_id

    json_follower_id: Union[Unset, str] = UNSET
    if not isinstance(follower_id, Unset):
        json_follower_id = str(follower_id)
    params["follower_id"] = json_follower_id

    json_account_id: Union[Unset, str] = UNSET
    if not isinstance(account_id, Unset):
        json_account_id = str(account_id)
    params["account_id"] = json_account_id

    json_signal_id: Union[Unset, str] = UNSET
    if not isinstance(signal_id, Unset):
        json_signal_id = str(signal_id)
    params["signal_id"] = json_signal_id

    json_outcome: Union[Unset, list[str]] = UNSET
    if not isinstance(outcome, Unset):
        json_outcome = []
        for outcome_item_data in outcome:
            outcome_item = outcome_item_data.value
            json_outcome.append(outcome_item)

    params["outcome"] = json_outcome

    json_reason: Union[Unset, list[str]] = UNSET
    if not isinstance(reason, Unset):
        json_reason = []
        for reason_item_data in reason:
            reason_item = reason_item_data.value
            json_reason.append(reason_item)

    params["reason"] = json_reason

    json_venue: Union[Unset, list[str]] = UNSET
    if not isinstance(venue, Unset):
        json_venue = []
        for venue_item_data in venue:
            venue_item = venue_item_data.value
            json_venue.append(venue_item)

    params["venue"] = json_venue

    json_from_: Union[Unset, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to: Union[Unset, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/copy/log",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopyLogPage, Error]:
    if response.status_code == 200:
        response_200 = CopyLogPage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopyLogPage, Error]]:
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
    leader_id: Union[Unset, UUID] = UNSET,
    follower_id: Union[Unset, UUID] = UNSET,
    account_id: Union[Unset, UUID] = UNSET,
    signal_id: Union[Unset, UUID] = UNSET,
    outcome: Union[Unset, list[CopyOutcome]] = UNSET,
    reason: Union[Unset, list[CopyReason]] = UNSET,
    venue: Union[Unset, list[Venue]] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    sort: Union[Unset, ListCopyLogSort] = ListCopyLogSort.CREATED_AT,
) -> Response[Union[CopyLogPage, Error]]:
    """What became of each copy - one row a follower a signal, with its outcome, reason and stage timings

     Newest first unless `sort` says otherwise. Every filter narrows the rows in the query, before the
    page is cut, and the stats row is over the same rows: the whole filtered window, on every page. The
    window is `from` to `to`, at most 31 days (422 `window_too_wide`); without `from` it is the last 24
    hours. Rows older than the plan's log retention are gone and are not returned. Times are
    milliseconds; MFX Hub's part of a copy (`mfx_ms`) is reported apart from the venue's (`broker_ms`).

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        leader_id (Union[Unset, UUID]):
        follower_id (Union[Unset, UUID]):
        account_id (Union[Unset, UUID]):
        signal_id (Union[Unset, UUID]):
        outcome (Union[Unset, list[CopyOutcome]]):
        reason (Union[Unset, list[CopyReason]]):
        venue (Union[Unset, list[Venue]]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        sort (Union[Unset, ListCopyLogSort]):  Default: ListCopyLogSort.CREATED_AT.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyLogPage, Error]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        leader_id=leader_id,
        follower_id=follower_id,
        account_id=account_id,
        signal_id=signal_id,
        outcome=outcome,
        reason=reason,
        venue=venue,
        from_=from_,
        to=to,
        sort=sort,
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
    leader_id: Union[Unset, UUID] = UNSET,
    follower_id: Union[Unset, UUID] = UNSET,
    account_id: Union[Unset, UUID] = UNSET,
    signal_id: Union[Unset, UUID] = UNSET,
    outcome: Union[Unset, list[CopyOutcome]] = UNSET,
    reason: Union[Unset, list[CopyReason]] = UNSET,
    venue: Union[Unset, list[Venue]] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    sort: Union[Unset, ListCopyLogSort] = ListCopyLogSort.CREATED_AT,
) -> Optional[Union[CopyLogPage, Error]]:
    """What became of each copy - one row a follower a signal, with its outcome, reason and stage timings

     Newest first unless `sort` says otherwise. Every filter narrows the rows in the query, before the
    page is cut, and the stats row is over the same rows: the whole filtered window, on every page. The
    window is `from` to `to`, at most 31 days (422 `window_too_wide`); without `from` it is the last 24
    hours. Rows older than the plan's log retention are gone and are not returned. Times are
    milliseconds; MFX Hub's part of a copy (`mfx_ms`) is reported apart from the venue's (`broker_ms`).

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        leader_id (Union[Unset, UUID]):
        follower_id (Union[Unset, UUID]):
        account_id (Union[Unset, UUID]):
        signal_id (Union[Unset, UUID]):
        outcome (Union[Unset, list[CopyOutcome]]):
        reason (Union[Unset, list[CopyReason]]):
        venue (Union[Unset, list[Venue]]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        sort (Union[Unset, ListCopyLogSort]):  Default: ListCopyLogSort.CREATED_AT.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyLogPage, Error]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        leader_id=leader_id,
        follower_id=follower_id,
        account_id=account_id,
        signal_id=signal_id,
        outcome=outcome,
        reason=reason,
        venue=venue,
        from_=from_,
        to=to,
        sort=sort,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    leader_id: Union[Unset, UUID] = UNSET,
    follower_id: Union[Unset, UUID] = UNSET,
    account_id: Union[Unset, UUID] = UNSET,
    signal_id: Union[Unset, UUID] = UNSET,
    outcome: Union[Unset, list[CopyOutcome]] = UNSET,
    reason: Union[Unset, list[CopyReason]] = UNSET,
    venue: Union[Unset, list[Venue]] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    sort: Union[Unset, ListCopyLogSort] = ListCopyLogSort.CREATED_AT,
) -> Response[Union[CopyLogPage, Error]]:
    """What became of each copy - one row a follower a signal, with its outcome, reason and stage timings

     Newest first unless `sort` says otherwise. Every filter narrows the rows in the query, before the
    page is cut, and the stats row is over the same rows: the whole filtered window, on every page. The
    window is `from` to `to`, at most 31 days (422 `window_too_wide`); without `from` it is the last 24
    hours. Rows older than the plan's log retention are gone and are not returned. Times are
    milliseconds; MFX Hub's part of a copy (`mfx_ms`) is reported apart from the venue's (`broker_ms`).

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        leader_id (Union[Unset, UUID]):
        follower_id (Union[Unset, UUID]):
        account_id (Union[Unset, UUID]):
        signal_id (Union[Unset, UUID]):
        outcome (Union[Unset, list[CopyOutcome]]):
        reason (Union[Unset, list[CopyReason]]):
        venue (Union[Unset, list[Venue]]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        sort (Union[Unset, ListCopyLogSort]):  Default: ListCopyLogSort.CREATED_AT.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyLogPage, Error]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        leader_id=leader_id,
        follower_id=follower_id,
        account_id=account_id,
        signal_id=signal_id,
        outcome=outcome,
        reason=reason,
        venue=venue,
        from_=from_,
        to=to,
        sort=sort,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    leader_id: Union[Unset, UUID] = UNSET,
    follower_id: Union[Unset, UUID] = UNSET,
    account_id: Union[Unset, UUID] = UNSET,
    signal_id: Union[Unset, UUID] = UNSET,
    outcome: Union[Unset, list[CopyOutcome]] = UNSET,
    reason: Union[Unset, list[CopyReason]] = UNSET,
    venue: Union[Unset, list[Venue]] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    sort: Union[Unset, ListCopyLogSort] = ListCopyLogSort.CREATED_AT,
) -> Optional[Union[CopyLogPage, Error]]:
    """What became of each copy - one row a follower a signal, with its outcome, reason and stage timings

     Newest first unless `sort` says otherwise. Every filter narrows the rows in the query, before the
    page is cut, and the stats row is over the same rows: the whole filtered window, on every page. The
    window is `from` to `to`, at most 31 days (422 `window_too_wide`); without `from` it is the last 24
    hours. Rows older than the plan's log retention are gone and are not returned. Times are
    milliseconds; MFX Hub's part of a copy (`mfx_ms`) is reported apart from the venue's (`broker_ms`).

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        leader_id (Union[Unset, UUID]):
        follower_id (Union[Unset, UUID]):
        account_id (Union[Unset, UUID]):
        signal_id (Union[Unset, UUID]):
        outcome (Union[Unset, list[CopyOutcome]]):
        reason (Union[Unset, list[CopyReason]]):
        venue (Union[Unset, list[Venue]]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        sort (Union[Unset, ListCopyLogSort]):  Default: ListCopyLogSort.CREATED_AT.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyLogPage, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            leader_id=leader_id,
            follower_id=follower_id,
            account_id=account_id,
            signal_id=signal_id,
            outcome=outcome,
            reason=reason,
            venue=venue,
            from_=from_,
            to=to,
            sort=sort,
        )
    ).parsed

import datetime
from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.risk_activity_kind import RiskActivityKind
from ...models.risk_activity_page import RiskActivityPage
from ...models.risk_outcome import RiskOutcome
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    kind: Union[Unset, list[RiskActivityKind]] = UNSET,
    terminal_id: Union[Unset, UUID] = UNSET,
    outcome: Union[Unset, RiskOutcome] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_kind: Union[Unset, list[str]] = UNSET
    if not isinstance(kind, Unset):
        json_kind = []
        for kind_item_data in kind:
            kind_item = kind_item_data.value
            json_kind.append(kind_item)

    params["kind"] = json_kind

    json_terminal_id: Union[Unset, str] = UNSET
    if not isinstance(terminal_id, Unset):
        json_terminal_id = str(terminal_id)
    params["terminal_id"] = json_terminal_id

    json_outcome: Union[Unset, str] = UNSET
    if not isinstance(outcome, Unset):
        json_outcome = outcome.value

    params["outcome"] = json_outcome

    json_from_: Union[Unset, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to: Union[Unset, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/risk/activity",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, RiskActivityPage]:
    if response.status_code == 200:
        response_200 = RiskActivityPage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, RiskActivityPage]]:
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
    kind: Union[Unset, list[RiskActivityKind]] = UNSET,
    terminal_id: Union[Unset, UUID] = UNSET,
    outcome: Union[Unset, RiskOutcome] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Union[Error, RiskActivityPage]]:
    """Every warning, breach, action and its outcome, policy and plan change, unresolved first, with
    evidence

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        kind (Union[Unset, list[RiskActivityKind]]):
        terminal_id (Union[Unset, UUID]):
        outcome (Union[Unset, RiskOutcome]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskActivityPage]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        kind=kind,
        terminal_id=terminal_id,
        outcome=outcome,
        from_=from_,
        to=to,
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
    kind: Union[Unset, list[RiskActivityKind]] = UNSET,
    terminal_id: Union[Unset, UUID] = UNSET,
    outcome: Union[Unset, RiskOutcome] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[Union[Error, RiskActivityPage]]:
    """Every warning, breach, action and its outcome, policy and plan change, unresolved first, with
    evidence

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        kind (Union[Unset, list[RiskActivityKind]]):
        terminal_id (Union[Unset, UUID]):
        outcome (Union[Unset, RiskOutcome]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskActivityPage]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        kind=kind,
        terminal_id=terminal_id,
        outcome=outcome,
        from_=from_,
        to=to,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    kind: Union[Unset, list[RiskActivityKind]] = UNSET,
    terminal_id: Union[Unset, UUID] = UNSET,
    outcome: Union[Unset, RiskOutcome] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Union[Error, RiskActivityPage]]:
    """Every warning, breach, action and its outcome, policy and plan change, unresolved first, with
    evidence

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        kind (Union[Unset, list[RiskActivityKind]]):
        terminal_id (Union[Unset, UUID]):
        outcome (Union[Unset, RiskOutcome]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskActivityPage]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        kind=kind,
        terminal_id=terminal_id,
        outcome=outcome,
        from_=from_,
        to=to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    kind: Union[Unset, list[RiskActivityKind]] = UNSET,
    terminal_id: Union[Unset, UUID] = UNSET,
    outcome: Union[Unset, RiskOutcome] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[Union[Error, RiskActivityPage]]:
    """Every warning, breach, action and its outcome, policy and plan change, unresolved first, with
    evidence

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        kind (Union[Unset, list[RiskActivityKind]]):
        terminal_id (Union[Unset, UUID]):
        outcome (Union[Unset, RiskOutcome]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskActivityPage]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            kind=kind,
            terminal_id=terminal_id,
            outcome=outcome,
            from_=from_,
            to=to,
        )
    ).parsed

import datetime
from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_risk_activity_sort import ListRiskActivitySort
from ...models.risk_activity_kind import RiskActivityKind
from ...models.risk_activity_page import RiskActivityPage
from ...models.risk_outcome import RiskOutcome
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    kind: Union[Unset, list[RiskActivityKind]] = UNSET,
    account_id: Union[Unset, list[UUID]] = UNSET,
    outcome: Union[Unset, list[RiskOutcome]] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    sort: Union[Unset, ListRiskActivitySort] = ListRiskActivitySort.UNRESOLVED_FIRST,
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

    json_account_id: Union[Unset, list[str]] = UNSET
    if not isinstance(account_id, Unset):
        json_account_id = []
        for account_id_item_data in account_id:
            account_id_item = str(account_id_item_data)
            json_account_id.append(account_id_item)

    params["account_id"] = json_account_id

    json_outcome: Union[Unset, list[str]] = UNSET
    if not isinstance(outcome, Unset):
        json_outcome = []
        for outcome_item_data in outcome:
            outcome_item = outcome_item_data.value
            json_outcome.append(outcome_item)

    params["outcome"] = json_outcome

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
    account_id: Union[Unset, list[UUID]] = UNSET,
    outcome: Union[Unset, list[RiskOutcome]] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    sort: Union[Unset, ListRiskActivitySort] = ListRiskActivitySort.UNRESOLVED_FIRST,
) -> Response[Union[Error, RiskActivityPage]]:
    """Every warning, breach, action and its outcome, policy and plan change, unresolved first, with
    evidence

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        kind (Union[Unset, list[RiskActivityKind]]):
        account_id (Union[Unset, list[UUID]]):
        outcome (Union[Unset, list[RiskOutcome]]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        sort (Union[Unset, ListRiskActivitySort]):  Default:
            ListRiskActivitySort.UNRESOLVED_FIRST.

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
        account_id=account_id,
        outcome=outcome,
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
    kind: Union[Unset, list[RiskActivityKind]] = UNSET,
    account_id: Union[Unset, list[UUID]] = UNSET,
    outcome: Union[Unset, list[RiskOutcome]] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    sort: Union[Unset, ListRiskActivitySort] = ListRiskActivitySort.UNRESOLVED_FIRST,
) -> Optional[Union[Error, RiskActivityPage]]:
    """Every warning, breach, action and its outcome, policy and plan change, unresolved first, with
    evidence

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        kind (Union[Unset, list[RiskActivityKind]]):
        account_id (Union[Unset, list[UUID]]):
        outcome (Union[Unset, list[RiskOutcome]]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        sort (Union[Unset, ListRiskActivitySort]):  Default:
            ListRiskActivitySort.UNRESOLVED_FIRST.

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
        account_id=account_id,
        outcome=outcome,
        from_=from_,
        to=to,
        sort=sort,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    kind: Union[Unset, list[RiskActivityKind]] = UNSET,
    account_id: Union[Unset, list[UUID]] = UNSET,
    outcome: Union[Unset, list[RiskOutcome]] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    sort: Union[Unset, ListRiskActivitySort] = ListRiskActivitySort.UNRESOLVED_FIRST,
) -> Response[Union[Error, RiskActivityPage]]:
    """Every warning, breach, action and its outcome, policy and plan change, unresolved first, with
    evidence

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        kind (Union[Unset, list[RiskActivityKind]]):
        account_id (Union[Unset, list[UUID]]):
        outcome (Union[Unset, list[RiskOutcome]]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        sort (Union[Unset, ListRiskActivitySort]):  Default:
            ListRiskActivitySort.UNRESOLVED_FIRST.

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
        account_id=account_id,
        outcome=outcome,
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
    kind: Union[Unset, list[RiskActivityKind]] = UNSET,
    account_id: Union[Unset, list[UUID]] = UNSET,
    outcome: Union[Unset, list[RiskOutcome]] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    sort: Union[Unset, ListRiskActivitySort] = ListRiskActivitySort.UNRESOLVED_FIRST,
) -> Optional[Union[Error, RiskActivityPage]]:
    """Every warning, breach, action and its outcome, policy and plan change, unresolved first, with
    evidence

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        kind (Union[Unset, list[RiskActivityKind]]):
        account_id (Union[Unset, list[UUID]]):
        outcome (Union[Unset, list[RiskOutcome]]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        sort (Union[Unset, ListRiskActivitySort]):  Default:
            ListRiskActivitySort.UNRESOLVED_FIRST.

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
            account_id=account_id,
            outcome=outcome,
            from_=from_,
            to=to,
            sort=sort,
        )
    ).parsed

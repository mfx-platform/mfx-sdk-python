from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_risk_challenge_accounts_rule import ListRiskChallengeAccountsRule
from ...models.list_risk_challenge_accounts_sort import ListRiskChallengeAccountsSort
from ...models.list_risk_challenge_accounts_state import ListRiskChallengeAccountsState
from ...models.risk_challenge_account_page import RiskChallengeAccountPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, ListRiskChallengeAccountsState] = UNSET,
    rule: Union[Unset, ListRiskChallengeAccountsRule] = UNSET,
    below_min_days: Union[Unset, bool] = UNSET,
    sort: Union[
        Unset, ListRiskChallengeAccountsSort
    ] = ListRiskChallengeAccountsSort.DAILY_LOSS_USED,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_state: Union[Unset, str] = UNSET
    if not isinstance(state, Unset):
        json_state = state.value

    params["state"] = json_state

    json_rule: Union[Unset, str] = UNSET
    if not isinstance(rule, Unset):
        json_rule = rule.value

    params["rule"] = json_rule

    params["below_min_days"] = below_min_days

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/risk/challenges/{id}/accounts".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, RiskChallengeAccountPage]:
    if response.status_code == 200:
        response_200 = RiskChallengeAccountPage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, RiskChallengeAccountPage]]:
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
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, ListRiskChallengeAccountsState] = UNSET,
    rule: Union[Unset, ListRiskChallengeAccountsRule] = UNSET,
    below_min_days: Union[Unset, bool] = UNSET,
    sort: Union[
        Unset, ListRiskChallengeAccountsSort
    ] = ListRiskChallengeAccountsSort.DAILY_LOSS_USED,
) -> Response[Union[Error, RiskChallengeAccountPage]]:
    """The challenge's accounts and their results; this list, paged, is the export

    Args:
        id (UUID):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, ListRiskChallengeAccountsState]):
        rule (Union[Unset, ListRiskChallengeAccountsRule]):
        below_min_days (Union[Unset, bool]):
        sort (Union[Unset, ListRiskChallengeAccountsSort]):  Default:
            ListRiskChallengeAccountsSort.DAILY_LOSS_USED.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskChallengeAccountPage]]
    """

    kwargs = _get_kwargs(
        id=id,
        cursor=cursor,
        limit=limit,
        state=state,
        rule=rule,
        below_min_days=below_min_days,
        sort=sort,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, ListRiskChallengeAccountsState] = UNSET,
    rule: Union[Unset, ListRiskChallengeAccountsRule] = UNSET,
    below_min_days: Union[Unset, bool] = UNSET,
    sort: Union[
        Unset, ListRiskChallengeAccountsSort
    ] = ListRiskChallengeAccountsSort.DAILY_LOSS_USED,
) -> Optional[Union[Error, RiskChallengeAccountPage]]:
    """The challenge's accounts and their results; this list, paged, is the export

    Args:
        id (UUID):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, ListRiskChallengeAccountsState]):
        rule (Union[Unset, ListRiskChallengeAccountsRule]):
        below_min_days (Union[Unset, bool]):
        sort (Union[Unset, ListRiskChallengeAccountsSort]):  Default:
            ListRiskChallengeAccountsSort.DAILY_LOSS_USED.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskChallengeAccountPage]
    """

    return sync_detailed(
        id=id,
        client=client,
        cursor=cursor,
        limit=limit,
        state=state,
        rule=rule,
        below_min_days=below_min_days,
        sort=sort,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, ListRiskChallengeAccountsState] = UNSET,
    rule: Union[Unset, ListRiskChallengeAccountsRule] = UNSET,
    below_min_days: Union[Unset, bool] = UNSET,
    sort: Union[
        Unset, ListRiskChallengeAccountsSort
    ] = ListRiskChallengeAccountsSort.DAILY_LOSS_USED,
) -> Response[Union[Error, RiskChallengeAccountPage]]:
    """The challenge's accounts and their results; this list, paged, is the export

    Args:
        id (UUID):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, ListRiskChallengeAccountsState]):
        rule (Union[Unset, ListRiskChallengeAccountsRule]):
        below_min_days (Union[Unset, bool]):
        sort (Union[Unset, ListRiskChallengeAccountsSort]):  Default:
            ListRiskChallengeAccountsSort.DAILY_LOSS_USED.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskChallengeAccountPage]]
    """

    kwargs = _get_kwargs(
        id=id,
        cursor=cursor,
        limit=limit,
        state=state,
        rule=rule,
        below_min_days=below_min_days,
        sort=sort,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, ListRiskChallengeAccountsState] = UNSET,
    rule: Union[Unset, ListRiskChallengeAccountsRule] = UNSET,
    below_min_days: Union[Unset, bool] = UNSET,
    sort: Union[
        Unset, ListRiskChallengeAccountsSort
    ] = ListRiskChallengeAccountsSort.DAILY_LOSS_USED,
) -> Optional[Union[Error, RiskChallengeAccountPage]]:
    """The challenge's accounts and their results; this list, paged, is the export

    Args:
        id (UUID):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, ListRiskChallengeAccountsState]):
        rule (Union[Unset, ListRiskChallengeAccountsRule]):
        below_min_days (Union[Unset, bool]):
        sort (Union[Unset, ListRiskChallengeAccountsSort]):  Default:
            ListRiskChallengeAccountsSort.DAILY_LOSS_USED.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskChallengeAccountPage]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            cursor=cursor,
            limit=limit,
            state=state,
            rule=rule,
            below_min_days=below_min_days,
            sort=sort,
        )
    ).parsed

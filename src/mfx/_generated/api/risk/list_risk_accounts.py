from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_risk_accounts_coverage import ListRiskAccountsCoverage
from ...models.list_risk_accounts_restriction import ListRiskAccountsRestriction
from ...models.list_risk_accounts_sort import ListRiskAccountsSort
from ...models.risk_account_page import RiskAccountPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    coverage: Union[Unset, ListRiskAccountsCoverage] = UNSET,
    restriction: Union[Unset, ListRiskAccountsRestriction] = UNSET,
    sort: Union[Unset, ListRiskAccountsSort] = ListRiskAccountsSort.DAILY_LOSS_USED,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_coverage: Union[Unset, str] = UNSET
    if not isinstance(coverage, Unset):
        json_coverage = coverage.value

    params["coverage"] = json_coverage

    json_restriction: Union[Unset, str] = UNSET
    if not isinstance(restriction, Unset):
        json_restriction = restriction.value

    params["restriction"] = json_restriction

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/risk/accounts",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, RiskAccountPage]:
    if response.status_code == 200:
        response_200 = RiskAccountPage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, RiskAccountPage]]:
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
    coverage: Union[Unset, ListRiskAccountsCoverage] = UNSET,
    restriction: Union[Unset, ListRiskAccountsRestriction] = UNSET,
    sort: Union[Unset, ListRiskAccountsSort] = ListRiskAccountsSort.DAILY_LOSS_USED,
) -> Response[Union[Error, RiskAccountPage]]:
    """Every account of the tenant with its allowance, drawdown, exposure, restriction and coverage

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        coverage (Union[Unset, ListRiskAccountsCoverage]):
        restriction (Union[Unset, ListRiskAccountsRestriction]):
        sort (Union[Unset, ListRiskAccountsSort]):  Default: ListRiskAccountsSort.DAILY_LOSS_USED.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskAccountPage]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        coverage=coverage,
        restriction=restriction,
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
    coverage: Union[Unset, ListRiskAccountsCoverage] = UNSET,
    restriction: Union[Unset, ListRiskAccountsRestriction] = UNSET,
    sort: Union[Unset, ListRiskAccountsSort] = ListRiskAccountsSort.DAILY_LOSS_USED,
) -> Optional[Union[Error, RiskAccountPage]]:
    """Every account of the tenant with its allowance, drawdown, exposure, restriction and coverage

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        coverage (Union[Unset, ListRiskAccountsCoverage]):
        restriction (Union[Unset, ListRiskAccountsRestriction]):
        sort (Union[Unset, ListRiskAccountsSort]):  Default: ListRiskAccountsSort.DAILY_LOSS_USED.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskAccountPage]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        coverage=coverage,
        restriction=restriction,
        sort=sort,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    coverage: Union[Unset, ListRiskAccountsCoverage] = UNSET,
    restriction: Union[Unset, ListRiskAccountsRestriction] = UNSET,
    sort: Union[Unset, ListRiskAccountsSort] = ListRiskAccountsSort.DAILY_LOSS_USED,
) -> Response[Union[Error, RiskAccountPage]]:
    """Every account of the tenant with its allowance, drawdown, exposure, restriction and coverage

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        coverage (Union[Unset, ListRiskAccountsCoverage]):
        restriction (Union[Unset, ListRiskAccountsRestriction]):
        sort (Union[Unset, ListRiskAccountsSort]):  Default: ListRiskAccountsSort.DAILY_LOSS_USED.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskAccountPage]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        coverage=coverage,
        restriction=restriction,
        sort=sort,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    coverage: Union[Unset, ListRiskAccountsCoverage] = UNSET,
    restriction: Union[Unset, ListRiskAccountsRestriction] = UNSET,
    sort: Union[Unset, ListRiskAccountsSort] = ListRiskAccountsSort.DAILY_LOSS_USED,
) -> Optional[Union[Error, RiskAccountPage]]:
    """Every account of the tenant with its allowance, drawdown, exposure, restriction and coverage

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        coverage (Union[Unset, ListRiskAccountsCoverage]):
        restriction (Union[Unset, ListRiskAccountsRestriction]):
        sort (Union[Unset, ListRiskAccountsSort]):  Default: ListRiskAccountsSort.DAILY_LOSS_USED.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskAccountPage]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            coverage=coverage,
            restriction=restriction,
            sort=sort,
        )
    ).parsed

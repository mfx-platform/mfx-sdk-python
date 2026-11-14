from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_risk_plans_sort import ListRiskPlansSort
from ...models.list_risk_plans_state_item import ListRiskPlansStateItem
from ...models.risk_plan_page import RiskPlanPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    account_id: Union[Unset, list[UUID]] = UNSET,
    state: Union[Unset, list[ListRiskPlansStateItem]] = UNSET,
    sort: Union[Unset, ListRiskPlansSort] = ListRiskPlansSort.NEWEST,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_account_id: Union[Unset, list[str]] = UNSET
    if not isinstance(account_id, Unset):
        json_account_id = []
        for account_id_item_data in account_id:
            account_id_item = str(account_id_item_data)
            json_account_id.append(account_id_item)

    params["account_id"] = json_account_id

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/risk/plans",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, RiskPlanPage]:
    if response.status_code == 200:
        response_200 = RiskPlanPage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, RiskPlanPage]]:
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
    account_id: Union[Unset, list[UUID]] = UNSET,
    state: Union[Unset, list[ListRiskPlansStateItem]] = UNSET,
    sort: Union[Unset, ListRiskPlansSort] = ListRiskPlansSort.NEWEST,
) -> Response[Union[Error, RiskPlanPage]]:
    """The tenant's exit plans, newest first

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        account_id (Union[Unset, list[UUID]]):
        state (Union[Unset, list[ListRiskPlansStateItem]]):
        sort (Union[Unset, ListRiskPlansSort]):  Default: ListRiskPlansSort.NEWEST.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskPlanPage]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        account_id=account_id,
        state=state,
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
    account_id: Union[Unset, list[UUID]] = UNSET,
    state: Union[Unset, list[ListRiskPlansStateItem]] = UNSET,
    sort: Union[Unset, ListRiskPlansSort] = ListRiskPlansSort.NEWEST,
) -> Optional[Union[Error, RiskPlanPage]]:
    """The tenant's exit plans, newest first

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        account_id (Union[Unset, list[UUID]]):
        state (Union[Unset, list[ListRiskPlansStateItem]]):
        sort (Union[Unset, ListRiskPlansSort]):  Default: ListRiskPlansSort.NEWEST.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskPlanPage]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        account_id=account_id,
        state=state,
        sort=sort,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    account_id: Union[Unset, list[UUID]] = UNSET,
    state: Union[Unset, list[ListRiskPlansStateItem]] = UNSET,
    sort: Union[Unset, ListRiskPlansSort] = ListRiskPlansSort.NEWEST,
) -> Response[Union[Error, RiskPlanPage]]:
    """The tenant's exit plans, newest first

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        account_id (Union[Unset, list[UUID]]):
        state (Union[Unset, list[ListRiskPlansStateItem]]):
        sort (Union[Unset, ListRiskPlansSort]):  Default: ListRiskPlansSort.NEWEST.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskPlanPage]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        account_id=account_id,
        state=state,
        sort=sort,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    account_id: Union[Unset, list[UUID]] = UNSET,
    state: Union[Unset, list[ListRiskPlansStateItem]] = UNSET,
    sort: Union[Unset, ListRiskPlansSort] = ListRiskPlansSort.NEWEST,
) -> Optional[Union[Error, RiskPlanPage]]:
    """The tenant's exit plans, newest first

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        account_id (Union[Unset, list[UUID]]):
        state (Union[Unset, list[ListRiskPlansStateItem]]):
        sort (Union[Unset, ListRiskPlansSort]):  Default: ListRiskPlansSort.NEWEST.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskPlanPage]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            account_id=account_id,
            state=state,
            sort=sort,
        )
    ).parsed

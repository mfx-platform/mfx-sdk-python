from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_risk_plans_state import ListRiskPlansState
from ...models.risk_plan_page import RiskPlanPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    terminal_id: Union[Unset, UUID] = UNSET,
    state: Union[Unset, ListRiskPlansState] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_terminal_id: Union[Unset, str] = UNSET
    if not isinstance(terminal_id, Unset):
        json_terminal_id = str(terminal_id)
    params["terminal_id"] = json_terminal_id

    json_state: Union[Unset, str] = UNSET
    if not isinstance(state, Unset):
        json_state = state.value

    params["state"] = json_state

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
    terminal_id: Union[Unset, UUID] = UNSET,
    state: Union[Unset, ListRiskPlansState] = UNSET,
) -> Response[Union[Error, RiskPlanPage]]:
    """The tenant's exit plans, newest first

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        terminal_id (Union[Unset, UUID]):
        state (Union[Unset, ListRiskPlansState]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskPlanPage]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        terminal_id=terminal_id,
        state=state,
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
    terminal_id: Union[Unset, UUID] = UNSET,
    state: Union[Unset, ListRiskPlansState] = UNSET,
) -> Optional[Union[Error, RiskPlanPage]]:
    """The tenant's exit plans, newest first

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        terminal_id (Union[Unset, UUID]):
        state (Union[Unset, ListRiskPlansState]):

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
        terminal_id=terminal_id,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    terminal_id: Union[Unset, UUID] = UNSET,
    state: Union[Unset, ListRiskPlansState] = UNSET,
) -> Response[Union[Error, RiskPlanPage]]:
    """The tenant's exit plans, newest first

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        terminal_id (Union[Unset, UUID]):
        state (Union[Unset, ListRiskPlansState]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskPlanPage]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        terminal_id=terminal_id,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    terminal_id: Union[Unset, UUID] = UNSET,
    state: Union[Unset, ListRiskPlansState] = UNSET,
) -> Optional[Union[Error, RiskPlanPage]]:
    """The tenant's exit plans, newest first

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        terminal_id (Union[Unset, UUID]):
        state (Union[Unset, ListRiskPlansState]):

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
            terminal_id=terminal_id,
            state=state,
        )
    ).parsed

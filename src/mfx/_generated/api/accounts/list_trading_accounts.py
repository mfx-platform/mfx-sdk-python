from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_trading_accounts_environment import ListTradingAccountsEnvironment
from ...models.list_trading_accounts_state_item import ListTradingAccountsStateItem
from ...models.list_trading_accounts_venue_item import ListTradingAccountsVenueItem
from ...models.trading_account_page import TradingAccountPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    venue: Union[Unset, list[ListTradingAccountsVenueItem]] = UNSET,
    environment: Union[Unset, ListTradingAccountsEnvironment] = UNSET,
    state: Union[Unset, list[ListTradingAccountsStateItem]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_venue: Union[Unset, list[str]] = UNSET
    if not isinstance(venue, Unset):
        json_venue = []
        for venue_item_data in venue:
            venue_item = venue_item_data.value
            json_venue.append(venue_item)

    params["venue"] = json_venue

    json_environment: Union[Unset, str] = UNSET
    if not isinstance(environment, Unset):
        json_environment = environment.value

    params["environment"] = json_environment

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/accounts",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, TradingAccountPage]:
    if response.status_code == 200:
        response_200 = TradingAccountPage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, TradingAccountPage]]:
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
    venue: Union[Unset, list[ListTradingAccountsVenueItem]] = UNSET,
    environment: Union[Unset, ListTradingAccountsEnvironment] = UNSET,
    state: Union[Unset, list[ListTradingAccountsStateItem]] = UNSET,
) -> Response[Union[Error, TradingAccountPage]]:
    """List your trading accounts over every venue, newest first (cursor pagination)

     Every account of yours, retired ones included, newest first. `venue`, `environment` and `state`
    narrow the list in the query, before the page is cut, so a filtered page is never short for being
    filtered.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        venue (Union[Unset, list[ListTradingAccountsVenueItem]]):
        environment (Union[Unset, ListTradingAccountsEnvironment]):
        state (Union[Unset, list[ListTradingAccountsStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TradingAccountPage]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        venue=venue,
        environment=environment,
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
    venue: Union[Unset, list[ListTradingAccountsVenueItem]] = UNSET,
    environment: Union[Unset, ListTradingAccountsEnvironment] = UNSET,
    state: Union[Unset, list[ListTradingAccountsStateItem]] = UNSET,
) -> Optional[Union[Error, TradingAccountPage]]:
    """List your trading accounts over every venue, newest first (cursor pagination)

     Every account of yours, retired ones included, newest first. `venue`, `environment` and `state`
    narrow the list in the query, before the page is cut, so a filtered page is never short for being
    filtered.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        venue (Union[Unset, list[ListTradingAccountsVenueItem]]):
        environment (Union[Unset, ListTradingAccountsEnvironment]):
        state (Union[Unset, list[ListTradingAccountsStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TradingAccountPage]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        venue=venue,
        environment=environment,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    venue: Union[Unset, list[ListTradingAccountsVenueItem]] = UNSET,
    environment: Union[Unset, ListTradingAccountsEnvironment] = UNSET,
    state: Union[Unset, list[ListTradingAccountsStateItem]] = UNSET,
) -> Response[Union[Error, TradingAccountPage]]:
    """List your trading accounts over every venue, newest first (cursor pagination)

     Every account of yours, retired ones included, newest first. `venue`, `environment` and `state`
    narrow the list in the query, before the page is cut, so a filtered page is never short for being
    filtered.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        venue (Union[Unset, list[ListTradingAccountsVenueItem]]):
        environment (Union[Unset, ListTradingAccountsEnvironment]):
        state (Union[Unset, list[ListTradingAccountsStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TradingAccountPage]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        venue=venue,
        environment=environment,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    venue: Union[Unset, list[ListTradingAccountsVenueItem]] = UNSET,
    environment: Union[Unset, ListTradingAccountsEnvironment] = UNSET,
    state: Union[Unset, list[ListTradingAccountsStateItem]] = UNSET,
) -> Optional[Union[Error, TradingAccountPage]]:
    """List your trading accounts over every venue, newest first (cursor pagination)

     Every account of yours, retired ones included, newest first. `venue`, `environment` and `state`
    narrow the list in the query, before the page is cut, so a filtered page is never short for being
    filtered.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        venue (Union[Unset, list[ListTradingAccountsVenueItem]]):
        environment (Union[Unset, ListTradingAccountsEnvironment]):
        state (Union[Unset, list[ListTradingAccountsStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TradingAccountPage]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            venue=venue,
            environment=environment,
            state=state,
        )
    ).parsed

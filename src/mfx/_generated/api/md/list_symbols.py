from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.symbol_page import SymbolPage
from ...models.symbol_state import SymbolState
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    server_id: Union[Unset, UUID] = UNSET,
    account_type: Union[Unset, str] = UNSET,
    status: Union[Unset, SymbolState] = UNSET,
    q: Union[Unset, str] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_server_id: Union[Unset, str] = UNSET
    if not isinstance(server_id, Unset):
        json_server_id = str(server_id)
    params["server_id"] = json_server_id

    params["account_type"] = account_type

    json_status: Union[Unset, str] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    params["q"] = q

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/brokers/{id}/symbols".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, SymbolPage]:
    if response.status_code == 200:
        response_200 = SymbolPage.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, SymbolPage]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    server_id: Union[Unset, UUID] = UNSET,
    account_type: Union[Unset, str] = UNSET,
    status: Union[Unset, SymbolState] = UNSET,
    q: Union[Unset, str] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
) -> Response[Union[Error, SymbolPage]]:
    """The tenant's symbol catalogue for one server and account type — spec, trade_mode (quotable ≠
    tradeable), pip_value_per_lot, spec_hash, trade sessions and derived status

     Read from the tenant's own terminals on that server. MFX holds no broker accounts and never shares
    one tenant's catalogue with another. A server where the tenant runs no terminal answers 409
    (`state_error`, details.reason `no_terminal_on_server`), never an empty list.

    Args:
        id (str):
        server_id (Union[Unset, UUID]):
        account_type (Union[Unset, str]):
        status (Union[Unset, SymbolState]): Checked in this order, first match wins: unknown (no
            terminal of the tenant on this server is connected, or the newest symbol report from one
            is older than 180 s by default — could-not-read is never reported as closed) →
            trade_disabled → closed_session (broker time outside this weekday's trade sessions) →
            paused (inside trade sessions, a watched symbol with no tick for 300 s by default) →
            close_only → long_only / short_only → open.
        q (Union[Unset, str]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SymbolPage]]
    """

    kwargs = _get_kwargs(
        id=id,
        server_id=server_id,
        account_type=account_type,
        status=status,
        q=q,
        cursor=cursor,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    server_id: Union[Unset, UUID] = UNSET,
    account_type: Union[Unset, str] = UNSET,
    status: Union[Unset, SymbolState] = UNSET,
    q: Union[Unset, str] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
) -> Optional[Union[Error, SymbolPage]]:
    """The tenant's symbol catalogue for one server and account type — spec, trade_mode (quotable ≠
    tradeable), pip_value_per_lot, spec_hash, trade sessions and derived status

     Read from the tenant's own terminals on that server. MFX holds no broker accounts and never shares
    one tenant's catalogue with another. A server where the tenant runs no terminal answers 409
    (`state_error`, details.reason `no_terminal_on_server`), never an empty list.

    Args:
        id (str):
        server_id (Union[Unset, UUID]):
        account_type (Union[Unset, str]):
        status (Union[Unset, SymbolState]): Checked in this order, first match wins: unknown (no
            terminal of the tenant on this server is connected, or the newest symbol report from one
            is older than 180 s by default — could-not-read is never reported as closed) →
            trade_disabled → closed_session (broker time outside this weekday's trade sessions) →
            paused (inside trade sessions, a watched symbol with no tick for 300 s by default) →
            close_only → long_only / short_only → open.
        q (Union[Unset, str]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SymbolPage]
    """

    return sync_detailed(
        id=id,
        client=client,
        server_id=server_id,
        account_type=account_type,
        status=status,
        q=q,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    server_id: Union[Unset, UUID] = UNSET,
    account_type: Union[Unset, str] = UNSET,
    status: Union[Unset, SymbolState] = UNSET,
    q: Union[Unset, str] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
) -> Response[Union[Error, SymbolPage]]:
    """The tenant's symbol catalogue for one server and account type — spec, trade_mode (quotable ≠
    tradeable), pip_value_per_lot, spec_hash, trade sessions and derived status

     Read from the tenant's own terminals on that server. MFX holds no broker accounts and never shares
    one tenant's catalogue with another. A server where the tenant runs no terminal answers 409
    (`state_error`, details.reason `no_terminal_on_server`), never an empty list.

    Args:
        id (str):
        server_id (Union[Unset, UUID]):
        account_type (Union[Unset, str]):
        status (Union[Unset, SymbolState]): Checked in this order, first match wins: unknown (no
            terminal of the tenant on this server is connected, or the newest symbol report from one
            is older than 180 s by default — could-not-read is never reported as closed) →
            trade_disabled → closed_session (broker time outside this weekday's trade sessions) →
            paused (inside trade sessions, a watched symbol with no tick for 300 s by default) →
            close_only → long_only / short_only → open.
        q (Union[Unset, str]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SymbolPage]]
    """

    kwargs = _get_kwargs(
        id=id,
        server_id=server_id,
        account_type=account_type,
        status=status,
        q=q,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    server_id: Union[Unset, UUID] = UNSET,
    account_type: Union[Unset, str] = UNSET,
    status: Union[Unset, SymbolState] = UNSET,
    q: Union[Unset, str] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
) -> Optional[Union[Error, SymbolPage]]:
    """The tenant's symbol catalogue for one server and account type — spec, trade_mode (quotable ≠
    tradeable), pip_value_per_lot, spec_hash, trade sessions and derived status

     Read from the tenant's own terminals on that server. MFX holds no broker accounts and never shares
    one tenant's catalogue with another. A server where the tenant runs no terminal answers 409
    (`state_error`, details.reason `no_terminal_on_server`), never an empty list.

    Args:
        id (str):
        server_id (Union[Unset, UUID]):
        account_type (Union[Unset, str]):
        status (Union[Unset, SymbolState]): Checked in this order, first match wins: unknown (no
            terminal of the tenant on this server is connected, or the newest symbol report from one
            is older than 180 s by default — could-not-read is never reported as closed) →
            trade_disabled → closed_session (broker time outside this weekday's trade sessions) →
            paused (inside trade sessions, a watched symbol with no tick for 300 s by default) →
            close_only → long_only / short_only → open.
        q (Union[Unset, str]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SymbolPage]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            server_id=server_id,
            account_type=account_type,
            status=status,
            q=q,
            cursor=cursor,
            limit=limit,
        )
    ).parsed

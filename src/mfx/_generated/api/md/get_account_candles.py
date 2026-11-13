import datetime
from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.candle_list import CandleList
from ...models.error import Error
from ...models.get_account_candles_tf import GetAccountCandlesTf
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    symbol: str,
    tf: GetAccountCandlesTf,
    from_: datetime.datetime,
    to: datetime.datetime,
    limit: Union[Unset, int] = 1000,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["symbol"] = symbol

    json_tf = tf.value
    params["tf"] = json_tf

    json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to = to.isoformat()
    params["to"] = json_to

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/accounts/{id}/md/candles".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CandleList, Error]:
    if response.status_code == 200:
        response_200 = CandleList.from_dict(response.json())

        return response_200

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CandleList, Error]]:
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
    symbol: str,
    tf: GetAccountCandlesTf,
    from_: datetime.datetime,
    to: datetime.datetime,
    limit: Union[Unset, int] = 1000,
) -> Response[Union[CandleList, Error]]:
    """Historical candles of one of your cTrader accounts by bar time, read from Spotware through the
    account; at most 1000 bars per call, the newest of the window

     The cTrader counterpart of `GET /md/candles`, keyed on the account instead of a broker and server.
    The bars are Spotware's trendbars for the account's own symbol name (`GET /accounts/{id}/symbols`),
    in UTC, `v` the bar's tick volume, oldest first, the forming bar included when the window reaches
    now. `source` is `terminal`: the account's runner read them, and nothing is stored. The read counts
    against the same per-terminal limit a minute as `GET /md/candles` (429 `terminal_reads_limit`).
    Another tenant's account, or none, is 404; an unknown symbol is 404; an MT5 account is 409
    `state_error` with `details.reason` `not_on_this_venue` (its candles are its server's: `GET
    /md/candles`).

    Args:
        id (UUID):
        symbol (str):
        tf (GetAccountCandlesTf):
        from_ (datetime.datetime):
        to (datetime.datetime):
        limit (Union[Unset, int]):  Default: 1000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CandleList, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        symbol=symbol,
        tf=tf,
        from_=from_,
        to=to,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    symbol: str,
    tf: GetAccountCandlesTf,
    from_: datetime.datetime,
    to: datetime.datetime,
    limit: Union[Unset, int] = 1000,
) -> Optional[Union[CandleList, Error]]:
    """Historical candles of one of your cTrader accounts by bar time, read from Spotware through the
    account; at most 1000 bars per call, the newest of the window

     The cTrader counterpart of `GET /md/candles`, keyed on the account instead of a broker and server.
    The bars are Spotware's trendbars for the account's own symbol name (`GET /accounts/{id}/symbols`),
    in UTC, `v` the bar's tick volume, oldest first, the forming bar included when the window reaches
    now. `source` is `terminal`: the account's runner read them, and nothing is stored. The read counts
    against the same per-terminal limit a minute as `GET /md/candles` (429 `terminal_reads_limit`).
    Another tenant's account, or none, is 404; an unknown symbol is 404; an MT5 account is 409
    `state_error` with `details.reason` `not_on_this_venue` (its candles are its server's: `GET
    /md/candles`).

    Args:
        id (UUID):
        symbol (str):
        tf (GetAccountCandlesTf):
        from_ (datetime.datetime):
        to (datetime.datetime):
        limit (Union[Unset, int]):  Default: 1000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CandleList, Error]
    """

    return sync_detailed(
        id=id,
        client=client,
        symbol=symbol,
        tf=tf,
        from_=from_,
        to=to,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    symbol: str,
    tf: GetAccountCandlesTf,
    from_: datetime.datetime,
    to: datetime.datetime,
    limit: Union[Unset, int] = 1000,
) -> Response[Union[CandleList, Error]]:
    """Historical candles of one of your cTrader accounts by bar time, read from Spotware through the
    account; at most 1000 bars per call, the newest of the window

     The cTrader counterpart of `GET /md/candles`, keyed on the account instead of a broker and server.
    The bars are Spotware's trendbars for the account's own symbol name (`GET /accounts/{id}/symbols`),
    in UTC, `v` the bar's tick volume, oldest first, the forming bar included when the window reaches
    now. `source` is `terminal`: the account's runner read them, and nothing is stored. The read counts
    against the same per-terminal limit a minute as `GET /md/candles` (429 `terminal_reads_limit`).
    Another tenant's account, or none, is 404; an unknown symbol is 404; an MT5 account is 409
    `state_error` with `details.reason` `not_on_this_venue` (its candles are its server's: `GET
    /md/candles`).

    Args:
        id (UUID):
        symbol (str):
        tf (GetAccountCandlesTf):
        from_ (datetime.datetime):
        to (datetime.datetime):
        limit (Union[Unset, int]):  Default: 1000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CandleList, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        symbol=symbol,
        tf=tf,
        from_=from_,
        to=to,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    symbol: str,
    tf: GetAccountCandlesTf,
    from_: datetime.datetime,
    to: datetime.datetime,
    limit: Union[Unset, int] = 1000,
) -> Optional[Union[CandleList, Error]]:
    """Historical candles of one of your cTrader accounts by bar time, read from Spotware through the
    account; at most 1000 bars per call, the newest of the window

     The cTrader counterpart of `GET /md/candles`, keyed on the account instead of a broker and server.
    The bars are Spotware's trendbars for the account's own symbol name (`GET /accounts/{id}/symbols`),
    in UTC, `v` the bar's tick volume, oldest first, the forming bar included when the window reaches
    now. `source` is `terminal`: the account's runner read them, and nothing is stored. The read counts
    against the same per-terminal limit a minute as `GET /md/candles` (429 `terminal_reads_limit`).
    Another tenant's account, or none, is 404; an unknown symbol is 404; an MT5 account is 409
    `state_error` with `details.reason` `not_on_this_venue` (its candles are its server's: `GET
    /md/candles`).

    Args:
        id (UUID):
        symbol (str):
        tf (GetAccountCandlesTf):
        from_ (datetime.datetime):
        to (datetime.datetime):
        limit (Union[Unset, int]):  Default: 1000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CandleList, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            symbol=symbol,
            tf=tf,
            from_=from_,
            to=to,
            limit=limit,
        )
    ).parsed

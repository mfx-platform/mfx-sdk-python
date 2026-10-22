import datetime
from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.candle_list import CandleList
from ...models.error import Error
from ...models.get_candles_tf import GetCandlesTf
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    broker: str,
    server_id: Union[Unset, str] = UNSET,
    symbol: str,
    tf: GetCandlesTf,
    from_: datetime.datetime,
    to: datetime.datetime,
    limit: Union[Unset, int] = 1000,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["broker"] = broker

    params["server_id"] = server_id

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
        "url": "/md/candles",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CandleList, Error]:
    if response.status_code == 200:
        response_200 = CandleList.from_dict(response.json())

        return response_200

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
    *,
    client: Union[AuthenticatedClient, Client],
    broker: str,
    server_id: Union[Unset, str] = UNSET,
    symbol: str,
    tf: GetCandlesTf,
    from_: datetime.datetime,
    to: datetime.datetime,
    limit: Union[Unset, int] = 1000,
) -> Response[Union[CandleList, Error]]:
    """Historical candles by bar time, read through one of your own terminals on the server; at most 1000
    bars per call, the newest of the window

    Args:
        broker (str):
        server_id (Union[Unset, str]):
        symbol (str):
        tf (GetCandlesTf):
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
        broker=broker,
        server_id=server_id,
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
    *,
    client: Union[AuthenticatedClient, Client],
    broker: str,
    server_id: Union[Unset, str] = UNSET,
    symbol: str,
    tf: GetCandlesTf,
    from_: datetime.datetime,
    to: datetime.datetime,
    limit: Union[Unset, int] = 1000,
) -> Optional[Union[CandleList, Error]]:
    """Historical candles by bar time, read through one of your own terminals on the server; at most 1000
    bars per call, the newest of the window

    Args:
        broker (str):
        server_id (Union[Unset, str]):
        symbol (str):
        tf (GetCandlesTf):
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
        client=client,
        broker=broker,
        server_id=server_id,
        symbol=symbol,
        tf=tf,
        from_=from_,
        to=to,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    broker: str,
    server_id: Union[Unset, str] = UNSET,
    symbol: str,
    tf: GetCandlesTf,
    from_: datetime.datetime,
    to: datetime.datetime,
    limit: Union[Unset, int] = 1000,
) -> Response[Union[CandleList, Error]]:
    """Historical candles by bar time, read through one of your own terminals on the server; at most 1000
    bars per call, the newest of the window

    Args:
        broker (str):
        server_id (Union[Unset, str]):
        symbol (str):
        tf (GetCandlesTf):
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
        broker=broker,
        server_id=server_id,
        symbol=symbol,
        tf=tf,
        from_=from_,
        to=to,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    broker: str,
    server_id: Union[Unset, str] = UNSET,
    symbol: str,
    tf: GetCandlesTf,
    from_: datetime.datetime,
    to: datetime.datetime,
    limit: Union[Unset, int] = 1000,
) -> Optional[Union[CandleList, Error]]:
    """Historical candles by bar time, read through one of your own terminals on the server; at most 1000
    bars per call, the newest of the window

    Args:
        broker (str):
        server_id (Union[Unset, str]):
        symbol (str):
        tf (GetCandlesTf):
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
            client=client,
            broker=broker,
            server_id=server_id,
            symbol=symbol,
            tf=tf,
            from_=from_,
            to=to,
            limit=limit,
        )
    ).parsed

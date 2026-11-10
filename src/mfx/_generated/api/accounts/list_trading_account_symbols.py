from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.trading_symbol_list import TradingSymbolList
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/accounts/{id}/symbols".format(
            id=id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, TradingSymbolList]:
    if response.status_code == 200:
        response_200 = TradingSymbolList.from_dict(response.json())

        return response_200

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, TradingSymbolList]]:
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
) -> Response[Union[Error, TradingSymbolList]]:
    """The symbols one cTrader account can trade, with their volume rules and leverage

     Read from Spotware through the account and held for an hour; what one account of a broker can trade
    need not be another's. A volume a command sends must be a whole `volume_step` between `volume_min`
    and `volume_max`, in lots. An MT5 account is answered 409 `not_on_this_venue`: its symbols are its
    broker's catalogue (`/brokers/{id}/symbols`).

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TradingSymbolList]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, TradingSymbolList]]:
    """The symbols one cTrader account can trade, with their volume rules and leverage

     Read from Spotware through the account and held for an hour; what one account of a broker can trade
    need not be another's. A volume a command sends must be a whole `volume_step` between `volume_min`
    and `volume_max`, in lots. An MT5 account is answered 409 `not_on_this_venue`: its symbols are its
    broker's catalogue (`/brokers/{id}/symbols`).

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TradingSymbolList]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, TradingSymbolList]]:
    """The symbols one cTrader account can trade, with their volume rules and leverage

     Read from Spotware through the account and held for an hour; what one account of a broker can trade
    need not be another's. A volume a command sends must be a whole `volume_step` between `volume_min`
    and `volume_max`, in lots. An MT5 account is answered 409 `not_on_this_venue`: its symbols are its
    broker's catalogue (`/brokers/{id}/symbols`).

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TradingSymbolList]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, TradingSymbolList]]:
    """The symbols one cTrader account can trade, with their volume rules and leverage

     Read from Spotware through the account and held for an hour; what one account of a broker can trade
    need not be another's. A volume a command sends must be a whole `volume_step` between `volume_min`
    and `volume_max`, in lots. An MT5 account is answered 409 `not_on_this_venue`: its symbols are its
    broker's catalogue (`/brokers/{id}/symbols`).

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TradingSymbolList]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.symbol import Symbol
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    symbol: str,
    *,
    server_id: Union[Unset, UUID] = UNSET,
    account_type: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_server_id: Union[Unset, str] = UNSET
    if not isinstance(server_id, Unset):
        json_server_id = str(server_id)
    params["server_id"] = json_server_id

    params["account_type"] = account_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/brokers/{id}/symbols/{symbol}".format(
            id=id,
            symbol=symbol,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, Symbol]:
    if response.status_code == 200:
        response_200 = Symbol.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, Symbol]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    symbol: str,
    *,
    client: Union[AuthenticatedClient, Client],
    server_id: Union[Unset, UUID] = UNSET,
    account_type: Union[Unset, str] = UNSET,
) -> Response[Union[Error, Symbol]]:
    """Check that a symbol exists for this server and account type, with its spec and status

     404 (`not_found`) carries `details.symbol`, `details.account_type` and `details.did_you_mean`: the
    names on this catalogue that differ only by suffix or case. MFX never substitutes one — the caller
    chooses. 400 and 409 as for `listSymbols`.

    Args:
        id (str):
        symbol (str):
        server_id (Union[Unset, UUID]):
        account_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Symbol]]
    """

    kwargs = _get_kwargs(
        id=id,
        symbol=symbol,
        server_id=server_id,
        account_type=account_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    symbol: str,
    *,
    client: Union[AuthenticatedClient, Client],
    server_id: Union[Unset, UUID] = UNSET,
    account_type: Union[Unset, str] = UNSET,
) -> Optional[Union[Error, Symbol]]:
    """Check that a symbol exists for this server and account type, with its spec and status

     404 (`not_found`) carries `details.symbol`, `details.account_type` and `details.did_you_mean`: the
    names on this catalogue that differ only by suffix or case. MFX never substitutes one — the caller
    chooses. 400 and 409 as for `listSymbols`.

    Args:
        id (str):
        symbol (str):
        server_id (Union[Unset, UUID]):
        account_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Symbol]
    """

    return sync_detailed(
        id=id,
        symbol=symbol,
        client=client,
        server_id=server_id,
        account_type=account_type,
    ).parsed


async def asyncio_detailed(
    id: str,
    symbol: str,
    *,
    client: Union[AuthenticatedClient, Client],
    server_id: Union[Unset, UUID] = UNSET,
    account_type: Union[Unset, str] = UNSET,
) -> Response[Union[Error, Symbol]]:
    """Check that a symbol exists for this server and account type, with its spec and status

     404 (`not_found`) carries `details.symbol`, `details.account_type` and `details.did_you_mean`: the
    names on this catalogue that differ only by suffix or case. MFX never substitutes one — the caller
    chooses. 400 and 409 as for `listSymbols`.

    Args:
        id (str):
        symbol (str):
        server_id (Union[Unset, UUID]):
        account_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Symbol]]
    """

    kwargs = _get_kwargs(
        id=id,
        symbol=symbol,
        server_id=server_id,
        account_type=account_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    symbol: str,
    *,
    client: Union[AuthenticatedClient, Client],
    server_id: Union[Unset, UUID] = UNSET,
    account_type: Union[Unset, str] = UNSET,
) -> Optional[Union[Error, Symbol]]:
    """Check that a symbol exists for this server and account type, with its spec and status

     404 (`not_found`) carries `details.symbol`, `details.account_type` and `details.did_you_mean`: the
    names on this catalogue that differ only by suffix or case. MFX never substitutes one — the caller
    chooses. 400 and 409 as for `listSymbols`.

    Args:
        id (str):
        symbol (str):
        server_id (Union[Unset, UUID]):
        account_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Symbol]
    """

    return (
        await asyncio_detailed(
            id=id,
            symbol=symbol,
            client=client,
            server_id=server_id,
            account_type=account_type,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ctrader_return_origins import CtraderReturnOrigins
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/accounts/ctrader/return-origins",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CtraderReturnOrigins, Error]:
    if response.status_code == 200:
        response_200 = CtraderReturnOrigins.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CtraderReturnOrigins, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[CtraderReturnOrigins, Error]]:
    """The https origins a cTrader grant may send the trader back to

     Your registered return origins, like an OAuth client's redirect URIs. `enforced` says whether a
    grant's `return_url` is checked against them now: true once you list at least one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CtraderReturnOrigins, Error]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[CtraderReturnOrigins, Error]]:
    """The https origins a cTrader grant may send the trader back to

     Your registered return origins, like an OAuth client's redirect URIs. `enforced` says whether a
    grant's `return_url` is checked against them now: true once you list at least one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CtraderReturnOrigins, Error]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[CtraderReturnOrigins, Error]]:
    """The https origins a cTrader grant may send the trader back to

     Your registered return origins, like an OAuth client's redirect URIs. `enforced` says whether a
    grant's `return_url` is checked against them now: true once you list at least one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CtraderReturnOrigins, Error]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[CtraderReturnOrigins, Error]]:
    """The https origins a cTrader grant may send the trader back to

     Your registered return origins, like an OAuth client's redirect URIs. `enforced` says whether a
    grant's `return_url` is checked against them now: true once you list at least one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CtraderReturnOrigins, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed

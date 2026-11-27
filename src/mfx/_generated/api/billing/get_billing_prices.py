from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.billing_price_list import BillingPriceList
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/billing/prices",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[BillingPriceList, Error]:
    if response.status_code == 200:
        response_200 = BillingPriceList.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[BillingPriceList, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[BillingPriceList, Error]]:
    """The prices your organisation pays, in the shape of the price list

     Your Enterprise agreement's prices when one is in force (`scope: tenant`, with `agreement` and each
    line's dates and value), otherwise the list in force. One object, not paged.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BillingPriceList, Error]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[BillingPriceList, Error]]:
    """The prices your organisation pays, in the shape of the price list

     Your Enterprise agreement's prices when one is in force (`scope: tenant`, with `agreement` and each
    line's dates and value), otherwise the list in force. One object, not paged.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BillingPriceList, Error]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[BillingPriceList, Error]]:
    """The prices your organisation pays, in the shape of the price list

     Your Enterprise agreement's prices when one is in force (`scope: tenant`, with `agreement` and each
    line's dates and value), otherwise the list in force. One object, not paged.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BillingPriceList, Error]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[BillingPriceList, Error]]:
    """The prices your organisation pays, in the shape of the price list

     Your Enterprise agreement's prices when one is in force (`scope: tenant`, with `agreement` and each
    line's dates and value), otherwise the list in force. One object, not paged.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BillingPriceList, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed

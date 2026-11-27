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
        "url": "/price-list",
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
    """The public price list, and the next one once it is released; no key needed

     The list version marked public: the plans, every item with its public name, unit and monthly price,
    which plans have it, the Standard account limit and when to talk to sales. `next` is the following
    version once it is released, with the date it starts. Cached for five minutes; never anything of a
    tenant's own. The website's pricing page and calculator read this. It needs no key, and it also
    accepts a signed request: the signature headers and the key are ignored here, so an SDK that signs
    every request calls it as it is and is never refused for carrying a key.

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
    """The public price list, and the next one once it is released; no key needed

     The list version marked public: the plans, every item with its public name, unit and monthly price,
    which plans have it, the Standard account limit and when to talk to sales. `next` is the following
    version once it is released, with the date it starts. Cached for five minutes; never anything of a
    tenant's own. The website's pricing page and calculator read this. It needs no key, and it also
    accepts a signed request: the signature headers and the key are ignored here, so an SDK that signs
    every request calls it as it is and is never refused for carrying a key.

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
    """The public price list, and the next one once it is released; no key needed

     The list version marked public: the plans, every item with its public name, unit and monthly price,
    which plans have it, the Standard account limit and when to talk to sales. `next` is the following
    version once it is released, with the date it starts. Cached for five minutes; never anything of a
    tenant's own. The website's pricing page and calculator read this. It needs no key, and it also
    accepts a signed request: the signature headers and the key are ignored here, so an SDK that signs
    every request calls it as it is and is never refused for carrying a key.

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
    """The public price list, and the next one once it is released; no key needed

     The list version marked public: the plans, every item with its public name, unit and monthly price,
    which plans have it, the Standard account limit and when to talk to sales. `next` is the following
    version once it is released, with the date it starts. Cached for five minutes; never anything of a
    tenant's own. The website's pricing page and calculator read this. It needs no key, and it also
    accepts a signed request: the signature headers and the key are ignored here, so an SDK that signs
    every request calls it as it is and is never refused for carrying a key.

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

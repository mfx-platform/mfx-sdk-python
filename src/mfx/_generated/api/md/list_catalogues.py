from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.broker_catalogue_list import BrokerCatalogueList
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/brokers/{id}/catalogues".format(
            id=id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[BrokerCatalogueList, Error]:
    if response.status_code == 200:
        response_200 = BrokerCatalogueList.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[BrokerCatalogueList, Error]]:
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
) -> Response[Union[BrokerCatalogueList, Error]]:
    """One row per server and account type you hold a catalogue for, with a hash of the whole list -
    compare it to re-read only what changed

     `catalogue_hash` changes when any symbol is added, removed or comes back, or any symbol's spec_hash,
    description or identity fields change; never on a quote figure. A tenant that holds no catalogue for
    this broker gets an empty list.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BrokerCatalogueList, Error]]
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
) -> Optional[Union[BrokerCatalogueList, Error]]:
    """One row per server and account type you hold a catalogue for, with a hash of the whole list -
    compare it to re-read only what changed

     `catalogue_hash` changes when any symbol is added, removed or comes back, or any symbol's spec_hash,
    description or identity fields change; never on a quote figure. A tenant that holds no catalogue for
    this broker gets an empty list.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BrokerCatalogueList, Error]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[BrokerCatalogueList, Error]]:
    """One row per server and account type you hold a catalogue for, with a hash of the whole list -
    compare it to re-read only what changed

     `catalogue_hash` changes when any symbol is added, removed or comes back, or any symbol's spec_hash,
    description or identity fields change; never on a quote figure. A tenant that holds no catalogue for
    this broker gets an empty list.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BrokerCatalogueList, Error]]
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
) -> Optional[Union[BrokerCatalogueList, Error]]:
    """One row per server and account type you hold a catalogue for, with a hash of the whole list -
    compare it to re-read only what changed

     `catalogue_hash` changes when any symbol is added, removed or comes back, or any symbol's spec_hash,
    description or identity fields change; never on a quote figure. A tenant that holds no catalogue for
    this broker gets an empty list.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BrokerCatalogueList, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.billing_forecast import BillingForecast
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    month: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["month"] = month

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/billing/profiles/{id}/forecast".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[BillingForecast, Error]:
    if response.status_code == 200:
        response_200 = BillingForecast.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[BillingForecast, Error]]:
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
    month: Union[Unset, str] = UNSET,
) -> Response[Union[BillingForecast, Error]]:
    """This month for one billing profile, to date by product, and the forecast to month end

     Per day: each line's account-days to date at this month's daily rate (the monthly price divided by
    the days in the month), and the forecast at today's accounts and add-ons for the days left. One
    object, not paged.

    Args:
        id (UUID):
        month (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BillingForecast, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        month=month,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    month: Union[Unset, str] = UNSET,
) -> Optional[Union[BillingForecast, Error]]:
    """This month for one billing profile, to date by product, and the forecast to month end

     Per day: each line's account-days to date at this month's daily rate (the monthly price divided by
    the days in the month), and the forecast at today's accounts and add-ons for the days left. One
    object, not paged.

    Args:
        id (UUID):
        month (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BillingForecast, Error]
    """

    return sync_detailed(
        id=id,
        client=client,
        month=month,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    month: Union[Unset, str] = UNSET,
) -> Response[Union[BillingForecast, Error]]:
    """This month for one billing profile, to date by product, and the forecast to month end

     Per day: each line's account-days to date at this month's daily rate (the monthly price divided by
    the days in the month), and the forecast at today's accounts and add-ons for the days left. One
    object, not paged.

    Args:
        id (UUID):
        month (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BillingForecast, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        month=month,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    month: Union[Unset, str] = UNSET,
) -> Optional[Union[BillingForecast, Error]]:
    """This month for one billing profile, to date by product, and the forecast to month end

     Per day: each line's account-days to date at this month's daily rate (the monthly price divided by
    the days in the month), and the forecast at today's accounts and add-ons for the days left. One
    object, not paged.

    Args:
        id (UUID):
        month (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BillingForecast, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            month=month,
        )
    ).parsed

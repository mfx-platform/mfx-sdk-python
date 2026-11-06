import datetime
from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.risk_equity_series import RiskEquitySeries
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    from_: datetime.datetime,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to: Union[Unset, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/risk/accounts/{id}/equity".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, RiskEquitySeries]:
    if response.status_code == 200:
        response_200 = RiskEquitySeries.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, RiskEquitySeries]]:
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
    from_: datetime.datetime,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Union[Error, RiskEquitySeries]]:
    """The account's equity and balance series from the stored account reads (one a minute and on every
    change)

    Args:
        id (UUID):
        from_ (datetime.datetime):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskEquitySeries]]
    """

    kwargs = _get_kwargs(
        id=id,
        from_=from_,
        to=to,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    from_: datetime.datetime,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[Union[Error, RiskEquitySeries]]:
    """The account's equity and balance series from the stored account reads (one a minute and on every
    change)

    Args:
        id (UUID):
        from_ (datetime.datetime):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskEquitySeries]
    """

    return sync_detailed(
        id=id,
        client=client,
        from_=from_,
        to=to,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    from_: datetime.datetime,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Union[Error, RiskEquitySeries]]:
    """The account's equity and balance series from the stored account reads (one a minute and on every
    change)

    Args:
        id (UUID):
        from_ (datetime.datetime):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskEquitySeries]]
    """

    kwargs = _get_kwargs(
        id=id,
        from_=from_,
        to=to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    from_: datetime.datetime,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[Union[Error, RiskEquitySeries]]:
    """The account's equity and balance series from the stored account reads (one a minute and on every
    change)

    Args:
        id (UUID):
        from_ (datetime.datetime):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskEquitySeries]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            from_=from_,
            to=to,
        )
    ).parsed

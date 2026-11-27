import datetime
from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.risk_stops import RiskStops
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    from_: datetime.datetime,
    to: datetime.datetime,
    account_id: Union[Unset, list[UUID]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to = to.isoformat()
    params["to"] = json_to

    json_account_id: Union[Unset, list[str]] = UNSET
    if not isinstance(account_id, Unset):
        json_account_id = []
        for account_id_item_data in account_id:
            account_id_item = str(account_id_item_data)
            json_account_id.append(account_id_item)

    params["account_id"] = json_account_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/risk/stops",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, RiskStops]:
    if response.status_code == 200:
        response_200 = RiskStops.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, RiskStops]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    from_: datetime.datetime,
    to: datetime.datetime,
    account_id: Union[Unset, list[UUID]] = UNSET,
) -> Response[Union[Error, RiskStops]]:
    r"""Per account over a window, the entries a rule refused and the positions a rule closed, the closes
    split by magic number

     For a report such as an expert advisor's \"stopped by a risk rule\". `refused` counts the entries a
    rule in force refused (422 `risk_refused`) whose Activity row falls in the window; an entry refused
    because the check could not run (`risk_check_unavailable`) is not counted, since no rule refused it.
    `closed` counts the positions a rule's or a challenge's `close_positions` action closed, in whole or
    in part, by the time the action began; an operator's close is not counted. Each close names the
    magic number its position carried when the action listed it, so `closed_by_magic` can be read per
    expert advisor; a close listed before magic numbers were recorded counts in `closed_unattributed`.
    Only an order sent through MFX Hub can be refused, and such an order has no expert advisor, so
    refusals are counted per account only. An account with nothing in the window is left out.

    Args:
        from_ (datetime.datetime):
        to (datetime.datetime):
        account_id (Union[Unset, list[UUID]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskStops]]
    """

    kwargs = _get_kwargs(
        from_=from_,
        to=to,
        account_id=account_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    from_: datetime.datetime,
    to: datetime.datetime,
    account_id: Union[Unset, list[UUID]] = UNSET,
) -> Optional[Union[Error, RiskStops]]:
    r"""Per account over a window, the entries a rule refused and the positions a rule closed, the closes
    split by magic number

     For a report such as an expert advisor's \"stopped by a risk rule\". `refused` counts the entries a
    rule in force refused (422 `risk_refused`) whose Activity row falls in the window; an entry refused
    because the check could not run (`risk_check_unavailable`) is not counted, since no rule refused it.
    `closed` counts the positions a rule's or a challenge's `close_positions` action closed, in whole or
    in part, by the time the action began; an operator's close is not counted. Each close names the
    magic number its position carried when the action listed it, so `closed_by_magic` can be read per
    expert advisor; a close listed before magic numbers were recorded counts in `closed_unattributed`.
    Only an order sent through MFX Hub can be refused, and such an order has no expert advisor, so
    refusals are counted per account only. An account with nothing in the window is left out.

    Args:
        from_ (datetime.datetime):
        to (datetime.datetime):
        account_id (Union[Unset, list[UUID]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskStops]
    """

    return sync_detailed(
        client=client,
        from_=from_,
        to=to,
        account_id=account_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    from_: datetime.datetime,
    to: datetime.datetime,
    account_id: Union[Unset, list[UUID]] = UNSET,
) -> Response[Union[Error, RiskStops]]:
    r"""Per account over a window, the entries a rule refused and the positions a rule closed, the closes
    split by magic number

     For a report such as an expert advisor's \"stopped by a risk rule\". `refused` counts the entries a
    rule in force refused (422 `risk_refused`) whose Activity row falls in the window; an entry refused
    because the check could not run (`risk_check_unavailable`) is not counted, since no rule refused it.
    `closed` counts the positions a rule's or a challenge's `close_positions` action closed, in whole or
    in part, by the time the action began; an operator's close is not counted. Each close names the
    magic number its position carried when the action listed it, so `closed_by_magic` can be read per
    expert advisor; a close listed before magic numbers were recorded counts in `closed_unattributed`.
    Only an order sent through MFX Hub can be refused, and such an order has no expert advisor, so
    refusals are counted per account only. An account with nothing in the window is left out.

    Args:
        from_ (datetime.datetime):
        to (datetime.datetime):
        account_id (Union[Unset, list[UUID]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskStops]]
    """

    kwargs = _get_kwargs(
        from_=from_,
        to=to,
        account_id=account_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    from_: datetime.datetime,
    to: datetime.datetime,
    account_id: Union[Unset, list[UUID]] = UNSET,
) -> Optional[Union[Error, RiskStops]]:
    r"""Per account over a window, the entries a rule refused and the positions a rule closed, the closes
    split by magic number

     For a report such as an expert advisor's \"stopped by a risk rule\". `refused` counts the entries a
    rule in force refused (422 `risk_refused`) whose Activity row falls in the window; an entry refused
    because the check could not run (`risk_check_unavailable`) is not counted, since no rule refused it.
    `closed` counts the positions a rule's or a challenge's `close_positions` action closed, in whole or
    in part, by the time the action began; an operator's close is not counted. Each close names the
    magic number its position carried when the action listed it, so `closed_by_magic` can be read per
    expert advisor; a close listed before magic numbers were recorded counts in `closed_unattributed`.
    Only an order sent through MFX Hub can be refused, and such an order has no expert advisor, so
    refusals are counted per account only. An account with nothing in the window is left out.

    Args:
        from_ (datetime.datetime):
        to (datetime.datetime):
        account_id (Union[Unset, list[UUID]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskStops]
    """

    return (
        await asyncio_detailed(
            client=client,
            from_=from_,
            to=to,
            account_id=account_id,
        )
    ).parsed

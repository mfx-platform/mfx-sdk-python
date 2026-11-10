from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ctrader_accounts_choice import CtraderAccountsChoice
from ...models.error import Error
from ...models.trading_account_list import TradingAccountList
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: CtraderAccountsChoice,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/accounts/ctrader/grants/{id}/accounts".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, TradingAccountList]:
    if response.status_code == 200:
        response_200 = TradingAccountList.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, TradingAccountList]]:
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
    body: CtraderAccountsChoice,
    idempotency_key: str,
) -> Response[Union[Error, TradingAccountList]]:
    """Connect some of a grant's cTrader accounts to MFX Hub

     Each chosen account becomes a trading account of yours (`venue: ctrader`), PENDING until MFX Hub has
    authorised it at cTrader, then CONNECTED with an `account.connected` event. Choosing an account
    already connected answers it unchanged. A grant that is not ACTIVE is 409 `state_error`; an id the
    grant does not list is 422 `unprocessable`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CtraderAccountsChoice):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TradingAccountList]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CtraderAccountsChoice,
    idempotency_key: str,
) -> Optional[Union[Error, TradingAccountList]]:
    """Connect some of a grant's cTrader accounts to MFX Hub

     Each chosen account becomes a trading account of yours (`venue: ctrader`), PENDING until MFX Hub has
    authorised it at cTrader, then CONNECTED with an `account.connected` event. Choosing an account
    already connected answers it unchanged. A grant that is not ACTIVE is 409 `state_error`; an id the
    grant does not list is 422 `unprocessable`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CtraderAccountsChoice):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TradingAccountList]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CtraderAccountsChoice,
    idempotency_key: str,
) -> Response[Union[Error, TradingAccountList]]:
    """Connect some of a grant's cTrader accounts to MFX Hub

     Each chosen account becomes a trading account of yours (`venue: ctrader`), PENDING until MFX Hub has
    authorised it at cTrader, then CONNECTED with an `account.connected` event. Choosing an account
    already connected answers it unchanged. A grant that is not ACTIVE is 409 `state_error`; an id the
    grant does not list is 422 `unprocessable`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CtraderAccountsChoice):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TradingAccountList]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CtraderAccountsChoice,
    idempotency_key: str,
) -> Optional[Union[Error, TradingAccountList]]:
    """Connect some of a grant's cTrader accounts to MFX Hub

     Each chosen account becomes a trading account of yours (`venue: ctrader`), PENDING until MFX Hub has
    authorised it at cTrader, then CONNECTED with an `account.connected` event. Choosing an account
    already connected answers it unchanged. A grant that is not ACTIVE is 409 `state_error`; an id the
    grant does not list is 422 `unprocessable`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CtraderAccountsChoice):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TradingAccountList]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.account_md_subscription import AccountMdSubscription
from ...models.account_md_subscription_create import AccountMdSubscriptionCreate
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: AccountMdSubscriptionCreate,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/accounts/{id}/md/subscriptions".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[AccountMdSubscription, Error]:
    if response.status_code == 201:
        response_201 = AccountMdSubscription.from_dict(response.json())

        return response_201

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[AccountMdSubscription, Error]]:
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
    body: AccountMdSubscriptionCreate,
    idempotency_key: str,
) -> Response[Union[AccountMdSubscription, Error]]:
    """Stream one symbol's spots of one of your cTrader accounts; state pending until its first spot

     The cTrader counterpart of `POST /md/subscriptions`, keyed on the account instead of a server. The
    platform subscribes the symbol's spots on that account at Spotware, and they stream on the
    `md:{account_id}:{symbol}` channel as `md.tick`. Two of your accounts at one broker and environment
    share one stream. A resource, not a command: it is created at once, `pending` until the first spot
    arrives. One per account and symbol: asking again answers the live one; asking after a stop reopens
    it. Stopped with `DELETE /md/subscriptions/{id}`. Another tenant's account, or none, is 404; an MT5
    account is 409 `state_error` with `details.reason` `not_on_this_venue` (it streams its server: `POST
    /md/subscriptions`).

    Args:
        id (UUID):
        idempotency_key (str):
        body (AccountMdSubscriptionCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountMdSubscription, Error]]
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
    body: AccountMdSubscriptionCreate,
    idempotency_key: str,
) -> Optional[Union[AccountMdSubscription, Error]]:
    """Stream one symbol's spots of one of your cTrader accounts; state pending until its first spot

     The cTrader counterpart of `POST /md/subscriptions`, keyed on the account instead of a server. The
    platform subscribes the symbol's spots on that account at Spotware, and they stream on the
    `md:{account_id}:{symbol}` channel as `md.tick`. Two of your accounts at one broker and environment
    share one stream. A resource, not a command: it is created at once, `pending` until the first spot
    arrives. One per account and symbol: asking again answers the live one; asking after a stop reopens
    it. Stopped with `DELETE /md/subscriptions/{id}`. Another tenant's account, or none, is 404; an MT5
    account is 409 `state_error` with `details.reason` `not_on_this_venue` (it streams its server: `POST
    /md/subscriptions`).

    Args:
        id (UUID):
        idempotency_key (str):
        body (AccountMdSubscriptionCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountMdSubscription, Error]
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
    body: AccountMdSubscriptionCreate,
    idempotency_key: str,
) -> Response[Union[AccountMdSubscription, Error]]:
    """Stream one symbol's spots of one of your cTrader accounts; state pending until its first spot

     The cTrader counterpart of `POST /md/subscriptions`, keyed on the account instead of a server. The
    platform subscribes the symbol's spots on that account at Spotware, and they stream on the
    `md:{account_id}:{symbol}` channel as `md.tick`. Two of your accounts at one broker and environment
    share one stream. A resource, not a command: it is created at once, `pending` until the first spot
    arrives. One per account and symbol: asking again answers the live one; asking after a stop reopens
    it. Stopped with `DELETE /md/subscriptions/{id}`. Another tenant's account, or none, is 404; an MT5
    account is 409 `state_error` with `details.reason` `not_on_this_venue` (it streams its server: `POST
    /md/subscriptions`).

    Args:
        id (UUID):
        idempotency_key (str):
        body (AccountMdSubscriptionCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountMdSubscription, Error]]
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
    body: AccountMdSubscriptionCreate,
    idempotency_key: str,
) -> Optional[Union[AccountMdSubscription, Error]]:
    """Stream one symbol's spots of one of your cTrader accounts; state pending until its first spot

     The cTrader counterpart of `POST /md/subscriptions`, keyed on the account instead of a server. The
    platform subscribes the symbol's spots on that account at Spotware, and they stream on the
    `md:{account_id}:{symbol}` channel as `md.tick`. Two of your accounts at one broker and environment
    share one stream. A resource, not a command: it is created at once, `pending` until the first spot
    arrives. One per account and symbol: asking again answers the live one; asking after a stop reopens
    it. Stopped with `DELETE /md/subscriptions/{id}`. Another tenant's account, or none, is 404; an MT5
    account is 409 `state_error` with `details.reason` `not_on_this_venue` (it streams its server: `POST
    /md/subscriptions`).

    Args:
        id (UUID):
        idempotency_key (str):
        body (AccountMdSubscriptionCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountMdSubscription, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

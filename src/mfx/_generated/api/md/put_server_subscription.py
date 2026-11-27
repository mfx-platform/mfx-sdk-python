from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.billing_payment_required_error import BillingPaymentRequiredError
from ...models.error import Error
from ...models.md_server_subscription import MdServerSubscription
from ...models.md_server_subscription_put import MdServerSubscriptionPut
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: MdServerSubscriptionPut,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/md/servers/{id}/subscription".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[BillingPaymentRequiredError, Error, MdServerSubscription]:
    if response.status_code == 200:
        response_200 = MdServerSubscription.from_dict(response.json())

        return response_200

    if response.status_code == 402:
        response_402 = BillingPaymentRequiredError.from_dict(response.json())

        return response_402

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[BillingPaymentRequiredError, Error, MdServerSubscription]]:
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
    body: MdServerSubscriptionPut,
    idempotency_key: str,
) -> Response[Union[BillingPaymentRequiredError, Error, MdServerSubscription]]:
    """Subscribe to every symbol your terminals on a server read, each symbol's newest quote once an
    interval, on one channel

     One subscription per server. It is created if there is none, and its interval is changed if there is
    one; the same body twice changes nothing. A change of interval reaches the channel within 10
    seconds, with no reconnect. After a `DELETE`, a `PUT` makes a new subscription with a new `id`. A
    server of a cTrader venue is refused 409 `state_error` (`details.reason` `not_on_this_venue`):
    subscribe by account there. While the channel is not offered in an environment the answer is 409
    `state_error` (`details.reason` `server_channel_disabled`).

    Args:
        id (UUID):
        idempotency_key (str):
        body (MdServerSubscriptionPut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BillingPaymentRequiredError, Error, MdServerSubscription]]
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
    body: MdServerSubscriptionPut,
    idempotency_key: str,
) -> Optional[Union[BillingPaymentRequiredError, Error, MdServerSubscription]]:
    """Subscribe to every symbol your terminals on a server read, each symbol's newest quote once an
    interval, on one channel

     One subscription per server. It is created if there is none, and its interval is changed if there is
    one; the same body twice changes nothing. A change of interval reaches the channel within 10
    seconds, with no reconnect. After a `DELETE`, a `PUT` makes a new subscription with a new `id`. A
    server of a cTrader venue is refused 409 `state_error` (`details.reason` `not_on_this_venue`):
    subscribe by account there. While the channel is not offered in an environment the answer is 409
    `state_error` (`details.reason` `server_channel_disabled`).

    Args:
        id (UUID):
        idempotency_key (str):
        body (MdServerSubscriptionPut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BillingPaymentRequiredError, Error, MdServerSubscription]
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
    body: MdServerSubscriptionPut,
    idempotency_key: str,
) -> Response[Union[BillingPaymentRequiredError, Error, MdServerSubscription]]:
    """Subscribe to every symbol your terminals on a server read, each symbol's newest quote once an
    interval, on one channel

     One subscription per server. It is created if there is none, and its interval is changed if there is
    one; the same body twice changes nothing. A change of interval reaches the channel within 10
    seconds, with no reconnect. After a `DELETE`, a `PUT` makes a new subscription with a new `id`. A
    server of a cTrader venue is refused 409 `state_error` (`details.reason` `not_on_this_venue`):
    subscribe by account there. While the channel is not offered in an environment the answer is 409
    `state_error` (`details.reason` `server_channel_disabled`).

    Args:
        id (UUID):
        idempotency_key (str):
        body (MdServerSubscriptionPut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BillingPaymentRequiredError, Error, MdServerSubscription]]
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
    body: MdServerSubscriptionPut,
    idempotency_key: str,
) -> Optional[Union[BillingPaymentRequiredError, Error, MdServerSubscription]]:
    """Subscribe to every symbol your terminals on a server read, each symbol's newest quote once an
    interval, on one channel

     One subscription per server. It is created if there is none, and its interval is changed if there is
    one; the same body twice changes nothing. A change of interval reaches the channel within 10
    seconds, with no reconnect. After a `DELETE`, a `PUT` makes a new subscription with a new `id`. A
    server of a cTrader venue is refused 409 `state_error` (`details.reason` `not_on_this_venue`):
    subscribe by account there. While the channel is not offered in an environment the answer is 409
    `state_error` (`details.reason` `server_channel_disabled`).

    Args:
        id (UUID):
        idempotency_key (str):
        body (MdServerSubscriptionPut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BillingPaymentRequiredError, Error, MdServerSubscription]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

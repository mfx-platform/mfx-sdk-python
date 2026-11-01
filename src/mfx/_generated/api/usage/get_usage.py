from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.usage import Usage
from ...types import UNSET, Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/usage",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, Usage]:
    if response.status_code == 200:
        response_200 = Usage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, Usage]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, Usage]]:
    """The calling key's and its tenant's limits, where each comes from, and how much is in use

     Every limit that applies to the calling key and its tenant, so an integration paces itself
    below them. Per-key figures come from the tenant's plan unless the tenant or the key has
    its own (the key's beats the tenant's, which beats the plan's), and say whether they are
    applied yet (`enforced`).

    Defaults per plan, per API key:

    | Limit | Standard | Enterprise | System |
    |---|---|---|---|
    | Commands per second, steady | 5 | 20 | 50 |
    | Commands, burst | 10 | 50 | 100 |
    | Market-data messages per second | 200 | 2,000 | 5,000 |
    | Stream connections | 3 | 10 | 20 |
    | Account channels per connection | 50 | 500 | 1,000 |
    | Terminals per tenant | 20 | 200 | 500 |
    | Terminals per broker login | the broker's own limit | the broker's own limit | the broker's own
    limit |

    The terminals-per-tenant figures apply together with per-key enforcement; until then the
    tenant's terminal limit is the one `tenant.terminals` serves.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Usage]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, Usage]]:
    """The calling key's and its tenant's limits, where each comes from, and how much is in use

     Every limit that applies to the calling key and its tenant, so an integration paces itself
    below them. Per-key figures come from the tenant's plan unless the tenant or the key has
    its own (the key's beats the tenant's, which beats the plan's), and say whether they are
    applied yet (`enforced`).

    Defaults per plan, per API key:

    | Limit | Standard | Enterprise | System |
    |---|---|---|---|
    | Commands per second, steady | 5 | 20 | 50 |
    | Commands, burst | 10 | 50 | 100 |
    | Market-data messages per second | 200 | 2,000 | 5,000 |
    | Stream connections | 3 | 10 | 20 |
    | Account channels per connection | 50 | 500 | 1,000 |
    | Terminals per tenant | 20 | 200 | 500 |
    | Terminals per broker login | the broker's own limit | the broker's own limit | the broker's own
    limit |

    The terminals-per-tenant figures apply together with per-key enforcement; until then the
    tenant's terminal limit is the one `tenant.terminals` serves.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Usage]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, Usage]]:
    """The calling key's and its tenant's limits, where each comes from, and how much is in use

     Every limit that applies to the calling key and its tenant, so an integration paces itself
    below them. Per-key figures come from the tenant's plan unless the tenant or the key has
    its own (the key's beats the tenant's, which beats the plan's), and say whether they are
    applied yet (`enforced`).

    Defaults per plan, per API key:

    | Limit | Standard | Enterprise | System |
    |---|---|---|---|
    | Commands per second, steady | 5 | 20 | 50 |
    | Commands, burst | 10 | 50 | 100 |
    | Market-data messages per second | 200 | 2,000 | 5,000 |
    | Stream connections | 3 | 10 | 20 |
    | Account channels per connection | 50 | 500 | 1,000 |
    | Terminals per tenant | 20 | 200 | 500 |
    | Terminals per broker login | the broker's own limit | the broker's own limit | the broker's own
    limit |

    The terminals-per-tenant figures apply together with per-key enforcement; until then the
    tenant's terminal limit is the one `tenant.terminals` serves.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Usage]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, Usage]]:
    """The calling key's and its tenant's limits, where each comes from, and how much is in use

     Every limit that applies to the calling key and its tenant, so an integration paces itself
    below them. Per-key figures come from the tenant's plan unless the tenant or the key has
    its own (the key's beats the tenant's, which beats the plan's), and say whether they are
    applied yet (`enforced`).

    Defaults per plan, per API key:

    | Limit | Standard | Enterprise | System |
    |---|---|---|---|
    | Commands per second, steady | 5 | 20 | 50 |
    | Commands, burst | 10 | 50 | 100 |
    | Market-data messages per second | 200 | 2,000 | 5,000 |
    | Stream connections | 3 | 10 | 20 |
    | Account channels per connection | 50 | 500 | 1,000 |
    | Terminals per tenant | 20 | 200 | 500 |
    | Terminals per broker login | the broker's own limit | the broker's own limit | the broker's own
    limit |

    The terminals-per-tenant figures apply together with per-key enforcement; until then the
    tenant's terminal limit is the one `tenant.terminals` serves.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Usage]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed

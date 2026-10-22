from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.command import Command
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/commands/{id}".format(
            id=id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Command, Error]:
    if response.status_code == 200:
        response_200 = Command.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Command, Error]]:
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
) -> Response[Union[Command, Error]]:
    """Command state + result — mt5_retcode, retcode_text, reason (granular), comment_raw, tickets,
    exec_price, exec_volume, broker_latency_ms, agent_latency_ms, terminal_state

     UNKNOWN is visible and not final; it resolves to SUCCEEDED or FAILED by reconciliation. Another
    tenant's command is 404.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Command, Error]]
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
) -> Optional[Union[Command, Error]]:
    """Command state + result — mt5_retcode, retcode_text, reason (granular), comment_raw, tickets,
    exec_price, exec_volume, broker_latency_ms, agent_latency_ms, terminal_state

     UNKNOWN is visible and not final; it resolves to SUCCEEDED or FAILED by reconciliation. Another
    tenant's command is 404.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Command, Error]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Command, Error]]:
    """Command state + result — mt5_retcode, retcode_text, reason (granular), comment_raw, tickets,
    exec_price, exec_volume, broker_latency_ms, agent_latency_ms, terminal_state

     UNKNOWN is visible and not final; it resolves to SUCCEEDED or FAILED by reconciliation. Another
    tenant's command is 404.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Command, Error]]
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
) -> Optional[Union[Command, Error]]:
    """Command state + result — mt5_retcode, retcode_text, reason (granular), comment_raw, tickets,
    exec_price, exec_volume, broker_latency_ms, agent_latency_ms, terminal_state

     UNKNOWN is visible and not final; it resolves to SUCCEEDED or FAILED by reconciliation. Another
    tenant's command is 404.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Command, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed

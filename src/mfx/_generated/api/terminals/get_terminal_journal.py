from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.terminal_journal import TerminalJournal
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    lines: Union[Unset, int] = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["lines"] = lines

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/terminals/{id}/journal".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, TerminalJournal]:
    if response.status_code == 200:
        response_200 = TerminalJournal.from_dict(response.json())

        return response_200

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, TerminalJournal]]:
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
    lines: Union[Unset, int] = 100,
) -> Response[Union[Error, TerminalJournal]]:
    """The terminal's MetaTrader journal, newest first - read live while it runs, its last lines for 24
    hours after it stops

     While the terminal runs, the lines are read from its cell on request (`from: live`, within 10 s, as
    a quote is). When it has stopped, failed or been retired, the answer is the last lines its cell kept
    at the stop (`from: last_words`), kept 24 hours. Account numbers are masked (`****` and the last
    four digits, yours included) and the cell's file paths are removed; MetaTrader writes no password to
    its journal. Expert advisor logs are not included. Every read is audited. Another tenant's terminal
    is 404.

    Args:
        id (UUID):
        lines (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TerminalJournal]]
    """

    kwargs = _get_kwargs(
        id=id,
        lines=lines,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    lines: Union[Unset, int] = 100,
) -> Optional[Union[Error, TerminalJournal]]:
    """The terminal's MetaTrader journal, newest first - read live while it runs, its last lines for 24
    hours after it stops

     While the terminal runs, the lines are read from its cell on request (`from: live`, within 10 s, as
    a quote is). When it has stopped, failed or been retired, the answer is the last lines its cell kept
    at the stop (`from: last_words`), kept 24 hours. Account numbers are masked (`****` and the last
    four digits, yours included) and the cell's file paths are removed; MetaTrader writes no password to
    its journal. Expert advisor logs are not included. Every read is audited. Another tenant's terminal
    is 404.

    Args:
        id (UUID):
        lines (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TerminalJournal]
    """

    return sync_detailed(
        id=id,
        client=client,
        lines=lines,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    lines: Union[Unset, int] = 100,
) -> Response[Union[Error, TerminalJournal]]:
    """The terminal's MetaTrader journal, newest first - read live while it runs, its last lines for 24
    hours after it stops

     While the terminal runs, the lines are read from its cell on request (`from: live`, within 10 s, as
    a quote is). When it has stopped, failed or been retired, the answer is the last lines its cell kept
    at the stop (`from: last_words`), kept 24 hours. Account numbers are masked (`****` and the last
    four digits, yours included) and the cell's file paths are removed; MetaTrader writes no password to
    its journal. Expert advisor logs are not included. Every read is audited. Another tenant's terminal
    is 404.

    Args:
        id (UUID):
        lines (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TerminalJournal]]
    """

    kwargs = _get_kwargs(
        id=id,
        lines=lines,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    lines: Union[Unset, int] = 100,
) -> Optional[Union[Error, TerminalJournal]]:
    """The terminal's MetaTrader journal, newest first - read live while it runs, its last lines for 24
    hours after it stops

     While the terminal runs, the lines are read from its cell on request (`from: live`, within 10 s, as
    a quote is). When it has stopped, failed or been retired, the answer is the last lines its cell kept
    at the stop (`from: last_words`), kept 24 hours. Account numbers are masked (`****` and the last
    four digits, yours included) and the cell's file paths are removed; MetaTrader writes no password to
    its journal. Expert advisor logs are not included. Every read is audited. Another tenant's terminal
    is 404.

    Args:
        id (UUID):
        lines (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TerminalJournal]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            lines=lines,
        )
    ).parsed

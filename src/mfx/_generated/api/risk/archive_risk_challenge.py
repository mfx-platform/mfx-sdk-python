from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.risk_challenge import RiskChallenge
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/risk/challenges/{id}/archive".format(
            id=id,
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, RiskChallenge]:
    if response.status_code == 200:
        response_200 = RiskChallenge.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, RiskChallenge]]:
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
    idempotency_key: str,
) -> Response[Union[Error, RiskChallenge]]:
    """Archive a challenge with no account in progress; it no longer counts toward the challenges_max quota

     Refused 409 `state_error` while any account is in progress in the challenge; `details.accounts`
    lists those accounts. An account that passed, failed or ended does not hold it. An archived
    challenge stays readable with its versions, its accounts' results and their periods, and Activity
    keeps everything it did. It takes no new version and enrols no account (409 `state_error`). A failed
    account's block on entries is unchanged by the archive; the account's clear lifts it. Archiving an
    archived challenge answers it as it is.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskChallenge]]
    """

    kwargs = _get_kwargs(
        id=id,
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
    idempotency_key: str,
) -> Optional[Union[Error, RiskChallenge]]:
    """Archive a challenge with no account in progress; it no longer counts toward the challenges_max quota

     Refused 409 `state_error` while any account is in progress in the challenge; `details.accounts`
    lists those accounts. An account that passed, failed or ended does not hold it. An archived
    challenge stays readable with its versions, its accounts' results and their periods, and Activity
    keeps everything it did. It takes no new version and enrols no account (409 `state_error`). A failed
    account's block on entries is unchanged by the archive; the account's clear lifts it. Archiving an
    archived challenge answers it as it is.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskChallenge]
    """

    return sync_detailed(
        id=id,
        client=client,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    idempotency_key: str,
) -> Response[Union[Error, RiskChallenge]]:
    """Archive a challenge with no account in progress; it no longer counts toward the challenges_max quota

     Refused 409 `state_error` while any account is in progress in the challenge; `details.accounts`
    lists those accounts. An account that passed, failed or ended does not hold it. An archived
    challenge stays readable with its versions, its accounts' results and their periods, and Activity
    keeps everything it did. It takes no new version and enrols no account (409 `state_error`). A failed
    account's block on entries is unchanged by the archive; the account's clear lifts it. Archiving an
    archived challenge answers it as it is.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskChallenge]]
    """

    kwargs = _get_kwargs(
        id=id,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    idempotency_key: str,
) -> Optional[Union[Error, RiskChallenge]]:
    """Archive a challenge with no account in progress; it no longer counts toward the challenges_max quota

     Refused 409 `state_error` while any account is in progress in the challenge; `details.accounts`
    lists those accounts. An account that passed, failed or ended does not hold it. An archived
    challenge stays readable with its versions, its accounts' results and their periods, and Activity
    keeps everything it did. It takes no new version and enrols no account (409 `state_error`). A failed
    account's block on entries is unchanged by the archive; the account's clear lifts it. Archiving an
    archived challenge answers it as it is.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskChallenge]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            idempotency_key=idempotency_key,
        )
    ).parsed

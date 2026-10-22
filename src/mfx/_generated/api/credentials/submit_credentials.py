from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.credential_accepted import CredentialAccepted
from ...models.credential_submission import CredentialSubmission
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: CredentialSubmission,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/terminals/{id}/credentials".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, CredentialAccepted, Error]:
    if response.status_code == 202:
        response_202 = CredentialAccepted.from_dict(response.json())

        return response_202

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, CredentialAccepted, Error]]:
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
    body: CredentialSubmission,
    idempotency_key: str,
) -> Response[Union[Any, CredentialAccepted, Error]]:
    """Submit or rotate credentials (master | investor) — stored securely, response by reference, never
    echoed

     The first submission for a terminal stores its credential. A later one for the **same login**
    rotates it: a new stored version, used from the terminal's next login. `takes_effect` says when that
    is: an ACTIVE terminal is restarted now, open positions or not while the platform's open-position
    confirmation setting is off (its default), a FAILED one rejoins its login queue now, any other uses
    it at its next login. When the restart or retry-login is refused, `not_applied_reason` says why. A
    different login is 409 `conflict` (`details.reason = login_changed`): another account is another
    terminal. A DRAINING or RETIRED terminal is 409 `state_error`. **Several terminals on one login.** A
    login may be given to more than one terminal, on every plan, and each trades independently; they
    share the account at the broker. Two limits apply to a terminal's FIRST credential. The plan's
    entitlement, terminals per login, counted on your own terminals: 409 `quota_exceeded` with
    `details.reason = login_terminal_limit` and `details {quota, in_use}`. The broker server's session
    cap, counted on every session on the login: 409 `placement_error` with `details.reason =
    login_session_limit` and no counts. While the server's cap is still being measured by another
    terminal, the same refusal carries `details.retry_after_s`. A session above what the server is known
    to allow is accepted as a watched probe: if the broker refuses it or it displaces another session,
    that terminal is stopped and FAILED or retired with the reason, and the cap is recorded.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CredentialSubmission): What a tenant sends to put its own broker login on a
            terminal. The only request body in MFX Hub that carries a secret: it is read once,
            wrapped, written to the platform's secret store and never kept anywhere else, logged or
            echoed. Unknown properties are refused rather than ignored, so a misspelled password is an
            error and not a credential with no password.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CredentialAccepted, Error]]
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
    body: CredentialSubmission,
    idempotency_key: str,
) -> Optional[Union[Any, CredentialAccepted, Error]]:
    """Submit or rotate credentials (master | investor) — stored securely, response by reference, never
    echoed

     The first submission for a terminal stores its credential. A later one for the **same login**
    rotates it: a new stored version, used from the terminal's next login. `takes_effect` says when that
    is: an ACTIVE terminal is restarted now, open positions or not while the platform's open-position
    confirmation setting is off (its default), a FAILED one rejoins its login queue now, any other uses
    it at its next login. When the restart or retry-login is refused, `not_applied_reason` says why. A
    different login is 409 `conflict` (`details.reason = login_changed`): another account is another
    terminal. A DRAINING or RETIRED terminal is 409 `state_error`. **Several terminals on one login.** A
    login may be given to more than one terminal, on every plan, and each trades independently; they
    share the account at the broker. Two limits apply to a terminal's FIRST credential. The plan's
    entitlement, terminals per login, counted on your own terminals: 409 `quota_exceeded` with
    `details.reason = login_terminal_limit` and `details {quota, in_use}`. The broker server's session
    cap, counted on every session on the login: 409 `placement_error` with `details.reason =
    login_session_limit` and no counts. While the server's cap is still being measured by another
    terminal, the same refusal carries `details.retry_after_s`. A session above what the server is known
    to allow is accepted as a watched probe: if the broker refuses it or it displaces another session,
    that terminal is stopped and FAILED or retired with the reason, and the cap is recorded.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CredentialSubmission): What a tenant sends to put its own broker login on a
            terminal. The only request body in MFX Hub that carries a secret: it is read once,
            wrapped, written to the platform's secret store and never kept anywhere else, logged or
            echoed. Unknown properties are refused rather than ignored, so a misspelled password is an
            error and not a credential with no password.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CredentialAccepted, Error]
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
    body: CredentialSubmission,
    idempotency_key: str,
) -> Response[Union[Any, CredentialAccepted, Error]]:
    """Submit or rotate credentials (master | investor) — stored securely, response by reference, never
    echoed

     The first submission for a terminal stores its credential. A later one for the **same login**
    rotates it: a new stored version, used from the terminal's next login. `takes_effect` says when that
    is: an ACTIVE terminal is restarted now, open positions or not while the platform's open-position
    confirmation setting is off (its default), a FAILED one rejoins its login queue now, any other uses
    it at its next login. When the restart or retry-login is refused, `not_applied_reason` says why. A
    different login is 409 `conflict` (`details.reason = login_changed`): another account is another
    terminal. A DRAINING or RETIRED terminal is 409 `state_error`. **Several terminals on one login.** A
    login may be given to more than one terminal, on every plan, and each trades independently; they
    share the account at the broker. Two limits apply to a terminal's FIRST credential. The plan's
    entitlement, terminals per login, counted on your own terminals: 409 `quota_exceeded` with
    `details.reason = login_terminal_limit` and `details {quota, in_use}`. The broker server's session
    cap, counted on every session on the login: 409 `placement_error` with `details.reason =
    login_session_limit` and no counts. While the server's cap is still being measured by another
    terminal, the same refusal carries `details.retry_after_s`. A session above what the server is known
    to allow is accepted as a watched probe: if the broker refuses it or it displaces another session,
    that terminal is stopped and FAILED or retired with the reason, and the cap is recorded.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CredentialSubmission): What a tenant sends to put its own broker login on a
            terminal. The only request body in MFX Hub that carries a secret: it is read once,
            wrapped, written to the platform's secret store and never kept anywhere else, logged or
            echoed. Unknown properties are refused rather than ignored, so a misspelled password is an
            error and not a credential with no password.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CredentialAccepted, Error]]
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
    body: CredentialSubmission,
    idempotency_key: str,
) -> Optional[Union[Any, CredentialAccepted, Error]]:
    """Submit or rotate credentials (master | investor) — stored securely, response by reference, never
    echoed

     The first submission for a terminal stores its credential. A later one for the **same login**
    rotates it: a new stored version, used from the terminal's next login. `takes_effect` says when that
    is: an ACTIVE terminal is restarted now, open positions or not while the platform's open-position
    confirmation setting is off (its default), a FAILED one rejoins its login queue now, any other uses
    it at its next login. When the restart or retry-login is refused, `not_applied_reason` says why. A
    different login is 409 `conflict` (`details.reason = login_changed`): another account is another
    terminal. A DRAINING or RETIRED terminal is 409 `state_error`. **Several terminals on one login.** A
    login may be given to more than one terminal, on every plan, and each trades independently; they
    share the account at the broker. Two limits apply to a terminal's FIRST credential. The plan's
    entitlement, terminals per login, counted on your own terminals: 409 `quota_exceeded` with
    `details.reason = login_terminal_limit` and `details {quota, in_use}`. The broker server's session
    cap, counted on every session on the login: 409 `placement_error` with `details.reason =
    login_session_limit` and no counts. While the server's cap is still being measured by another
    terminal, the same refusal carries `details.retry_after_s`. A session above what the server is known
    to allow is accepted as a watched probe: if the broker refuses it or it displaces another session,
    that terminal is stopped and FAILED or retired with the reason, and the cap is recorded.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CredentialSubmission): What a tenant sends to put its own broker login on a
            terminal. The only request body in MFX Hub that carries a secret: it is read once,
            wrapped, written to the platform's secret store and never kept anywhere else, logged or
            echoed. Unknown properties are refused rather than ignored, so a misspelled password is an
            error and not a credential with no password.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CredentialAccepted, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

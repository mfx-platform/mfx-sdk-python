from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_external_close import CopyExternalClose
from ...models.copy_external_open import CopyExternalOpen
from ...models.copy_signal_accepted import CopySignalAccepted
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: Union["CopyExternalClose", "CopyExternalOpen"],
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/copy/leaders/{id}/signals".format(
            id=id,
        ),
    }

    _kwargs["json"]: dict[str, Any]
    if isinstance(body, CopyExternalOpen):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopySignalAccepted, Error]:
    if response.status_code == 202:
        response_202 = CopySignalAccepted.from_dict(response.json())

        return response_202

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopySignalAccepted, Error]]:
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
    body: Union["CopyExternalClose", "CopyExternalOpen"],
    idempotency_key: str,
) -> Response[Union[CopySignalAccepted, Error]]:
    """An external leader's signal - an open, or the close of an earlier open - copied to its followers

     Only for a leader whose source is `external`; any other is 409 `state_error` with `details.reason =
    leader_not_external`. The request is signed as every call is, and that signature is what authorises
    the signal: MFX Hub signs the copy signal once it is accepted.
    **Idempotent by your `id`.** An `id` this leader has sent before is answered with the original
    signal and `duplicate: true`, whatever the `Idempotency-Key`; the same `id` with a different body is
    409 `conflict` with `details.reason = signal_id_reused`. Nothing is copied twice.
    **Two forms.** An open names `symbol`, `side` and `volume` (or `units`), with `sl` and `tp` when you
    have them; it is a market entry. A close names the `id` of the open it closes, in `close`, and
    closes all of what each follower copied from it; a close for an open this leader never sent is 422
    `unprocessable` with `details.reason = unknown_open`. Every price and volume is a decimal string.
    **Time is MFX Hub's.** The signal's lifetime (the leader's `signal_lifetime_s`) runs from when MFX
    Hub accepts it, in UTC; your `time` is kept beside it as the source's own and is never used for the
    lifetime or the order.
    **The symbol.** `symbol` is your name for the instrument; give `instrument_key` (for example
    `fx:EURUSD`, `index:US30`) where you know it, and each follower's symbol is found from it by the
    mapping rule. A `volume` is in lots of the instrument's standard contract in MFX Hub's catalogue; a
    symbol with no contract size there is 422 `unprocessable` with `details.reason = no_contract_size`,
    and `units` (base units) may be sent instead.
    A paused leader's opens are 409 `state_error`; its closes are taken. Over the plan's signals a day
    is 409 `quota_exceeded` with `details.reason = plan_limit` and `details.limit =
    copy_signals_per_day`; nothing is copied. What became of each follower's copy is on the copy log and
    in `copy.copied` and `copy.refused`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (Union['CopyExternalClose', 'CopyExternalOpen']): An open or a close; they are told
            apart by close, which only a close carries

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopySignalAccepted, Error]]
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
    body: Union["CopyExternalClose", "CopyExternalOpen"],
    idempotency_key: str,
) -> Optional[Union[CopySignalAccepted, Error]]:
    """An external leader's signal - an open, or the close of an earlier open - copied to its followers

     Only for a leader whose source is `external`; any other is 409 `state_error` with `details.reason =
    leader_not_external`. The request is signed as every call is, and that signature is what authorises
    the signal: MFX Hub signs the copy signal once it is accepted.
    **Idempotent by your `id`.** An `id` this leader has sent before is answered with the original
    signal and `duplicate: true`, whatever the `Idempotency-Key`; the same `id` with a different body is
    409 `conflict` with `details.reason = signal_id_reused`. Nothing is copied twice.
    **Two forms.** An open names `symbol`, `side` and `volume` (or `units`), with `sl` and `tp` when you
    have them; it is a market entry. A close names the `id` of the open it closes, in `close`, and
    closes all of what each follower copied from it; a close for an open this leader never sent is 422
    `unprocessable` with `details.reason = unknown_open`. Every price and volume is a decimal string.
    **Time is MFX Hub's.** The signal's lifetime (the leader's `signal_lifetime_s`) runs from when MFX
    Hub accepts it, in UTC; your `time` is kept beside it as the source's own and is never used for the
    lifetime or the order.
    **The symbol.** `symbol` is your name for the instrument; give `instrument_key` (for example
    `fx:EURUSD`, `index:US30`) where you know it, and each follower's symbol is found from it by the
    mapping rule. A `volume` is in lots of the instrument's standard contract in MFX Hub's catalogue; a
    symbol with no contract size there is 422 `unprocessable` with `details.reason = no_contract_size`,
    and `units` (base units) may be sent instead.
    A paused leader's opens are 409 `state_error`; its closes are taken. Over the plan's signals a day
    is 409 `quota_exceeded` with `details.reason = plan_limit` and `details.limit =
    copy_signals_per_day`; nothing is copied. What became of each follower's copy is on the copy log and
    in `copy.copied` and `copy.refused`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (Union['CopyExternalClose', 'CopyExternalOpen']): An open or a close; they are told
            apart by close, which only a close carries

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopySignalAccepted, Error]
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
    body: Union["CopyExternalClose", "CopyExternalOpen"],
    idempotency_key: str,
) -> Response[Union[CopySignalAccepted, Error]]:
    """An external leader's signal - an open, or the close of an earlier open - copied to its followers

     Only for a leader whose source is `external`; any other is 409 `state_error` with `details.reason =
    leader_not_external`. The request is signed as every call is, and that signature is what authorises
    the signal: MFX Hub signs the copy signal once it is accepted.
    **Idempotent by your `id`.** An `id` this leader has sent before is answered with the original
    signal and `duplicate: true`, whatever the `Idempotency-Key`; the same `id` with a different body is
    409 `conflict` with `details.reason = signal_id_reused`. Nothing is copied twice.
    **Two forms.** An open names `symbol`, `side` and `volume` (or `units`), with `sl` and `tp` when you
    have them; it is a market entry. A close names the `id` of the open it closes, in `close`, and
    closes all of what each follower copied from it; a close for an open this leader never sent is 422
    `unprocessable` with `details.reason = unknown_open`. Every price and volume is a decimal string.
    **Time is MFX Hub's.** The signal's lifetime (the leader's `signal_lifetime_s`) runs from when MFX
    Hub accepts it, in UTC; your `time` is kept beside it as the source's own and is never used for the
    lifetime or the order.
    **The symbol.** `symbol` is your name for the instrument; give `instrument_key` (for example
    `fx:EURUSD`, `index:US30`) where you know it, and each follower's symbol is found from it by the
    mapping rule. A `volume` is in lots of the instrument's standard contract in MFX Hub's catalogue; a
    symbol with no contract size there is 422 `unprocessable` with `details.reason = no_contract_size`,
    and `units` (base units) may be sent instead.
    A paused leader's opens are 409 `state_error`; its closes are taken. Over the plan's signals a day
    is 409 `quota_exceeded` with `details.reason = plan_limit` and `details.limit =
    copy_signals_per_day`; nothing is copied. What became of each follower's copy is on the copy log and
    in `copy.copied` and `copy.refused`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (Union['CopyExternalClose', 'CopyExternalOpen']): An open or a close; they are told
            apart by close, which only a close carries

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopySignalAccepted, Error]]
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
    body: Union["CopyExternalClose", "CopyExternalOpen"],
    idempotency_key: str,
) -> Optional[Union[CopySignalAccepted, Error]]:
    """An external leader's signal - an open, or the close of an earlier open - copied to its followers

     Only for a leader whose source is `external`; any other is 409 `state_error` with `details.reason =
    leader_not_external`. The request is signed as every call is, and that signature is what authorises
    the signal: MFX Hub signs the copy signal once it is accepted.
    **Idempotent by your `id`.** An `id` this leader has sent before is answered with the original
    signal and `duplicate: true`, whatever the `Idempotency-Key`; the same `id` with a different body is
    409 `conflict` with `details.reason = signal_id_reused`. Nothing is copied twice.
    **Two forms.** An open names `symbol`, `side` and `volume` (or `units`), with `sl` and `tp` when you
    have them; it is a market entry. A close names the `id` of the open it closes, in `close`, and
    closes all of what each follower copied from it; a close for an open this leader never sent is 422
    `unprocessable` with `details.reason = unknown_open`. Every price and volume is a decimal string.
    **Time is MFX Hub's.** The signal's lifetime (the leader's `signal_lifetime_s`) runs from when MFX
    Hub accepts it, in UTC; your `time` is kept beside it as the source's own and is never used for the
    lifetime or the order.
    **The symbol.** `symbol` is your name for the instrument; give `instrument_key` (for example
    `fx:EURUSD`, `index:US30`) where you know it, and each follower's symbol is found from it by the
    mapping rule. A `volume` is in lots of the instrument's standard contract in MFX Hub's catalogue; a
    symbol with no contract size there is 422 `unprocessable` with `details.reason = no_contract_size`,
    and `units` (base units) may be sent instead.
    A paused leader's opens are 409 `state_error`; its closes are taken. Over the plan's signals a day
    is 409 `quota_exceeded` with `details.reason = plan_limit` and `details.limit =
    copy_signals_per_day`; nothing is copied. What became of each follower's copy is on the copy log and
    in `copy.copied` and `copy.refused`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (Union['CopyExternalClose', 'CopyExternalOpen']): An open or a close; they are told
            apart by close, which only a close carries

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopySignalAccepted, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.billing_payment_required_error import BillingPaymentRequiredError
from ...models.copy_group_rollover import CopyGroupRollover
from ...models.copy_group_rollover_result import CopyGroupRolloverResult
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    body: CopyGroupRollover,
    idempotency_key: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/copy/groups/{id}/rollover".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[BillingPaymentRequiredError, CopyGroupRolloverResult, Error]:
    if response.status_code == 200:
        response_200 = CopyGroupRolloverResult.from_dict(response.json())

        return response_200

    if response.status_code == 402:
        response_402 = BillingPaymentRequiredError.from_dict(response.json())

        return response_402

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[BillingPaymentRequiredError, CopyGroupRolloverResult, Error]]:
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
    body: CopyGroupRollover,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[Union[BillingPaymentRequiredError, CopyGroupRolloverResult, Error]]:
    """Set the group's template on its live members, or see what it would change (Enterprise)

     A template is what a follower created into the group starts from; this sets it on the followers
    already in it. Each member that has not unfollowed, in id order after `after`, at most `limit` (1 to
    500), has each field named in `fields` (by default every field the template sets) set to the
    template's, checked as an update of that follower is: `scaling` is replaced, `bounds`, `options` and
    `risk_limits` are laid over what it holds. Each member is answered `changed` with each field's
    `from` and `to`, `unchanged`, or `refused` with the reason an update would be refused
    (`not_on_this_venue` when its venue cannot honour an option, `needs_leader_account` for a ratio mode
    under an external leader); the others still change. `next_after` continues with the next page, null
    after the last. A dry run changes nothing and needs no Idempotency-Key. An applied rollover needs
    one (400 `validation_error` without it): each changed member's `mandate_version` rises once and its
    new mandate reaches its copy host as any update's does, the page is audited with its results, and a
    repeated Idempotency-Key answers the same results. A field named that the template does not set is
    422 `validation_error` with `details.unset`.

    Args:
        id (UUID):
        idempotency_key (Union[Unset, str]):
        body (CopyGroupRollover):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BillingPaymentRequiredError, CopyGroupRolloverResult, Error]]
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
    body: CopyGroupRollover,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[Union[BillingPaymentRequiredError, CopyGroupRolloverResult, Error]]:
    """Set the group's template on its live members, or see what it would change (Enterprise)

     A template is what a follower created into the group starts from; this sets it on the followers
    already in it. Each member that has not unfollowed, in id order after `after`, at most `limit` (1 to
    500), has each field named in `fields` (by default every field the template sets) set to the
    template's, checked as an update of that follower is: `scaling` is replaced, `bounds`, `options` and
    `risk_limits` are laid over what it holds. Each member is answered `changed` with each field's
    `from` and `to`, `unchanged`, or `refused` with the reason an update would be refused
    (`not_on_this_venue` when its venue cannot honour an option, `needs_leader_account` for a ratio mode
    under an external leader); the others still change. `next_after` continues with the next page, null
    after the last. A dry run changes nothing and needs no Idempotency-Key. An applied rollover needs
    one (400 `validation_error` without it): each changed member's `mandate_version` rises once and its
    new mandate reaches its copy host as any update's does, the page is audited with its results, and a
    repeated Idempotency-Key answers the same results. A field named that the template does not set is
    422 `validation_error` with `details.unset`.

    Args:
        id (UUID):
        idempotency_key (Union[Unset, str]):
        body (CopyGroupRollover):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BillingPaymentRequiredError, CopyGroupRolloverResult, Error]
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
    body: CopyGroupRollover,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[Union[BillingPaymentRequiredError, CopyGroupRolloverResult, Error]]:
    """Set the group's template on its live members, or see what it would change (Enterprise)

     A template is what a follower created into the group starts from; this sets it on the followers
    already in it. Each member that has not unfollowed, in id order after `after`, at most `limit` (1 to
    500), has each field named in `fields` (by default every field the template sets) set to the
    template's, checked as an update of that follower is: `scaling` is replaced, `bounds`, `options` and
    `risk_limits` are laid over what it holds. Each member is answered `changed` with each field's
    `from` and `to`, `unchanged`, or `refused` with the reason an update would be refused
    (`not_on_this_venue` when its venue cannot honour an option, `needs_leader_account` for a ratio mode
    under an external leader); the others still change. `next_after` continues with the next page, null
    after the last. A dry run changes nothing and needs no Idempotency-Key. An applied rollover needs
    one (400 `validation_error` without it): each changed member's `mandate_version` rises once and its
    new mandate reaches its copy host as any update's does, the page is audited with its results, and a
    repeated Idempotency-Key answers the same results. A field named that the template does not set is
    422 `validation_error` with `details.unset`.

    Args:
        id (UUID):
        idempotency_key (Union[Unset, str]):
        body (CopyGroupRollover):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BillingPaymentRequiredError, CopyGroupRolloverResult, Error]]
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
    body: CopyGroupRollover,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[Union[BillingPaymentRequiredError, CopyGroupRolloverResult, Error]]:
    """Set the group's template on its live members, or see what it would change (Enterprise)

     A template is what a follower created into the group starts from; this sets it on the followers
    already in it. Each member that has not unfollowed, in id order after `after`, at most `limit` (1 to
    500), has each field named in `fields` (by default every field the template sets) set to the
    template's, checked as an update of that follower is: `scaling` is replaced, `bounds`, `options` and
    `risk_limits` are laid over what it holds. Each member is answered `changed` with each field's
    `from` and `to`, `unchanged`, or `refused` with the reason an update would be refused
    (`not_on_this_venue` when its venue cannot honour an option, `needs_leader_account` for a ratio mode
    under an external leader); the others still change. `next_after` continues with the next page, null
    after the last. A dry run changes nothing and needs no Idempotency-Key. An applied rollover needs
    one (400 `validation_error` without it): each changed member's `mandate_version` rises once and its
    new mandate reaches its copy host as any update's does, the page is audited with its results, and a
    repeated Idempotency-Key answers the same results. A field named that the template does not set is
    422 `validation_error` with `details.unset`.

    Args:
        id (UUID):
        idempotency_key (Union[Unset, str]):
        body (CopyGroupRollover):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BillingPaymentRequiredError, CopyGroupRolloverResult, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

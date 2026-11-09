from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_follower import CopyFollower
from ...models.copy_follower_create import CopyFollowerCreate
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: CopyFollowerCreate,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/copy/followers",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopyFollower, Error]:
    if response.status_code == 201:
        response_201 = CopyFollower.from_dict(response.json())

        return response_201

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
) -> Response[Union[CopyFollower, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyFollowerCreate,
    idempotency_key: str,
) -> Response[Union[CopyFollower, Error]]:
    """Make one of your accounts follow a leader, with its own scaling, bounds, symbol map, options and
    limits

     The follow is checked once, here, against the account's venue, never on a signal: an option the
    account's venue cannot honour (copying pending orders on a venue without them, for example) is 422
    `unprocessable` with `details.reason = not_on_this_venue` and `details.options` naming each one. The
    leader's own account cannot follow it: 422 `unprocessable` with `details.reason = follows_itself`.
    An account follows a leader once: a second follow while the first has not unfollowed is 409
    `conflict` with `details.reason = already_following` and `details.follower_id`. A leader that is
    retired is 409 `state_error`; an account the leader's `who_may_join` does not admit is 422
    `unprocessable` with `details.reason = not_admitted`. A ratio mode (`balance_ratio`, `equity_ratio`)
    needs the leader's account figures, so it cannot follow an external leader: 422 `unprocessable` with
    `details.reason = needs_leader_account`. Over the plan's number of followers is 409 `quota_exceeded`
    with `details.reason = plan_limit` and `details.limit = copy_followers`.
    With `group_id`, the group's template fills every field this request leaves out; the follower holds
    its own copy from then on. Risk limits are in the follower account's own currency. The answer's
    `mandate_version` is 1; every change makes a new version.

    Args:
        idempotency_key (str):
        body (CopyFollowerCreate): scaling is required unless group_id names a group whose
            template has it

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyFollower, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyFollowerCreate,
    idempotency_key: str,
) -> Optional[Union[CopyFollower, Error]]:
    """Make one of your accounts follow a leader, with its own scaling, bounds, symbol map, options and
    limits

     The follow is checked once, here, against the account's venue, never on a signal: an option the
    account's venue cannot honour (copying pending orders on a venue without them, for example) is 422
    `unprocessable` with `details.reason = not_on_this_venue` and `details.options` naming each one. The
    leader's own account cannot follow it: 422 `unprocessable` with `details.reason = follows_itself`.
    An account follows a leader once: a second follow while the first has not unfollowed is 409
    `conflict` with `details.reason = already_following` and `details.follower_id`. A leader that is
    retired is 409 `state_error`; an account the leader's `who_may_join` does not admit is 422
    `unprocessable` with `details.reason = not_admitted`. A ratio mode (`balance_ratio`, `equity_ratio`)
    needs the leader's account figures, so it cannot follow an external leader: 422 `unprocessable` with
    `details.reason = needs_leader_account`. Over the plan's number of followers is 409 `quota_exceeded`
    with `details.reason = plan_limit` and `details.limit = copy_followers`.
    With `group_id`, the group's template fills every field this request leaves out; the follower holds
    its own copy from then on. Risk limits are in the follower account's own currency. The answer's
    `mandate_version` is 1; every change makes a new version.

    Args:
        idempotency_key (str):
        body (CopyFollowerCreate): scaling is required unless group_id names a group whose
            template has it

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyFollower, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyFollowerCreate,
    idempotency_key: str,
) -> Response[Union[CopyFollower, Error]]:
    """Make one of your accounts follow a leader, with its own scaling, bounds, symbol map, options and
    limits

     The follow is checked once, here, against the account's venue, never on a signal: an option the
    account's venue cannot honour (copying pending orders on a venue without them, for example) is 422
    `unprocessable` with `details.reason = not_on_this_venue` and `details.options` naming each one. The
    leader's own account cannot follow it: 422 `unprocessable` with `details.reason = follows_itself`.
    An account follows a leader once: a second follow while the first has not unfollowed is 409
    `conflict` with `details.reason = already_following` and `details.follower_id`. A leader that is
    retired is 409 `state_error`; an account the leader's `who_may_join` does not admit is 422
    `unprocessable` with `details.reason = not_admitted`. A ratio mode (`balance_ratio`, `equity_ratio`)
    needs the leader's account figures, so it cannot follow an external leader: 422 `unprocessable` with
    `details.reason = needs_leader_account`. Over the plan's number of followers is 409 `quota_exceeded`
    with `details.reason = plan_limit` and `details.limit = copy_followers`.
    With `group_id`, the group's template fills every field this request leaves out; the follower holds
    its own copy from then on. Risk limits are in the follower account's own currency. The answer's
    `mandate_version` is 1; every change makes a new version.

    Args:
        idempotency_key (str):
        body (CopyFollowerCreate): scaling is required unless group_id names a group whose
            template has it

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyFollower, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyFollowerCreate,
    idempotency_key: str,
) -> Optional[Union[CopyFollower, Error]]:
    """Make one of your accounts follow a leader, with its own scaling, bounds, symbol map, options and
    limits

     The follow is checked once, here, against the account's venue, never on a signal: an option the
    account's venue cannot honour (copying pending orders on a venue without them, for example) is 422
    `unprocessable` with `details.reason = not_on_this_venue` and `details.options` naming each one. The
    leader's own account cannot follow it: 422 `unprocessable` with `details.reason = follows_itself`.
    An account follows a leader once: a second follow while the first has not unfollowed is 409
    `conflict` with `details.reason = already_following` and `details.follower_id`. A leader that is
    retired is 409 `state_error`; an account the leader's `who_may_join` does not admit is 422
    `unprocessable` with `details.reason = not_admitted`. A ratio mode (`balance_ratio`, `equity_ratio`)
    needs the leader's account figures, so it cannot follow an external leader: 422 `unprocessable` with
    `details.reason = needs_leader_account`. Over the plan's number of followers is 409 `quota_exceeded`
    with `details.reason = plan_limit` and `details.limit = copy_followers`.
    With `group_id`, the group's template fills every field this request leaves out; the follower holds
    its own copy from then on. Risk limits are in the follower account's own currency. The answer's
    `mandate_version` is 1; every change makes a new version.

    Args:
        idempotency_key (str):
        body (CopyFollowerCreate): scaling is required unless group_id names a group whose
            template has it

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyFollower, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

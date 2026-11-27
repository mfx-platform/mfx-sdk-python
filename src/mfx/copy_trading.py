"""``client.copy`` — Copy Trading: leaders, followers, groups, stop-outs and the copy log.

One of the tenant's accounts, or an external signal source, **leads**; other accounts **follow**
it, each with its own scaling, bounds, symbol map, options and limits. The tenant chooses the
leader, the scaling and the limits; MFX Hub executes and suggests none of them. Leaders and
followers are trading accounts (``account_id``, the id ``client.trading_accounts`` lists), each
with its ``venue``; a leader and its followers may be on different venues.

Reads need ``copy:read`` and writes ``copy:write``. Every write takes an ``idempotency_key`` and is
sent once: the SDK never retries a write. A list is cursor-paginated; each list method answers a
:class:`CopyPage`, which is a :class:`~mfx.pages.Page` with the list's ``stats`` row (counted over
everything the filters match, not over the page), and an ``all_*`` method follows the cursor.

What became of each copy is on the copy log (:meth:`Copy.log`) and in the ``copy.*`` events
(:mod:`mfx.events`). A copy that did not fill names one of :data:`REFUSAL_REASONS`, a closed list.
A close of copied positions (an unfollow or a retire with ``close_copied``, or a group's close) is
a requested close: :meth:`Copy.closes` and :meth:`Copy.get_close` follow it, and ``copy.closed``
says when it is final.

**What a nested setting takes.** ``scaling``, ``bounds``, ``options``, ``risk_limits``,
``filters``, ``copies``, ``limits``, ``who_may_join``, ``template`` and preview ``rows`` are
mappings in the contract's own names (``{"mode": "fixed_multiplier", "multiplier": "0.5"}``). A
decimal is a ``Decimal``, a string or an int; a ``float`` anywhere is a ``TypeError``, a name the
contract does not have or a word outside its list is a ``ValueError``, both before anything is
sent.

**Risk-protected followers.** ``options`` takes ``when_risk_unchecked``, ``"refuse"`` (the
default) or ``"copy"``. When the follower account is protected by Risk Management (an active
policy or a challenge in progress) and its copy host cannot yet check a copy against it: refuse
refuses the copy with risk_rule (reason risk_inputs_stale); copy copies it unchecked. Once the host
can check, every copy is checked whatever this says. A follower read back shows it.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import AsyncIterator, Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Final, Literal, Protocol, Self, get_args
from uuid import UUID

from mfx._generated.api.copy import add_copy_group_followers as _add_group_followers
from mfx._generated.api.copy import close_copy_group as _close_group
from mfx._generated.api.copy import create_copy_follower as _create_follower
from mfx._generated.api.copy import create_copy_group as _create_group
from mfx._generated.api.copy import create_copy_leader as _create_leader
from mfx._generated.api.copy import get_copy_close as _get_close
from mfx._generated.api.copy import get_copy_follower as _get_follower
from mfx._generated.api.copy import get_copy_group as _get_group
from mfx._generated.api.copy import get_copy_leader as _get_leader
from mfx._generated.api.copy import list_copy_closes as _list_closes
from mfx._generated.api.copy import list_copy_followers as _list_followers
from mfx._generated.api.copy import list_copy_groups as _list_groups
from mfx._generated.api.copy import list_copy_leaders as _list_leaders
from mfx._generated.api.copy import list_copy_log as _list_log
from mfx._generated.api.copy import list_copy_signals as _list_signals
from mfx._generated.api.copy import list_copy_stopouts as _list_stopouts
from mfx._generated.api.copy import list_tenant_copy_stopouts as _list_tenant_stopouts
from mfx._generated.api.copy import pause_copy_follower as _pause_follower
from mfx._generated.api.copy import pause_copy_group as _pause_group
from mfx._generated.api.copy import pause_copy_leader as _pause_leader
from mfx._generated.api.copy import preview_copy_follower as _preview_follower
from mfx._generated.api.copy import remove_copy_group_followers as _remove_group_followers
from mfx._generated.api.copy import reset_copy_stopouts as _reset_stopouts
from mfx._generated.api.copy import resume_copy_follower as _resume_follower
from mfx._generated.api.copy import resume_copy_group as _resume_group
from mfx._generated.api.copy import resume_copy_leader as _resume_leader
from mfx._generated.api.copy import resync_copy_follower as _resync_follower
from mfx._generated.api.copy import retire_copy_leader as _retire_leader
from mfx._generated.api.copy import rollover_copy_group as _rollover_group
from mfx._generated.api.copy import send_copy_signal as _send_signal
from mfx._generated.api.copy import unfollow_copy_leader as _unfollow
from mfx._generated.api.copy import update_copy_follower as _update_follower
from mfx._generated.api.copy import update_copy_group as _update_group
from mfx._generated.api.copy import update_copy_leader as _update_leader
from mfx._generated.models.copy_close import CopyClose
from mfx._generated.models.copy_close_page_stats import CopyClosePageStats
from mfx._generated.models.copy_close_state import CopyCloseState
from mfx._generated.models.copy_external_close import CopyExternalClose
from mfx._generated.models.copy_external_open import CopyExternalOpen
from mfx._generated.models.copy_follower import CopyFollower
from mfx._generated.models.copy_follower_create import CopyFollowerCreate
from mfx._generated.models.copy_follower_page_stats import CopyFollowerPageStats
from mfx._generated.models.copy_follower_state import CopyFollowerState
from mfx._generated.models.copy_follower_update import CopyFollowerUpdate
from mfx._generated.models.copy_group import CopyGroup
from mfx._generated.models.copy_group_close import CopyGroupClose
from mfx._generated.models.copy_group_close_result import CopyGroupCloseResult
from mfx._generated.models.copy_group_create import CopyGroupCreate
from mfx._generated.models.copy_group_members import CopyGroupMembers
from mfx._generated.models.copy_group_members_result import CopyGroupMembersResult
from mfx._generated.models.copy_group_page_stats import CopyGroupPageStats
from mfx._generated.models.copy_group_rollover import CopyGroupRollover
from mfx._generated.models.copy_group_rollover_result import CopyGroupRolloverResult
from mfx._generated.models.copy_group_state import CopyGroupState
from mfx._generated.models.copy_group_update import CopyGroupUpdate
from mfx._generated.models.copy_leader import CopyLeader
from mfx._generated.models.copy_leader_create import CopyLeaderCreate
from mfx._generated.models.copy_leader_page_stats import CopyLeaderPageStats
from mfx._generated.models.copy_leader_retire import CopyLeaderRetire
from mfx._generated.models.copy_leader_source import CopyLeaderSource
from mfx._generated.models.copy_leader_state import CopyLeaderState
from mfx._generated.models.copy_leader_update import CopyLeaderUpdate
from mfx._generated.models.copy_log_entry import CopyLogEntry
from mfx._generated.models.copy_log_page_stats import CopyLogPageStats
from mfx._generated.models.copy_outcome import CopyOutcome
from mfx._generated.models.copy_preview import CopyPreview
from mfx._generated.models.copy_preview_request import CopyPreviewRequest
from mfx._generated.models.copy_reason import CopyReason
from mfx._generated.models.copy_signal_accepted import CopySignalAccepted
from mfx._generated.models.copy_signal_entry import CopySignalEntry
from mfx._generated.models.copy_signal_page_stats import CopySignalPageStats
from mfx._generated.models.copy_stopout import CopyStopout
from mfx._generated.models.copy_stopout_reset import CopyStopoutReset
from mfx._generated.models.copy_stopout_state import CopyStopoutState
from mfx._generated.models.copy_tenant_stopout_page_stats import CopyTenantStopoutPageStats
from mfx._generated.models.copy_unfollow import CopyUnfollow
from mfx._generated.models.list_copy_followers_sort import ListCopyFollowersSort
from mfx._generated.models.list_copy_log_sort import ListCopyLogSort
from mfx._generated.models.list_copy_signals_action_item import ListCopySignalsActionItem
from mfx._generated.models.list_copy_signals_kind_item import ListCopySignalsKindItem
from mfx._generated.models.venue import Venue
from mfx._generated.types import UNSET
from mfx._words import refuse_unknown_words
from mfx.execution import Amount, _decimal
from mfx.pages import Page, page_of, states_param

if TYPE_CHECKING:
    from mfx.client import MfxClient

__all__ = [
    "REFUSAL_REASONS",
    "CloseStateName",
    "Copy",
    "CopyLogSort",
    "CopyOutcomeName",
    "CopyPage",
    "FollowerStateName",
    "GroupStateName",
    "LeaderSourceName",
    "LeaderStateName",
    "LimitKindName",
    "NewestOrOldest",
    "RolloverField",
    "SignalActionName",
    "SignalKindName",
    "RefusalReason",
    "Setting",
    "StopoutStateName",
]

Id = str | UUID
#: A nested setting, in the contract's names: ``{"mode": "fixed_multiplier", "multiplier": "2"}``.
Setting = Mapping[str, Any]

#: Where a leader's deals come from: one of your accounts, or your own signals.
LeaderSourceName = Literal["account", "external"]
#: A leader's state. ``retired`` is final.
LeaderStateName = Literal["active", "paused", "retired"]
#: A follower's state. ``unfollowed`` is final.
FollowerStateName = Literal["copying", "paused", "stopped_out", "unfollowed"]
#: A group's state.
GroupStateName = Literal["active", "paused"]
#: A stop-out's state.
StopoutStateName = Literal["active", "reset", "expired"]
#: The follower limit a stop-out reached, or the one a reset names.
LimitKindName = Literal["daily", "monthly", "lifetime"]
#: What became of one copy.
CopyOutcomeName = Literal["filled", "refused", "skipped", "stopout"]
#: A requested close's state: ``pending`` until every copied position it covers is closed or
#: found closed (``done``), it gives up on one (``incomplete``), or a wider close takes it over
#: (``superseded``).
CloseStateName = Literal["pending", "done", "incomplete", "superseded"]
#: A list's order by when each row was made.
NewestOrOldest = Literal["newest", "oldest"]
#: A template field a group's rollover can set on its members.
RolloverField = Literal["scaling", "bounds", "options", "risk_limits", "close_on_stopout"]
#: Where a signal came from: a leader account's fill, or an external leader's own signal.
SignalKindName = Literal["fill", "external"]
#: What a signal does.
SignalActionName = Literal[
    "open", "modify", "close", "close_part", "pending_place", "pending_modify", "pending_cancel"
]
#: The log's order: newest first, or the slowest of MFX Hub's part first.
CopyLogSort = Literal["created_at", "mfx_ms"]
#: Why a copy did not fill. The list is closed: a new reason is a change to the contract.
RefusalReason = Literal[
    "mapping",
    "min_volume",
    "no_stop",
    "risk_rule",
    "plan_limit",
    "stopped_out",
    "signal_expired",
    "skip_pending",
    "close_only",
    "paused",
    "account_not_connected",
    "market_closed",
    "no_conversion",
    "not_on_this_venue",
    "venue_unavailable",
    "broker",
]

#: Every refusal reason the contract names, in its order. ``broker`` comes with the venue's own
#: code beside it as ``venue_code``.
REFUSAL_REASONS: Final[tuple[str, ...]] = get_args(RefusalReason)

#: How many follower ids one group call takes.
_MEMBERS_MAX: Final = 500


@dataclass(frozen=True, slots=True)
class CopyPage[T, S](Page[T]):
    """A page of a copy list and its ``stats`` row.

    ``stats`` counts everything the filters (and, on the log, the window) match, not this page,
    and is the same on every page: for leaders and followers a count of each state, for the log
    the outcomes and the p50, p95 and p99 of MFX Hub's part. None when the answer carries none.
    """

    stats: S | None = None


class _Model(Protocol):
    """What a generated request model offers."""

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self: ...

    def to_dict(self) -> dict[str, Any]: ...


class _Omit:
    """A body field the caller did not give: not sent at all, unlike ``None``, which is sent as
    null (and clears the field where the contract allows it)."""


_OMIT: Final = _Omit()


def _uuid(value: Id) -> UUID:
    return value if isinstance(value, UUID) else UUID(str(value))


def _wire(name: str, value: Any) -> Any:  # noqa: ANN401, PLR0911 - any JSON value, one case each
    """A caller's value as the contract writes it: decimals as plain strings, ids and instants as
    text, mappings and sequences walked. A float anywhere is refused, as everywhere in this SDK."""
    if value is None or isinstance(value, bool | str | int):
        return value
    if isinstance(value, float):
        raise TypeError(
            f"{name} must be a Decimal, a str or an int, not a float: a computed float carries "
            f"binary error, and the platform takes decimals as strings. Send "
            f'Decimal("{value!r}") or a string.'
        )
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError(f"{name} must be a finite decimal, not {value!r}")
        return format(value, "f")
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, dt.datetime):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): _wire(f"{name}.{key}", item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [_wire(f"{name}[{index}]", item) for index, item in enumerate(value)]
    raise TypeError(f"{name} cannot be sent: {type(value).__name__}")


def _kept(name: str, sent: Any, kept: Any) -> None:  # noqa: ANN401 - JSON values
    """Refuse a name the contract does not have: the generated model drops one it does not know,
    and a misspelt setting that silently vanished would be a follow with a setting nobody chose."""
    if isinstance(sent, dict) and isinstance(kept, dict):
        for key, item in sent.items():
            if key not in kept:
                raise ValueError(f"{name}.{key} is not a field the contract has")
            _kept(f"{name}.{key}", item, kept[key])
    elif isinstance(sent, list) and isinstance(kept, list):
        for index, (item, kept_item) in enumerate(zip(sent, kept, strict=False)):
            _kept(f"{name}[{index}]", item, kept_item)


def _body[M: _Model](model: type[M], name: str, fields: Mapping[str, Any]) -> M:
    """Build a request body from the fields given, checked against the contract before sending."""
    sent = {key: _wire(key, value) for key, value in fields.items() if value is not _OMIT}
    try:
        built = refuse_unknown_words(model.from_dict(sent))
    except (KeyError, ValueError, TypeError, AttributeError) as exc:
        raise ValueError(f"{name} does not fit the contract: {type(exc).__name__}: {exc}") from exc
    _kept(name, sent, built.to_dict())
    return built


def _signed_decimal(name: str, value: Amount) -> str:
    """A decimal that may be negative, as the contract's ``CopyDecimal`` allows (``^-?...``): a
    stop loss or take profit is a price, and some instruments trade below zero. The magnitude is
    checked as every other decimal is; a float is refused."""
    negative, magnitude = False, value
    if isinstance(value, str):
        negative, magnitude = value.strip().startswith("-"), value.strip().removeprefix("-")
    elif isinstance(value, Decimal | int) and not isinstance(value, bool):
        negative = value.is_signed() if isinstance(value, Decimal) else value < 0
        magnitude = -value if negative else value
    out = _decimal(name, magnitude)  # a float, or no decimal at all, is refused there
    return f"-{out}" if negative and Decimal(out) != 0 else out


def _given(value: Any) -> Any:  # noqa: ANN401 - any optional argument
    """An optional argument that was left out is not sent."""
    return _OMIT if value is None else value


def _opt_uuid(value: Id | None) -> Any:  # noqa: ANN401 - UUID or UNSET
    return UNSET if value is None else _uuid(value)


def _window(what: str, from_: dt.datetime | None, to: dt.datetime | None) -> None:
    """A list's window: each end an aware datetime, and the end not before the start."""
    for name, moment in (("from_", from_), ("to", to)):
        if moment is not None and moment.utcoffset() is None:
            raise ValueError(
                f"{name} is a naive datetime: give it a timezone, such as "
                f"datetime(..., tzinfo=datetime.UTC), so the window is the instant you mean"
            )
    if from_ is not None and to is not None and to < from_:
        raise ValueError(f"{what}'s window ends before it starts")


def _when(moment: dt.datetime | None) -> Any:  # noqa: ANN401 - a datetime or UNSET
    return UNSET if moment is None else moment


def _copy_page[T, S](parsed: Any) -> CopyPage[T, S]:  # noqa: ANN401 - a generated page model
    page: Page[T] = page_of(parsed)
    stats = getattr(parsed, "stats", None)
    return CopyPage(
        items=page.items,
        next_cursor=page.next_cursor,
        returned=page.returned,
        source=page.source,
        stats=None if stats is UNSET else stats,
    )


class Copy:
    """Copy Trading for this key's tenant: ``client.copy``."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    # ----------------------------------------------------------------------------- leaders

    async def create_leader(  # noqa: PLR0913 - a leader's every setting
        self,
        *,
        source: LeaderSourceName,
        signal_lifetime_s: int,
        idempotency_key: str,
        account_id: Id | None = None,
        filters: Setting | None = None,
        copies: Setting | None = None,
        limits: Setting | None = None,
        who_may_join: Setting | None = None,
    ) -> CopyLeader:
        """Make one of your accounts (``source="account"`` with ``account_id``), or an external
        signal source (``source="external"``), a leader.

        ``signal_lifetime_s`` (1 to 3600) is how long a signal may still be copied after MFX Hub
        makes it; a follower that cannot act in time logs ``signal_expired``. An account leads
        once: a second live leader on it is a ``ConflictError`` (``account_already_leads``). Over
        the plan's leaders is a ``ConflictError`` with ``code == "quota_exceeded"``
        (``details["reason"] == "plan_limit"``).

        Args:
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _body(
            CopyLeaderCreate,
            "create_leader",
            {
                "source": source,
                "signal_lifetime_s": signal_lifetime_s,
                "account_id": _given(account_id),
                "filters": _given(filters),
                "copies": _given(copies),
                "limits": _given(limits),
                "who_may_join": _given(who_may_join),
            },
        )
        leader = await self._client.write(
            lambda: _create_leader.asyncio_detailed(
                client=self._client.generated, body=body, idempotency_key=idempotency_key
            ),
            "POST /copy/leaders",
        )
        return leader  # type: ignore[no-any-return]

    async def get_leader(self, leader_id: Id) -> CopyLeader:
        """One leader; another tenant's id is a ``NotFoundError``.

        Args:
            leader_id: The leader to act on.
        """
        leader = await self._client.read(
            lambda: _get_leader.asyncio_detailed(
                id=_uuid(leader_id), client=self._client.generated
            ),
            f"GET /copy/leaders/{leader_id}",
        )
        return leader  # type: ignore[no-any-return]

    async def leaders(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        state: LeaderStateName | Sequence[LeaderStateName] | None = None,
        source: LeaderSourceName | None = None,
        account_id: Id | None = None,
    ) -> CopyPage[CopyLeader, CopyLeaderPageStats]:
        """One page of your leaders, newest first, with the count of each state in ``stats``.

        ``state`` is one state or several (sent comma-separated, checked here); every filter
        narrows the list on the platform before the page is cut.

        Args:
            cursor: Where to continue from: the previous page's ``next_cursor``.
            limit: How many to return at most, on one page.
        """
        states = states_param(state, CopyLeaderState)
        sources = CopyLeaderSource(source) if source is not None else UNSET
        parsed = await self._client.read(
            lambda: _list_leaders.asyncio_detailed(
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                state=states,
                source=sources,
                account_id=_opt_uuid(account_id),
            ),
            "GET /copy/leaders",
        )
        return _copy_page(parsed)

    async def all_leaders(
        self,
        *,
        limit: int | None = None,
        state: LeaderStateName | Sequence[LeaderStateName] | None = None,
        source: LeaderSourceName | None = None,
        account_id: Id | None = None,
    ) -> AsyncIterator[CopyLeader]:
        """Every leader, following the cursor, narrowed as :meth:`leaders` is.

        Args:
            limit: How many to return at most, on one page.
        """
        cursor: str | None = None
        while True:
            page = await self.leaders(
                cursor=cursor, limit=limit, state=state, source=source, account_id=account_id
            )
            for leader in page.items:
                yield leader
            if not page.next_cursor:
                return
            cursor = page.next_cursor

    async def update_leader(  # noqa: PLR0913 - every field a leader's change can carry
        self,
        leader_id: Id,
        *,
        idempotency_key: str,
        filters: Setting | None = None,
        copies: Setting | None = None,
        signal_lifetime_s: int | None = None,
        limits: Setting | None = None,
        who_may_join: Setting | None = None,
    ) -> CopyLeader:
        """Change what a leader's followers receive; only the fields given are sent and change.

        Applies to the leader's next deal. A retired leader is a ``StateError``. Narrowing
        ``who_may_join`` does not end a follow already made.

        Args:
            leader_id: The leader to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _body(
            CopyLeaderUpdate,
            "update_leader",
            {
                "filters": _given(filters),
                "copies": _given(copies),
                "signal_lifetime_s": _given(signal_lifetime_s),
                "limits": _given(limits),
                "who_may_join": _given(who_may_join),
            },
        )
        leader = await self._client.write(
            lambda: _update_leader.asyncio_detailed(
                id=_uuid(leader_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"PATCH /copy/leaders/{leader_id}",
        )
        return leader  # type: ignore[no-any-return]

    async def pause_leader(self, leader_id: Id, *, idempotency_key: str) -> CopyLeader:
        """Stop copying the leader's new entries; its closes and stop changes are still copied.

        Each follower's entry is logged ``refused`` with reason ``paused``. A paused leader is
        answered as it is; a retired one is a ``StateError``.

        Args:
            leader_id: The leader to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        leader = await self._client.write(
            lambda: _pause_leader.asyncio_detailed(
                id=_uuid(leader_id),
                client=self._client.generated,
                idempotency_key=idempotency_key,
            ),
            f"POST /copy/leaders/{leader_id}/pause",
        )
        return leader  # type: ignore[no-any-return]

    async def resume_leader(self, leader_id: Id, *, idempotency_key: str) -> CopyLeader:
        """Copy the leader's entries again, from its next deal; deals made while paused are not
        copied afterwards.

        Args:
            leader_id: The leader to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        leader = await self._client.write(
            lambda: _resume_leader.asyncio_detailed(
                id=_uuid(leader_id),
                client=self._client.generated,
                idempotency_key=idempotency_key,
            ),
            f"POST /copy/leaders/{leader_id}/resume",
        )
        return leader  # type: ignore[no-any-return]

    async def retire_leader(
        self, leader_id: Id, *, close_copied: bool, reason: str, idempotency_key: str
    ) -> CopyLeader:
        """Retire a leader: every follow of it ends (``unfollowed``, ``why: leader_retired``).

        With ``close_copied`` each follower's volume copied from this leader is closed, never the
        account's own positions; without it the copied positions stay open. Retired is final.
        ``close_copied`` has no default: closing positions is a choice the caller makes.

        The retire is final when this returns. Each follower's close is a requested close
        (``cause`` ``leader_retired``), all under one ``batch_id``: :meth:`closes` with
        ``leader_id`` follows them, and each is final when ``done`` or ``incomplete``, with one
        ``copy.closed`` event each.

        Args:
            reason: Your own words, recorded with the action.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _body(
            CopyLeaderRetire, "retire_leader", {"close_copied": close_copied, "reason": reason}
        )
        leader = await self._client.write(
            lambda: _retire_leader.asyncio_detailed(
                id=_uuid(leader_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"POST /copy/leaders/{leader_id}/retire",
        )
        return leader  # type: ignore[no-any-return]

    async def send_open_signal(  # noqa: PLR0913 - an open signal's every field
        self,
        leader_id: Id,
        *,
        id_: str,
        symbol: str,
        side: Literal["buy", "sell"],
        idempotency_key: str,
        volume: Amount | None = None,
        units: Amount | None = None,
        instrument_key: str | None = None,
        sl: Amount | None = None,
        tp: Amount | None = None,
        time: dt.datetime | None = None,
        account: Setting | None = None,
    ) -> CopySignalAccepted:
        """An external leader opens a position (a market entry), copied to its followers.

        ``id_`` is your id for the signal (the contract's ``id``), unique for the leader; a close
        names it. Exactly one of ``volume`` (lots of the catalogue's standard contract) and
        ``units`` (base units) is given; both or neither is a ``ValueError`` here. An ``id_`` sent
        before is answered with the original signal and ``duplicate`` true, whatever the
        idempotency key; nothing is copied twice. A leader that is not external is a
        ``StateError`` (``leader_not_external``).

        Args:
            leader_id: The leader to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        # DECISION: both or neither of volume and units is refused here, before the wire: the
        # contract answers it 422 volume_or_units, and an SDK refuses what it can see is wrong.
        if (volume is None) == (units is None):
            raise ValueError("send_open_signal takes exactly one of volume and units")
        body = _body(
            CopyExternalOpen,
            "send_open_signal",
            {
                "id": id_,
                "symbol": symbol,
                "side": side,
                "volume": _OMIT if volume is None else _decimal("volume", volume),
                "units": _OMIT if units is None else _decimal("units", units),
                "instrument_key": _given(instrument_key),
                "sl": _OMIT if sl is None else _signed_decimal("sl", sl),
                "tp": _OMIT if tp is None else _signed_decimal("tp", tp),
                "time": _given(time),
                "account": _given(account),
            },
        )
        return await self._signal(leader_id, body, idempotency_key)

    async def send_close_signal(
        self,
        leader_id: Id,
        *,
        id_: str,
        close: str,
        idempotency_key: str,
        time: dt.datetime | None = None,
    ) -> CopySignalAccepted:
        """An external leader closes the position an earlier open made: ``close`` is that open's
        ``id_``. Every follower closes what it copied from it. ``id_`` is this signal's own id.

        Args:
            leader_id: The leader to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _body(
            CopyExternalClose,
            "send_close_signal",
            {"id": id_, "close": close, "time": _given(time)},
        )
        return await self._signal(leader_id, body, idempotency_key)

    async def _signal(
        self, leader_id: Id, body: CopyExternalOpen | CopyExternalClose, idempotency_key: str
    ) -> CopySignalAccepted:
        accepted = await self._client.write(
            lambda: _send_signal.asyncio_detailed(
                id=_uuid(leader_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"POST /copy/leaders/{leader_id}/signals",
        )
        return accepted  # type: ignore[no-any-return]

    # --------------------------------------------------------------------------- followers

    async def create_follower(  # noqa: PLR0913 - a follower's every setting
        self,
        *,
        account_id: Id,
        leader_id: Id,
        idempotency_key: str,
        scaling: Setting | None = None,
        bounds: Setting | None = None,
        symbol_map: Mapping[str, str] | None = None,
        options: Setting | None = None,
        risk_limits: Setting | None = None,
        close_on_stopout: bool | None = None,
        group_id: Id | None = None,
    ) -> CopyFollower:
        """Make one of your accounts follow a leader, with its own scaling and limits.

        ``scaling`` is required unless ``group_id`` names a group whose template has it. The follow
        is checked once, here, against the account's venue: an option the venue cannot honour is
        a ``ValidationError`` with ``details["reason"] == "not_on_this_venue"``. Use
        :meth:`preview_follower` first to see each symbol's match and volume.

        Args:
            account_id: The trading account to act on. Another tenant's id answers 404, never 403.
            leader_id: The leader to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _body(
            CopyFollowerCreate,
            "create_follower",
            {
                "account_id": account_id,
                "leader_id": leader_id,
                "scaling": _given(scaling),
                "bounds": _given(bounds),
                "symbol_map": _given(symbol_map),
                "options": _given(options),
                "risk_limits": _given(risk_limits),
                "close_on_stopout": _given(close_on_stopout),
                "group_id": _given(group_id),
            },
        )
        follower = await self._client.write(
            lambda: _create_follower.asyncio_detailed(
                client=self._client.generated, body=body, idempotency_key=idempotency_key
            ),
            "POST /copy/followers",
        )
        return follower  # type: ignore[no-any-return]

    async def preview_follower(  # noqa: PLR0913 - a follow's settings and the rows to try
        self,
        *,
        account_id: Id,
        leader_id: Id,
        scaling: Setting,
        rows: Sequence[Setting],
        bounds: Setting | None = None,
        symbol_map: Mapping[str, str] | None = None,
        options: Setting | None = None,
    ) -> CopyPreview:
        """What a follow would do before it is made: for each row (a leader ``symbol`` and
        ``volume``), the follower symbol, how it was matched and the follower's volume, or the
        reason it would be refused. ``refusal`` says when the follow itself would be refused.

        Read-only (``copy:read``): nothing is created and no idempotency key is taken. 1 to 200
        rows.

        Args:
            account_id: The trading account to act on. Another tenant's id answers 404, never 403.
            leader_id: The leader to act on.
        """
        if not rows:
            raise ValueError("preview_follower needs at least one row")
        body = _body(
            CopyPreviewRequest,
            "preview_follower",
            {
                "account_id": account_id,
                "leader_id": leader_id,
                "scaling": scaling,
                "rows": list(rows),
                "bounds": _given(bounds),
                "symbol_map": _given(symbol_map),
                "options": _given(options),
            },
        )
        # DECISION: a preview creates nothing, so it is sent as a read: retried after a 429 as
        # every read is, and never given an idempotency key the contract does not take.
        preview = await self._client.read(
            lambda: _preview_follower.asyncio_detailed(client=self._client.generated, body=body),
            "POST /copy/followers/preview",
        )
        return preview  # type: ignore[no-any-return]

    async def get_follower(self, follower_id: Id) -> CopyFollower:
        """One follower: its mandate and version, its state and the stop-outs in force.

        Args:
            follower_id: The follower to act on.
        """
        follower = await self._client.read(
            lambda: _get_follower.asyncio_detailed(
                id=_uuid(follower_id), client=self._client.generated
            ),
            f"GET /copy/followers/{follower_id}",
        )
        return follower  # type: ignore[no-any-return]

    async def followers(  # noqa: PLR0913 - the page, its five filters and the order
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        state: FollowerStateName | Sequence[FollowerStateName] | None = None,
        leader_id: Id | None = None,
        account_id: Id | None = None,
        group_id: Id | None = None,
        out_of_step: bool | None = None,
        sort: NewestOrOldest = "newest",
    ) -> CopyPage[CopyFollower, CopyFollowerPageStats]:
        """One page of your followers, newest first (``sort="oldest"`` the other way), with the
        count of each state, and of those out of step, in ``stats``.

        A group's followers are ``followers(group_id=...)``. ``out_of_step=True`` is the followers
        whose copy host does not hold their latest mandate. Each follower read carries what is
        live: ``drift``, ``limits_use``, ``today``, its ``exposure`` against its group's cap and
        its requested ``close``, each None when there is none.

        Args:
            cursor: Where to continue from: the previous page's ``next_cursor``.
            limit: How many to return at most, on one page.
        """
        states = states_param(state, CopyFollowerState)
        parsed = await self._client.read(
            lambda: _list_followers.asyncio_detailed(
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                state=states,
                leader_id=_opt_uuid(leader_id),
                account_id=_opt_uuid(account_id),
                group_id=_opt_uuid(group_id),
                sort=ListCopyFollowersSort(sort),
                out_of_step=UNSET if out_of_step is None else out_of_step,
            ),
            "GET /copy/followers",
        )
        return _copy_page(parsed)

    async def all_followers(  # noqa: PLR0913 - the filters and the order
        self,
        *,
        limit: int | None = None,
        state: FollowerStateName | Sequence[FollowerStateName] | None = None,
        leader_id: Id | None = None,
        account_id: Id | None = None,
        group_id: Id | None = None,
        out_of_step: bool | None = None,
        sort: NewestOrOldest = "newest",
    ) -> AsyncIterator[CopyFollower]:
        """Every follower, following the cursor, narrowed as :meth:`followers` is.

        Args:
            limit: How many to return at most, on one page.
        """
        cursor: str | None = None
        while True:
            page = await self.followers(
                cursor=cursor,
                limit=limit,
                state=state,
                leader_id=leader_id,
                account_id=account_id,
                group_id=group_id,
                out_of_step=out_of_step,
                sort=sort,
            )
            for follower in page.items:
                yield follower
            if not page.next_cursor:
                return
            cursor = page.next_cursor

    async def update_follower(  # noqa: PLR0913 - every field a follower's change can carry
        self,
        follower_id: Id,
        *,
        idempotency_key: str,
        scaling: Setting | None = None,
        bounds: Setting | None = None,
        symbol_map: Mapping[str, str] | None = None,
        options: Setting | None = None,
        risk_limits: Setting | None = None,
        close_on_stopout: bool | None = None,
    ) -> CopyFollower:
        """Change a follower's mandate; only the fields given are sent, and each change is a new
        ``mandate_version``. Checked as a follow is; an unfollowed follower is a ``StateError``.

        Args:
            follower_id: The follower to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _body(
            CopyFollowerUpdate,
            "update_follower",
            {
                "scaling": _given(scaling),
                "bounds": _given(bounds),
                "symbol_map": _given(symbol_map),
                "options": _given(options),
                "risk_limits": _given(risk_limits),
                "close_on_stopout": _given(close_on_stopout),
            },
        )
        follower = await self._client.write(
            lambda: _update_follower.asyncio_detailed(
                id=_uuid(follower_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"PATCH /copy/followers/{follower_id}",
        )
        return follower  # type: ignore[no-any-return]

    async def pause_follower(self, follower_id: Id, *, idempotency_key: str) -> CopyFollower:
        """Stop copying new entries to this follower; closes of what it copied still are.

        Args:
            follower_id: The follower to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        follower = await self._client.write(
            lambda: _pause_follower.asyncio_detailed(
                id=_uuid(follower_id),
                client=self._client.generated,
                idempotency_key=idempotency_key,
            ),
            f"POST /copy/followers/{follower_id}/pause",
        )
        return follower  # type: ignore[no-any-return]

    async def resume_follower(self, follower_id: Id, *, idempotency_key: str) -> CopyFollower:
        """Copy to this follower again from the leader's next deal; ``stopped_out`` while one of
        its stop-outs is still active (reset it to copy again).

        Args:
            follower_id: The follower to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        follower = await self._client.write(
            lambda: _resume_follower.asyncio_detailed(
                id=_uuid(follower_id),
                client=self._client.generated,
                idempotency_key=idempotency_key,
            ),
            f"POST /copy/followers/{follower_id}/resume",
        )
        return follower  # type: ignore[no-any-return]

    async def resync_follower(self, follower_id: Id, *, idempotency_key: str) -> CopyFollower:
        """Send the follower's mandate to its account's copy host again and heal its copied
        positions from the account. Nothing is traded; drift found is sent as ``copy.drift``.

        Args:
            follower_id: The follower to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        follower = await self._client.write(
            lambda: _resync_follower.asyncio_detailed(
                id=_uuid(follower_id),
                client=self._client.generated,
                idempotency_key=idempotency_key,
            ),
            f"POST /copy/followers/{follower_id}/resync",
        )
        return follower  # type: ignore[no-any-return]

    async def unfollow(
        self, follower_id: Id, *, close_copied: bool, idempotency_key: str
    ) -> CopyFollower:
        """End the follow (``unfollowed``, final). With ``close_copied`` the volume copied from
        this leader is closed, never the account's own; without it the copied positions stay open
        and are the account's own from then on. ``close_copied`` has no default.

        The follow is final when this returns. The close is a requested close, the answer's
        ``close``: final when ``done`` (every copied position closed or found closed) or
        ``incomplete`` (any not closed), with one ``copy.closed`` event; :meth:`get_close` has each
        position and attempt.

        Args:
            follower_id: The follower to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _body(CopyUnfollow, "unfollow", {"close_copied": close_copied})
        follower = await self._client.write(
            lambda: _unfollow.asyncio_detailed(
                id=_uuid(follower_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"POST /copy/followers/{follower_id}/unfollow",
        )
        return follower  # type: ignore[no-any-return]

    # --------------------------------------------------------------------------- stop-outs

    async def stopouts(
        self,
        follower_id: Id,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        state: StopoutStateName | Sequence[StopoutStateName] | None = None,
    ) -> Page[CopyStopout]:
        """One page of a follower's stop-outs, newest first: the limit reached, what was used,
        its period, what it closed and, once reset, who reset it and why.

        Args:
            follower_id: The follower to act on.
            cursor: Where to continue from: the previous page's ``next_cursor``.
            limit: How many to return at most, on one page.
        """
        states = states_param(state, CopyStopoutState)
        parsed = await self._client.read(
            lambda: _list_stopouts.asyncio_detailed(
                id=_uuid(follower_id),
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                state=states,
            ),
            f"GET /copy/followers/{follower_id}/stopouts",
        )
        return page_of(parsed)

    async def all_stopouts(
        self,
        follower_id: Id,
        *,
        limit: int | None = None,
        state: StopoutStateName | Sequence[StopoutStateName] | None = None,
    ) -> AsyncIterator[CopyStopout]:
        """Every stop-out of a follower, following the cursor; ``limit`` is the page size.

        Args:
            follower_id: The follower to act on.
        """
        cursor: str | None = None
        while True:
            page = await self.stopouts(follower_id, cursor=cursor, limit=limit, state=state)
            for stopout in page.items:
                yield stopout
            if not page.next_cursor:
                return
            cursor = page.next_cursor

    async def reset_stopouts(
        self,
        follower_id: Id,
        *,
        reason: str,
        idempotency_key: str,
        limit: LimitKindName | None = None,
    ) -> CopyFollower:
        """Reset a follower's active stop-outs before their period ends, or only the one for
        ``limit``. Positions a stop-out closed stay closed. No active stop-out is a ``StateError``
        (``no_active_stopout``).

        Args:
            follower_id: The follower to act on.
            reason: Your own words, recorded with the action.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _body(CopyStopoutReset, "reset_stopouts", {"reason": reason, "limit": _given(limit)})
        follower = await self._client.write(
            lambda: _reset_stopouts.asyncio_detailed(
                id=_uuid(follower_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"POST /copy/followers/{follower_id}/stopouts/reset",
        )
        return follower  # type: ignore[no-any-return]

    # ------------------------------------------------------------------------------ groups

    async def create_group(
        self,
        *,
        name: str,
        idempotency_key: str,
        template: Setting | None = None,
        gross_exposure_cap: Amount | None = None,
        placement_policy: str | None = None,
    ) -> CopyGroup:
        """A group of followers managed together under one template and one exposure cap
        (Enterprise; another plan is a ``ForbiddenError`` with ``details["part"] == "groups"``).

        ``gross_exposure_cap`` is in US dollars: each live member is signed an equal share of it,
        and its host refuses an open that would take it past its share. ``placement_policy`` is
        deprecated: it is stored and returned, and placement never reads it.

        Args:
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _body(
            CopyGroupCreate,
            "create_group",
            {
                "name": name,
                "template": _given(template),
                "gross_exposure_cap": (
                    _OMIT
                    if gross_exposure_cap is None
                    else _decimal("gross_exposure_cap", gross_exposure_cap)
                ),
                "placement_policy": _given(placement_policy),
            },
        )
        group = await self._client.write(
            lambda: _create_group.asyncio_detailed(
                client=self._client.generated, body=body, idempotency_key=idempotency_key
            ),
            "POST /copy/groups",
        )
        return group  # type: ignore[no-any-return]

    async def get_group(self, group_id: Id) -> CopyGroup:
        """One group, with its template, exposure cap and how many followers it has.

        Args:
            group_id: The group to act on.
        """
        group = await self._client.read(
            lambda: _get_group.asyncio_detailed(id=_uuid(group_id), client=self._client.generated),
            f"GET /copy/groups/{group_id}",
        )
        return group  # type: ignore[no-any-return]

    async def groups(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        state: GroupStateName | None = None,
    ) -> CopyPage[CopyGroup, CopyGroupPageStats]:
        """One page of your groups, newest first, with the count of each state in ``stats``.

        Args:
            cursor: Where to continue from: the previous page's ``next_cursor``.
            limit: How many to return at most, on one page.
        """
        states = CopyGroupState(state) if state is not None else UNSET
        parsed = await self._client.read(
            lambda: _list_groups.asyncio_detailed(
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                state=states,
            ),
            "GET /copy/groups",
        )
        return _copy_page(parsed)

    async def all_groups(
        self, *, limit: int | None = None, state: GroupStateName | None = None
    ) -> AsyncIterator[CopyGroup]:
        """Every group, following the cursor; ``limit`` is the page size."""
        cursor: str | None = None
        while True:
            page = await self.groups(cursor=cursor, limit=limit, state=state)
            for group in page.items:
                yield group
            if not page.next_cursor:
                return
            cursor = page.next_cursor

    async def update_group(  # noqa: PLR0913 - every field a group's change can carry
        self,
        group_id: Id,
        *,
        idempotency_key: str,
        name: str | None = None,
        template: Setting | None = None,
        gross_exposure_cap: Amount | None | _Omit = _OMIT,
        placement_policy: str | None | _Omit = _OMIT,
    ) -> CopyGroup:
        """Change a group's name, template, exposure cap or placement policy; only the fields
        given are sent. ``gross_exposure_cap=None`` and ``placement_policy=None`` clear them.

        A new template applies to followers created into the group afterwards;
        :meth:`rollover_group` sets it on the members already in it. ``placement_policy`` is
        deprecated: it is stored and returned, and placement never reads it.

        Args:
            group_id: The group to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        cap: Any = gross_exposure_cap
        if cap is not None and not isinstance(cap, _Omit):
            cap = _decimal("gross_exposure_cap", cap)
        body = _body(
            CopyGroupUpdate,
            "update_group",
            {
                "name": _given(name),
                "template": _given(template),
                "gross_exposure_cap": cap,
                "placement_policy": placement_policy,
            },
        )
        group = await self._client.write(
            lambda: _update_group.asyncio_detailed(
                id=_uuid(group_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"PATCH /copy/groups/{group_id}",
        )
        return group  # type: ignore[no-any-return]

    async def add_group_followers(
        self, group_id: Id, follower_ids: Sequence[Id], *, idempotency_key: str
    ) -> CopyGroupMembersResult:
        """Add followers to a group, 1 to 500 at once; each follower's outcome is answered apart
        (one in another group is refused ``in_another_group``). Mandates are not changed.

        Args:
            group_id: The group to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = self._members("add_group_followers", follower_ids)
        result = await self._client.write(
            lambda: _add_group_followers.asyncio_detailed(
                id=_uuid(group_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"POST /copy/groups/{group_id}/followers",
        )
        return result  # type: ignore[no-any-return]

    async def remove_group_followers(
        self, group_id: Id, follower_ids: Sequence[Id], *, idempotency_key: str
    ) -> CopyGroupMembersResult:
        """Take followers out of a group; they keep following with their own mandates.

        Args:
            group_id: The group to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = self._members("remove_group_followers", follower_ids)
        result = await self._client.write(
            lambda: _remove_group_followers.asyncio_detailed(
                id=_uuid(group_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"POST /copy/groups/{group_id}/followers/remove",
        )
        return result  # type: ignore[no-any-return]

    @staticmethod
    def _members(name: str, follower_ids: Sequence[Id]) -> CopyGroupMembers:
        ids = [str(_uuid(i)) for i in follower_ids]
        if not 1 <= len(ids) <= _MEMBERS_MAX:
            raise ValueError(f"{name} takes 1 to {_MEMBERS_MAX} follower ids, not {len(ids)}")
        return _body(CopyGroupMembers, name, {"follower_ids": ids})

    async def pause_group(self, group_id: Id, *, idempotency_key: str) -> CopyGroup:
        """Stop copying new entries to every follower of the group; closes still are. Each
        follower keeps its own state, so resuming restores each one as it was.

        Args:
            group_id: The group to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        group = await self._client.write(
            lambda: _pause_group.asyncio_detailed(
                id=_uuid(group_id), client=self._client.generated, idempotency_key=idempotency_key
            ),
            f"POST /copy/groups/{group_id}/pause",
        )
        return group  # type: ignore[no-any-return]

    async def resume_group(self, group_id: Id, *, idempotency_key: str) -> CopyGroup:
        """Copy to the group's followers again, from the leader's next deal.

        Args:
            group_id: The group to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        group = await self._client.write(
            lambda: _resume_group.asyncio_detailed(
                id=_uuid(group_id), client=self._client.generated, idempotency_key=idempotency_key
            ),
            f"POST /copy/groups/{group_id}/resume",
        )
        return group  # type: ignore[no-any-return]

    async def close_group(
        self, group_id: Id, *, reason: str, pause: bool, idempotency_key: str
    ) -> CopyGroupCloseResult:
        """Close the copied positions of every live member of the group (Enterprise); the follows
        are kept.

        Each member that has not unfollowed gets one requested close (``cause`` ``group_close``),
        all under one ``batch_id``, covering what was copied from leader deals signalled up to
        now; only copied volume is closed, never the account's own. ``pause`` has no default:
        ``True`` pauses the group in the same act, ``False`` leaves its state, and later deals are
        copied again. :meth:`closes` with ``batch_id`` follows the progress.

        Args:
            group_id: The group to act on.
            reason: Your own words, recorded with the action.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _body(CopyGroupClose, "close_group", {"reason": reason, "pause": pause})
        result = await self._client.write(
            lambda: _close_group.asyncio_detailed(
                id=_uuid(group_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"POST /copy/groups/{group_id}/close",
        )
        return result  # type: ignore[no-any-return]

    async def rollover_group(  # noqa: PLR0913 - the run, its fields and its page
        self,
        group_id: Id,
        *,
        dry_run: bool,
        fields: Sequence[RolloverField] | None = None,
        after: Id | None = None,
        limit: int | None = None,
        idempotency_key: str | None = None,
    ) -> CopyGroupRolloverResult:
        """Set the group's template on its live members, or with ``dry_run=True`` see what it
        would change (Enterprise).

        Each member, in id order after ``after``, at most ``limit`` (1 to 500), has each field in
        ``fields`` (by default every field the template sets) set to the template's, and is
        answered ``changed`` (each field's ``from`` and ``to``), ``unchanged`` or ``refused`` with
        the reason. ``next_after`` continues with the next page, None after the last. A dry run
        changes nothing and sends no key; an applied rollover needs ``idempotency_key``.

        Args:
            group_id: The group to act on.
        """
        # DECISION: the contract requires the key unless dry_run is true (400 without it), and a
        # dry run needs none. The SDK checks both here, before anything is sent, as it checks
        # every other argument.
        if not dry_run and idempotency_key is None:
            raise ValueError("an applied rollover_group (dry_run=False) needs an idempotency_key")
        if dry_run and idempotency_key is not None:
            raise ValueError("a dry run of rollover_group changes nothing and takes no key")
        body = _body(
            CopyGroupRollover,
            "rollover_group",
            {
                "dry_run": dry_run,
                "fields": _OMIT if fields is None else list(fields),
                "after": _OMIT if after is None else _uuid(after),
                "limit": _given(limit),
            },
        )
        if fields is None:
            # The generated model reads an absent list as an empty one, and an empty `fields` is
            # not "every field the template sets": it is refused (minItems 1). Absent stays absent.
            body.fields = UNSET
        result = await self._client.write(
            lambda: _rollover_group.asyncio_detailed(
                id=_uuid(group_id),
                client=self._client.generated,
                body=body,
                idempotency_key=UNSET if idempotency_key is None else idempotency_key,
            ),
            f"POST /copy/groups/{group_id}/rollover",
        )
        return result  # type: ignore[no-any-return]

    # ---------------------------------------------------------------------- requested closes

    async def closes(  # noqa: PLR0913 - the page, five filters and the window
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        follower_id: Id | None = None,
        leader_id: Id | None = None,
        group_id: Id | None = None,
        batch_id: Id | None = None,
        state: CloseStateName | Sequence[CloseStateName] | None = None,
        from_: dt.datetime | None = None,
        to: dt.datetime | None = None,
    ) -> CopyPage[CopyClose, CopyClosePageStats]:
        """One page of your requested closes of copied positions, newest first, with a count of
        each state in ``stats``: each an unfollow or a retire with ``close_copied``, or a group's
        close, asked. A retire's or a group close's closes share one ``batch_id``.

        ``state`` is one state or several (sent comma-separated, checked here). The window is
        ``from_`` to ``to`` on when the close was asked, at most 31 days; without ``from_`` it is
        the last 24 hours. Each end is an aware datetime.

        Args:
            cursor: Where to continue from: the previous page's ``next_cursor``.
            limit: How many to return at most, on one page.
        """
        _window("the closes", from_, to)
        states = states_param(state, CopyCloseState)
        parsed = await self._client.read(
            lambda: _list_closes.asyncio_detailed(
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                follower_id=_opt_uuid(follower_id),
                leader_id=_opt_uuid(leader_id),
                group_id=_opt_uuid(group_id),
                batch_id=_opt_uuid(batch_id),
                state=states,
                from_=_when(from_),
                to=_when(to),
            ),
            "GET /copy/closes",
        )
        return _copy_page(parsed)

    async def all_closes(  # noqa: PLR0913 - the filters and the window
        self,
        *,
        limit: int | None = None,
        follower_id: Id | None = None,
        leader_id: Id | None = None,
        group_id: Id | None = None,
        batch_id: Id | None = None,
        state: CloseStateName | Sequence[CloseStateName] | None = None,
        from_: dt.datetime | None = None,
        to: dt.datetime | None = None,
    ) -> AsyncIterator[CopyClose]:
        """Every requested close the filters and window match, following the cursor.

        Args:
            limit: How many to return at most, on one page.
        """
        cursor: str | None = None
        while True:
            page = await self.closes(
                cursor=cursor,
                limit=limit,
                follower_id=follower_id,
                leader_id=leader_id,
                group_id=group_id,
                batch_id=batch_id,
                state=state,
                from_=from_,
                to=to,
            )
            for close in page.items:
                yield close
            if not page.next_cursor:
                return
            cursor = page.next_cursor

    async def get_close(self, close_id: Id) -> CopyClose:
        """One requested close: each copied position it covers and each attempt to close it.
        Another tenant's close is a ``NotFoundError``."""
        close = await self._client.read(
            lambda: _get_close.asyncio_detailed(id=_uuid(close_id), client=self._client.generated),
            f"GET /copy/closes/{close_id}",
        )
        return close  # type: ignore[no-any-return]

    # ----------------------------------------------------------------------------- the log

    async def log(  # noqa: PLR0913 - the page, seven filters, the window and the order
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        leader_id: Id | None = None,
        follower_id: Id | None = None,
        account_id: Id | None = None,
        group_id: Id | None = None,
        signal_id: Id | None = None,
        outcome: CopyOutcomeName | Sequence[CopyOutcomeName] | None = None,
        reason: RefusalReason | Sequence[RefusalReason] | None = None,
        venue: Literal["mt5", "ctrader"] | Sequence[Literal["mt5", "ctrader"]] | None = None,
        from_: dt.datetime | None = None,
        to: dt.datetime | None = None,
        sort: CopyLogSort | None = None,
    ) -> CopyPage[CopyLogEntry, CopyLogPageStats]:
        """One page of the copy log: one row a follower a signal, with its outcome, reason, the
        command it became and MFX Hub's stage timings in milliseconds.

        Newest first, or ``sort="mfx_ms"`` for the slowest of MFX Hub's part first. ``outcome``,
        ``reason`` and ``venue`` are one value or several (sent comma-separated, each checked
        here: a reason outside :data:`REFUSAL_REASONS` is a ``ValueError``). The window is
        ``from_`` to ``to``, at most 31 days (wider is a ``ValidationError``, ``window_too_wide``);
        without ``from_`` it is the last 24 hours. Each is an aware datetime; a naive one is a
        ``ValueError``, as is a window that ends before it starts. ``stats`` is over the whole
        filtered window. ``group_id`` is the group's followers now.

        Each row names the leader's ``deal``, the follower's ``symbol`` and, when Risk Management
        refused the copy, ``risk``: the rule, the policy or challenge with its version, and the
        figures, as text.

        Args:
            cursor: Where to continue from: the previous page's ``next_cursor``.
            limit: How many to return at most, on one page.
        """
        _window("the copy log", from_, to)
        outcomes = states_param(outcome, CopyOutcome)
        reasons = states_param(reason, CopyReason)
        venues = states_param(venue, Venue)
        order = ListCopyLogSort(sort) if sort is not None else UNSET
        parsed = await self._client.read(
            lambda: _list_log.asyncio_detailed(
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                leader_id=_opt_uuid(leader_id),
                follower_id=_opt_uuid(follower_id),
                account_id=_opt_uuid(account_id),
                group_id=_opt_uuid(group_id),
                signal_id=_opt_uuid(signal_id),
                outcome=outcomes,
                reason=reasons,
                venue=venues,
                from_=from_ if from_ is not None else UNSET,
                to=to if to is not None else UNSET,
                sort=order,
            ),
            "GET /copy/log",
        )
        return _copy_page(parsed)

    async def all_log(  # noqa: PLR0913 - the filters, the window and the order
        self,
        *,
        limit: int | None = None,
        leader_id: Id | None = None,
        follower_id: Id | None = None,
        account_id: Id | None = None,
        group_id: Id | None = None,
        signal_id: Id | None = None,
        outcome: CopyOutcomeName | Sequence[CopyOutcomeName] | None = None,
        reason: RefusalReason | Sequence[RefusalReason] | None = None,
        venue: Literal["mt5", "ctrader"] | Sequence[Literal["mt5", "ctrader"]] | None = None,
        from_: dt.datetime | None = None,
        to: dt.datetime | None = None,
        sort: CopyLogSort | None = None,
    ) -> AsyncIterator[CopyLogEntry]:
        """Every row of the copy log the filters and window match, following the cursor.

        Args:
            limit: How many to return at most, on one page.
        """
        cursor: str | None = None
        while True:
            page = await self.log(
                cursor=cursor,
                limit=limit,
                leader_id=leader_id,
                follower_id=follower_id,
                account_id=account_id,
                group_id=group_id,
                signal_id=signal_id,
                outcome=outcome,
                reason=reason,
                venue=venue,
                from_=from_,
                to=to,
                sort=sort,
            )
            for row in page.items:
                yield row
            if not page.next_cursor:
                return
            cursor = page.next_cursor

    # ------------------------------------------------------------ signals and every stop-out

    async def signals(  # noqa: PLR0913 - the page, three filters and the window
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        leader_id: Id | None = None,
        kind: SignalKindName | Sequence[SignalKindName] | None = None,
        action: SignalActionName | Sequence[SignalActionName] | None = None,
        from_: dt.datetime | None = None,
        to: dt.datetime | None = None,
    ) -> CopyPage[CopySignalEntry, CopySignalPageStats]:
        """One page of your leaders' signals, newest first, each with ``outcomes``: how many of
        its own copies were filled, refused and skipped. ``stats`` counts every signal the window
        and filters match, by kind.

        ``kind`` and ``action`` are one value or several (sent comma-separated, checked here). The
        window is ``from_`` to ``to``, at most 31 days; without ``from_`` it is the last 24 hours.

        Args:
            cursor: Where to continue from: the previous page's ``next_cursor``.
            limit: How many to return at most, on one page.
        """
        _window("the signals", from_, to)
        kinds = states_param(kind, ListCopySignalsKindItem)
        actions = states_param(action, ListCopySignalsActionItem)
        parsed = await self._client.read(
            lambda: _list_signals.asyncio_detailed(
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                from_=_when(from_),
                to=_when(to),
                leader_id=_opt_uuid(leader_id),
                kind=kinds,
                action=actions,
            ),
            "GET /copy/signals",
        )
        return _copy_page(parsed)

    async def all_signals(  # noqa: PLR0913 - the filters and the window
        self,
        *,
        limit: int | None = None,
        leader_id: Id | None = None,
        kind: SignalKindName | Sequence[SignalKindName] | None = None,
        action: SignalActionName | Sequence[SignalActionName] | None = None,
        from_: dt.datetime | None = None,
        to: dt.datetime | None = None,
    ) -> AsyncIterator[CopySignalEntry]:
        """Every signal the filters and window match, following the cursor.

        Args:
            limit: How many to return at most, on one page.
        """
        cursor: str | None = None
        while True:
            page = await self.signals(
                cursor=cursor,
                limit=limit,
                leader_id=leader_id,
                kind=kind,
                action=action,
                from_=from_,
                to=to,
            )
            for signal in page.items:
                yield signal
            if not page.next_cursor:
                return
            cursor = page.next_cursor

    async def tenant_stopouts(  # noqa: PLR0913 - the page, three filters and the window
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        state: StopoutStateName | Sequence[StopoutStateName] | None = None,
        follower_id: Id | None = None,
        group_id: Id | None = None,
        from_: dt.datetime | None = None,
        to: dt.datetime | None = None,
    ) -> CopyPage[CopyStopout, CopyTenantStopoutPageStats]:
        """One page of every stop-out of your followers, newest first, with a count of each state
        in ``stats``. ``group_id`` is the group's followers now.

        The window is ``from_`` to ``to`` on each stop-out's ``created_at``, at most 31 days;
        without ``from_`` it is the last 24 hours. One follower's are also :meth:`stopouts`.

        Args:
            cursor: Where to continue from: the previous page's ``next_cursor``.
            limit: How many to return at most, on one page.
        """
        _window("the stop-outs", from_, to)
        states = states_param(state, CopyStopoutState)
        parsed = await self._client.read(
            lambda: _list_tenant_stopouts.asyncio_detailed(
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                from_=_when(from_),
                to=_when(to),
                state=states,
                follower_id=_opt_uuid(follower_id),
                group_id=_opt_uuid(group_id),
            ),
            "GET /copy/stopouts",
        )
        return _copy_page(parsed)

    async def all_tenant_stopouts(  # noqa: PLR0913 - the filters and the window
        self,
        *,
        limit: int | None = None,
        state: StopoutStateName | Sequence[StopoutStateName] | None = None,
        follower_id: Id | None = None,
        group_id: Id | None = None,
        from_: dt.datetime | None = None,
        to: dt.datetime | None = None,
    ) -> AsyncIterator[CopyStopout]:
        """Every stop-out the filters and window match, following the cursor.

        Args:
            limit: How many to return at most, on one page.
        """
        cursor: str | None = None
        while True:
            page = await self.tenant_stopouts(
                cursor=cursor,
                limit=limit,
                state=state,
                follower_id=follower_id,
                group_id=group_id,
                from_=from_,
                to=to,
            )
            for stopout in page.items:
                yield stopout
            if not page.next_cursor:
                return
            cursor = page.next_cursor

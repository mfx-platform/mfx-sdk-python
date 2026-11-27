"""``client.risk`` — Risk Management: account rules, the trade planner, exit plans and challenges.

The rules, thresholds and actions are yours. MFX Hub runs them on the account's own numbers and
says what it did and why:

* **Policies** (``risk:write``; relaxing one needs ``risk:override`` and a reason): versioned rule
  sets - daily loss, drawdown, exposure, loss at stops, a schedule - put in force on accounts.
* **Accounts**: each protected account's figures, coverage and restriction; what a "close all
  positions" action would close now; clearing a breach (``risk:override``).
* **The planner**: size a trade from a risk budget and check it against every rule, before
  anything is sent.
* **Exit plans**: steps on a position (move the stop, close part, trail), held by the broker or by
  MFX Hub.
* **Challenges**: one versioned rule set over many accounts, each passing or failing on its own.
* **Activity**: every warning, breach, action and change, unresolved first.

A new entry that breaks a rule in force is refused with :class:`mfx.errors.RiskRefusedError`,
whose ``refusal`` names the rule, the figure used, its limit and what the entry would have made it.
Closes, partial closes and cancels are never refused.

Bodies (rules, steps, orders) are given as the generated models or as plain mappings in the
contract's shape; decimals are strings, always::

    policy = await client.risk.create_policy(
        "Funded account",
        {"daily_loss": {"limit": {"pct": "5"}, "basis": "start_balance",
                        "actions": {"kinds": ["notify", "block_entries"]}}},
        reset={"zone": "broker"},
        idempotency_key="policy-1",
    )
    await client.risk.activate(policy.id, [account_id], version=1, idempotency_key="act-1")

Lists come two ways: ``*_page`` returns one page with its ``stats`` for the filtered set, and the
plural name follows the cursor to the end. A cursor belongs to the sort it was issued for.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import AsyncIterator, Awaitable, Callable, Mapping, Sequence
from decimal import Decimal
from enum import Enum
from functools import partial
from typing import TYPE_CHECKING, Any, Literal
from uuid import UUID

from mfx._generated.api.risk import activate_risk_policy as _activate
from mfx._generated.api.risk import amend_risk_plan as _amend_plan
from mfx._generated.api.risk import archive_risk_challenge as _archive_challenge
from mfx._generated.api.risk import archive_risk_policy as _archive
from mfx._generated.api.risk import check_risk_order as _check
from mfx._generated.api.risk import clear_risk_breach as _clear
from mfx._generated.api.risk import create_risk_challenge as _create_challenge
from mfx._generated.api.risk import create_risk_challenge_version as _challenge_version
from mfx._generated.api.risk import create_risk_plan as _create_plan
from mfx._generated.api.risk import create_risk_policy as _create_policy
from mfx._generated.api.risk import create_risk_policy_version as _policy_version
from mfx._generated.api.risk import deactivate_risk_account as _deactivate
from mfx._generated.api.risk import end_risk_plan as _end_plan
from mfx._generated.api.risk import enrol_risk_challenge_accounts as _enrol
from mfx._generated.api.risk import get_risk_account as _get_account
from mfx._generated.api.risk import get_risk_account_close_scope as _close_scope
from mfx._generated.api.risk import get_risk_challenge as _get_challenge
from mfx._generated.api.risk import get_risk_challenge_account as _get_enrolled
from mfx._generated.api.risk import get_risk_coverage as _coverage
from mfx._generated.api.risk import get_risk_equity as _equity
from mfx._generated.api.risk import get_risk_plan as _get_plan
from mfx._generated.api.risk import get_risk_policy as _get_policy
from mfx._generated.api.risk import get_risk_policy_version as _get_policy_version
from mfx._generated.api.risk import list_risk_accounts as _list_accounts
from mfx._generated.api.risk import list_risk_activity as _list_activity
from mfx._generated.api.risk import list_risk_challenge_accounts as _list_enrolled
from mfx._generated.api.risk import list_risk_challenges as _list_challenges
from mfx._generated.api.risk import list_risk_plans as _list_plans
from mfx._generated.api.risk import list_risk_policies as _list_policies
from mfx._generated.api.risk import list_risk_policy_versions as _list_policy_versions
from mfx._generated.api.risk import pause_risk_plan as _pause_plan
from mfx._generated.api.risk import preview_risk_plan as _preview
from mfx._generated.api.risk import resume_risk_plan as _resume_plan
from mfx._generated.models.get_risk_account_close_scope_scope import (
    GetRiskAccountCloseScopeScope,
)
from mfx._generated.models.list_risk_accounts_coverage_item import ListRiskAccountsCoverageItem
from mfx._generated.models.list_risk_accounts_restriction_item import (
    ListRiskAccountsRestrictionItem,
)
from mfx._generated.models.list_risk_accounts_sort import ListRiskAccountsSort
from mfx._generated.models.list_risk_activity_sort import ListRiskActivitySort
from mfx._generated.models.list_risk_challenge_accounts_rule_item import (
    ListRiskChallengeAccountsRuleItem,
)
from mfx._generated.models.list_risk_challenge_accounts_sort import ListRiskChallengeAccountsSort
from mfx._generated.models.list_risk_challenge_accounts_state_item import (
    ListRiskChallengeAccountsStateItem,
)
from mfx._generated.models.list_risk_plans_sort import ListRiskPlansSort
from mfx._generated.models.list_risk_plans_state_item import ListRiskPlansStateItem
from mfx._generated.models.list_risk_policies_sort import ListRiskPoliciesSort
from mfx._generated.models.list_risk_policies_state import ListRiskPoliciesState
from mfx._generated.models.risk_activate import RiskActivate
from mfx._generated.models.risk_activity_kind import RiskActivityKind
from mfx._generated.models.risk_challenge_create import RiskChallengeCreate
from mfx._generated.models.risk_challenge_rules import RiskChallengeRules
from mfx._generated.models.risk_check_request import RiskCheckRequest
from mfx._generated.models.risk_clear import RiskClear
from mfx._generated.models.risk_enrol import RiskEnrol
from mfx._generated.models.risk_outcome import RiskOutcome
from mfx._generated.models.risk_plan_amend import RiskPlanAmend
from mfx._generated.models.risk_plan_create import RiskPlanCreate
from mfx._generated.models.risk_policy_create import RiskPolicyCreate
from mfx._generated.models.risk_policy_version_create import RiskPolicyVersionCreate
from mfx._generated.models.risk_preview_request import RiskPreviewRequest
from mfx._generated.models.risk_reason import RiskReason
from mfx._generated.types import UNSET
from mfx._words import refuse_unknown_words

if TYPE_CHECKING:  # pragma: no cover - typing only
    from mfx._generated.models.risk_account import RiskAccount
    from mfx._generated.models.risk_account_page import RiskAccountPage
    from mfx._generated.models.risk_activation_result import RiskActivationResult
    from mfx._generated.models.risk_activity import RiskActivity
    from mfx._generated.models.risk_activity_page import RiskActivityPage
    from mfx._generated.models.risk_challenge import RiskChallenge
    from mfx._generated.models.risk_challenge_account import RiskChallengeAccount
    from mfx._generated.models.risk_challenge_account_detail import RiskChallengeAccountDetail
    from mfx._generated.models.risk_challenge_account_page import RiskChallengeAccountPage
    from mfx._generated.models.risk_check_result import RiskCheckResult
    from mfx._generated.models.risk_close_scope import RiskCloseScope
    from mfx._generated.models.risk_coverage_summary import RiskCoverageSummary
    from mfx._generated.models.risk_equity_series import RiskEquitySeries
    from mfx._generated.models.risk_plan import RiskPlan
    from mfx._generated.models.risk_plan_page import RiskPlanPage
    from mfx._generated.models.risk_policy import RiskPolicy
    from mfx._generated.models.risk_policy_version import RiskPolicyVersion
    from mfx._generated.models.risk_preview import RiskPreview
    from mfx.client import MfxClient

__all__ = ["Risk"]

Id = str | UUID
Body = Mapping[str, Any]

Coverage = Literal["healthy", "degraded", "disconnected", "unknown", "no_rules"]
Restriction = Literal["none", "entries_blocked"]
AccountSort = Literal["daily_loss_used", "drawdown_used", "exposure", "inputs_age", "plans"]
PlanState = Literal["draft", "armed", "managing", "paused", "completed", "failed", "ended"]
TimeSort = Literal["newest", "oldest"]
ActivitySort = Literal["unresolved_first", "newest", "oldest"]
ChallengeState = Literal["in_progress", "passed", "failed", "ended"]
ChallengeRule = Literal["daily_loss", "max_drawdown"]
ChallengeSort = Literal["daily_loss_used", "drawdown", "profit", "trading_days", "period_ends_at"]
CloseScope = Literal["mfx_positions", "all_positions"]


def _uuid(value: Id) -> UUID:
    return value if isinstance(value, UUID) else UUID(str(value))


def _wire(value: Any) -> Any:  # noqa: ANN401 - any part of a body
    """A body part as the platform reads it: a Decimal as exact text, a float refused (it has
    already been rounded: ``0.07 * 3`` is ``0.21000000000000002``), the rest as given."""
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, float):
        raise TypeError(f"a figure must be a Decimal or a string, never a float: {value!r}")
    if isinstance(value, Mapping):
        return {str(k): _wire(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [_wire(v) for v in value]
    return value


def _model[M](kind: type[M], value: M | Body) -> M:
    """A body as the generated model: given as one already, or as a mapping in its shape."""
    if isinstance(value, kind):
        return value
    return _request(kind, _wire(value))


def _request[M](kind: type[M], body: Any) -> M:  # noqa: ANN401 - JSON values
    """A request body as the generated model, refusing an enum word the contract does not list:
    ``from_dict`` reads one as UNKNOWN, which is right for an answer and wrong for a request."""
    return refuse_unknown_words(kind.from_dict(body))  # type: ignore[attr-defined, no-any-return]


def _many[E: Enum](values: str | Sequence[str] | None, kind: type[E]) -> Any:  # noqa: ANN401
    """A filter of one value or several, sent as repeated parameters; a misspelt value is a
    ValueError here, not a 400 from the platform."""
    if values is None:
        return UNSET
    wanted = [values] if isinstance(values, str) else list(values)
    return [kind(v) for v in wanted] if wanted else UNSET


def _ids(values: Id | Sequence[Id] | None) -> Any:  # noqa: ANN401
    if values is None:
        return UNSET
    wanted = [values] if isinstance(values, str | UUID) else list(values)
    return [_uuid(v) for v in wanted] if wanted else UNSET


def _opt(value: Any) -> Any:  # noqa: ANN401
    return UNSET if value is None else value


def _given(**fields: Any) -> dict[str, Any]:
    """A body of what was given: a field left None is left out, never sent as null."""
    return {k: v for k, v in fields.items() if v is not None}


class Risk:
    """Risk Management (``risk:read`` to read, ``risk:write`` to change, ``risk:override`` to
    relax protection or clear a breach). Every route needs Risk Management in the plan."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    @property
    def _g(self) -> Any:  # noqa: ANN401 - the generated client
        return self._client.generated

    async def _all(
        self, call: Callable[[str | None], Awaitable[Any]], what: str
    ) -> AsyncIterator[Any]:
        cursor: str | None = None
        while True:
            page = await self._client.read(partial(call, cursor), what)
            for item in page.items:
                yield item
            cursor = page.next_cursor if isinstance(page.next_cursor, str) else None
            if not cursor:
                return

    # --- policies ------------------------------------------------------------------------------

    async def create_policy(
        self, name: str, rules: Body, *, reset: Body, idempotency_key: str
    ) -> RiskPolicy:
        """A new policy at version 1. It protects nothing until it is activated on accounts.

        Args:
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _request(RiskPolicyCreate, _wire({"name": name, "rules": rules, "reset": reset}))
        created = await self._client.write(
            lambda: _create_policy.asyncio_detailed(
                client=self._g, body=body, idempotency_key=idempotency_key
            ),
            "POST /risk/policies",
        )
        return created  # type: ignore[no-any-return]

    async def add_policy_version(
        self,
        policy_id: Id,
        rules: Body,
        *,
        reset: Body,
        reason: str | None = None,
        idempotency_key: str,
    ) -> RiskPolicyVersion:
        """A new version of the policy. One that relaxes protection needs ``risk:override`` and
        a ``reason`` (403 ``risk_override_required`` otherwise).

        Args:
            policy_id: The policy to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _request(
            RiskPolicyVersionCreate, _wire(_given(rules=rules, reset=reset, reason=reason))
        )
        created = await self._client.write(
            lambda: _policy_version.asyncio_detailed(
                id=_uuid(policy_id), client=self._g, body=body, idempotency_key=idempotency_key
            ),
            f"POST /risk/policies/{policy_id}/versions",
        )
        return created  # type: ignore[no-any-return]

    async def archive_policy(self, policy_id: Id, *, idempotency_key: str) -> RiskPolicy:
        """Archive the policy: it can no longer be activated or given a new version. Refused 409
        ``state_error`` while any account holds it, active or paused (``details.accounts`` names
        them); archiving it again answers it unchanged.

        Args:
            policy_id: The policy to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        archived = await self._client.write(
            lambda: _archive.asyncio_detailed(
                id=_uuid(policy_id), client=self._g, idempotency_key=idempotency_key
            ),
            f"POST /risk/policies/{policy_id}/archive",
        )
        return archived  # type: ignore[no-any-return]

    async def activate(
        self,
        policy_id: Id,
        account_ids: Sequence[Id],
        *,
        version: int,
        reason: str | None = None,
        idempotency_key: str,
    ) -> RiskActivationResult:
        """Put a version in force on accounts; each account's outcome separately.

        Args:
            policy_id: The policy to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _request(RiskActivate,
            _given(account_ids=[str(_uuid(a)) for a in account_ids], version=version,
                   reason=reason)
        )  # fmt: skip
        result = await self._client.write(
            lambda: _activate.asyncio_detailed(
                id=_uuid(policy_id), client=self._g, body=body, idempotency_key=idempotency_key
            ),
            f"POST /risk/policies/{policy_id}/activate",
        )
        return result  # type: ignore[no-any-return]

    async def policy(self, policy_id: Id) -> RiskPolicy:
        """A policy, its current version and the accounts it is on.

        Args:
            policy_id: The policy to act on.
        """
        found = await self._client.read(
            lambda: _get_policy.asyncio_detailed(id=_uuid(policy_id), client=self._g),
            f"GET /risk/policies/{policy_id}",
        )
        return found  # type: ignore[no-any-return]

    async def policy_version(self, policy_id: Id, version: int) -> RiskPolicyVersion:
        """One version of a policy, with what changed and who made it.

        Args:
            policy_id: The policy to act on.
        """
        found = await self._client.read(
            lambda: _get_policy_version.asyncio_detailed(
                id=_uuid(policy_id), version=version, client=self._g
            ),
            f"GET /risk/policies/{policy_id}/versions/{version}",
        )
        return found  # type: ignore[no-any-return]

    def policies(
        self,
        *,
        state: Literal["active", "archived"] | None = None,
        sort: TimeSort = "newest",
        limit: int | None = None,
    ) -> AsyncIterator[RiskPolicy]:
        """Every policy, newest first (or ``sort="oldest"``).

        Args:
            limit: How many to return at most, on one page.
        """
        kept = UNSET if state is None else ListRiskPoliciesState(state)
        order = ListRiskPoliciesSort(sort)
        return self._all(
            lambda after: _list_policies.asyncio_detailed(
                client=self._g, cursor=_opt(after), limit=_opt(limit), state=kept, sort=order,
            ),
            "GET /risk/policies",
        )  # fmt: skip

    def policy_versions(self, policy_id: Id, *, limit: int | None = None) -> AsyncIterator[Any]:
        """Every version of a policy, newest first.

        Args:
            policy_id: The policy to act on.
            limit: How many to return at most, on one page.
        """
        return self._all(
            lambda after: _list_policy_versions.asyncio_detailed(
                id=_uuid(policy_id), client=self._g, cursor=_opt(after), limit=_opt(limit)
            ),
            f"GET /risk/policies/{policy_id}/versions",
        )

    # --- accounts ------------------------------------------------------------------------------

    async def accounts_page(  # noqa: PLR0913 - the list's filters
        self,
        *,
        coverage: Coverage | Sequence[Coverage] | None = None,
        restriction: Restriction | Sequence[Restriction] | None = None,
        sort: AccountSort = "daily_loss_used",
        cursor: str | None = None,
        limit: int | None = None,
    ) -> RiskAccountPage:
        """One page of accounts with their figures, and ``stats`` over the whole set.

        Args:
            cursor: Where to continue from: the previous page's ``next_cursor``.
            limit: How many to return at most, on one page.
        """
        covered = _many(coverage, ListRiskAccountsCoverageItem)
        restricted = _many(restriction, ListRiskAccountsRestrictionItem)
        order = ListRiskAccountsSort(sort)
        page = await self._client.read(
            lambda: _list_accounts.asyncio_detailed(
                client=self._g, cursor=_opt(cursor), limit=_opt(limit), coverage=covered,
                restriction=restricted, sort=order,
            ),
            "GET /risk/accounts",
        )  # fmt: skip
        return page  # type: ignore[no-any-return]

    async def accounts(
        self,
        *,
        coverage: Coverage | Sequence[Coverage] | None = None,
        restriction: Restriction | Sequence[Restriction] | None = None,
        sort: AccountSort = "daily_loss_used",
    ) -> AsyncIterator[RiskAccount]:
        """Every account, in the order ``sort`` names, following the cursor to the end."""
        cursor: str | None = None
        while True:
            page = await self.accounts_page(
                coverage=coverage, restriction=restriction, sort=sort, cursor=cursor
            )
            for item in page.items:
                yield item
            cursor = page.next_cursor if isinstance(page.next_cursor, str) else None
            if not cursor:
                return

    async def account(self, account_id: Id) -> RiskAccount:
        """One account's figures, each with its inputs and their times.

        Args:
            account_id: The trading account to act on. Another tenant's id answers 404, never 403.
        """
        found = await self._client.read(
            lambda: _get_account.asyncio_detailed(id=_uuid(account_id), client=self._g),
            f"GET /risk/accounts/{account_id}",
        )
        return found  # type: ignore[no-any-return]

    async def equity(
        self, account_id: Id, start: dt.datetime, end: dt.datetime | None = None
    ) -> RiskEquitySeries:
        """The account's equity and balance from its stored reads, between two moments.

        Args:
            account_id: The trading account to act on. Another tenant's id answers 404, never 403.
        """
        found = await self._client.read(
            lambda: _equity.asyncio_detailed(
                id=_uuid(account_id), client=self._g, from_=start, to=_opt(end)
            ),
            f"GET /risk/accounts/{account_id}/equity",
        )
        return found  # type: ignore[no-any-return]

    async def close_scope(self, account_id: Id, scope: CloseScope) -> RiskCloseScope:
        """The positions a ``close_positions`` action would close now under ``scope``: only those
        MFX Hub placed (``mfx_positions``), or every one (``all_positions``).

        Args:
            account_id: The trading account to act on. Another tenant's id answers 404, never 403.
        """
        found = await self._client.read(
            lambda: _close_scope.asyncio_detailed(
                id=_uuid(account_id), client=self._g, scope=GetRiskAccountCloseScopeScope(scope)
            ),
            f"GET /risk/accounts/{account_id}/close-scope",
        )
        return found  # type: ignore[no-any-return]

    async def deactivate(self, account_id: Id, *, reason: str, idempotency_key: str) -> Any:  # noqa: ANN401
        """End the account's activation (``risk:override``): no rule applies after it.

        Args:
            account_id: The trading account to act on. Another tenant's id answers 404, never 403.
            reason: Your own words, recorded with the action.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = RiskReason(reason=reason)
        return await self._client.write(
            lambda: _deactivate.asyncio_detailed(
                id=_uuid(account_id), client=self._g, body=body, idempotency_key=idempotency_key
            ),
            f"POST /risk/accounts/{account_id}/deactivate",
        )

    async def clear(
        self,
        account_id: Id,
        rule: Literal["daily_loss", "drawdown", "restriction"],
        *,
        reason: str,
        idempotency_key: str,
    ) -> Any:  # noqa: ANN401
        """Clear a breach, or lift a restriction before it clears itself (``risk:override``).

        Args:
            account_id: The trading account to act on. Another tenant's id answers 404, never 403.
            reason: Your own words, recorded with the action.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _request(RiskClear, {"rule": rule, "reason": reason})
        return await self._client.write(
            lambda: _clear.asyncio_detailed(
                id=_uuid(account_id), client=self._g, body=body, idempotency_key=idempotency_key
            ),
            f"POST /risk/accounts/{account_id}/clear",
        )

    async def coverage(self) -> RiskCoverageSummary:
        """Coverage by kind and state, and every account where it is not healthy."""
        found = await self._client.read(
            lambda: _coverage.asyncio_detailed(client=self._g), "GET /risk/coverage"
        )
        return found  # type: ignore[no-any-return]

    # --- the planner ---------------------------------------------------------------------------

    async def preview(self, request: RiskPreviewRequest | Body) -> RiskPreview:
        """Size a trade from a risk budget and check every rule. Nothing is sent to the broker."""
        body = _model(RiskPreviewRequest, request)
        found = await self._client.read(
            lambda: _preview.asyncio_detailed(client=self._g, body=body),
            "POST /risk/planner/preview",
        )
        return found  # type: ignore[no-any-return]

    async def check(self, account_id: Id, order: Body) -> RiskCheckResult:
        """Check an order already sized, exactly as the pre-trade check would.

        Args:
            account_id: The trading account to act on. Another tenant's id answers 404, never 403.
        """
        body = _request(
            RiskCheckRequest, _wire({"account_id": str(_uuid(account_id)), "order": order})
        )
        found = await self._client.read(
            lambda: _check.asyncio_detailed(client=self._g, body=body), "POST /risk/planner/check"
        )
        return found  # type: ignore[no-any-return]

    # --- exit plans ----------------------------------------------------------------------------

    async def create_plan(self, plan: RiskPlanCreate | Body, *, idempotency_key: str) -> RiskPlan:
        """An exit plan on a held position (``ticket``) or placed with its order (``order``).

        Args:
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _model(RiskPlanCreate, plan)
        created = await self._client.write(
            lambda: _create_plan.asyncio_detailed(
                client=self._g, body=body, idempotency_key=idempotency_key
            ),
            "POST /risk/plans",
        )
        return created  # type: ignore[no-any-return]

    async def plan(self, plan_id: Id) -> RiskPlan:
        """An exit plan, each step with its holder, state and outcome, and ``r_now``.

        Args:
            plan_id: The plan to act on.
        """
        found = await self._client.read(
            lambda: _get_plan.asyncio_detailed(id=_uuid(plan_id), client=self._g),
            f"GET /risk/plans/{plan_id}",
        )
        return found  # type: ignore[no-any-return]

    async def plans_page(
        self,
        *,
        account_id: Id | Sequence[Id] | None = None,
        state: PlanState | Sequence[PlanState] | None = None,
        sort: TimeSort = "newest",
        cursor: str | None = None,
        limit: int | None = None,
    ) -> RiskPlanPage:
        """One page of plans, with ``stats`` over the filtered set.

        Args:
            cursor: Where to continue from: the previous page's ``next_cursor``.
            limit: How many to return at most, on one page.
        """
        accounts, states = _ids(account_id), _many(state, ListRiskPlansStateItem)
        order = ListRiskPlansSort(sort)
        page = await self._client.read(
            lambda: _list_plans.asyncio_detailed(
                client=self._g, cursor=_opt(cursor), limit=_opt(limit), account_id=accounts,
                state=states, sort=order,
            ),
            "GET /risk/plans",
        )  # fmt: skip
        return page  # type: ignore[no-any-return]

    def plans(
        self,
        *,
        account_id: Id | Sequence[Id] | None = None,
        state: PlanState | Sequence[PlanState] | None = None,
        sort: TimeSort = "newest",
    ) -> AsyncIterator[RiskPlan]:
        """Every plan, following the cursor to the end."""
        accounts, states = _ids(account_id), _many(state, ListRiskPlansStateItem)
        order = ListRiskPlansSort(sort)
        return self._all(
            lambda after: _list_plans.asyncio_detailed(
                client=self._g, cursor=_opt(after), account_id=accounts, state=states, sort=order,
            ),
            "GET /risk/plans",
        )  # fmt: skip

    async def amend_plan(
        self, plan_id: Id, steps: Sequence[Body], *, reason: str | None = None,
        idempotency_key: str,
    ) -> RiskPlan:  # fmt: skip
        """A new version of the plan's steps.

        Args:
            plan_id: The plan to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _request(RiskPlanAmend, _wire(_given(steps=list(steps), reason=reason)))
        found = await self._client.write(
            lambda: _amend_plan.asyncio_detailed(
                id=_uuid(plan_id), client=self._g, body=body, idempotency_key=idempotency_key
            ),
            f"POST /risk/plans/{plan_id}/amend",
        )
        return found  # type: ignore[no-any-return]

    async def pause_plan(self, plan_id: Id, *, reason: str, idempotency_key: str) -> RiskPlan:
        """Pause the plan's MFX-held steps; stops held at the broker stay where they are.

        Args:
            plan_id: The plan to act on.
            reason: Your own words, recorded with the action.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = RiskReason(reason=reason)
        found = await self._client.write(
            lambda: _pause_plan.asyncio_detailed(
                id=_uuid(plan_id), client=self._g, body=body, idempotency_key=idempotency_key
            ),
            f"POST /risk/plans/{plan_id}/pause",
        )
        return found  # type: ignore[no-any-return]

    async def resume_plan(self, plan_id: Id, *, idempotency_key: str) -> RiskPlan:
        """Resume the plan's MFX-held steps.

        Args:
            plan_id: The plan to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        found = await self._client.write(
            lambda: _resume_plan.asyncio_detailed(
                id=_uuid(plan_id), client=self._g, idempotency_key=idempotency_key
            ),
            f"POST /risk/plans/{plan_id}/resume",
        )
        return found  # type: ignore[no-any-return]

    async def end_plan(self, plan_id: Id, *, idempotency_key: str) -> RiskPlan:
        """End the plan; stops held at the broker stay where they are.

        Args:
            plan_id: The plan to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        found = await self._client.write(
            lambda: _end_plan.asyncio_detailed(
                id=_uuid(plan_id), client=self._g, idempotency_key=idempotency_key
            ),
            f"DELETE /risk/plans/{plan_id}",
        )
        return found  # type: ignore[no-any-return]

    # --- challenges ----------------------------------------------------------------------------

    async def create_challenge(
        self, name: str, rules: RiskChallengeRules | Body, *, idempotency_key: str
    ) -> RiskChallenge:
        """A challenge at version 1: one rule set over many accounts.

        Args:
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        given = rules.to_dict() if isinstance(rules, RiskChallengeRules) else _wire(rules)
        body = _request(RiskChallengeCreate, {"name": name, "rules": given})
        created = await self._client.write(
            lambda: _create_challenge.asyncio_detailed(
                client=self._g, body=body, idempotency_key=idempotency_key
            ),
            "POST /risk/challenges",
        )
        return created  # type: ignore[no-any-return]

    async def add_challenge_version(
        self, challenge_id: Id, rules: RiskChallengeRules | Body, *, idempotency_key: str
    ) -> RiskChallenge:
        """A new version, for accounts enrolled after it; one already running keeps its own.

        Args:
            challenge_id: The challenge to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _model(RiskChallengeRules, rules)
        created = await self._client.write(
            lambda: _challenge_version.asyncio_detailed(
                id=_uuid(challenge_id), client=self._g, body=body,
                idempotency_key=idempotency_key,
            ),
            f"POST /risk/challenges/{challenge_id}/versions",
        )  # fmt: skip
        return created  # type: ignore[no-any-return]

    async def archive_challenge(self, challenge_id: Id, *, idempotency_key: str) -> RiskChallenge:
        """Archive the challenge: no account can be enrolled in it or given a new version of it.
        Refused 409 ``state_error`` while any account is in progress (``details.accounts`` names
        them); archiving it again answers it unchanged.

        Args:
            challenge_id: The challenge to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        archived = await self._client.write(
            lambda: _archive_challenge.asyncio_detailed(
                id=_uuid(challenge_id), client=self._g, idempotency_key=idempotency_key
            ),
            f"POST /risk/challenges/{challenge_id}/archive",
        )
        return archived  # type: ignore[no-any-return]

    async def challenge(self, challenge_id: Id) -> RiskChallenge:
        """A challenge, its current rule set and its counts.

        Args:
            challenge_id: The challenge to act on.
        """
        found = await self._client.read(
            lambda: _get_challenge.asyncio_detailed(id=_uuid(challenge_id), client=self._g),
            f"GET /risk/challenges/{challenge_id}",
        )
        return found  # type: ignore[no-any-return]

    def challenges(self, *, limit: int | None = None) -> AsyncIterator[RiskChallenge]:
        """Every challenge, newest first, each with its counts.

        Args:
            limit: How many to return at most, on one page.
        """
        return self._all(
            lambda after: _list_challenges.asyncio_detailed(
                client=self._g, cursor=_opt(after), limit=_opt(limit)
            ),
            "GET /risk/challenges",
        )

    async def enrol(
        self, challenge_id: Id, account_ids: Sequence[Id], *, idempotency_key: str
    ) -> Any:  # noqa: ANN401
        """Enrol accounts in the challenge's current version; each account's outcome
        separately (one with a stale read is refused ``risk_inputs_stale``).

        Args:
            challenge_id: The challenge to act on.
            idempotency_key: Required on every write and never defaulted. Sending again with the
                same key answers the original; a fresh key asks for a new action.
        """
        body = _request(RiskEnrol, {"account_ids": [str(_uuid(a)) for a in account_ids]})
        return await self._client.write(
            lambda: _enrol.asyncio_detailed(
                id=_uuid(challenge_id), client=self._g, body=body,
                idempotency_key=idempotency_key,
            ),
            f"POST /risk/challenges/{challenge_id}/accounts",
        )  # fmt: skip

    async def challenge_accounts_page(  # noqa: PLR0913 - the list's filters
        self,
        challenge_id: Id,
        *,
        state: ChallengeState | Sequence[ChallengeState] | None = None,
        rule: ChallengeRule | Sequence[ChallengeRule] | None = None,
        below_min_days: bool | None = None,
        sort: ChallengeSort = "daily_loss_used",
        cursor: str | None = None,
        limit: int | None = None,
    ) -> RiskChallengeAccountPage:
        """One page of the challenge's accounts, with ``stats`` over the filtered set. This list,
        paged, is the export.

        Args:
            challenge_id: The challenge to act on.
            cursor: Where to continue from: the previous page's ``next_cursor``.
            limit: How many to return at most, on one page.
        """
        states = _many(state, ListRiskChallengeAccountsStateItem)
        rules = _many(rule, ListRiskChallengeAccountsRuleItem)
        order = ListRiskChallengeAccountsSort(sort)
        page = await self._client.read(
            lambda: _list_enrolled.asyncio_detailed(
                id=_uuid(challenge_id), client=self._g, cursor=_opt(cursor), limit=_opt(limit),
                state=states, rule=rules, below_min_days=_opt(below_min_days), sort=order,
            ),
            f"GET /risk/challenges/{challenge_id}/accounts",
        )  # fmt: skip
        return page  # type: ignore[no-any-return]

    async def challenge_accounts(
        self,
        challenge_id: Id,
        *,
        state: ChallengeState | Sequence[ChallengeState] | None = None,
        rule: ChallengeRule | Sequence[ChallengeRule] | None = None,
        below_min_days: bool | None = None,
        sort: ChallengeSort = "daily_loss_used",
    ) -> AsyncIterator[RiskChallengeAccount]:
        """Every account of the challenge, in the order ``sort`` names.

        Args:
            challenge_id: The challenge to act on.
        """
        cursor: str | None = None
        while True:
            page = await self.challenge_accounts_page(
                challenge_id, state=state, rule=rule, below_min_days=below_min_days,
                sort=sort, cursor=cursor,
            )  # fmt: skip
            for item in page.items:
                yield item
            cursor = page.next_cursor if isinstance(page.next_cursor, str) else None
            if not cursor:
                return

    async def challenge_account(
        self, challenge_id: Id, account_id: Id
    ) -> RiskChallengeAccountDetail:
        """One enrolled account, its result and its periods with their statistics.

        Args:
            challenge_id: The challenge to act on.
            account_id: The trading account to act on. Another tenant's id answers 404, never 403.
        """
        found = await self._client.read(
            lambda: _get_enrolled.asyncio_detailed(
                id=_uuid(challenge_id), account_id=_uuid(account_id), client=self._g
            ),
            f"GET /risk/challenges/{challenge_id}/accounts/{account_id}",
        )
        return found  # type: ignore[no-any-return]

    # --- activity ------------------------------------------------------------------------------

    async def activity_page(  # noqa: PLR0913 - the list's filters
        self,
        *,
        kind: str | Sequence[str] | None = None,
        account_id: Id | Sequence[Id] | None = None,
        outcome: str | Sequence[str] | None = None,
        start: dt.datetime | None = None,
        end: dt.datetime | None = None,
        sort: ActivitySort = "unresolved_first",
        cursor: str | None = None,
        limit: int | None = None,
    ) -> RiskActivityPage:
        """One page of activity, unresolved first by default, with ``stats``.

        Args:
            cursor: Where to continue from: the previous page's ``next_cursor``.
            limit: How many to return at most, on one page.
        """
        kinds, accounts = _many(kind, RiskActivityKind), _ids(account_id)
        outcomes, order = _many(outcome, RiskOutcome), ListRiskActivitySort(sort)
        page = await self._client.read(
            lambda: _list_activity.asyncio_detailed(
                client=self._g, cursor=_opt(cursor), limit=_opt(limit), kind=kinds,
                account_id=accounts, outcome=outcomes, from_=_opt(start), to=_opt(end),
                sort=order,
            ),
            "GET /risk/activity",
        )  # fmt: skip
        return page  # type: ignore[no-any-return]

    async def activity(  # noqa: PLR0913 - the list's filters
        self,
        *,
        kind: str | Sequence[str] | None = None,
        account_id: Id | Sequence[Id] | None = None,
        outcome: str | Sequence[str] | None = None,
        start: dt.datetime | None = None,
        end: dt.datetime | None = None,
        sort: ActivitySort = "unresolved_first",
    ) -> AsyncIterator[RiskActivity]:
        """Every warning, breach, action and change, following the cursor to the end."""
        cursor: str | None = None
        while True:
            page = await self.activity_page(
                kind=kind, account_id=account_id, outcome=outcome, start=start, end=end,
                sort=sort, cursor=cursor,
            )  # fmt: skip
            for item in page.items:
                yield item
            cursor = page.next_cursor if isinstance(page.next_cursor, str) else None
            if not cursor:
                return

"""``client.risk`` — Risk Management: policies, accounts, the planner, exit plans, challenges and
activity, and the typed refusal of an entry that breaks a rule."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs

import httpx
import pytest
import yaml

from mfx import errors
from mfx.client import MfxClient

from .conftest import FakeMfx, body_of

SPEC = yaml.safe_load(
    (Path(__file__).resolve().parents[2] / "spec" / "openapi.yaml").read_text("utf-8")
)
SCHEMAS: dict[str, Any] = SPEC["components"]["schemas"]
ID = "4c2d3e4f-5a6b-7c8d-9e0f-102030405060"
ACCOUNT = "5c2d3e4f-5a6b-7c8d-9e0f-102030405060"


def sample(schema: dict[str, Any], depth: int = 0) -> Any:  # noqa: ANN401, C901, PLR0911 - a walk
    """A minimal instance the contract accepts: every required field, the first of each choice."""
    if "$ref" in schema:
        return sample(SCHEMAS[schema["$ref"].rsplit("/", 1)[1]], depth)
    for key in ("oneOf", "anyOf"):
        if key in schema:
            options = [s for s in schema[key] if s.get("type") != "null"]
            return sample(options[0], depth)
    if "allOf" in schema:
        merged: dict[str, Any] = {}
        for part in schema["allOf"]:
            value = sample(part, depth)
            if isinstance(value, dict):
                merged |= value
        return merged
    if "enum" in schema:
        return next(v for v in schema["enum"] if v is not None)
    kind = schema.get("type", "object")
    if isinstance(kind, list):
        kind = next(k for k in kind if k != "null")
    if kind == "object":
        props = schema.get("properties", {})
        return {k: sample(props[k], depth + 1) for k in schema.get("required", []) if k in props}
    if kind == "array":
        return [] if depth > 3 else [sample(schema.get("items", {}), depth + 1)]  # noqa: PLR2004
    if kind == "integer":
        return 1
    if kind == "number":
        return 1
    if kind == "boolean":
        return False
    fmt = schema.get("format")
    if fmt == "uuid":
        return ID
    if fmt == "date-time":
        return "2026-11-14T12:00:00Z"
    if fmt == "date":
        return "2026-11-14"
    return "1"


def of(name: str, **over: Any) -> dict[str, Any]:
    body = sample(SCHEMAS[name])
    body.update(over)
    return body


def answer(name: str, status: int = 200, **over: Any) -> httpx.Response:
    return httpx.Response(status, json=of(name, **over))


def query(request: httpx.Request) -> dict[str, list[str]]:
    return parse_qs(request.url.query.decode())


RULES = {
    "daily_loss": {
        "limit": {"pct": "5"},
        "basis": "start_balance",
        "warn_at": {"pct": "4"},
        "act_at": {"pct": "5"},
        "check_entries": True,
        "actions": {"kinds": ["notify", "block_entries"]},
    }
}


async def test_a_policy_is_created_versioned_and_put_in_force_with_one_outcome_per_account(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant with risk:write
    When it creates a policy, adds a version that relaxes it with a reason, activates it on two
    accounts, reads the policy, one version and every policy oldest first, and archives it while an
    account still holds it and then once none does
    Then each is one request to its route with the idempotency key and the body in the contract's
    shape, decimals as text; the activation answers one outcome per account; the list follows the
    cursor and sends its sort; the archive sends no body, a refused one is a StateError naming the
    accounts that hold it, and the archived policy carries archived_at."""
    mfx.responses.append(answer("RiskPolicy", 201))
    await client.risk.create_policy(
        "Funded", RULES, reset={"zone": "broker"}, idempotency_key="p-1"
    )
    request = mfx.last
    assert (request.method, request.url.path) == ("POST", "/v1/risk/policies")
    assert request.headers["Idempotency-Key"] == "p-1"
    sent = body_of(request)
    assert sent["name"] == "Funded" and sent["rules"]["daily_loss"]["limit"] == {"pct": "5"}

    mfx.responses.append(answer("RiskPolicyVersion", 201, version=2, relaxes=True))
    version = await client.risk.add_policy_version(
        ID, RULES, reset={"zone": "UTC"}, reason="desk asked", idempotency_key="v-2"
    )
    assert mfx.last.url.path == f"/v1/risk/policies/{ID}/versions" and version.version == 2  # noqa: PLR2004
    assert body_of(mfx.last)["reason"] == "desk asked"

    mfx.responses.append(
        httpx.Response(
            200,
            json={
                "results": [
                    {"account_id": ACCOUNT, "outcome": "done", "reason": None},
                    {"account_id": ID, "outcome": "refused", "reason": "risk_inputs_stale"},
                ]
            },
        )
    )
    result = await client.risk.activate(ID, [ACCOUNT, ID], version=2, idempotency_key="a-1")
    assert body_of(mfx.last) == {"account_ids": [ACCOUNT, ID], "version": 2}
    assert [r.outcome.value for r in result.results] == ["done", "refused"]

    mfx.responses.append(answer("RiskPolicy"))
    await client.risk.policy(ID)
    mfx.responses.append(answer("RiskPolicyVersion"))
    await client.risk.policy_version(ID, 1)
    assert mfx.last.url.path == f"/v1/risk/policies/{ID}/versions/1"

    first = of("RiskPolicyPage", next_cursor="c1")
    mfx.responses += [
        httpx.Response(200, json=first),
        httpx.Response(200, json=of("RiskPolicyPage", next_cursor=None)),
    ]
    listed = [p async for p in client.risk.policies(state="active", sort="oldest", limit=1)]
    assert len(listed) == 2  # noqa: PLR2004
    assert query(mfx.requests[-2]) == {"limit": ["1"], "state": ["active"], "sort": ["oldest"]}
    assert query(mfx.last)["cursor"] == ["c1"]
    mfx.responses.append(answer("RiskPolicyVersionPage", next_cursor=None))
    assert len([v async for v in client.risk.policy_versions(ID, limit=5)]) == 1

    mfx.responses.append(
        httpx.Response(
            409,
            json={
                "error": {
                    "code": "state_error",
                    "message": "the policy is held by 1 account",
                    "details": {"accounts": [ACCOUNT]},
                }
            },
        )
    )
    sent_before = len(mfx.requests)
    with pytest.raises(errors.StateError) as held:
        await client.risk.archive_policy(ID, idempotency_key="ar-1")
    assert held.value.details["accounts"] == [ACCOUNT]
    assert len(mfx.requests) == sent_before + 1  # a refused write is sent once
    mfx.responses.append(answer("RiskPolicy", archived_at="2026-11-16T07:00:00Z"))
    archived = await client.risk.archive_policy(ID, idempotency_key="ar-2")
    request = mfx.last
    assert (request.method, request.url.path) == ("POST", f"/v1/risk/policies/{ID}/archive")
    assert request.headers["Idempotency-Key"] == "ar-2" and request.content == b""
    assert archived.archived_at == dt.datetime(2026, 11, 16, 7, tzinfo=dt.UTC)


async def test_accounts_are_listed_with_several_values_per_filter_and_their_stats_and_read_one(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given protected accounts
    When the tenant lists them by two coverage states and a restriction, sorted by plans, walks
    every page, reads one, its equity, what a close would reach, and the coverage summary
    Then several values go as repeated parameters, the page keeps its stats, the walk follows the
    cursor, and each read is its own route; a misspelt filter is a ValueError before any call."""
    page = of("RiskAccountPage", next_cursor="n1")
    page["stats"] = {**page["stats"], "warnings": 2, "active_plans": 3, "gross_exposure": "4.5"}
    mfx.responses.append(httpx.Response(200, json=page))
    shown = await client.risk.accounts_page(
        coverage=["healthy", "degraded"], restriction="entries_blocked", sort="plans"
    )
    assert query(mfx.last) == {
        "coverage": ["healthy", "degraded"],
        "restriction": ["entries_blocked"],
        "sort": ["plans"],
    }
    assert shown.stats.warnings == 2 and shown.stats.gross_exposure == "4.5"  # noqa: PLR2004
    mfx.responses += [
        httpx.Response(200, json=page),
        httpx.Response(200, json=of("RiskAccountPage", next_cursor=None)),
    ]
    assert len([a async for a in client.risk.accounts(coverage=[])]) == 2  # noqa: PLR2004
    assert "coverage" not in query(mfx.requests[-2])
    with pytest.raises(ValueError, match="not_a_state"):
        await client.risk.accounts_page(coverage="not_a_state")  # type: ignore[arg-type]

    mfx.responses.append(answer("RiskAccount"))
    await client.risk.account(ACCOUNT)
    assert mfx.last.url.path == f"/v1/risk/accounts/{ACCOUNT}"
    mfx.responses.append(answer("RiskEquitySeries"))
    start = dt.datetime(2026, 11, 1, tzinfo=dt.UTC)
    await client.risk.equity(ACCOUNT, start)
    assert query(mfx.last)["from"][0].startswith("2026-11-01T00:00:00")
    mfx.responses.append(answer("RiskCloseScope", count=1))
    scope = await client.risk.close_scope(ACCOUNT, "mfx_positions")
    assert query(mfx.last) == {"scope": ["mfx_positions"]} and scope.count == 1
    mfx.responses.append(answer("RiskCoverageSummary"))
    await client.risk.coverage()
    assert mfx.last.url.path == "/v1/risk/coverage"


async def test_an_override_clears_a_breach_or_ends_an_activation_with_its_reason(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an account with a drawdown breach
    When a key with risk:override clears it and then ends the activation, and a key without it
    tries to relax a policy
    Then each sends the rule and the reason with its idempotency key; the refused one raises
    RiskOverrideRequiredError, a ForbiddenError."""
    mfx.responses.append(answer("RiskAccount"))
    await client.risk.clear(ACCOUNT, "drawdown", reason="checked", idempotency_key="c-1")
    assert mfx.last.url.path == f"/v1/risk/accounts/{ACCOUNT}/clear"
    assert body_of(mfx.last) == {"rule": "drawdown", "reason": "checked"}
    mfx.responses.append(answer("RiskAccount"))
    await client.risk.deactivate(ACCOUNT, reason="closing", idempotency_key="d-1")
    assert body_of(mfx.last) == {"reason": "closing"}
    mfx.responses.append(
        httpx.Response(
            403,
            json={"error": {"code": "risk_override_required", "message": "relaxes", "details": {}}},
        )
    )
    with pytest.raises(errors.RiskOverrideRequiredError) as raised:
        await client.risk.add_policy_version(
            ID, RULES, reset={"zone": "broker"}, idempotency_key="v-3"
        )
    assert isinstance(raised.value, errors.ForbiddenError)


async def test_the_planner_sizes_and_checks_a_trade_and_a_refused_entry_names_its_rule(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an account with a daily loss rule
    When the tenant previews a trade from a budget, checks a sized order, and an order is refused
    by the policy, and another by a challenge's rule
    Then the preview and the check post the contract's body with decimals as text; a refusal
    raises RiskRefusedError (a ValidationError) whose refusal names the rule, the version, the
    figures as text, and the challenge when one refused."""
    preview = {
        "account_id": ACCOUNT,
        "symbol": "EURUSD",
        "side": "buy",
        "entry_type": "market",
        "sl": "1.081",
        "budget": {"kind": "pct_of_equity", "value": "0.5"},
    }
    mfx.responses.append(answer("RiskPreview"))
    await client.risk.preview(preview)
    assert (mfx.last.url.path, body_of(mfx.last)["budget"]) == (
        "/v1/risk/planner/preview",
        {"kind": "pct_of_equity", "value": "0.5"},
    )
    from mfx._generated.models.risk_preview_request import RiskPreviewRequest  # noqa: PLC0415

    mfx.responses.append(answer("RiskPreview"))
    await client.risk.preview(RiskPreviewRequest.from_dict(preview))
    assert body_of(mfx.last)["symbol"] == "EURUSD"
    mfx.responses.append(answer("RiskCheckResult"))
    order = {"symbol": "EURUSD", "side": "buy", "type": "market", "volume": "0.4"}
    await client.risk.check(ACCOUNT, order)
    assert body_of(mfx.last) == {"account_id": ACCOUNT, "order": order}

    from decimal import Decimal  # noqa: PLC0415

    mfx.responses.append(answer("RiskCheckResult"))
    await client.risk.check(ACCOUNT, {**order, "volume": Decimal("0.40"), "sl": None})
    assert body_of(mfx.last)["order"]["volume"] == "0.40"
    sent_before = len(mfx.requests)
    with pytest.raises(TypeError, match="never a float"):
        await client.risk.check(ACCOUNT, {**order, "volume": 0.4})
    with pytest.raises(TypeError, match="never a float"):
        await client.risk.amend_plan(
            ID, [{"trigger": {"kind": "price", "value": 1.1}}], idempotency_key="x"
        )
    assert len(mfx.requests) == sent_before
    mfx.responses.append(answer("RiskPlan"))
    steps = (
        {"trigger": {"kind": "r", "value": "1"}, "action": {"kind": "move_stop"}, "held_by": "mfx"},
    )
    await client.risk.amend_plan(ID, steps, idempotency_key="y")
    details = {
        "reason": "daily_loss_reached",
        "rule": "daily_loss",
        "policy_id": ID,
        "version": 3,
        "used": "240",
        "limit": "300",
        "would_be": "310",
    }
    refused = errors.error_for("risk_refused", "refused", status=422, details=details)
    assert isinstance(refused, errors.RiskRefusedError)
    assert isinstance(refused, errors.ValidationError)
    assert refused.refusal == errors.RiskRefusal(
        reason="daily_loss_reached",
        rule="daily_loss",
        policy_id=ID,
        version=3,
        challenge_id=None,
        challenge_version=None,
        used="240",
        limit="300",
        would_be="310",
    )
    by_challenge = errors.error_for(
        "risk_refused",
        "refused",
        status=422,
        details={
            "reason": "risk_entries_blocked",
            "rule": "max_drawdown",
            "policy_id": "",
            "challenge_id": ID,
            "challenge_version": "2",
            "version": True,
        },
    )
    assert by_challenge.refusal.challenge_version == 2  # type: ignore[attr-defined]  # noqa: PLR2004
    assert (by_challenge.refusal.policy_id, by_challenge.refusal.version) == (None, None)  # type: ignore[attr-defined]
    bare = errors.error_for("risk_refused", "refused", status=422, details={"version": "x"})
    assert (bare.refusal.reason, bare.refusal.version) == ("risk_refused", None)  # type: ignore[attr-defined]


async def test_an_exit_plan_is_created_amended_paused_resumed_ended_and_listed_with_its_stats(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a held position
    When the tenant arms an exit plan on it, reads it, amends its steps, pauses, resumes and ends
    it, and lists plans for two accounts in two states, oldest first
    Then each is its own route with its idempotency key; the steps go as given; the list sends
    the repeated filters and the sort and keeps its stats; the walk follows the cursor."""
    plan = {
        "account_id": ACCOUNT,
        "ticket": "9001",
        "order": {"symbol": "EURUSD", "side": "buy", "type": "market", "volume": "0.4"},
        "steps": [
            {
                "trigger": {"kind": "r", "value": "1"},
                "action": {"kind": "close_part", "pct": "50"},
                "held_by": "mfx",
            }
        ],
    }
    mfx.responses.append(answer("RiskPlan", 201))
    await client.risk.create_plan(plan, idempotency_key="plan-1")
    assert body_of(mfx.last)["steps"][0]["action"] == {"kind": "close_part", "pct": "50"}
    for call, path in (
        (lambda: client.risk.plan(ID), f"/v1/risk/plans/{ID}"),
        (
            lambda: client.risk.amend_plan(
                ID,
                plan["steps"],
                reason="wider",  # type: ignore[arg-type]
                idempotency_key="am-1",
            ),
            f"/v1/risk/plans/{ID}/amend",
        ),
        (
            lambda: client.risk.pause_plan(ID, reason="news", idempotency_key="pa-1"),
            f"/v1/risk/plans/{ID}/pause",
        ),
        (
            lambda: client.risk.resume_plan(ID, idempotency_key="re-1"),
            f"/v1/risk/plans/{ID}/resume",
        ),
        (lambda: client.risk.end_plan(ID, idempotency_key="en-1"), f"/v1/risk/plans/{ID}"),
    ):
        mfx.responses.append(answer("RiskPlan"))
        await call()
        assert mfx.last.url.path == path
    assert mfx.last.method == "DELETE"

    page = of("RiskPlanPage", next_cursor="p2")
    mfx.responses.append(httpx.Response(200, json=page))
    shown = await client.risk.plans_page(
        account_id=[ACCOUNT, ID], state=["armed", "managing"], sort="oldest"
    )
    assert query(mfx.last) == {
        "account_id": [ACCOUNT, ID],
        "state": ["armed", "managing"],
        "sort": ["oldest"],
    }
    assert shown.stats is not None
    mfx.responses += [
        httpx.Response(200, json=page),
        httpx.Response(200, json=of("RiskPlanPage", next_cursor=None)),
    ]
    assert len([p async for p in client.risk.plans(account_id=ACCOUNT, state="armed")]) == 2  # noqa: PLR2004
    mfx.responses.append(answer("RiskPlanPage", next_cursor=None))
    await client.risk.plans_page(account_id=[])
    assert "account_id" not in query(mfx.last)


async def test_a_challenge_is_created_versioned_and_enrolled_and_its_accounts_sorted_by_figure(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a prop-firm programme
    When the tenant creates a challenge, adds a version, enrols two accounts, lists its accounts
    in two states sorted by profit, walks every page, and reads one account's periods
    Then each is its own route; the list sends the repeated filters and the sort and keeps its
    stats; the walk follows the cursor; the account reads its periods; archiving sends no body,
    is a StateError naming the accounts in progress while any is, sent once, and the archived
    challenge carries archived_at."""
    rules = sample(SCHEMAS["RiskChallengeRules"])
    mfx.responses.append(answer("RiskChallenge", 201))
    await client.risk.create_challenge("Phase 1", rules, idempotency_key="ch-1")
    assert body_of(mfx.last)["name"] == "Phase 1"
    from mfx._generated.models.risk_challenge_rules import RiskChallengeRules  # noqa: PLC0415

    mfx.responses.append(answer("RiskChallenge", 201))
    await client.risk.create_challenge(
        "Phase 2", RiskChallengeRules.from_dict(rules), idempotency_key="ch-2"
    )
    mfx.responses.append(answer("RiskChallenge", 201))
    await client.risk.add_challenge_version(ID, rules, idempotency_key="cv-1")
    assert mfx.last.url.path == f"/v1/risk/challenges/{ID}/versions"
    mfx.responses.append(httpx.Response(200, json={"results": []}))
    await client.risk.enrol(ID, [ACCOUNT, ID], idempotency_key="en-1")
    assert body_of(mfx.last) == {"account_ids": [ACCOUNT, ID]}
    mfx.responses.append(
        httpx.Response(
            409,
            json={
                "error": {
                    "code": "state_error",
                    "message": "1 account is in progress",
                    "details": {"accounts": [ACCOUNT]},
                }
            },
        )
    )
    sent_before = len(mfx.requests)
    with pytest.raises(errors.StateError) as running:
        await client.risk.archive_challenge(ID, idempotency_key="ca-1")
    assert running.value.details["accounts"] == [ACCOUNT]
    assert len(mfx.requests) == sent_before + 1  # a refused write is sent once
    mfx.responses.append(answer("RiskChallenge", archived_at="2026-11-16T12:00:00Z"))
    archived = await client.risk.archive_challenge(ID, idempotency_key="ca-2")
    assert (mfx.last.method, mfx.last.url.path) == ("POST", f"/v1/risk/challenges/{ID}/archive")
    assert mfx.last.headers["Idempotency-Key"] == "ca-2" and mfx.last.content == b""
    assert archived.archived_at == dt.datetime(2026, 11, 16, 12, tzinfo=dt.UTC)
    mfx.responses.append(answer("RiskChallenge"))
    await client.risk.challenge(ID)
    mfx.responses.append(answer("RiskChallengePage", next_cursor=None))
    assert len([c async for c in client.risk.challenges(limit=10)]) == 1

    page = of("RiskChallengeAccountPage", next_cursor="k2")
    mfx.responses.append(httpx.Response(200, json=page))
    shown = await client.risk.challenge_accounts_page(
        ID, state=["in_progress", "passed"], rule="daily_loss", below_min_days=True, sort="profit"
    )
    assert query(mfx.last) == {
        "state": ["in_progress", "passed"],
        "rule": ["daily_loss"],
        "below_min_days": ["true"],
        "sort": ["profit"],
    }
    assert shown.stats is not None
    mfx.responses += [
        httpx.Response(200, json=page),
        httpx.Response(200, json=of("RiskChallengeAccountPage", next_cursor=None)),
    ]
    assert len([a async for a in client.risk.challenge_accounts(ID)]) == 2  # noqa: PLR2004
    assert query(mfx.last)["cursor"] == ["k2"]
    mfx.responses.append(answer("RiskChallengeAccountDetail"))
    detail = await client.risk.challenge_account(ID, ACCOUNT)
    assert mfx.last.url.path == f"/v1/risk/challenges/{ID}/accounts/{ACCOUNT}"
    assert detail.periods is not None


async def test_activity_is_read_unresolved_first_or_by_time_with_several_values_per_filter(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given Risk Management's activity
    When the tenant reads breaches and actions for two accounts with two outcomes since a time,
    newest first, and walks every page in the default order
    Then the filters go as repeated parameters with the sort, the page keeps its stats, and the
    walk sends no sort but the default and follows the cursor."""
    page = of("RiskActivityPage", next_cursor="a2")
    mfx.responses.append(httpx.Response(200, json=page))
    since = dt.datetime(2026, 11, 14, tzinfo=dt.UTC)
    shown = await client.risk.activity_page(
        kind=["breach", "action"],
        account_id=[ACCOUNT],
        outcome=["unresolved", "failed"],
        start=since,
        sort="newest",
    )
    sent = query(mfx.last)
    assert (sent["kind"], sent["account_id"], sent["outcome"], sent["sort"]) == (
        ["breach", "action"],
        [ACCOUNT],
        ["unresolved", "failed"],
        ["newest"],
    )
    assert shown.stats is not None
    mfx.responses += [
        httpx.Response(200, json=page),
        httpx.Response(200, json=of("RiskActivityPage", next_cursor=None)),
    ]
    assert len([a async for a in client.risk.activity(kind="breach")]) == 2  # noqa: PLR2004
    assert query(mfx.last)["sort"] == ["unresolved_first"] and query(mfx.last)["cursor"] == ["a2"]
    assert json.dumps(page)  # the page is plain JSON, as the platform sends it


def test_risk_events_are_read_as_typed_values_from_the_flat_stream_and_a_webhook_body() -> None:
    """Given risk events as the stream carries them (every value text, nested parts as JSON text,
    an empty string for none) and as a webhook body carries them (JSON)
    When each is read
    Then a rule event names its policy or its challenge, its figures as Decimals and its actions;
    a coverage change its kind and both states; a result its rule; a closed period its
    statistics; a period with none is a ValueError naming it."""
    import mfx  # noqa: PLC0415

    breached = mfx.event_of(
        mfx.StreamMessage(
            "events",
            1,
            "risk.rule_breached",
            {
                "schema_version": "1",
                "account_id": ACCOUNT,
                "rule": "daily_loss",
                "policy_id": ID,
                "challenge_id": "",
                "version": "3",
                "used": "300.5",
                "limit": "300",
                "level": "act",
                "actions": '["notify", "block_entries"]',
                "cleared_by": "",
                "at": "2026-11-14T12:00:00Z",
            },
        )
    )
    assert isinstance(breached, mfx.RiskRuleEvent)
    assert (breached.kind, breached.policy_id, breached.challenge_id) == (
        "risk.rule_breached",
        __import__("uuid").UUID(ID),
        None,
    )
    assert (str(breached.used), breached.actions, breached.cleared_by) == (
        "300.5",
        ("notify", "block_entries"),
        None,
    )
    cleared = mfx.event_of(
        mfx.StreamMessage(
            "events",
            2,
            "risk.rule_cleared",
            {
                "schema_version": "1",
                "account_id": ACCOUNT,
                "rule": "restriction",
                "policy_id": "",
                "challenge_id": ID,
                "version": "",
                "used": "",
                "limit": "",
                "level": "cleared",
                "actions": [],
                "cleared_by": "override",
                "at": "2026-11-14T12:00:00Z",
            },
        )
    )
    assert isinstance(cleared, mfx.RiskRuleEvent)
    assert (cleared.version, cleared.used, cleared.cleared_by) == (None, None, "override")

    changed = mfx.event_of(
        mfx.StreamMessage(
            "events",
            3,
            "risk.coverage_changed",
            {
                "schema_version": "1",
                "account_id": ACCOUNT,
                "kind": "monitoring",
                "from": "healthy",
                "to": "degraded",
                "reason": "reads_old",
                "at": "2026-11-14T12:00:00Z",
            },
        )
    )
    assert isinstance(changed, mfx.RiskCoverageChanged)
    assert (changed.coverage, changed.from_state, changed.to_state) == (
        "monitoring",
        "healthy",
        "degraded",
    )
    result = mfx.event_of(
        mfx.StreamMessage(
            "events",
            4,
            "risk.programme_result",
            {
                "schema_version": "1",
                "challenge_id": ID,
                "version": "2",
                "account_id": ACCOUNT,
                "result": "passed",
                "rule": "",
                "at": "2026-11-14T12:00:00Z",
            },
        )
    )
    assert isinstance(result, mfx.RiskProgrammeResult) and result.rule is None
    period = {
        "kind": "date",
        "start": "2026-11-13T00:00:00Z",
        "end": "2026-11-14T00:00:00Z",
        "state": "closed",
        "stats": {"profit": "120.5", "days_traded": 1},
    }
    closed = mfx.event_of(
        mfx.StreamMessage(
            "events",
            5,
            "risk.period_closed",
            {
                "schema_version": "1",
                "challenge_id": ID,
                "account_id": ACCOUNT,
                "period": json.dumps(period),
                "at": "2026-11-14T00:00:01Z",
            },
        )
    )
    assert isinstance(closed, mfx.RiskPeriodClosed) and closed.period["stats"]["profit"] == "120.5"
    as_webhook = mfx.event_of(
        mfx.StreamMessage(
            "events",
            6,
            "risk.period_closed",
            {
                "schema_version": "1",
                "challenge_id": ID,
                "account_id": ACCOUNT,
                "period": period,
                "at": "2026-11-14T00:00:01Z",
            },
        )
    )
    assert isinstance(as_webhook, mfx.RiskPeriodClosed)
    for missing in ("", None):
        with pytest.raises(ValueError, match="period"):
            mfx.event_of(
                mfx.StreamMessage(
                    "events",
                    7,
                    "risk.period_closed",
                    {
                        "schema_version": "1",
                        "challenge_id": ID,
                        "account_id": ACCOUNT,
                        "period": missing,
                        "at": "2026-11-14T00:00:01Z",
                    },
                )
            )

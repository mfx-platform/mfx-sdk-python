"""A tenant's own Expert Advisor through the SDK."""

from __future__ import annotations

import base64
from typing import Any

import httpx
import pytest

from mfx import EaRecord, EaTelemetry, EaTelemetryLost, telemetry_of
from mfx.client import MfxClient
from mfx.errors import ConflictError, ForbiddenError
from mfx.streaming import Channel, StreamMessage

from .conftest import TERMINAL_ID, FakeMfx, body_of

EA_ID = "06ad13b0-7371-756e-8000-beebf2c73ccd"
OP_ID = "06ad13b8-deea-76b5-8000-b18f3301ec52"
SOURCE = "#property strict\nint OnInit() { return INIT_SUCCEEDED; }\n"


def _version(
    state: str = "uploaded", verdict: str | None = None, **overrides: Any
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "id": EA_ID, "name": "lane3-cycle", "version": 4, "state": state, "verdict": verdict,
        "findings": {"red": 0, "amber": 0, "note": 2}, "policy_version": 1,
        "analysers": [{"analyser": "scan", "state": "done", "finished_at": None, "failure": None}],
        "source_sha256": "69e2" * 16, "build_sha256": None,
        "size_bytes": 4819, "file_count": 1, "terminals": [], "decision": None,
        "source_kept_until": None, "source_deleted_at": None,
        "created_at": "2026-10-15T20:43:51Z",
    }  # fmt: skip
    body.update(overrides)
    return body


def _operation(state: str) -> dict[str, Any]:
    return {"operation_id": OP_ID, "kind": "attach", "terminal_id": TERMINAL_ID, "state": state,
            "requested_by": "tenant", "reason": "attach", "forced_stop": None, "step": None,
            "timeline": [{"at": "2026-10-15T20:46:05Z", "state": "ACCEPTED"}],
            "cooldown_until": None, "created_at": "2026-10-15T20:46:05Z",
            "finished_at": None}  # fmt: skip


async def test_a_version_is_uploaded_as_its_source_text_and_waited_for_until_its_checks_settle_it(
    client: MfxClient, mfx: FakeMfx, sleeps: list[float]
) -> None:
    """Given an expert's source, one .mq5 and an .mqh, as text or bytes
    When the tenant uploads it and waits for the verdict
    Then one POST /expert-advisors carries the name and each file's path and UTF-8 source in
    base64 with the idempotency key; the wait reads the version until it is approved, held,
    rejected, withdrawn or revoked, pausing longer each time, and answers it; and a wait whose time
    runs out answers the version as it stands rather than raising."""
    mfx.responses.append(httpx.Response(202, json=_version()))
    version = await client.expert_advisors.upload(
        "lane3-cycle", {"cycle.mq5": SOURCE, "mfx.mqh": SOURCE.encode()}, idempotency_key="up-1"
    )
    request = mfx.last
    assert (request.method, request.url.path) == ("POST", "/v1/expert-advisors")
    assert request.headers["Idempotency-Key"] == "up-1"
    sent = body_of(request)
    assert sent["name"] == "lane3-cycle"
    assert [(f["path"], base64.b64decode(f["content_base64"]).decode()) for f in sent["files"]] == [
        ("cycle.mq5", SOURCE), ("mfx.mqh", SOURCE),
    ]  # fmt: skip
    assert version.state.value == "uploaded"

    for state, verdict in (("analysing", None), ("judged", "green"), ("approved", "green")):
        mfx.responses.append(httpx.Response(200, json=_version(state, verdict)))
    settled = await client.expert_advisors.wait_for_verdict(EA_ID)
    assert (settled.state.value, settled.verdict.value) == ("approved", "green")
    assert sleeps[-2:] == [2.0, 4.0], "longer each time"

    mfx.responses.append(httpx.Response(200, json=_version("analysing")))
    still = await client.expert_advisors.wait_for_verdict(EA_ID, timeout_s=0)
    assert still.state.value == "analysing" and still.verdict is None


async def test_versions_are_listed_read_reported_and_withdrawn(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant's versions over two pages
    When it lists them, reads one, asks for its report and withdraws it
    Then the list follows the cursor to the end; the read and the report are GETs on the
    version; a report asked for before the verdict is the platform's 409 as a ConflictError; and the
    withdrawal is a DELETE with the idempotency key."""
    mfx.responses.append(httpx.Response(200, json={"items": [_version()], "next_cursor": "c2"}))
    mfx.responses.append(
        httpx.Response(200, json={"items": [_version(version=3)], "next_cursor": None})
    )
    listed = [v async for v in client.expert_advisors.list(limit=1)]
    assert [v.version for v in listed] == [4, 3]
    assert dict(mfx.requests[-1].url.params) == {"cursor": "c2", "limit": "1"}

    mfx.responses.append(httpx.Response(200, json=_version("approved", "green")))
    assert (await client.expert_advisors.get(EA_ID)).verdict.value == "green"
    report = {
        "policy_version": 1,
        "verdict": "green",
        "summary": None,
        "categories": [{"group": "security", "colour": "green", "findings": 0}],
        "findings": [
            {
                "rule_id": "BST-02",
                "group": "best_practice",
                "name": "n",
                "colour": "note",
                "found_by": "rules",
                "file": "cycle.mq5",
                "line_from": 3,
                "line_to": 3,
                "evidence": None,
                "why": "w",
                "change": None,
            }
        ],
    }
    mfx.responses.append(httpx.Response(200, json=report))
    read = await client.expert_advisors.report(EA_ID)
    assert mfx.last.url.path == f"/v1/expert-advisors/{EA_ID}/report"
    assert read.findings[0].rule_id == "BST-02"
    mfx.responses.append(
        httpx.Response(409, json={"error": {"code": "conflict", "message": "no verdict yet"}})
    )
    with pytest.raises(ConflictError):
        await client.expert_advisors.report(EA_ID)

    mfx.responses.append(httpx.Response(200, json=_version("withdrawn")))
    gone = await client.expert_advisors.delete(EA_ID, idempotency_key="wd-1")
    assert (mfx.last.method, mfx.last.url.path) == ("DELETE", f"/v1/expert-advisors/{EA_ID}")
    assert mfx.last.headers["Idempotency-Key"] == "wd-1" and gone.state.value == "withdrawn"


async def test_a_version_is_attached_followed_to_the_end_of_its_operation_and_detached(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an approved version and a terminal on a customer-code farm
    When the tenant attaches it, waits for the operation and later detaches it
    Then the attach is one PUT with the version, symbol, timeframe and reason; the wait reads the
    operation until it is over (SUCCEEDED, FAILED, NOT_STARTED, EXPIRED, CANCELLED or SUPERSEDED)
    and answers it, or answers it as it stands when the time runs out; and the detach is one
    DELETE carrying its reason as the route asks."""
    mfx.responses.append(httpx.Response(202, json={"operation_id": OP_ID, "state": "ACCEPTED"}))
    accepted = await client.terminals.attach_expert_advisor(
        TERMINAL_ID, EA_ID, symbol="EURUSD", timeframe="M1", reason="the cycle",
        idempotency_key="at-1",
    )  # fmt: skip
    assert (mfx.last.method, mfx.last.url.path) == (
        "PUT",
        f"/v1/terminals/{TERMINAL_ID}/expert-advisor",
    )
    assert body_of(mfx.last) == {"expert_advisor_id": EA_ID, "symbol": "EURUSD", "timeframe": "M1",
                                 "reason": "the cycle", "queue": False,
                                 "confirm_open_positions": False}  # fmt: skip
    assert str(accepted.operation_id) == OP_ID

    for state in ("ACCEPTED", "RELAUNCHING", "SUCCEEDED"):
        mfx.responses.append(httpx.Response(200, json=_operation(state)))
    done = await client.terminals.wait_for_operation(TERMINAL_ID, OP_ID)
    assert done.state.value == "SUCCEEDED"
    assert mfx.last.url.path == f"/v1/terminals/{TERMINAL_ID}/operations/{OP_ID}"
    mfx.responses.append(httpx.Response(200, json=_operation("CLOSING")))
    running = await client.terminals.wait_for_operation(TERMINAL_ID, OP_ID, timeout_s=0)
    assert running.state.value == "CLOSING"

    mfx.responses.append(httpx.Response(202, json={"operation_id": OP_ID, "state": "ACCEPTED"}))
    await client.terminals.detach_expert_advisor(TERMINAL_ID, reason="done", idempotency_key="dt-1")
    assert (mfx.last.method, mfx.last.url.path) == (
        "DELETE",
        f"/v1/terminals/{TERMINAL_ID}/expert-advisor",
    )
    assert mfx.last.url.params["reason"] == "done"


async def test_live_trading_is_confirmed_with_the_code_and_a_refused_code_says_nothing_more(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a terminal whose attachment waits for confirmation after a green trial
    When the tenant confirms with the one-time code, and again with a wrong one
    Then the first is one POST carrying the code and answers the attachment running; the second
    is the platform's 403 confirmation_refused as a ForbiddenError, which does not say why."""
    mfx.responses.append(httpx.Response(200, json={
        "terminal_id": TERMINAL_ID, "expert_advisor": {"id": EA_ID, "label": "lane3-cycle v4"},
        "state": "running", "since": "2026-10-15T21:03:41Z", "symbol": "EURUSD",
        "timeframe": "M1"}))  # fmt: skip
    attachment = await client.terminals.confirm_expert_advisor(TERMINAL_ID, code="482915")
    assert (mfx.last.method, mfx.last.url.path) == (
        "POST", f"/v1/terminals/{TERMINAL_ID}/expert-advisor/confirm",
    )  # fmt: skip
    assert body_of(mfx.last) == {"code": "482915"} and attachment.state.value == "running"
    mfx.responses.append(httpx.Response(403, json={"error": {"code": "confirmation_refused",
                                                             "message": "refused"}}))  # fmt: skip
    with pytest.raises(ForbiddenError) as refused:
        await client.terminals.confirm_expert_advisor(TERMINAL_ID, code="000000")
    assert refused.value.code == "confirmation_refused"


async def test_the_tenants_contacts_are_read_with_their_roles(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant whose contacts an operator set
    When it reads them
    Then one GET /tenant/contacts answers each with its role, name and email."""
    mfx.responses.append(httpx.Response(200, json={"items": [{
        "id": EA_ID, "role": "representative", "name": "R", "email": "r@example.com",
        "mobile": None, "updated_at": "2026-10-07T10:00:00Z"}]}))  # fmt: skip
    contacts = await client.tenant.contacts()
    assert mfx.last.url.path == "/v1/tenant/contacts"
    assert [(c.role.value, c.email) for c in contacts.items] == [
        ("representative", "r@example.com")
    ]


def test_an_experts_telemetry_reads_as_numbered_records_and_a_loss_says_how_much() -> None:
    """Given messages on a terminal's ea channel
    When the caller reads them with telemetry_of
    Then a telemetry batch is its records in order, each with the segment and line it came from
    and the record as the expert wrote it, with skipped and dropped; a loss names the discarded
    segments and how many records they held; and any other message is not telemetry."""
    channel = Channel.ea(TERMINAL_ID)
    batch = telemetry_of(
        StreamMessage(
            channel=channel,
            seq=5,
            type="expert_advisor.telemetry",
            data={
                "schema_version": "1",
                "skipped": 1,
                "dropped": 0,
                "records": [
                    {"segment": 3, "line": 10, "record": {"kind": "signal", "n": 4}},
                    {"segment": 3, "line": 11, "record": {"kind": "signal", "n": 5}},
                ],
            },
        )
    )
    assert batch == EaTelemetry(
        channel=channel,
        seq=5,
        skipped=1,
        dropped=0,
        records=(
            EaRecord(3, 10, {"kind": "signal", "n": 4}),
            EaRecord(3, 11, {"kind": "signal", "n": 5}),
        ),
    )
    lost = telemetry_of(
        StreamMessage(
            channel=channel,
            seq=6,
            type="expert_advisor.telemetry_lost",
            data={"schema_version": "1", "segment_from": 1, "segment_to": 2, "records": 40},
        )
    )
    assert lost == EaTelemetryLost(channel=channel, seq=6, segment_from=1, segment_to=2, records=40)
    empty = telemetry_of(
        StreamMessage(channel=channel, seq=7, type="expert_advisor.telemetry", data={"records": []})
    )
    assert isinstance(empty, EaTelemetry) and empty.records == () and empty.skipped == 0
    assert telemetry_of(StreamMessage(channel="events", seq=1, type="md.book", data={})) is None


async def test_a_failed_trial_is_read_on_the_version_and_in_the_report_after_it_ended(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a version whose trial failed and whose expert the platform took off the terminal
    When the tenant reads the version and its report
    Then the version keeps its last trial with the reason it ended and every figure, and counts
    the trials failed of those judged; and the report carries the trial's verdict, the finding
    of each rule it crossed and the figures, while the version's own verdict stays its checks'."""
    figure = {
        "key": "cpu_peak",
        "label": "Processor, worst minute",
        "value": 84.0,
        "display": "84 % of its cap",
        "grade": "amber",
    }
    trial = {
        "state": "ended",
        "started_at": "2026-10-16T16:01:25Z",
        "ended_at": "2026-10-16T16:31:55Z",
        "minutes": 30,
        "verdict": "amber",
        "figures": [figure],
    }
    mfx.responses.append(
        httpx.Response(
            200,
            json=_version(
                "approved",
                "green",
                trials={"failed": 1, "judged": 2},
                last_trial={
                    "terminal_id": TERMINAL_ID,
                    "state": "detached",
                    "symbol": "EURUSD",
                    "timeframe": "M1",
                    "ended_at": "2026-10-16T16:31:55Z",
                    "ended_reason": "trial_failed",
                    "trial": trial,
                },
            ),
        )
    )
    version = await client.expert_advisors.get(EA_ID)
    last = version.last_trial
    assert (last.state.value, last.ended_reason.value) == ("detached", "trial_failed")
    assert (
        last.trial.verdict.value == "amber" and last.trial.figures[0].display == "84 % of its cap"
    )
    assert (version.trials.failed, version.trials.judged) == (1, 2)
    assert version.verdict.value == "green", "a trial colours the attachment, not the version"

    finding = {
        "rule_id": "PRF-08",
        "group": "performance",
        "name": "n",
        "colour": "amber",
        "found_by": "trial",
        "file": None,
        "line_from": None,
        "line_to": None,
        "evidence": "84 % of its cap in its worst minute",
        "why": "w",
        "change": None,
    }
    mfx.responses.append(
        httpx.Response(
            200,
            json={
                "policy_version": 1,
                "verdict": "green",
                "summary": None,
                "categories": [],
                "findings": [],
                "trial": {
                    "terminal_id": TERMINAL_ID,
                    "ended_at": "2026-10-16T16:31:55Z",
                    "verdict": "amber",
                    "findings": [finding],
                    "reason": "PRF-08: 84 % of its cap",
                    "figures": [figure],
                },
            },
        )
    )
    report = await client.expert_advisors.report(EA_ID)
    assert report.verdict.value == "green" and report.trial.verdict.value == "amber"
    assert [f.rule_id for f in report.trial.findings] == ["PRF-08"]

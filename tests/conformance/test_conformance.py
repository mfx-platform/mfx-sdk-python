"""The Python SDK passes the shared SDK test suite: every case, played back by the suite's fake MFX
Hub on localhost, through this SDK's public surface.

This file is the Python runner. It holds no rule: it starts the fake hub, asks it for each case,
turns the case's neutral operation into the Python call, and checks what came back against the
case and against the hub's verdict on what was sent. The rules are the suite's
(``suite/cases``), vendored at the version in ``suite-version.txt``.
"""

from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
from collections.abc import Iterator
from decimal import Decimal
from pathlib import Path
from typing import Any

import httpx
import pytest

import mfx
from mfx import errors
from mfx.signing import SigningKey, signing_message

SUITE = Path(__file__).resolve().parent / "suite"
VOCABULARY = json.loads((SUITE / "vocabulary.json").read_text(encoding="utf-8"))
#: Cases this SDK does not pass yet, each with the reason. Empty at 1.0 (the suite's rule).
NOT_YET: dict[str, str] = json.loads(
    (Path(__file__).resolve().parent / "not-yet.json").read_text(encoding="utf-8")
)
#: The suite's neutral error kinds, as this SDK's classes.
KINDS: dict[str, type[Exception]] = {
    "ApiError": errors.MfxApiError,
    "TransportError": errors.MfxTransportError,
    "Timeout": errors.MfxTimeout,
    **{name: getattr(errors, name) for name in VOCABULARY["errors"] if hasattr(errors, name)},
}


def _case_ids() -> list[str]:
    ids: list[str] = []
    for path in sorted((SUITE / "cases").glob("*.json")):
        ids += [case["id"] for case in json.loads(path.read_text(encoding="utf-8"))]
    return ids


@pytest.fixture(scope="module")
def hub() -> Iterator[str]:
    """The suite's fake hub, on a free local port, for this module; its base URL."""
    env = {**os.environ, "PYTHONPATH": str(SUITE)}
    process = subprocess.Popen(  # noqa: S603 - fixed argv, this interpreter
        [sys.executable, "-m", "mfx_fake_hub", "--cases", str(SUITE / "cases")],
        stdout=subprocess.PIPE,
        text=True,
        env=env,
    )
    assert process.stdout is not None
    line = process.stdout.readline().strip()
    assert line.startswith("listening "), line
    yield line.removeprefix("listening ")
    process.terminate()
    process.wait(timeout=10)


def _value(raw: Any) -> Any:  # noqa: ANN401 - a case's JSON value
    """A case argument as Python: ``$decimal`` is a Decimal, ``$float`` a float."""
    if isinstance(raw, dict) and "$decimal" in raw:
        return Decimal(raw["$decimal"])
    if isinstance(raw, dict) and "$float" in raw:
        return float(raw["$float"])
    return raw


async def _call(client: mfx.MfxClient, op: str, args: dict[str, Any]) -> dict[str, Any]:
    """Make the case's call through this SDK and describe what came back in the suite's names."""
    a = {name: _value(value) for name, value in args.items()}
    if op == "signing.sign":
        key = SigningKey(base64.b64encode(bytes.fromhex(VOCABULARY["key"]["seed_hex"])).decode())
        message = signing_message(
            a["timestamp"], a["nonce"], a["method"], a["path_with_query"], a["body"].encode()
        )
        return {"signature": key.sign(message)}
    if op == "terminals.get":
        terminal = await client.terminals.get(a["terminal_id"])
        return {"id": str(terminal.id), "state": str(terminal.state)}
    if op == "terminals.page":
        page = await client.terminals.page(cursor=a.get("cursor"), limit=a.get("limit"))
        return {"count": len(page), "next_cursor": page.next_cursor}
    if op == "terminals.list":
        return {"ids": [str(t.id) async for t in client.terminals.list()]}
    if op == "terminals.create":
        terminal = await client.terminals.create(**a)
        return {"id": str(terminal.id), "state": str(terminal.state)}
    if op == "execution.place_order":
        result = await client.execution.place_order(a.pop("terminal_id"), **a)
        return {
            "ok": result.ok,
            "state": str(result.state) if result.state else None,
            "command_id": result.command_id,
            "duplicate": result.duplicate,
            "retryable": result.retryable,
        }
    if op == "catalog.quote":
        quote = await client.catalog.quote(a["broker_id"], a["symbol"])
        return {"bid": quote.bid, "ask": quote.ask, "age_s": quote.age_s, "state": str(quote.state)}
    raise AssertionError(f"this runner does not know the operation {op!r}")


def _same(got: Any, want: Any) -> bool:  # noqa: ANN401 - JSON values
    if isinstance(want, dict) and "$decimal" in want:
        return got is not None and Decimal(str(got)) == Decimal(want["$decimal"])
    return bool(got == want)


async def _noop(_: float) -> None:
    """The client's sleep: a retry is decided as the server said, without waiting for it."""


@pytest.mark.parametrize("case_id", _case_ids())
async def test_the_sdk_passes_every_case_of_the_shared_suite(hub: str, case_id: str) -> None:
    """Given a case of the shared SDK test suite, played back by the suite's fake MFX Hub
    When this SDK makes the case's call, signed with the suite's test key
    Then it returns, raises or refuses exactly as the case observes, and the hub's verdict is that
    every request the case expects arrived in order, signed and shaped as the case says, and
    nothing else did. A case listed in not-yet.json is expected to fail, for the reason given."""
    if case_id in NOT_YET:
        pytest.xfail(NOT_YET[case_id])
    control = httpx.AsyncClient(base_url=hub.removesuffix("/v1"))
    case = (await control.post("/_hub/case", json={"id": case_id})).json()
    seed = base64.b64encode(bytes.fromhex(VOCABULARY["key"]["seed_hex"])).decode()
    observe = case["observe"]
    async with mfx.MfxClient(hub, VOCABULARY["key"]["id"], seed, sleep=_noop) as client:
        if "raises" in observe:
            with pytest.raises(KINDS[observe["raises"]]) as raised:
                await _call(client, case["call"]["op"], case["call"]["args"])
            for name, want in observe.get("fields", {}).items():
                assert getattr(raised.value, name) == want, name
        elif "refuses" in observe:
            assert observe["refuses"] == "invalid_argument"
            with pytest.raises((TypeError, ValueError)):
                await _call(client, case["call"]["op"], case["call"]["args"])
        else:
            got = await _call(client, case["call"]["op"], case["call"]["args"])
            for name, want in observe["returns"].items():
                assert _same(got[name], want), f"{name}: {got[name]!r}, the case wants {want!r}"
    verdict = (await control.get("/_hub/verdict")).json()
    await control.aclose()
    assert verdict["ok"], "\n".join(verdict["problems"])

"""The trailing stop and the farms have typed methods, and what the SDK leaves to plain HTTPS is
listed in the README from the contract itself."""

from __future__ import annotations

import json
import re
from decimal import Decimal
from pathlib import Path
from typing import Any

import httpx
import pytest
import yaml

from mfx.client import MfxClient
from mfx.results import CommandState, Reason

from .conftest import FARM_ID, TERMINAL_ID, FakeMfx, error, page

COMMAND_ID = "0191f0c2-bbbb-7ccc-8ddd-000000000002"
REPO = Path(__file__).resolve().parents[2]


def _accepted() -> httpx.Response:
    return httpx.Response(
        202, json={"command_id": COMMAND_ID, "state": "ACCEPTED", "duplicate": False}
    )


async def test_a_trailing_stop_is_set_with_a_decimal_distance_and_cleared_as_a_command(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an open position
    When its trailing stop is set with a decimal distance, set with a float, refused for its stops
    level, and cleared
    Then the set is one PUT to the position's trailing-stop route carrying the distance as the
    decimal text it was given, under its idempotency key, answered as an accepted command; a float
    is refused before anything is sent; a refusal is a result naming the reason, never an
    exception; and the clear is one DELETE to the same route."""
    mfx.responses.append(_accepted())
    result = await client.execution.set_trailing_stop(
        TERMINAL_ID, 8811, distance=Decimal("0.0020"), idempotency_key="trail-1"
    )
    request = mfx.last
    assert (request.method, request.url.path) == (
        "PUT", f"/v1/terminals/{TERMINAL_ID}/positions/8811/trailing-stop",
    )  # fmt: skip
    assert json.loads(request.content) == {"distance": "0.0020"}
    assert request.headers["Idempotency-Key"] == "trail-1"
    assert result.command_id == COMMAND_ID and result.state is CommandState.ACCEPTED

    sent = len(mfx.requests)
    with pytest.raises(TypeError):
        await client.execution.set_trailing_stop(
            TERMINAL_ID,
            8811,
            distance=0.002,
            idempotency_key="trail-2",  # type: ignore[arg-type]
        )
    assert len(mfx.requests) == sent, "a float never leaves the SDK"

    mfx.responses.append(error(422, "invalid_stops", "inside the stops level"))
    refused = await client.execution.set_trailing_stop(
        TERMINAL_ID, 8811, distance="0.00001", idempotency_key="trail-3"
    )
    assert refused.ok is False and refused.reason is Reason.REFUSED
    assert refused.detail is not None and "invalid_stops" in refused.detail

    mfx.responses.append(_accepted())
    cleared = await client.execution.clear_trailing_stop(
        TERMINAL_ID, 8811, idempotency_key="trail-4"
    )
    assert (mfx.last.method, mfx.last.url.path) == (
        "DELETE", f"/v1/terminals/{TERMINAL_ID}/positions/8811/trailing-stop",
    )  # fmt: skip
    assert mfx.last.headers["Idempotency-Key"] == "trail-4"
    assert cleared.command_id == COMMAND_ID


def _farm(name: str) -> dict[str, Any]:
    return {
        "id": FARM_ID,
        "name": name,
        "os": "windows",
        "region": "uksouth",
        "usages": ["quote_streaming"],
        "redundancy": "none",
        "refresh_ms": 500,
        "instruments_max": 100,
        "status": "active",
    }


async def test_the_farms_the_plan_allows_are_listed_following_the_cursor_and_read_one_by_one(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given two pages of farms
    When the farms are listed and one is read
    Then the list follows the cursor to the last page from GET /farms, and the read is GET
    /farms/{id}."""
    mfx.responses.append(page([_farm("dev-uk-west")], "c2"))
    mfx.responses.append(page([_farm("dev-uk-south")], None))
    farms = [farm async for farm in client.farms.list(limit=1)]
    assert [farm.name for farm in farms] == ["dev-uk-west", "dev-uk-south"]
    assert mfx.requests[-2].url.path == "/v1/farms"
    assert mfx.requests[-1].url.params["cursor"] == "c2"

    mfx.responses.append(httpx.Response(200, json=_farm("dev-uk-west")))
    farm = await client.farms.get(FARM_ID)
    assert mfx.last.url.path == f"/v1/farms/{FARM_ID}" and farm.name == "dev-uk-west"


def _unwrapped() -> set[str]:
    """The contract's tenant operations that no module of the SDK calls."""
    spec = yaml.safe_load((REPO / "spec" / "openapi.yaml").read_text(encoding="utf-8"))
    operations = {
        op["operationId"]
        for path, item in spec["paths"].items()
        if not path.startswith(("/admin", "/fleet"))
        for op in item.values()
        if isinstance(op, dict) and "operationId" in op
    }
    used: set[str] = set()
    for module in (REPO / "src" / "mfx").glob("*.py"):
        text = module.read_text(encoding="utf-8")
        used |= set(re.findall(r"_generated\.api\.\w+ import \(?\s*(\w+)", text))

    def snake(name: str) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()

    return {op for op in operations if snake(op) not in used} - {"openStream"}


def test_the_readme_lists_exactly_the_contracts_operations_the_sdk_leaves_to_plain_https() -> None:
    """Given the vendored contract and the SDK's modules
    When the tenant operations no module calls are worked out
    Then they are exactly the README's REST-only table - the stream aside, which is the WebSocket
    - so a method added, or an operation added to the contract, cannot leave the list wrong."""
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    table = readme.split("<!-- rest-only:start -->")[1].split("<!-- rest-only:end -->")[0]
    listed = set(re.findall(r"^\| `(\w+)` \|", table, flags=re.MULTILINE))
    assert listed == _unwrapped()
    assert {"setTrailingStop", "clearTrailingStop", "listFarms", "getFarm"}.isdisjoint(listed)

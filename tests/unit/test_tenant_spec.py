"""The cut between the vendored spec and the generator.

``tools/tenant_spec.py`` decides what a customer's wheel contains. Two ways for it to be wrong, and
they fail in opposite directions:

* **too little cut** — an operator endpoint ships to tenants, the thing this exists to stop;
* **too much cut** — a tenant schema disappears and the SDK silently loses part of its own surface,
  or the generator meets a dangling ``$ref``.

So it is asserted both ways, and against the **real vendored spec** rather than only a fixture: the
fixture pins the semantics, the real spec is what actually ships.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))

from generate import (  # noqa: E402 - after the path insert, by necessity
    GeneratorDroppedSchemaError,
    _module_name,
    dropped_schemas,
)
from tenant_spec import ADMIN_PREFIX, tenant_only  # noqa: E402 - after the path insert

#: The Story these cases are Tested By: generated core + ergonomic layer + conformance suite.

SCHEMAS = "#/components/schemas/"


@pytest.fixture(scope="module")
def whole() -> dict[str, Any]:
    return yaml.safe_load((REPO / "spec" / "openapi.yaml").read_text(encoding="utf-8"))


def _refs(node: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(node, dict):
        target = node.get("$ref")
        if isinstance(target, str):
            found.add(target)
        for value in node.values():
            found |= _refs(value)
    elif isinstance(node, list):
        for value in node:
            found |= _refs(value)
    return found


def test_the_wheel_carries_every_tenant_path_and_no_operator_one(whole: dict[str, Any]) -> None:
    """Given the vendored spec, which is the public contract / When the tenant half is cut for the
    generator / Then every path survives, none is an operator's, and the vendored file itself
    carries no operator route and no internal annotation.

    The SDK vendors the public contract, never the internal one, so the operator
    surface is not in this repository at all; the cut stays as a second net, and on the public file
    it removes nothing."""
    cut = tenant_only(whole)

    expected = [p for p in whole["paths"] if not p.startswith(ADMIN_PREFIX)]
    assert list(cut["paths"]) == expected, "every tenant path, in the same order"
    assert expected, "the fixture would pass vacuously on a spec with no tenant paths"
    assert not [p for p in cut["paths"] if p.startswith(ADMIN_PREFIX)]
    assert not [p for p in whole["paths"] if p.startswith(ADMIN_PREFIX)], (
        "public: no operator route"
    )
    assert "x-mfx-" not in yaml.safe_dump(whole), "public: no internal annotation"


def test_nothing_the_generator_would_choke_on_survives_the_cut(whole: dict[str, Any]) -> None:
    """A pruned schema that something kept still refers to is a dangling `$ref`, and the generator
    meets it as a crash or a silently dropped model. This is the assertion that makes pruning safe
    to do at all."""
    cut = tenant_only(whole)
    kept = set(cut["components"]["schemas"])

    dangling = sorted(
        r for r in _refs(cut) if r.startswith(SCHEMAS) and r[len(SCHEMAS) :] not in kept
    )

    assert dangling == []


def test_the_vendored_spec_is_not_modified(whole: dict[str, Any]) -> None:
    """The cut is a copy. The vendored file stays exactly the public contract the platform
    publishes, which is what lets it be diffed against the source to prove it has not drifted."""
    before = yaml.safe_dump(whole, sort_keys=True)

    tenant_only(whole)

    assert yaml.safe_dump(whole, sort_keys=True) == before


def test_a_schema_only_an_operator_reaches_goes_and_a_deeply_reached_one_stays() -> None:
    """The walk is transitive in both directions, which a name-based filter cannot be.

    `TenantOnly` is reached from a tenant path three hops down and must stay. `OperatorOnly` is
    reached only from an admin path and must go — and note it is not named `admin_*`, which is
    exactly how an exclude list starts missing things (`BrokerDetail`, `ServerDisable`,
    `EnrollmentRequest` are all real examples in this spec)."""
    spec = {
        "paths": {
            "/v1/terminals": {"get": {"responses": {"200": {"$ref": "#/components/schemas/Hop1"}}}},
            "/admin/v1/brokers": {
                "get": {"responses": {"200": {"$ref": "#/components/schemas/OperatorOnly"}}}
            },
        },
        "components": {
            "schemas": {
                "Hop1": {"properties": {"next": {"$ref": "#/components/schemas/Hop2"}}},
                "Hop2": {"properties": {"next": {"$ref": "#/components/schemas/TenantOnly"}}},
                "TenantOnly": {"type": "string"},
                "OperatorOnly": {
                    "properties": {"x": {"$ref": "#/components/schemas/OperatorDeep"}}
                },
                "OperatorDeep": {"type": "string"},
                "ReachedByNobody": {"type": "string"},
            }
        },
    }

    kept = set(tenant_only(spec)["components"]["schemas"])

    assert {"Hop1", "Hop2", "TenantOnly"} <= kept, "transitively reachable from a tenant path"
    assert "OperatorOnly" not in kept and "OperatorDeep" not in kept
    assert "ReachedByNobody" not in kept, "a schema nothing reaches is not worth shipping either"


def test_a_schema_a_shared_component_names_is_kept() -> None:
    """Parameters and responses are kept whole, because both surfaces share them. A schema named
    only from one of those is still reachable and must not be pruned — otherwise the cut breaks a
    tenant path through a component it does not mention directly."""
    spec = {
        "paths": {"/admin/v1/x": {"get": {"responses": {"200": {"description": "ok"}}}}},
        "components": {
            "responses": {"Error": {"content": {"schema": {"$ref": "#/components/schemas/Error"}}}},
            "schemas": {"Error": {"type": "object"}, "Unused": {"type": "string"}},
        },
    }

    kept = set(tenant_only(spec)["components"]["schemas"])

    assert "Error" in kept, "named by a shared response, so it stays even with no tenant path"
    assert "Unused" not in kept


# --------------------------------------------------------------------------------------
# The generator dropping a schema without saying so
# --------------------------------------------------------------------------------------


def _generated(tmp_path: Path, *modules: str) -> Path:
    out = tmp_path / "generated"
    (out / "models").mkdir(parents=True)
    for module in modules:
        (out / "models" / f"{module}.py").write_text("", encoding="utf-8")
    return out


def test_a_schema_the_generator_wrote_no_model_for_is_reported(tmp_path: Path) -> None:
    """Given a spec declaring two schemas and a generator that wrote a model for only one / When the
    output is checked / Then the missing one is named.

    openapi-python-client **exits 0** when it cannot express a shape: no model, no message. First
    sign is an ImportError or a missing type long afterwards."""
    spec = {"components": {"schemas": {"TenantTerminal": {}, "FarmCreate": {}}}}

    assert dropped_schemas(spec, _generated(tmp_path, "tenant_terminal")) == ["FarmCreate"]


def test_nothing_is_reported_when_every_schema_has_its_model(tmp_path: Path) -> None:
    """The negative control: a complete generation is silent, or it would block every build."""
    spec = {"components": {"schemas": {"TenantTerminal": {}, "Spread": {}}}}

    assert dropped_schemas(spec, _generated(tmp_path, "tenant_terminal", "spread")) == []


def test_a_generator_that_wrote_nothing_at_all_is_reported(tmp_path: Path) -> None:
    """No models directory is not "nothing was declared" — it is the worst case, and every schema is
    missing."""
    spec = {"components": {"schemas": {"Spread": {}}}}

    assert dropped_schemas(spec, tmp_path / "never-written") == ["Spread"]


def test_a_spec_with_no_schemas_is_not_an_error(tmp_path: Path) -> None:
    spec: dict[str, Any] = {"components": {}}

    assert dropped_schemas(spec, _generated(tmp_path)) == []


@pytest.mark.parametrize(
    ("schema", "module"),
    [
        ("FarmCreate", "farm_create"),
        ("TenantTerminal", "tenant_terminal"),
        ("Spread", "spread"),
        ("SpreadList", "spread_list"),
    ],
)
def test_the_module_name_matches_what_the_generator_writes(schema: str, module: str) -> None:
    """The comparison is by module name, so it has to agree with the generator's own naming."""
    assert _module_name(schema) == module


def test_the_guard_would_have_caught_the_case_that_prompted_it(tmp_path: Path) -> None:
    """`sweep_hz: {type: number, enum: [0.5, 1, 2, 5]}` is a numeric enum, which
    openapi-python-client cannot model, so it dropped `FarmCreate` in silence.

    The tenant client never saw it — `FarmCreate` is reachable only from `/admin/v1/farms`, so
    `tenant_only` prunes it — but nothing would have said so if it were a tenant schema.
    """
    spec = {
        "components": {
            "schemas": {
                "FarmCreate": {
                    "type": "object",
                    "properties": {"sweep_hz": {"type": "number", "enum": [0.5, 1, 2, 5]}},
                }
            }
        }
    }

    missing = dropped_schemas(spec, _generated(tmp_path))

    assert missing == ["FarmCreate"]
    assert "sweep_hz" in str(GeneratorDroppedSchemaError(missing)), "and the error says why"

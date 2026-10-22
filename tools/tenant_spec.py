"""The tenant half of the spec, cut from the whole one.

``spec/openapi.yaml`` is vendored **whole**, because it says so itself: it is the single source that
the platform and this SDK are both produced from, and a trimmed copy could not be diffed
against the original to prove it had not drifted.

But the whole spec includes the admin surface, and this package is what a *customer* installs. The
admin API is served only by the operator console, behind Cloudflare Access, and answers 404 on any
``api.`` host — so shipping a generated client for it gives a tenant nothing but a tab-completable
list of operator endpoints, their request bodies and their state machines. The full contract is
internal and never published; a customer wheel carrying the shape of every operator endpoint would
publish precisely what keeping it internal keeps in.

So the cut happens here, between the vendored file and the generator:

* the vendored spec stays whole and canonical, and the drift job still means something, because it
  re-runs this same deterministic filter;
* the generated package contains no admin operation and no admin-only schema, so there is nothing
  to exclude at build time and nothing to remember at publish time.

**Why not an exclude list in ``pyproject.toml``.** Two reasons, both found by trying. The admin
*endpoints* can be excluded from a wheel safely, but the admin *models* cannot: the generator writes
one ``models/__init__.py`` that imports every model by name, so removing those files breaks
``import mfx`` outright. And a name-based list misses the admin-only schemas that are not called
``admin_*`` — ``BrokerDetail``, ``ServerDisable``, ``EnrollmentRequest``, ``CellDrainState`` — and
goes on missing each new one silently. Reachability is the only filter that cannot rot.
"""

from __future__ import annotations

from typing import Any

__all__ = ["ADMIN_PREFIX", "tenant_only"]

#: Every operator path. The spec's own convention, and the thing `mfx-adminbff` alone serves.
ADMIN_PREFIX = "/admin/"

#: Component sections whose members are pruned when nothing reachable refers to them. `schemas` is
#: the one that matters; the others are small and kept whole so a response or parameter shared by
#: both surfaces cannot vanish from under a tenant path.
_PRUNED_SECTIONS = ("schemas",)


def _refs(node: Any) -> set[str]:
    """Every ``$ref`` string anywhere beneath ``node``."""
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


def _named(ref: str, section: str) -> str | None:
    """``#/components/schemas/Foo`` → ``Foo``, for the section asked about."""
    prefix = f"#/components/{section}/"
    return ref[len(prefix) :] if ref.startswith(prefix) else None


def tenant_only(spec: dict[str, Any]) -> dict[str, Any]:
    """``spec`` without the admin paths, and without the schemas only they reached.

    Pure: the input is not modified, so a caller can diff the two. The walk is transitive — a
    schema kept only because an admin schema referenced it goes too, and a schema a tenant path
    reaches through three others stays.
    """
    kept_paths = {
        path: item
        for path, item in (spec.get("paths") or {}).items()
        if not path.startswith(ADMIN_PREFIX)
    }
    cut = {**spec, "paths": kept_paths}

    components = spec.get("components") or {}
    # Seeded from the surviving paths *and* from every component section that is being kept whole:
    # a parameter or response body kept for a tenant path can name a schema, and dropping that
    # schema would leave a dangling $ref the generator cannot resolve.
    reachable = _refs(kept_paths) | _refs(
        {name: section for name, section in components.items() if name not in _PRUNED_SECTIONS}
    )
    for section in _PRUNED_SECTIONS:
        members = components.get(section) or {}
        wanted = {name for ref in reachable if (name := _named(ref, section)) is not None}
        # Closure: a kept schema's own refs are reachable too, until nothing new is added.
        while True:
            grown = wanted | {
                name
                for held in wanted
                if held in members
                for ref in _refs(members[held])
                if (name := _named(ref, section)) is not None
            }
            if grown == wanted:
                break
            wanted = grown
        cut["components"] = {
            **cut.get("components", components),
            section: {name: value for name, value in members.items() if name in wanted},
        }
    return cut

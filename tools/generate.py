"""Regenerate ``src/mfx/_generated`` from ``spec/openapi.yaml``.

Run it after the vendored spec changes::

    uv run python tools/generate.py

CI runs it and fails if anything differs, which is how "never edited by hand" is enforced rather
than asked for. The generator is invoked as an isolated tool at an exact version:
it pins its own ruff, and a code generator must not choose this library's linter.
"""

from __future__ import annotations

import re
import shutil
import subprocess  # noqa: S404 - fixed argv, never a shell
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tenant_spec import tenant_only  # noqa: E402 - after the path insert, by necessity

#: Exact, because the output is compared byte for byte. A range is drift with extra steps.
GENERATOR = "openapi-python-client==0.26.1"
REPO = Path(__file__).resolve().parents[1]
SPEC = REPO / "spec" / "openapi.yaml"
OUTPUT = REPO / "src" / "mfx" / "_generated"
CONFIG = Path(__file__).resolve().parent / "generator-config.yaml"


def generate(spec: Path = SPEC, output: Path = OUTPUT) -> Path:
    """Write the generated client to ``output``, replacing whatever was there.

    The vendored spec is whole; what reaches the generator is its tenant half
    (``tools.tenant_spec``). The cut happens here rather than in the vendored file, so that
    file stays canonical and diffable; and here rather than in the wheel, because the generator
    writes one ``models/__init__.py`` importing every model by name, so excluding files from the
    package breaks ``import mfx``.
    """
    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp) / "out"
        whole = yaml.safe_load(spec.read_text(encoding="utf-8"))
        tenant = Path(tmp) / "tenant-openapi.yaml"
        tenant.write_text(
            yaml.safe_dump(tenant_only(whole), sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        spec = tenant
        # uvx by name, not by path: it is whatever the developer or the CI runner installed, and
        # pinning a path here would make this work on one machine.
        argv = [
            "uvx",
            "--from",
            GENERATOR,
            "openapi-python-client",
            "generate",
            "--path",
            str(spec),
            "--output-path",
            str(staged),
            "--meta",
            "none",
            "--overwrite",
            "--config",
            str(CONFIG),
        ]
        subprocess.run(argv, check=True, cwd=tmp)  # noqa: S603, S607 - fixed argv, never a shell
        missing = dropped_schemas(yaml.safe_load(spec.read_text(encoding="utf-8")), staged)
        if missing:
            raise GeneratorDroppedSchemaError(missing)
        if output.exists():
            shutil.rmtree(output)
        shutil.move(str(staged), str(output))
    return output


class GeneratorDroppedSchemaError(RuntimeError):
    """The generator exited 0 having silently left a schema out."""

    def __init__(self, missing: list[str]) -> None:
        super().__init__(
            f"openapi-python-client exited 0 but wrote no model for: {', '.join(missing)}. "
            "It does this silently for shapes it cannot express. A numeric `enum` is the one that "
            "caught us: `sweep_hz: {type: number, enum: [0.5, 1, 2, 5]}` on FarmCreate, which is "
            "admin-only, so the tenant client never saw it. Either express the shape "
            "another way in "
            "`openapi.yaml`, or, if the schema is not part of the tenant surface at all, stop the "
            "tenant cut from carrying it (`tools/tenant_spec.py`)."
        )


def dropped_schemas(spec: dict[str, Any], generated: Path) -> list[str]:
    """Schemas the spec declares that the generator produced no model for.

    The generator **exits 0** when it cannot express a shape: it writes no model and says nothing,
    so the first sign is an `ImportError` or a missing type long afterwards. This turns that into a
    build failure at the moment it happens.

    Compared by the generator's own naming, `snake_case` of the schema name — so this asks "is there
    a module for it", not "is the class importable", and needs no import of the package.
    """
    models = generated / "models"
    present = {path.stem for path in models.glob("*.py")} if models.is_dir() else set()
    declared = (spec.get("components") or {}).get("schemas") or {}
    return sorted(name for name in declared if _module_name(name) not in present)


def _module_name(schema: str) -> str:
    """`TenantTerminal` -> `tenant_terminal`, as openapi-python-client names its modules."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", schema).lower()


if __name__ == "__main__":  # pragma: no cover - a tool, proven by the drift test
    sys.stdout.write(f"generated {generate()}\n")

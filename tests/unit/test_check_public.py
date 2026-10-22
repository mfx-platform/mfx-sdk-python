"""Nothing internal is published: the public check finds it in the wheel, the source distribution,
the documents and a whole repository tree, and passes only when there is none.

The internal-looking strings below are assembled at run time ("AB" + "#123"), so that this file
passes the check it tests when it is published itself.
"""

from __future__ import annotations

import io
import sys
import tarfile
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

import check_public  # noqa: E402

WORK_ITEM = "AB" + "#123"
DESIGN = "design" + "/terminal.md"
NAMES = frozenset({"acme-private", "hushco"})


def _wheel(dist: Path, files: dict[str, str]) -> None:
    with zipfile.ZipFile(dist / "mfx_sdk-1.0.0-py3-none-any.whl", "w") as wheel:
        for name, text in files.items():
            wheel.writestr(name, text)


def _sdist(dist: Path, files: dict[str, str]) -> None:
    with tarfile.open(dist / "mfx_sdk-1.0.0.tar.gz", "w:gz") as sdist:
        for name, text in files.items():
            data = text.encode()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            sdist.addfile(info, io.BytesIO(data))


def test_the_public_check_finds_internal_text_in_the_wheel_the_sdist_and_the_documents(
    tmp_path: Path,
) -> None:
    """Given a wheel, a source distribution and documents, clean and then each carrying one
    internal reference
    When the public check runs
    Then it passes on the clean set; it names the archive, the file, the line and the match for
    each internal reference, in any case; it ignores binary files; and it refuses to pass when
    nothing was built."""
    dist, repo = tmp_path / "dist", tmp_path / "repo"
    dist.mkdir()
    repo.mkdir()
    (repo / "README.md").write_text("# MFX Hub Python SDK\n", encoding="utf-8")
    _wheel(dist, {"mfx/__init__.py": '"""The client."""\n', "mfx/logo.png": f"{WORK_ITEM} binary"})
    _sdist(dist, {"mfx_sdk-1.0.0/PKG-INFO": "Name: mfx-sdk\n"})
    assert check_public.findings(dist, repo, NAMES) == []

    _wheel(dist, {"mfx/terminals.py": f'"""Retire it."""\n# see {DESIGN}\n'})
    _sdist(dist, {"mfx_sdk-1.0.0/src/mfx/x.py": f"x = 1  # {WORK_ITEM}\n"})
    (repo / "SECURITY.md").write_text("Report to us.\nAs HushCo does.\n", encoding="utf-8")
    found = check_public.findings(dist, repo, NAMES)
    assert f"mfx_sdk-1.0.0-py3-none-any.whl:mfx/terminals.py:2: {DESIGN[:7]}" in found
    assert f"mfx_sdk-1.0.0.tar.gz:mfx_sdk-1.0.0/src/mfx/x.py:1: {WORK_ITEM}" in found
    assert "SECURITY.md:2: hushco" in found

    for word in ("DEC-" + "12", "ADR-" + "30", "TC-S" + "1-W4-001", "§" + "9.6", "MFX\\" + "SDK"):
        assert check_public.INTERNAL.search(f"see {word}"), word
    assert not check_public.INTERNAL.search("a decimal string, ADR and DEC alone are words")

    assert check_public.main([str(tmp_path / "empty")]) == 2
    empty = tmp_path / "none"
    empty.mkdir()
    assert check_public.main([str(empty)]) == 2


def test_the_public_check_reads_private_names_from_a_file_and_scans_a_whole_tree(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Given a names file kept out of the public repository, and a repository tree
    When the check loads the names and scans the tree
    Then a name is found whole, inside a hyphenated word and in any case; comments and blank
    lines in the names file are ignored; a missing names file means no names; git's own files,
    a virtual environment and binary files are skipped; and the command line exits 0 on a clean
    tree, 1 on a dirty one and 2 when the directory does not exist."""
    names_file = tmp_path / "names.txt"
    names_file.write_text("# private\nHushCo   # a customer\n\nacme-private\n", encoding="utf-8")
    names = check_public.load_names(names_file)
    assert names == frozenset({"hushco", "acme-private"})
    assert check_public.load_names(tmp_path / "absent.txt") == frozenset()

    assert check_public.match("Built for HushCo's desk.", names) == "hushco"
    assert check_public.match("see hushco-workspace/notes", names) == "hushco-workspace"
    assert check_public.match("the acme-private repository", names) == "acme-private"
    assert check_public.match("acme and private are words", names) is None

    root = tmp_path / "tree"
    (root / ".git").mkdir(parents=True)
    (root / ".git" / "config").write_text(f"{WORK_ITEM}\n", encoding="utf-8")
    (root / ".venv" / "lib").mkdir(parents=True)
    (root / ".venv" / "lib" / "dep.py").write_text(f"# {WORK_ITEM}\n", encoding="utf-8")
    (root / "logo.png").write_bytes(b"hushco")
    (root / "src").mkdir()
    (root / "src" / "ok.py").write_text('"""Fine."""\n', encoding="utf-8")
    assert check_public.tree_findings(root, names) == []
    assert check_public.main(["--tree", str(root)]) == 0

    (root / "src" / "bad.py").write_text(f"# {WORK_ITEM}\n", encoding="utf-8")
    assert check_public.tree_findings(root, names) == [f"src/bad.py:1: {WORK_ITEM}"]
    assert check_public.main(["--tree", str(root)]) == 1
    assert check_public.main(["--tree", str(tmp_path / "missing")]) == 2
    assert f"src/bad.py:1: {WORK_ITEM}" in capsys.readouterr().out

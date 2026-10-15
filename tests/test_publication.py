from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.verify_publication import verify


def fixture_tree(root: Path) -> list[str]:
    assets = {}
    for name, content in {
        "ActiveInferenceSynthetic_Revised.pdf": b"%PDF-1.7 fixture",
        "ActiveInferenceSynthetic_20min.mp4": b"ftyp fixture",
    }.items():
        (root / name).write_bytes(content)
        assets[name] = {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
    (root / "publication.json").write_text(json.dumps({"schema_version": 1, "assets": assets}))
    (root / "SHA256SUMS.txt").write_text(
        "".join(f"{entry['sha256']}  {name}\n" for name, entry in assets.items())
    )
    (root / "README.md").write_text("# Fixture\n[paper](ActiveInferenceSynthetic_Revised.pdf)\n")
    (root / "AGENTS.md").write_text("# Fixture instructions\n")
    return sorted(path.name for path in root.iterdir())


def test_valid_files_and_local_links(tmp_path: Path) -> None:
    paths = fixture_tree(tmp_path)
    result = verify(tmp_path, paths)
    assert result["assets"] == 2
    assert result["maintained_folders"] == 1
    assert result["local_link_paths"] == 1


@pytest.mark.parametrize("content", [b"truncated", b"%PDF-1.7 corrupt"])
def test_corrupt_asset_is_rejected(tmp_path: Path, content: bytes) -> None:
    paths = fixture_tree(tmp_path)
    (tmp_path / "ActiveInferenceSynthetic_Revised.pdf").write_bytes(content)
    with pytest.raises(ValueError, match="Publication (size|hash) mismatch"):
        verify(tmp_path, paths)


def test_broken_link_is_rejected(tmp_path: Path) -> None:
    paths = fixture_tree(tmp_path)
    (tmp_path / "README.md").write_text("[broken](missing.md)\n")
    with pytest.raises(ValueError, match="Broken local link"):
        verify(tmp_path, paths)


def test_untracked_link_is_rejected(tmp_path: Path) -> None:
    paths = fixture_tree(tmp_path)
    (tmp_path / "local-only.md").write_text("Untracked\n")
    (tmp_path / "README.md").write_text("[local](local-only.md)\n")
    with pytest.raises(ValueError, match="Untracked local link"):
        verify(tmp_path, paths)


def test_new_folder_requires_both_guides(tmp_path: Path) -> None:
    paths = fixture_tree(tmp_path)
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested/README.md").write_text("# Nested\n")
    paths.append("nested/README.md")
    with pytest.raises(ValueError, match="Missing maintained folder guide: nested/AGENTS.md"):
        verify(tmp_path, paths)


def test_modified_checksum_list_is_rejected(tmp_path: Path) -> None:
    paths = fixture_tree(tmp_path)
    (tmp_path / "SHA256SUMS.txt").write_text("")
    with pytest.raises(ValueError, match="SHA256SUMS.txt differs"):
        verify(tmp_path, paths)

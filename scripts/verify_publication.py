from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit


def tracked_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, check=True, capture_output=True
    )
    return sorted(set(result.stdout.decode().strip("\0").split("\0")))


def verify(root: Path, paths: list[str] | None = None) -> dict[str, object]:
    root = root.resolve()
    paths = tracked_paths(root) if paths is None else paths
    manifest = json.loads((root / "publication.json").read_text())
    if manifest.get("schema_version") != 1 or not manifest.get("assets"):
        raise ValueError("Publication manifest must contain versioned assets")
    assets = manifest["assets"]
    required = {"ActiveInferenceSynthetic_Revised.pdf", "ActiveInferenceSynthetic_20min.mp4"}
    if not required <= assets.keys():
        raise ValueError("Publication manifest must bind root PDF and MP4")
    for name, entry in assets.items():
        target = (root / name).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            raise ValueError(f"Missing or unsafe publication asset: {name}")
        if target.stat().st_size != entry["bytes"]:
            raise ValueError(f"Publication size mismatch: {name}")
        digest = hashlib.sha256()
        with target.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
        actual = digest.hexdigest()
        if actual != entry["sha256"]:
            raise ValueError(f"Publication hash mismatch: {name}")
    checksum_rows = [f"{entry['sha256']}  {name}" for name, entry in assets.items()]
    if (root / "SHA256SUMS.txt").read_text().splitlines() != checksum_rows:
        raise ValueError("SHA256SUMS.txt differs from publication manifest")

    folders = {Path(".")}
    for name in paths:
        folders.update(Path(name).parents)
    for folder in sorted(folders):
        for name in ("README.md", "AGENTS.md"):
            relative = (folder / name).as_posix()
            if relative not in paths or not (root / relative).is_file():
                raise ValueError(f"Missing maintained folder guide: {relative}")

    if ".github/README.md" in paths:
        def rebase_link(match: re.Match[str]) -> str:
            destination = match.group(2)
            url = urlsplit(destination)
            if url.scheme or url.netloc or not url.path:
                return match.group(0)
            return f"{match.group(1)}../{destination})"

        expected = re.sub(
            r"(!?\[[^\]\n]*\]\()([^)\n]+)\)",
            rebase_link,
            (root / "README.md").read_text(),
        )
        if (root / ".github/README.md").read_text() != expected:
            raise ValueError("GitHub homepage README differs from root reader guide")

    source = root / "src/figures/render_all.py"
    figures = set()
    if source.is_file():
        for node in ast.walk(ast.parse(source.read_text())):
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "FIGURE_RENDERERS"
                for target in node.targets
            ):
                figures = {ast.literal_eval(key) for key in node.value.keys}
    checked = 0
    for name in paths:
        if not name.endswith(".md"):
            continue
        document = root / name
        text = re.sub(r"(?ms)^```.*?^```[^\n]*", "", document.read_text())
        for match in re.finditer(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", text):
            destination = match.group(1).strip()
            if destination.startswith("<"):
                destination = destination[1:].split(">", 1)[0]
            else:
                destination = destination.split(' "', 1)[0]
            url = urlsplit(destination)
            if url.scheme or url.netloc or not url.path:
                continue
            relative = unquote(url.path)
            if relative.startswith("../output/figures/") and name.startswith("docs/manuscript/"):
                if Path(relative).name not in figures:
                    raise ValueError(f"Unknown manuscript figure in {name}: {relative}")
            else:
                target = (document.parent / relative).resolve()
                if not target.is_relative_to(root) or not target.exists():
                    raise ValueError(f"Broken local link in {name}: {relative}")
                tracked = target.relative_to(root).as_posix()
                if target.is_file() and tracked not in paths:
                    raise ValueError(f"Untracked local link in {name}: {relative}")
            checked += 1
    return {
        "status": "PASS",
        "assets": len(assets),
        "maintained_folders": len(folders),
        "markdown_files": sum(name.endswith(".md") for name in paths),
        "local_link_paths": checked,
        "scope": "Asset bytes, paired tracked folder guides, and local Markdown target paths; external URLs and anchors need separate checks",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify public deliverables and documentation paths")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(verify(args.root), indent=2))


if __name__ == "__main__":
    main()

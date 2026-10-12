from __future__ import annotations

import argparse
import json
from pathlib import Path

from lecturecreate.canonical import file_sha256

parser = argparse.ArgumentParser()
parser.add_argument("--source", type=Path, required=True)
parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args()
source = args.source.resolve()
paths = [*source.joinpath("output/manuscript").glob("[0-9][0-9]_*.md")]
paths += list(source.joinpath("output/figures").glob("*.png"))
paths += list(source.joinpath("src").glob("*.py"))
paths += list(source.joinpath("formal/ActiveInferenceFormal").rglob("*.lean"))
paths += list(source.joinpath("data/gnn").glob("*.md"))
paths += [source / "docs/gnn_specifications.md", source / "output/data/gnn_specifications.json"]
paths += [source / name for name in (
    "README.md", "CITATION.cff", "pyproject.toml", "docs/positioning.md",
    "docs/methods.md", "docs/resources.md", "docs/manuscript/references.bib",
    "output/data/manuscript_variables.json", "output/data/teaching_experiments.json",
    "formal/lakefile.lean", "formal/lake-manifest.json", "formal/lean-toolchain",
    "data/claim_ledger.yaml", "output/pdf/ActiveInferenceSynthetic_combined.pdf",
)]
files = {str(path.relative_to(source)): file_sha256(path) for path in sorted(set(paths))}
if len(files) < 50:
    raise ValueError("Incomplete scientific source inventory")
with args.out.open("x") as stream:
    json.dump({"edition": "v15", "files": files}, stream, indent=2)
    stream.write("\n")
print(f"Frozen {len(files)} scientific inputs")

"""Compose attributed slide plates and freeze a supplied final scientific snapshot."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

from lecturecreate.canonical import file_sha256
from lecturecreate.schema import Beat, Citation, Lecture, Section, VisualKind, VisualSpec
from lecturecreate.source_bundle import require_no_drift

__all__ = ["author"]
PROJECT = Path(__file__).resolve().parent

TAKEAWAYS = [
    "Small executable models; explicit scientific boundaries",
    "Inference, decision, and dynamics answer different questions",
    "Prior × likelihood → joint distribution → posterior",
    "F[q] = surprise + KL(q || posterior)",
    "A closed-form posterior supplies an independent numerical oracle",
    "Dissipative descent + solenoidal motion along contours",
    "A deterministic spiral relaxes; a steady state describes an ensemble",
    "A displaced ensemble mean relaxes while covariance stays fixed",
    "Stationary: divergence-free current. Equilibrium: zero current.",
    "Irreversibility is model-specific; physical units require assumptions",
    "Marginal dependence can coexist with conditional independence",
    "Statistical screening alone does not establish causal direction",
    "Formal transfer binds one specified matrix and conditioning rule",
    "G(action) = − pragmatic value − epistemic value",
    "Preferences change the balance within one declared objective",
    "Information gain averages posterior changes over possible outcomes",
    "Terminal preference + cumulative information over observation histories",
    "Information in nats; contingent decision value in utility units",
    "Select → observe → update → re-evaluate → commit",
    "An independent cue carries observations, but no context information",
    "Context → state → observation; condition the joint to infer upward",
    "Hierarchical conditioning is exact; neural implementation is not assumed",
    "Finite path fluctuation identity: normalized laws and positive support",
    "History-channel normalization adds a policy-independent constant",
    "GNN parsing checks exact model parameters; it is not backend execution",
    "Synthetic teaches; FEP_Formal proves; GNN specifies models",
]


def author(source: Path, upstream_freeze: Path) -> None:
    """Copy finalized sources, create source-bound plates, then freeze every input."""
    from matplotlib.font_manager import FontProperties, findfont

    if (PROJECT / "sources/provenance.json").exists():
        raise FileExistsError("A source freeze already exists; preserve it and use a new edition")
    freeze = json.loads(upstream_freeze.read_text())
    require_no_drift(freeze["files"], lambda name: source / name, subject="Scientific handoff")
    manuscript = source / "output/manuscript"
    figures = source / "output/figures"
    raw = (PROJECT / "narration_draft.md").read_text()
    parts = re.split(r"^## ", raw, flags=re.MULTILINE)[1:]
    if len(parts) != len(TAKEAWAYS):
        raise ValueError("Narration/visual plan count mismatch")
    for directory in ("sources/manuscript", "sources/figures", "sources/code", "assets"):
        (PROJECT / directory).mkdir(parents=True, exist_ok=True)
    origin_hashes: dict[str, str] = {}
    inputs = list(manuscript.glob("[0-9][0-9]_*.md"))
    inputs += list(figures.glob("*.png"))
    inputs += list((source / "src").glob("*.py"))
    inputs += [source / "docs/positioning.md", source / "output/data/manuscript_variables.json"]
    inputs += [
        source / "docs/methods.md",
        source / "docs/resources.md",
        source / "output/data/teaching_experiments.json",
    ]
    inputs += [source / "README.md", source / "CITATION.cff", source / "pyproject.toml"]
    inputs += [source / "docs/manuscript/references.bib"]
    inputs += [source / "docs/gnn_specifications.md",
               source / "output/data/gnn_specifications.json"]
    inputs += list((source / "data/gnn").glob("*.md"))
    inputs += [upstream_freeze]
    inputs += list((source / "formal/ActiveInferenceFormal").rglob("*.lean"))
    inputs += [
        source / "formal/lakefile.lean",
        source / "formal/lake-manifest.json",
        source / "formal/lean-toolchain",
        source / "data/claim_ledger.yaml",
        source / "output/pdf/ActiveInferenceSynthetic_combined.pdf",
    ]
    for original in inputs:
        if original.parent == manuscript:
            relative = Path("sources/manuscript") / original.name
        elif original.parent == figures:
            relative = Path("sources/figures") / original.name
        elif original.parent == source / "src":
            relative = Path("sources/code") / original.name
        elif original.is_relative_to(source / "formal"):
            relative = Path("sources/formal") / original.relative_to(source / "formal")
        else:
            relative = Path("sources") / original.name
        (PROJECT / relative).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(original, PROJECT / relative)
        origin_hashes[str(original.relative_to(source))] = file_sha256(original)
    font_path = Path(findfont(FontProperties(family="DejaVu Sans")))
    shutil.copyfile(font_path, PROJECT / "assets/DejaVuSans.ttf")
    shutil.copyfile(font_path.parent / "LICENSE_DEJAVU", PROJECT / "assets/LICENSE_DEJAVU")
    import subprocess

    subprocess.run(
        [
            "pdftoppm",
            "-f",
            "1",
            "-l",
            "1",
            "-scale-to",
            "2000",
            "-singlefile",
            "-png",
            str(PROJECT / "sources/ActiveInferenceSynthetic_combined.pdf"),
            str(PROJECT / "assets/paper_cover"),
        ],
        check=True,
        capture_output=True,
    )

    lecture = Lecture(
        title="Active Inference Synthetic",
        subtitle="From beliefs to action: a worked introduction",
        fps=25,
    )
    lecture.metadata = {
        "source_repository": "https://github.com/docxology/ActiveInferenceSynthetic",
        "voice": "ElevenLabs Daniel Ari Friedman existing voice profile",
        "duration_target_seconds": 1200,
        "source_snapshot": "sources/provenance.json",
    }
    lecture.voice = "f1fdYDHzR22JxAxrWWgE"
    for index, part in enumerate(parts):
        header, narration = part.split("\n", 1)
        _, title, figure, section = [x.strip() for x in header.split(" | ")]
        narrative = " ".join(narration.split())
        reference = PROJECT / "sources/manuscript" / section
        if not reference.is_file() or "{{" in reference.read_text():
            raise ValueError(f"Missing or unhydrated final section: {reference}")
        from visual_design import build_slide

        plate = build_slide(PROJECT, index, title, figure, section)
        takeaway = TAKEAWAYS[index]
        relative_plate = f"assets/slide_{index + 1:02d}.png"
        plate.save(PROJECT / relative_plate)
        lecture.sections.append(
            Section(
                id=f"s{index + 1:02d}",
                title=title,
                objectives=[takeaway],
                beats=[
                    Beat(
                        id=f"b{index + 1:02d}",
                        narration=narrative,
                        visual=VisualSpec(
                            kind=VisualKind.IMAGE,
                            title=title,
                            image_path=relative_plate,
                            description=(
                                "Synthetic PDF cover with its DOI and published references."
                                if index == 0
                                else f"{title}. {takeaway}. Source figure: {figure}."
                            ),
                        ),
                        citation=Citation(
                            claim_id=f"synthetic-{index + 1:02d}",
                            source_url="https://github.com/docxology/ActiveInferenceSynthetic/releases/tag/synthetic-teaching-v0.6.0"
                            if index == 0
                            else f"sources/manuscript/{section}",
                            evidence_type="scope"
                            if index in (0, 1, 9, 11, 21, 22, 24, 25)
                            else "derivation",
                            confidence="Educational synthesis of the frozen project sources",
                            falsifiable_by=(
                                "A mismatch with the frozen model equations, numerical "
                                "references, or stated hypotheses."
                            ),
                        ),
                    )
                ],
            )
        )
    (PROJECT / "lecture.json").write_text(json.dumps(lecture.to_dict(), indent=2) + "\n")
    authored = {
        p.name: file_sha256(p)
        for p in PROJECT.iterdir()
        if p.is_file() and p.suffix in (".py", ".md", ".json", ".toml")
    }
    files = {
        str(p.relative_to(PROJECT)): file_sha256(p)
        for directory in (PROJECT / "sources", PROJECT / "assets")
        for p in sorted(directory.rglob("*"))
        if p.is_file()
    }
    require_no_drift(freeze["files"], lambda name: source / name, subject="Scientific handoff")
    provenance = {
        "source_repository": lecture.metadata["source_repository"],
        "source_origin_files_sha256": origin_hashes,
        "files_sha256": files,
        "authored_source_hashes": authored,
        "note": (
            "Copied final scientific inputs; digest inventory is the snapshot identity. "
            "Uncommitted authored improvements are included; "
            "HEAD alone does not identify this edition."
        ),
    }
    (PROJECT / "sources/provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print(f"Authored {len(parts)} slides, {lecture.word_count()} words, {len(files)} frozen inputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--freeze", type=Path, required=True)
    args = parser.parse_args()
    author(args.source.resolve(), args.freeze.resolve())

"""Check a completed production against its persisted media and source receipts."""

from __future__ import annotations

import argparse
import json
import subprocess
import wave
from pathlib import Path
from typing import Any

from lecturecreate.canonical import file_sha256
from lecturecreate.pipeline import PipelineResult
from lecturecreate.source_bundle import parse_inventory, require_no_drift

__all__ = ["verify"]


def verify(out: Path) -> dict[str, Any]:
    """Require exact duration, real audio, complete companions and source custody."""
    receipt = json.loads((out / "production_receipt.json").read_text())
    require_no_drift(receipt["files_sha256"], lambda name: out / name, subject="Production")
    source = out / "source_bundle"
    provenance = json.loads((source / "sources/provenance.json").read_text())
    frozen = parse_inventory(provenance)
    require_no_drift(frozen.files, lambda name: source / name, subject="Delivered source")
    require_no_drift(frozen.authored, lambda name: source / name, subject="Delivered authoring")
    result = PipelineResult.from_manifest(out / "manifests/render_manifest.json")
    if result.total_ms != 1_200_000 or sum(result.frame_durations_ms) != 1_200_000:
        raise ValueError("Timeline is not exactly twenty minutes")
    for clip in result.clips:
        with wave.open(str(clip.path), "rb") as audio:
            duration = round(1000 * audio.getnframes() / audio.getframerate())
        if duration != clip.duration_ms:
            raise ValueError(f"Measured speech drift: {clip.beat_id}")
    with wave.open(str(out / "audio/voiceover.wav"), "rb") as audio:
        if audio.getnframes() != audio.getframerate() * 1200:
            raise ValueError("Voiceover sample count is not exactly twenty minutes")
    for beat, frame in zip(result.lecture.iter_beats(), result.frame_paths, strict=True):
        if file_sha256(frame) != file_sha256(source / beat.visual.image_path):
            raise ValueError(f"Slide plate mismatch: {beat.id}")
    video = out / "ActiveInferenceSynthetic_20min.mp4"
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_streams",
        "-show_chapters",
        "-show_format",
        "-of",
        "json",
        str(video),
    ]
    probe = json.loads(subprocess.run(command, check=True, capture_output=True, text=True).stdout)
    if float(probe["format"]["duration"]) != 1200.0:
        raise ValueError("Encoded duration is not exactly twenty minutes")
    streams = probe["streams"]
    if not any(s["codec_type"] == "audio" for s in streams):
        raise ValueError("Video has no audio stream")
    if not any(
        s["codec_type"] == "video" and s["width"] == 1920 and s["height"] == 1080 for s in streams
    ):
        raise ValueError("Video geometry is not 1080p")
    if len(probe["chapters"]) != len(result.lecture.sections):
        raise ValueError("Embedded chapters are incomplete")
    pdf = subprocess.run(
        ["pdfinfo", str(out / "slides.pdf")], check=True, capture_output=True, text=True
    ).stdout
    pages = next(int(line.split(":")[1]) for line in pdf.splitlines() if line.startswith("Pages:"))
    if pages != len(result.frame_paths):
        raise ValueError("PDF page count differs from the video slides")
    for name in (
        "transcript.txt",
        "speaker_notes.md",
        "source_ledger.md",
        "captions/captions.srt",
        "captions/captions.vtt",
        "chapters/chapters.txt",
    ):
        if not (out / name).read_text().strip():
            raise ValueError(f"Empty companion: {name}")
    return {
        "status": "PASS",
        "scenario": "completed twenty-minute production",
        "invocation": "python examples/active_inference_synthetic/verify.py --out " + str(out),
        "target_ms": result.total_ms,
        "speech_ms": sum(c.duration_ms for c in result.clips),
        "pages": pages,
        "chapters": len(probe["chapters"]),
        "probe": probe,
        "pdfinfo": pdf,
        "checked_production_files": len(receipt["files_sha256"]),
        "checked_source_files": len(frozen.files) + len(frozen.authored),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    print(json.dumps(verify(parser.parse_args().out.resolve()), indent=2))

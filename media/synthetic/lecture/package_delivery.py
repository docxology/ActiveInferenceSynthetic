"""Repair an invalid trailing caption boundary, preserving speech and original receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import TypedDict

from aligned_captions import build_aligned_captions
from lecturecreate.pipeline import PipelineResult

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--production", type=Path, required=True)
parser.add_argument("--delivery-out", type=Path, required=True)
args = parser.parse_args()
production = args.production
out = args.delivery_out
out.mkdir()
source = production / "ActiveInferenceSynthetic_20min.mp4"
result = PipelineResult.from_manifest(production / "manifests/render_manifest.json")
original_srt = out / "aligned_source.srt"
alignment_receipt = build_aligned_captions(result, Path(__file__).resolve().parent, original_srt)
(out / "caption_alignment_receipt.json").write_text(json.dumps(alignment_receipt, indent=2) + "\n")


def digest(path: Path) -> str:
    """Hash one input or output without buffering the video."""
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def milliseconds(text: str) -> int:
    """Parse an SRT timestamp into integer milliseconds."""
    h, m, s, ms = map(int, re.split("[:,]", text))
    return ((h * 60 + m) * 60 + s) * 1000 + ms


def timestamp(value: int, separator: str = ",") -> str:
    """Format the same measured time for SRT or WebVTT."""
    h, remainder = divmod(value, 3600000)
    m, remainder = divmod(remainder, 60000)
    s, ms = divmod(remainder, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{separator}{ms:03d}"


class Cue(TypedDict):
    """One measured caption interval and its unchanged authored text."""

    index: int
    start: int
    end: int
    text: str


cues: list[Cue] = []
for block in re.split(r"\n\s*\n", original_srt.read_text().strip()):
    index, timing, text = block.split("\n", 2)
    start, end = timing.split(" --> ")
    cues.append(
        {"index": int(index), "start": milliseconds(start), "end": milliseconds(end), "text": text}
    )
repairs = []
for i, cue in enumerate(cues):
    if cue["end"] > cue["start"]:
        continue
    if i == 0 or cues[i - 1]["start"] >= cue["end"]:
        raise ValueError("Invalid cue cannot be repaired within its predecessor span")
    previous = cues[i - 1]
    old = [dict(previous), dict(cue)]
    previous_weight = len(previous["text"].replace("\n", " "))
    weight = previous_weight + len(cue["text"].replace("\n", " "))
    boundary = previous["start"] + round(
        (cue["end"] - previous["start"]) * previous_weight / weight
    )
    previous["end"] = boundary
    cue["start"] = boundary
    repairs.append(
        {
            "reason": "Reversed trailing cue from upstream minimum-duration allocation",
            "before": old,
            "after": [dict(previous), dict(cue)],
        }
    )
result = PipelineResult.from_manifest(production / "manifests/render_manifest.json")
expected_text = " ".join(" ".join(beat.narration.split()) for beat in result.lecture.iter_beats())
caption_text = " ".join(" ".join(cue["text"].split()) for cue in cues)
if caption_text != expected_text:
    raise ValueError("Caption text differs from the complete authored narration")
spans: list[tuple[int, int]] = []
for beat in result.lecture.iter_beats():
    if beat.start_ms is None or beat.duration_ms is None:
        raise ValueError(f"Missing measured timing: {beat.id}")
    spans.append((beat.start_ms, beat.start_ms + beat.duration_ms))
previous_end = 0
for cue in cues:
    if not 0 <= cue["start"] < cue["end"] <= 1200000 or cue["start"] < previous_end:
        raise ValueError(f"Invalid/nonmonotonic caption: {cue}")
    if not any(start <= cue["start"] < cue["end"] <= end for start, end in spans):
        raise ValueError(f"Caption outside measured narration: {cue}")
    previous_end = cue["end"]
srt = out / "captions.srt"
srt.write_text(
    "\n\n".join(
        f"{c['index']}\n{timestamp(c['start'])} --> {timestamp(c['end'])}\n{c['text']}"
        for c in cues
    )
    + "\n"
)
(out / "captions.vtt").write_text(
    "WEBVTT\n\n"
    + "\n\n".join(
        f"{timestamp(c['start'], '.')} --> {timestamp(c['end'], '.')}\n{c['text']}" for c in cues
    )
    + "\n"
)
video = out / "ActiveInferenceSynthetic_20min_captioned.mp4"
command = [
    "ffmpeg",
    "-v",
    "error",
    "-i",
    str(source),
    "-i",
    str(srt),
    "-map",
    "0:v:0",
    "-map",
    "0:a:0",
    "-map",
    "1:0",
    "-c",
    "copy",
    "-c:s",
    "mov_text",
    "-metadata:s:s:0",
    "language=eng",
    "-metadata:s:s:0",
    "title=English",
    "-map_metadata",
    "0",
    "-map_chapters",
    "0",
    "-movflags",
    "+faststart",
    str(video),
]
mux = subprocess.run(command, capture_output=True, text=True)
(out / "mux.log").write_text(
    "$ " + " ".join(command) + "\n" + mux.stdout + mux.stderr + f"\nexit_code={mux.returncode}\n"
)
mux.check_returncode()
probe_command = [
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
probe = json.loads(subprocess.run(probe_command, check=True, capture_output=True, text=True).stdout)
if float(probe["format"]["duration"]) != 1200 or len(probe["chapters"]) != 26:
    raise ValueError("Duration or chapter count changed")
if not any(
    s["codec_type"] == "subtitle"
    and s["codec_name"] == "mov_text"
    and s["tags"]["language"] == "eng"
    for s in probe["streams"]
):
    raise ValueError("English subtitle stream missing")
roundtrip = out / "embedded_caption_roundtrip.srt"
extract_command = [
    "ffmpeg",
    "-v",
    "error",
    "-i",
    str(video),
    "-map",
    "0:s:0",
    "-c:s",
    "srt",
    str(roundtrip),
]
subprocess.run(extract_command, check=True, capture_output=True, text=True)


def cue_blocks(path: Path) -> list[str]:
    """Read caption text and timing without sequence-number formatting."""
    return [b.split("\n", 1)[1] for b in re.split(r"\n\s*\n", path.read_text().strip())]


if cue_blocks(srt) != cue_blocks(roundtrip):
    raise ValueError("Caption text/timing failed exact embedded roundtrip")
decode_command = ["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"]
decode = subprocess.run(decode_command, capture_output=True, text=True)
(out / "decode.log").write_text(
    "$ "
    + " ".join(decode_command)
    + "\n"
    + decode.stdout
    + decode.stderr
    + f"\nexit_code={decode.returncode}\n"
)
decode.check_returncode()
record = {
    "status": "PASS",
    "input_video_sha256": digest(source),
    "original_srt_sha256": digest(original_srt),
    "srt_sha256": digest(srt),
    "captioned_video_sha256": digest(video),
    "production_receipt_sha256": digest(production / "production_receipt.json"),
    "mux_invocation": command,
    "mux_exit_code": mux.returncode,
    "probe_invocation": probe_command,
    "probe": probe,
    "decode_invocation": decode_command,
    "decode_exit_code": decode.returncode,
    "caption_roundtrip_invocation": extract_command,
    "caption_roundtrip_exact": True,
    "caption_count": len(cues),
    "narration_text_exact": True,
    "packaging_helper_sha256": digest(Path(__file__)),
    "caption_repairs": repairs,
    "all_cues_within_measured_speech": True,
    "caption_timing": (
        alignment_receipt["method"]
    ),
    "files_sha256": {str(p.relative_to(out)): digest(p) for p in out.rglob("*") if p.is_file()},
}
(out / "delivery_receipt.json").write_text(json.dumps(record, indent=2) + "\n")
print(
    json.dumps(
        {
            "status": "PASS",
            "cue_count": len(cues),
            "repairs": repairs,
            "sha256": record["captioned_video_sha256"],
        },
        indent=2,
    )
)

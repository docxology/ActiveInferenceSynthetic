"""Render frozen visuals with measured, paced ElevenLabs Daniel recordings."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import wave
from array import array
from pathlib import Path
from typing import Any

from lecturecreate import captions as captions_mod
from lecturecreate.assembly.video import encode_animation, probe_video
from lecturecreate.canonical import file_sha256
from lecturecreate.config import (
    AnimationConfig,
    AudioConfig,
    RenderConfig,
    Theme,
    VideoConfig,
    VoiceConfig,
)
from lecturecreate.export.pdf_slides import export_pdf_slides
from lecturecreate.export.speaker_notes import export_speaker_notes
from lecturecreate.export.transcript import export_transcript
from lecturecreate.pacing import allocate_reading_holds
from lecturecreate.pipeline import Pipeline
from lecturecreate.schema import Beat, Lecture, Section, VisualKind, VisualSpec
from lecturecreate.source_bundle import parse_inventory, require_no_drift
from lecturecreate.source_ledger import build_source_ledger
from lecturecreate.tts.reuse import ExistingAudioBackend
from lecturecreate.video_pipeline import build_voiceover
from lecturecreate.workspace import Workspace
from model_animation import iter_model_frames
from slide_links import link_slides

__all__ = ["verify_sources", "render", "main"]
PROJECT = Path(__file__).resolve().parent
DEFAULT_OUT = PROJECT.parents[2] / "output" / "active_inference_synthetic_20min_20261011"


def verify_sources(project: Path) -> Lecture:
    """Require a nonempty, complete frozen inventory and a valid lecture."""
    provenance = json.loads((project / "sources/provenance.json").read_text())
    inventory = parse_inventory(provenance)
    if not inventory.files or not {"lecture.json", "render.py"} <= inventory.authored.keys():
        raise ValueError("Source freeze must bind scientific inputs, lecture.json and render.py")
    for mapping in (inventory.files, inventory.authored):
        for name in mapping:
            if Path(name).is_absolute() or ".." in Path(name).parts:
                raise ValueError(f"Unsafe inventory path: {name}")
        require_no_drift(mapping, lambda name: project / name, subject="Frozen lecture source")
    lecture = Lecture.from_dict(json.loads((project / "lecture.json").read_text()))
    lecture.asset_root = project
    errors = lecture.validate()
    if errors:
        raise ValueError(str(errors))
    for beat in lecture.iter_beats():
        if not beat.narration.strip() or beat.citation is None:
            raise ValueError(f"Beat lacks narration or citation: {beat.id}")
        if beat.visual.image_path and beat.visual.image_path not in inventory.files:
            raise ValueError(f"Unfrozen image: {beat.visual.image_path}")
    return lecture


def _non_silent(path: Path) -> int:
    with wave.open(str(path), "rb") as stream:
        if stream.getsampwidth() != 2:
            raise ValueError(f"Expected PCM16: {path}")
        samples = array("h", stream.readframes(stream.getnframes()))
    peak = max((abs(sample) for sample in samples), default=0)
    if peak < 100:
        raise ValueError(f"Silent or unusable narration: {path}")
    return peak


def render(out: Path, *, smoke: bool = False) -> dict[str, Any]:
    """Render to a fresh directory; allocate only additional reading silence."""
    lecture = (
        Lecture(
            title="Synthetic lecture production smoke",
            fps=25,
            sections=[
                Section(
                    id="smoke",
                    title="Production verification",
                    beats=[
                        Beat(
                            id="smoke",
                            narration=(
                                "Active inference connects a model of the world with perception "
                                "and action. This production check uses measured system speech. "
                                "The final lecture will distinguish mathematical derivations, "
                                "numerical demonstrations, and interpretations."
                            ),
                            visual=VisualSpec(
                                kind=VisualKind.BULLETS,
                                title="Active Inference Synthetic",
                                bullets=[
                                    "Measured local narration",
                                    "Source-bound scientific visuals",
                                    "Exact presentation timing",
                                ],
                            ),
                        )
                    ],
                )
            ],
        )
        if smoke
        else verify_sources(PROJECT)
    )
    target = 20_000 if smoke else 1_200_000
    if out.exists() and any(out.iterdir()):
        raise FileExistsError(f"Refusing to overwrite existing production: {out}")
    backend = ExistingAudioBackend(PROJECT / "sources/audio", strict=True, sample_rate=48000)
    lecture.voice = "f1fdYDHzR22JxAxrWWgE"
    subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
    config = RenderConfig(
        theme=Theme.preset("daylight"),
        voice=VoiceConfig(
            backend="elevenlabs",
            voice=lecture.voice,
            sample_rate=48000,
            elevenlabs_voice_id=lecture.voice,
            elevenlabs_model="eleven_multilingual_v2",
        ),
        audio=AudioConfig(
            lead_silence_ms=400, gap_ms=350, trail_silence_ms=600, normalize=False, fade_ms=0
        ),
        animation=AnimationConfig(enabled=True, fps=25),
        video=VideoConfig(width=1920, height=1080, crf=18, preset="veryfast"),
    )
    workspace = Workspace(out)
    pipeline = Pipeline(config=config, backend=backend)
    clips = pipeline.synthesize(lecture, workspace)
    peaks = [_non_silent(clip.path) for clip in clips]
    holds = allocate_reading_holds([clip.duration_ms for clip in clips], target, config.audio)
    for beat, hold in zip(lecture.iter_beats(), holds, strict=True):
        beat.duration_override_ms = hold
    result = pipeline.render_frames(lecture, workspace, clips, frame_size=(1920, 1080))
    if result.total_ms != target:
        raise ValueError(f"Incorrect timeline: {result.total_ms} != {target}")
    if not smoke:
        for beat, frame in zip(lecture.iter_beats(), result.frame_paths, strict=True):
            if not beat.visual.image_path:
                raise ValueError(f"Missing authored slide plate: {beat.id}")
            shutil.copyfile(PROJECT / beat.visual.image_path, frame)
    pipeline.write_captions(result)
    pipeline.write_manifest(result)
    export_pdf_slides(result, out / "slides_unlinked.pdf")
    links = link_slides(out / "slides_unlinked.pdf", out / "slides.pdf", PROJECT)
    (out / "slide_links.json").write_text(json.dumps(links, indent=2) + "\n")
    export_speaker_notes(result, out / "speaker_notes.md")
    export_transcript(result, out / "transcript.txt")
    ledger = build_source_ledger(lecture)
    publication = json.loads((PROJECT / "publication.json").read_text())
    ledger += (
        "\n\n## Paper and published references\n\n"
        + "\n".join(f"- [{link['label']}]({link['url']})" for link in publication["links"])
        + "\n"
    )
    if not smoke:
        provenance = json.loads((PROJECT / "sources/provenance.json").read_text())
        frozen = parse_inventory(provenance)
        names = [*frozen.files, *frozen.authored, "sources/provenance.json"]
        for name in names:
            target_file = out / "source_bundle" / name
            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(PROJECT / name, target_file)
        ledger = ledger.replace("](sources/", "](source_bundle/sources/")
    (out / "source_ledger.md").write_text(ledger)
    (out / "render.yaml").write_text(config.to_yaml())
    if smoke:
        raise ValueError("This edition requires the complete frozen numerical animation sources")
    voiceover = build_voiceover(result, config)
    video = out / "ActiveInferenceSynthetic_20min.mp4"
    encode_animation(
        iter_model_frames(result, PROJECT),
        voiceover,
        video,
        size=(1920, 1080),
        fps=25,
        total_s=target / 1000,
        crf=config.video.crf,
        preset=config.video.preset,
    )
    metadata = out / "chapters/ffmetadata.txt"
    metadata.write_text(captions_mod.ffmetadata_chapters(result.lecture, result.total_ms))
    chaptered = out / "ActiveInferenceSynthetic_chaptered.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(video),
            "-i",
            str(metadata),
            "-map_metadata",
            "1",
            "-codec",
            "copy",
            str(chaptered),
        ],
        check=True,
        capture_output=True,
    )
    chaptered.replace(video)
    probe = probe_video(video)
    if probe is None or abs(probe["duration_s"] - target / 1000) > 0.04 or not probe["has_audio"]:
        raise ValueError(f"Video failed duration/audio validation: {probe}")
    decoded = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    (out / "decode.log").write_text(f"exit_code={decoded.returncode}\n" + decoded.stderr)
    decoded.check_returncode()
    if not smoke:
        verify_sources(PROJECT)
    receipt = {
        "target_ms": target,
        "timeline_ms": result.total_ms,
        "video_probe": probe,
        "voice": lecture.voice,
        "backend": "existing",
        "source_backend": "elevenlabs",
        "model": "eleven_multilingual_v2",
        "animated_chapters": [5, 7, 8, 9, 18],
        "animation_semantics": (
            "Frozen numerical cores; iteration, model time and known accuracy have separate clocks"
        ),
        "pacing": json.loads((PROJECT / "sources/pacing_receipt.json").read_text()),
        "narration_words": lecture.word_count(),
        "speech_ms": sum(c.duration_ms for c in clips),
        "reading_holds_ms": sum(holds) - sum(c.duration_ms for c in clips),
        "audio_peaks": peaks,
        "slides": len(clips),
        "video_sha256": file_sha256(video),
        "source_freeze_sha256": None if smoke else file_sha256(PROJECT / "sources/provenance.json"),
        "caption_timing": (
            "Character-proportional cues within measured speech spans; not forced alignment"
        ),
        "files_sha256": {
            str(p.relative_to(out)): file_sha256(p) for p in sorted(out.rglob("*")) if p.is_file()
        },
    }
    (out / "production_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


def main() -> None:
    """Run a source check, isolated smoke, or complete production."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", type=Path, default=DEFAULT_OUT / "production_v15_complete_daniel"
    )
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--verify-sources", action="store_true")
    args = parser.parse_args()
    if args.verify_sources:
        print(f"Verified {len(verify_sources(PROJECT).iter_beats())} beats")
    else:
        print(json.dumps(render(args.out.resolve(), smoke=args.smoke), indent=2))


if __name__ == "__main__":
    main()

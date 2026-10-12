"""Reuse narration only on exact text agreement; synthesize changed Daniel beats."""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path

from lecturecreate.canonical import file_sha256
from lecturecreate.tts.elevenlabs import ElevenLabsTTSBackend

PROJECT = Path(__file__).resolve().parent
VOICE = "f1fdYDHzR22JxAxrWWgE"


def main() -> None:
    """Read a credential from stdin and produce a fresh, attributed raw audio set."""
    secret = sys.stdin.readline().strip()
    if not secret:
        raise ValueError("An ElevenLabs credential is required for changed chapters")
    os.environ["ELEVENLABS_API_KEY"] = secret
    old = json.loads((PROJECT.parent / "edition_v11/lecture.json").read_text())
    previous = [beat for section in old["sections"] for beat in section["beats"]]
    parts = re.split(r"^## ", (PROJECT / "narration_draft.md").read_text(), flags=re.M)[1:]
    if len(parts) != len(previous):
        raise ValueError("Narration count changed; explicit audio mapping required")
    out = PROJECT / "raw_audio"
    out.mkdir()
    backend = ElevenLabsTTSBackend(voice_id=VOICE, sample_rate=48000)
    bindings = []
    prior_audio = PROJECT.parent / "edition_v10/raw_audio"
    try:
        for i, (part, beat) in enumerate(zip(parts, previous, strict=True), 1):
            narration = " ".join(part.split("\n", 1)[1].split())
            destination = out / f"b{i:02d}.wav"
            if narration == beat["narration"]:
                original = prior_audio / destination.name
                shutil.copyfile(original, destination)
                origin = {"method": "exact-text reuse", "original_sha256": file_sha256(original)}
            else:
                backend.synthesize(narration, destination, voice=VOICE)
                origin = {
                    "method": "ElevenLabs synthesis",
                    "voice": VOICE,
                    "model": "eleven_multilingual_v2",
                }
            bindings.append(
                {
                    "beat": destination.stem,
                    "text": narration,
                    "sha256": file_sha256(destination),
                    **origin,
                }
            )
            print(f"Prepared {destination.stem}: {origin['method']}", flush=True)
    finally:
        os.environ.pop("ELEVENLABS_API_KEY", None)
    (out / "voice_receipt.json").write_text(json.dumps(bindings, indent=2) + "\n")


if __name__ == "__main__":
    main()

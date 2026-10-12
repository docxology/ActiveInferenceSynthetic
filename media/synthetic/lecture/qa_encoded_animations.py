from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
from lecturecreate.pipeline import PipelineResult
from model_animation import numerical_frames
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("--production", type=Path, required=True)
parser.add_argument("--video", type=Path, required=True)
args = parser.parse_args()
result = PipelineResult.from_manifest(args.production / "manifests/render_manifest.json")
out = args.production / "encoded_animation_qa"
out.mkdir()
boundaries = np.cumsum([0, *result.frame_durations_ms])
project = Path(__file__).resolve().parent
records = []
for chapter in (4, 6, 7, 8, 17):
    frames, data = numerical_frames(project, chapter)
    captures = []
    for sample, fraction in enumerate((.02, .32, .79)):
        n = round((boundaries[chapter] + fraction*result.frame_durations_ms[chapter]) / 40)
        elapsed = n*40
        target = out / f"chapter_{chapter+1:02d}_{sample}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-ss", str(elapsed/1000), "-i",
                        str(args.video), "-frames:v", "1", str(target)],
                       check=True, capture_output=True)
        frame_index = round(min(1, (elapsed-boundaries[chapter]) /
                            (result.frame_durations_ms[chapter]*.8)) * (len(frames)-1))
        actual = np.array(Image.open(target).convert("RGB").crop((94, 243, 1260, 863)), dtype=float)
        expected = np.array(frames[frame_index], dtype=float)
        error = float(np.abs(actual-expected).mean())
        if error > 4:
            raise ValueError(f"Encoded model panel differs from its computed frame: {error}")
        captures.append(actual)
        records.append({"chapter": chapter+1, "time_ms": elapsed, "model_frame": frame_index,
                        "mean_rgb_error": error, "capture": target.name, "clock": data["clock"]})
    differences = [
        float(np.abs(a-b).mean()) for a, b in zip(captures[:-1], captures[1:], strict=True)
    ]
    if min(differences) < .1:
        raise ValueError("Encoded animation does not visibly advance")
(out / "receipt.json").write_text(json.dumps(records, indent=2) + "\n")
print("PASS: nine encoded frames match numerical panels and all animations visibly advance")

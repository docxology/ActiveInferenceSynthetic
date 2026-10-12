from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from model_animation import numerical_frames

project = Path(__file__).resolve().parent
out = project / "animation_preflight"
out.mkdir()
records = {}
for index in (4, 6, 7, 8, 17):
    frames, data = numerical_frames(project, index)
    if len({frame.tobytes() for frame in (frames[0], frames[len(frames) // 2], frames[-1])}) != 3:
        raise ValueError("Animation does not visibly change")
    for suffix, frame in (
        ("start", frames[0]),
        ("middle", frames[len(frames) // 2]),
        ("end", frames[-1]),
    ):
        frame.save(out / f"chapter_{index + 1:02d}_{suffix}.png")
    if index == 4:
        np.testing.assert_allclose(data["posterior"], [0.54 / 0.62, 0.08 / 0.62])
        if not np.all(np.diff(data["free_energy_nats"]) <= 1e-12):
            raise ValueError("Belief animation contradicts descent")
    elif index in (6, 7):
        t = np.array(data["sample_steps"]) * data["dt"]
        radial, rotating = np.array(data["paths"] if index == 6 else data["mean_paths"])
        np.testing.assert_allclose(radial[:, 0], 2.6 * np.exp(-t), atol=1e-10)
        np.testing.assert_allclose(rotating[:, 0], 2.6 * np.exp(-t) * np.cos(2.4 * t), atol=1e-9)
        np.testing.assert_allclose(rotating[:, 1], -2.6 * np.exp(-t) * np.sin(2.4 * t), atol=1e-9)
        if index == 7:
            np.testing.assert_allclose(data["initial_covariance"], np.eye(2), atol=1e-12)
    elif index == 8:
        drives = np.asarray(data["drive"])
        np.testing.assert_allclose(data["entropy_rate"], 2 * drives ** 2, atol=1e-12)
        np.testing.assert_allclose(data["entropy_rate"][0], data["entropy_rate"][-1])
        if data["entropy_rate"][len(drives) // 2] != 0:
            raise ValueError("Zero drive must have zero entropy-production rate")
    else:
        r = np.array(data["accuracy"])
        np.testing.assert_allclose(data["gross_utility"], r - 0.5, atol=1e-12)
        np.testing.assert_allclose(data["net_utility"], r - 0.65, atol=1e-12)
        np.testing.assert_allclose(data["information_nats"][-1], np.log(2))
    records[str(index + 1)] = data
try:
    numerical_frames(project, 3)
except ValueError:
    records["negative_control"] = "Undeclared animation rejects before rendering"
else:
    raise AssertionError("Undeclared animation was accepted")
(out / "numerical-animation-checks.json").write_text(json.dumps(records, indent=2) + "\n")
print(
    "PASS: five changing animations, independent analytic oracles and rejection control"
)

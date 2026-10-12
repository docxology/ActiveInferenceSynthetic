"""Render numerical changes from the frozen teaching cores, with explicit clocks."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def load_core(project: Path):
    name = "frozen_synthetic"
    spec = importlib.util.spec_from_file_location(
        name,
        project / "sources/code/__init__.py",
        submodule_search_locations=[str(project / "sources/code")],
    )
    if spec is None or spec.loader is None:
        raise ValueError("Frozen numerical package is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    demos = importlib.import_module(name + ".demos")
    return module, demos


def numerical_frames(project: Path, index: int) -> tuple[list[Image.Image], dict]:
    core, d = load_core(project)
    if index == 4:
        descent = core.minimize_free_energy(
            d.LIKELIHOOD,
            d.PRIOR,
            d.BELIEF_OBS,
            learning_rate=d.BELIEF_LEARNING_RATE,
            steps=d.BELIEF_STEPS,
        )
        reference = core.posterior(d.LIKELIHOOD, d.PRIOR, d.BELIEF_OBS)
        records = {
            "clock": "algorithm iteration",
            "beliefs": descent.beliefs.tolist(),
            "free_energy_nats": descent.free_energy.tolist(),
            "posterior": reference.tolist(),
        }
        count = len(descent.beliefs)
    elif index == 6:
        paths = [
            core.integrate_trajectory(
                d.TRAJECTORY_START,
                precision=d.FLOW.precision,
                gamma=d.FLOW.gamma,
                omega=omega,
                dt=d.TRAJECTORY_DT,
                steps=d.TRAJECTORY_STEPS,
            )
            for omega in (0, d.TRAJECTORY_OMEGA_NESS)
        ]
        samples = np.linspace(0, d.TRAJECTORY_STEPS, 61).astype(int)
        records = {
            "clock": "model time",
            "dt": d.TRAJECTORY_DT,
            "sample_steps": samples.tolist(),
            "paths": [p[samples].tolist() for p in paths],
            "meaning": "deterministic drift, not stationary current",
        }
        count = len(samples)
    elif index == 7:
        paths = [core.integrate_trajectory(
            d.TRAJECTORY_START, precision=d.FLOW.precision, gamma=d.FLOW.gamma,
            omega=omega, dt=d.TRAJECTORY_DT, steps=d.TRAJECTORY_STEPS
        ) for omega in (0, d.TRAJECTORY_OMEGA_NESS)]
        samples = np.linspace(0, d.TRAJECTORY_STEPS, 61).astype(int)
        records = {"clock": "model time", "sample_steps": samples.tolist(),
                   "dt": d.TRAJECTORY_DT, "mean_paths": [p[samples].tolist() for p in paths],
                   "initial_covariance": core.stationary_covariance(
                       precision=d.FLOW.precision, gamma=d.FLOW.gamma, omega=0).tolist(),
                   "meaning": "Transient Gaussian mean; stationary initial covariance stays fixed"}
        count = len(samples)
    elif index == 8:
        drives = np.linspace(-d.OMEGA_NESS, d.OMEGA_NESS, 61)
        sigma = [core.entropy_production_rate(
            precision=d.FLOW.precision, gamma=d.FLOW.gamma, omega=float(omega)
        ) for omega in drives]
        records = {"clock": "known stationary drive parameter, not physical time",
                   "drive": drives.tolist(), "entropy_rate": sigma,
                   "meaning": "Same stationary density; current direction changes with drive"}
        count = len(drives)
    elif index == 17:
        values = [
            core.value_of_information(
                np.array([[r, 1 - r], [1 - r, r]]), d.VOI_PRIOR, d.VOI_UTILITIES, cost=d.VOI_COST
            )
            for r in d.VOI_ACCURACIES
        ]
        gross = np.array([v.gross_value for v in values])
        net = np.array([v.net_value for v in values])
        information = np.array([v.information_nats for v in values])
        records = {
            "clock": "known cue accuracy sweep, not learning time",
            "accuracy": d.VOI_ACCURACIES.tolist(),
            "gross_utility": gross.tolist(),
            "net_utility": net.tolist(),
            "information_nats": information.tolist(),
            "cost_utility": d.VOI_COST,
        }
        count = len(values)
    else:
        raise ValueError(f"No numerical animation declared for chapter index {index}")
    images = []
    plt.rcParams.update({"font.size": 15, "axes.labelsize": 17, "axes.titlesize": 19})
    for frame in range(count):
        fig, axes = plt.subplots(1, 2, figsize=(11.66, 6.20), dpi=100)
        if index == 4:
            axes[0].bar([0, 1], descent.beliefs[frame], color=["#007d82", "#c65f2f"])
            axes[0].scatter(
                [0, 1], reference, marker="_", s=500, c="#153c42", label="Exact posterior"
            )
            axes[0].set(
                ylim=(0, 1),
                xticks=[0, 1],
                xticklabels=["State 0", "State 1"],
                ylabel="Belief probability",
            )
            axes[0].legend(loc="upper right")
            axes[1].plot(descent.free_energy, color="#ccd6d3", label="Complete reference")
            axes[1].plot(
                np.arange(frame + 1), descent.free_energy[: frame + 1], color="#007d82", lw=3
            )
            axes[1].axhline(
                core.surprise(d.LIKELIHOOD, d.PRIOR, d.BELIEF_OBS),
                color="#c65f2f",
                ls="--",
                label="Surprise bound",
            )
            axes[1].set(xlabel="Algorithm iteration", ylabel="Variational free energy (nats)")
            axes[1].legend()
            fig.suptitle(f"Belief descent: iteration {frame} / {count - 1}")
        elif index == 7:
            grid = np.linspace(-4, 4, 80)
            x, y = np.meshgrid(grid, grid)
            for ax, path, title, color in zip(
                axes, paths, ("Zero-drive transient", "Driven transient"),
                ("#007d82", "#c65f2f"), strict=True
            ):
                mean = path[samples[frame]]
                potential = core.free_energy(
                    x - mean[0], y - mean[1], precision=d.FLOW.precision
                )
                ax.contour(x, y, potential, levels=[0.5, 1, 2, 3], colors=color)
                ax.plot(path[:samples[frame] + 1, 0], path[:samples[frame] + 1, 1], color=color)
                ax.scatter(*mean, c=color, label="Ensemble mean")
                ax.scatter(0, 0, marker="+", c="#153c42", label="Stationary mean")
                ax.set(xlim=(-4, 4), ylim=(-4, 4), aspect="equal",
                       xlabel="State x", ylabel="State y", title=title)
                ax.legend(loc="upper left", fontsize=11)
            fig.suptitle(
                f"Model time = {samples[frame] * d.TRAJECTORY_DT:.2f}; covariance stays fixed")
        elif index == 8:
            grid = np.linspace(-2.4, 2.4, 13)
            x, y = np.meshgrid(grid, grid)
            omega = float(drives[frame])
            potential = core.free_energy(x, y, precision=d.FLOW.precision)
            axes[0].contour(x, y, potential, levels=8, colors="#ccd6d3")
            jx, jy = core.probability_current(
                x, y, precision=d.FLOW.precision, gamma=d.FLOW.gamma, omega=omega
            )
            axes[0].quiver(x, y, jx, jy, color="#c65f2f", scale=0.8)
            axes[0].set(aspect="equal", xlabel="State x", ylabel="State y",
                        title="Fixed density; stationary current")
            axes[1].plot(drives, sigma, c="#ccd6d3")
            axes[1].scatter(omega, sigma[frame], c="#007d82", s=90)
            axes[1].set(xlabel="Known drive parameter", ylabel="Entropy production (nats / time)",
                        title="Even-coordinate reversal")
            fig.suptitle(
                f"Stationary parameter sweep: drive = {omega:.2f}; not a time trajectory")
        elif index == 6:
            grid = np.linspace(-3, 3, 80)
            x, y = np.meshgrid(grid, grid)
            for ax, path, label in zip(
                axes, paths, ("Radial drift", "Rotating drift"), strict=True
            ):
                ax.contour(
                    x, y, 0.5 * d.FLOW.precision * (x * x + y * y), levels=8, colors="#d6e2df"
                )
                step = samples[frame]
                ax.plot(path[: step + 1, 0], path[: step + 1, 1], color="#007d82", lw=3)
                ax.scatter(*path[step], color="#c65f2f", s=110, zorder=4)
                ax.set(
                    xlim=(-3, 3),
                    ylim=(-3, 3),
                    aspect="equal",
                    xlabel="State x",
                    ylabel="State y",
                    title=label,
                )
            fig.suptitle(f"Model time = {samples[frame] * d.TRAJECTORY_DT:.2f}; both paths relax")
        else:
            r = d.VOI_ACCURACIES
            axes[0].plot(r, gross, color="#d6e2df")
            axes[0].plot(
                r[: frame + 1], gross[: frame + 1], color="#007d82", lw=3, label="Gross value"
            )
            axes[0].plot(
                r[: frame + 1], net[: frame + 1], color="#c65f2f", lw=3, label="Net after cost"
            )
            axes[0].axhline(0, color="#153c42", ls="--", label="Irrelevant-payoff control")
            axes[0].set(
                xlim=(0.5, 1),
                ylim=(-0.2, 0.55),
                xlabel="Known cue accuracy",
                ylabel="Expected utility gain",
            )
            axes[0].legend(loc="upper left")
            axes[1].plot(r, information, color="#d6e2df")
            axes[1].plot(r[: frame + 1], information[: frame + 1], color="#007d82", lw=3)
            axes[1].set(
                xlim=(0.5, 1),
                ylim=(0, 0.75),
                xlabel="Known cue accuracy",
                ylabel="Mutual information (nats)",
            )
            fig.suptitle(f"Accuracy = {r[frame]:.2f}; observation cost = {d.VOI_COST:.2f} utility")
        fig.tight_layout(rect=(0, 0, 1, 0.94))
        if index in (6, 7):
            fig.subplots_adjust(left=0.09, right=0.98, bottom=0.15, top=0.82, wspace=0.28)
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", facecolor="white")
        plt.close(fig)
        buffer.seek(0)
        images.append(Image.open(buffer).convert("RGB"))
    return images, records


def iter_model_frames(result, project: Path):
    cache = {}
    evidence = {}
    for index in (4, 6, 7, 8, 17):
        cache[index], evidence[str(index + 1)] = numerical_frames(project, index)
    (result.workspace.root / "animation_data.json").write_text(
        json.dumps(evidence, indent=2) + "\n"
    )
    boundaries = np.cumsum([0, *result.frame_durations_ms])
    chapter = 0
    plates = [Image.open(path).convert("RGB") for path in result.frame_paths]
    for n in range(round(result.total_ms / 1000 * 25)):
        elapsed = n * 40
        while chapter + 1 < len(plates) and elapsed >= boundaries[chapter + 1]:
            chapter += 1
        plate = plates[chapter]
        if chapter in cache:
            local = elapsed - boundaries[chapter]
            fraction = min(1, local / (result.frame_durations_ms[chapter] * 0.8))
            frame = round(fraction * (len(cache[chapter]) - 1))
            composed = plate.copy()
            composed.paste(cache[chapter][frame], (94, 243))
            yield composed
        else:
            yield plate

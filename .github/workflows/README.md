# Python checks

[checks.yml](checks.yml) runs on `main` pushes, pull requests and manual dispatch.

| Setting | Value |
| --- | --- |
| Python matrix | 3.10 minimum and established 3.14 verification runtime |
| uv | 0.12.0 |
| checkout | actions/checkout v7.0.1, pinned to its full commit |
| setup-uv | astral-sh/setup-uv v10.3.0, pinned to its full commit |
| Permissions | Repository contents read only |

Each job installs the locked dev extra, runs Ruff/mypy, checks tracked publication
assets and folder/link consistency, runs pytest with the 90% source coverage floor,
builds the package, and exercises the installed wheel in an isolated environment.

The workflow does not install Lean or the publication template. Native proof
tests report skips if Lake is absent; source-level formal contracts still run.
A green Python badge does not certify a native Lean build, rendered paper,
encoded video, hosted release or physical interpretation.

Reproduce the Python checks with [CONTRIBUTING.md](../../CONTRIBUTING.md).
For full proofs, use [formal setup](../../formal/README.md). Keep the action
versions and this inventory aligned. Edit requirements: [AGENTS.md](AGENTS.md).

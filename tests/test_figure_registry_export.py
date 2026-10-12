"""Real-file controls for the template-compatible figure metadata export."""

from pathlib import Path
import json

from PIL import Image
import pytest
import yaml

from src.figures.render_all import export_registry, FIGURE_RENDERERS


@pytest.fixture
def registry_root(tmp_path: Path) -> Path:
    source = (
        Path(__file__).resolve().parents[1] / "docs/manuscript/figure_registry.yaml"
    )
    target = tmp_path / "docs/manuscript/figure_registry.yaml"
    target.parent.mkdir(parents=True)
    target.write_bytes(source.read_bytes())
    figures = tmp_path / "output/figures"
    figures.mkdir(parents=True)
    for name in FIGURE_RENDERERS:
        Image.new("RGB", (2, 2), "white").save(figures / name)
    return tmp_path


def test_export_covers_generated_figures(registry_root: Path) -> None:
    result = json.loads(export_registry(registry_root).read_text())
    assert len(result["figures"]) == len(FIGURE_RENDERERS)
    assert {row["file"] for row in result["figures"]} == {
        f"output/figures/{name}" for name in FIGURE_RENDERERS
    }
    assert all(
        row["label"] == row["id"] and row["alt_text"] for row in result["figures"]
    )
    assert all(row["filename"] == Path(row["file"]).name for row in result["figures"])


@pytest.mark.parametrize(
    "case",
    [
        "root",
        "list",
        "entry",
        "label_type",
        "label_prefix",
        "duplicate_label",
        "path_type",
        "path_escape",
        "duplicate_file",
        "alt_type",
        "alt_empty",
        "incomplete",
        "corrupt",
        "missing",
    ],
)
def test_export_rejects_invalid_registry(registry_root: Path, case: str) -> None:
    source = registry_root / "docs/manuscript/figure_registry.yaml"
    payload = yaml.safe_load(source.read_text())
    first, second = payload["figures"][:2]
    if case == "root":
        payload = []
    elif case == "list":
        payload["figures"] = {}
    elif case == "entry":
        payload["figures"][0] = None
    elif case == "label_type":
        first["id"] = None
    elif case == "label_prefix":
        first["id"] = "wrong"
    elif case == "duplicate_label":
        second["id"] = first["id"]
    elif case == "path_type":
        first["file"] = None
    elif case == "path_escape":
        first["file"] = "output/figures/../escape.png"
    elif case == "duplicate_file":
        second["file"] = first["file"]
    elif case == "alt_type":
        first["alt_text"] = None
    elif case == "alt_empty":
        first["alt_text"] = " "
    elif case == "incomplete":
        payload["figures"].pop()
    elif case == "corrupt":
        (registry_root / first["file"]).write_bytes(b"broken")
    elif case == "missing":
        (registry_root / first["file"]).unlink()
    source.write_text(yaml.safe_dump(payload))
    with pytest.raises((ValueError, FileNotFoundError)):
        export_registry(registry_root)
    assert not (registry_root / "output/figures/figure_registry.json").exists()

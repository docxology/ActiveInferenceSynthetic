"""Exercise collection in a real checkout with no template infrastructure."""

import shutil
import subprocess
import sys
from pathlib import Path


def test_collects_without_template(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parent.parent
    tests = tmp_path / "tests"
    tests.mkdir()
    shutil.copy2(root / "tests/conftest.py", tests / "conftest.py")
    src = tmp_path / "src"
    src.mkdir()
    (src / "__init__.py").write_text("")
    shutil.copy2(root / "src/_prob.py", src / "_prob.py")
    (tests / "test_real_numerics.py").write_text(
        "import numpy as np\n"
        "import pytest\n"
        "from src._prob import kl_divergence\n"
        "def test_real_boundary():\n"
        "    assert kl_divergence(np.array([0.5, 0.5]), np.array([0.5, 0.5])) == 0\n"
        "    with pytest.raises(ValueError):\n"
        "        kl_divergence(np.array([1., 0.]), np.array([0., 1.]))\n"
    )
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(tests)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 passed" in result.stdout

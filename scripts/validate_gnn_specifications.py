"""Use the optional upstream GNN parser to check Synthetic's explicit carriers."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import demos


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--gnn-root', type=Path, required=True)
    parser.add_argument('--negative-controls', action='store_true')
    args = parser.parse_args()
    upstream = args.gnn_root.resolve()
    sys.path.insert(0, str(upstream / 'src'))
    from gnn.parsers.markdown_parser import MarkdownGNNParser

    root = Path(__file__).resolve().parents[1]
    expected = {
        'ou_regimes.md': {'precision': demos.FLOW.precision, 'gamma': demos.FLOW.gamma,
                          'omega_zero': 0.0, 'omega_driven': demos.OMEGA_NESS},
        'finite_agent.md': {'A_cue': demos.CUE, 'A_bet': demos.BET,
                            'D': demos.BELIEF, 'C_probs': demos.FLAT_PREFERENCES},
    }
    dimensions = {'ou_regimes.md': {'x': [2], 'Q_ou': [2, 2], 'D_ou': [2, 2]},
                  'finite_agent.md': {'A_cue': [2, 2], 'A_bet': [2, 2], 'D': [2]}}

    def validate(path: Path, name: str) -> dict[str, object]:
        result = MarkdownGNNParser().parse_file(str(path))
        if not result.success or result.errors:
            raise ValueError(f'GNN parse failed: {result.errors}')
        actual = {parameter.name: parameter.value for parameter in result.model.parameters}
        for key, value in expected[name].items():
            if key not in actual or not np.array_equal(np.asarray(actual[key]).squeeze(), value):
                raise ValueError(f'GNN/Synthetic parameter mismatch: {key}')
        declared = {variable.name: variable.dimensions for variable in result.model.variables}
        if any(declared.get(key) != value for key, value in dimensions[name].items()):
            raise ValueError('GNN/Synthetic dimension mismatch')
        return {'file': name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'parameters_checked': list(expected[name]), 'warnings': result.warnings}

    rows = [validate(root / 'data/gnn' / name, name) for name in expected]
    controls = []
    if args.negative_controls:
        source = (root / 'data/gnn/ou_regimes.md').read_text()
        for name, content in (
            ('wrong_gamma', source.replace('gamma=1.0', 'gamma=0.0')),
            ('wrong_dimension', source.replace('x[2,type=float]', 'x[3,type=float]')),
        ):
            with tempfile.TemporaryDirectory() as directory:
                changed = Path(directory) / 'ou_regimes.md'
                changed.write_text(content)
                try:
                    validate(changed, 'ou_regimes.md')
                except ValueError as error:
                    controls.append({'case': name, 'rejected': str(error)})
                else:
                    raise AssertionError(f'Negative control did not fail: {name}')
    revision = subprocess.run(['git', '-C', str(upstream), 'rev-parse', 'HEAD'],
                              check=True, capture_output=True, text=True).stdout.strip()
    parsers = upstream / 'src/gnn/parsers'
    receipt = {'status': 'PASS', 'gnn_revision': revision,
               'parser_sources_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                         for p in sorted(parsers.glob('*.py'))},
               'specifications': rows, 'negative_controls': controls,
               'scope': 'Upstream syntax parsing and exact local parameters/dimensions; no backend execution or proof transfer'}
    target = root / 'output/data/gnn_specifications.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({key: receipt[key] for key in ('status', 'gnn_revision', 'specifications', 'negative_controls')}, indent=2))


if __name__ == '__main__':
    main()

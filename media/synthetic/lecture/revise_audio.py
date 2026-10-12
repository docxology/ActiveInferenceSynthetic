"""Preserve the first production and regenerate only editorially flagged chapters."""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path

from lecturecreate.canonical import file_sha256
from lecturecreate.tts.elevenlabs import ElevenLabsTTSBackend


def main() -> None:
    """Create a fresh raw set with explicit text agreement for all reused recordings."""
    project = Path(__file__).resolve().parent
    secret = sys.stdin.readline().strip()
    if not secret:
        raise ValueError('Daniel credential required')
    os.environ['ELEVENLABS_API_KEY'] = secret
    backend = ElevenLabsTTSBackend(voice_id='f1fdYDHzR22JxAxrWWgE', sample_rate=48000)
    previous = json.loads((project / 'raw_audio/voice_receipt.json').read_text())
    parts = re.split(r'^## ', (project / 'narration_draft.md').read_text(), flags=re.M)[1:]
    out = project / 'raw_audio_reviewed'
    out.mkdir()
    rows = []
    try:
        for index, (part, old) in enumerate(zip(parts, previous, strict=True), 1):
            text = ' '.join(part.split('\n', 1)[1].split())
            target = out / f'b{index:02d}.wav'
            if text == old['text']:
                original = project / 'raw_audio' / target.name
                if file_sha256(original) != old['sha256']:
                    raise ValueError('Raw voice receipt drift')
                shutil.copyfile(original, target)
                method = 'exact-text recording reuse'
            else:
                backend.synthesize(text, target, voice='f1fdYDHzR22JxAxrWWgE')
                method = 'editorial Daniel resynthesis'
            rows.append({'beat': target.stem, 'text': text, 'sha256': file_sha256(target),
                         'method': method, 'voice': 'f1fdYDHzR22JxAxrWWgE'})
            print(f'{target.stem}: {method}', flush=True)
    finally:
        os.environ.pop('ELEVENLABS_API_KEY', None)
    (out / 'voice_receipt.json').write_text(json.dumps(rows, indent=2) + '\n')


if __name__ == '__main__':
    main()

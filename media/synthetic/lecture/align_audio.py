"""Align the measured paced recordings and transcribe every narration independently."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def main() -> None:
    """Use the supplied credential in memory; preserve raw service responses and bindings."""
    from elevenlabs.client import ElevenLabs

    parser = argparse.ArgumentParser()
    parser.add_argument('--action', choices=('align', 'transcribe'), required=True)
    args = parser.parse_args()
    secret = sys.stdin.readline().strip()
    if not secret:
        raise ValueError('Previously authorized ElevenLabs credential required')
    client = ElevenLabs(api_key=secret)
    project = Path(__file__).resolve().parent
    parts = re.split(r'^## ', (project / 'narration_draft.md').read_text(), flags=re.M)[1:]
    out = project / ('alignment' if args.action == 'align' else 'transcription')
    out.mkdir(exist_ok=True)

    def process(index: int) -> dict:
        text = ' '.join(parts[index - 1].split('\n', 1)[1].split())
        path = project / 'paced_audio' / f'b{index:02d}.wav'
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        target = out / f'b{index:02d}.json'
        if target.exists():
            saved = json.loads(target.read_text())
            if saved['audio_sha256'] != sha or saved['text'] != text:
                raise ValueError('Existing alignment/transcription input drift')
            return saved
        with wave.open(str(path)) as audio:
            duration = audio.getnframes() / audio.getframerate()
        with path.open('rb') as stream:
            if args.action == 'align':
                result = client.forced_alignment.create(
                    file=stream, text=text,
                    request_options={'timeout_in_seconds': 180, 'max_retries': 0})
            else:
                result = client.speech_to_text.convert(
                    file=stream, model_id='scribe_v1', language_code='en',
                    diarize=False, tag_audio_events=False, timestamps_granularity='word',
                    request_options={'timeout_in_seconds': 180, 'max_retries': 0})
        saved = {'beat': f'b{index:02d}', 'audio_sha256': sha, 'text': text,
                 'duration_s': duration, 'service': result.model_dump(mode='json')}
        if args.action == 'align':
            words = saved['service']['words']
            aligned_text = ' '.join(''.join(
                c['text'] for c in saved['service']['characters']).split())
            if not words or aligned_text != text:
                raise ValueError('Forced alignment lost authored text')
            if any(not 0 <= w['start'] <= w['end'] <= duration + 0.05 for w in words):
                raise ValueError('Alignment extends beyond measured speech')
        with target.open('x') as output:
            json.dump(saved, output, indent=2)
        print(f'{args.action}: b{index:02d} complete', flush=True)
        return saved

    with ThreadPoolExecutor(max_workers=3) as executor:
        rows = list(executor.map(process, range(1, len(parts) + 1)))
    summary = {'action': args.action, 'beats': len(rows),
               'files_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in sorted(out.glob('b*.json'))}}
    (out / 'receipt.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary | {'files_sha256': 'recorded'}, indent=2))


if __name__ == '__main__':
    main()

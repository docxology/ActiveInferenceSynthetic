"""Check every paced chapter with independent ASR and known-text CTC alignment."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import wave
from pathlib import Path


def main() -> None:
    """Preserve word times and ASR text for complete editorial and caption review."""
    import torch
    import whisperx
    from faster_whisper import WhisperModel
    from whisperx.alignment import align, load_align_model

    torch.set_num_threads(4)
    project = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio-dir', type=Path, default=project / 'paced_audio')
    parser.add_argument('--out', type=Path, default=project / 'local_speech_review')
    parser.add_argument('--previous', type=Path)
    args = parser.parse_args()
    parts = re.split(r'^## ', (project / 'narration_draft.md').read_text(), flags=re.M)[1:]
    out = args.out
    out.mkdir(exist_ok=True)
    alignment_model, metadata = load_align_model(language_code='en', device='cpu')
    asr_model = WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=4)
    print('Local English CTC and small.en ASR models ready', flush=True)
    rows = []
    for index, part in enumerate(parts, 1):
        path = args.audio_dir / f'b{index:02d}.wav'
        target = out / f'b{index:02d}.json'
        text = ' '.join(part.split('\n', 1)[1].split())
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        if args.previous and not target.exists():
            previous = args.previous / target.name
            if previous.is_file():
                saved = json.loads(previous.read_text())
                if saved['audio_sha256'] == sha and saved['text'] == text:
                    shutil.copyfile(previous, target)
        if target.exists():
            saved = json.loads(target.read_text())
            if saved['audio_sha256'] != sha or saved['text'] != text:
                raise ValueError('Existing speech-review binding drift')
            rows.append(saved)
            continue
        with wave.open(str(path)) as audio:
            duration = audio.getnframes() / audio.getframerate()
        samples = whisperx.load_audio(str(path))
        result = align([{'start': 0.0, 'end': duration, 'text': text}],
                       alignment_model, metadata, samples, 'cpu',
                       return_char_alignments=True)
        segments, _ = asr_model.transcribe(samples, language='en', beam_size=5,
                                           temperature=0, word_timestamps=True,
                                           condition_on_previous_text=False)
        segments = list(segments)
        transcription = ' '.join(segment.text.strip() for segment in segments)
        saved = {'beat': f'b{index:02d}', 'audio_sha256': sha, 'text': text,
                 'duration_s': duration, 'alignment': result,
                 'asr_text': transcription,
                 'asr_segments': [{'start': s.start, 'end': s.end, 'text': s.text,
                                    'avg_logprob': s.avg_logprob} for s in segments]}
        with target.open('x') as stream:
            json.dump(saved, stream, indent=2)
        rows.append(saved)
        print(f'Local complete-audio review: b{index:02d}', flush=True)
    receipt = {'chapters': len(rows),
               'method': 'Wav2Vec2 CTC known-text alignment + independent small.en ASR',
               'alignment_model': metadata, 'asr_model': 'Systran/faster-whisper-small.en',
               'files_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in sorted(out.glob('b*.json'))}}
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('PASS: every chapter aligned and independently transcribed', flush=True)


if __name__ == '__main__':
    main()

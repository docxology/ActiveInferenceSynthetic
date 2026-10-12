"""Construct lossless authored captions from measured CTC word alignment."""

from __future__ import annotations

import hashlib
import json
import math
import textwrap
from pathlib import Path

from lecturecreate.pipeline import PipelineResult


def build_aligned_captions(result: PipelineResult, project: Path, target: Path) -> dict:
    """Require complete audio/text bindings and valid word times before grouping cues."""
    cues = []
    bindings = []
    previous_end = 0
    for beat in result.lecture.iter_beats():
        row_path = project / 'sources/speech_review' / f'{beat.id}.json'
        row = json.loads(row_path.read_text())
        audio = project / 'sources/audio' / f'{beat.id}.wav'
        if row['audio_sha256'] != hashlib.sha256(audio.read_bytes()).hexdigest():
            raise ValueError('Caption alignment audio differs from frozen recording')
        if row['text'] != beat.narration or beat.start_ms is None or beat.duration_ms is None:
            raise ValueError('Caption narration or timeline differs from alignment')
        words = [word for segment in row['alignment']['segments']
                 for word in segment.get('words', [])]
        if [word['word'] for word in words] != beat.narration.split():
            raise ValueError('Aligned word sequence differs from complete authored narration')
        for word in words:
            if not all(isinstance(word.get(key), (int, float))
                       and math.isfinite(word[key]) for key in ('start', 'end')):
                raise ValueError('Missing or non-finite aligned word time')
            if not 0 <= word['start'] <= word['end'] <= row['duration_s'] + 0.002:
                raise ValueError('Aligned word outside measured recording')
        grouped = []
        current = []
        for word in words:
            proposed = current + [word]
            text = ' '.join(item['word'] for item in proposed)
            if current and (len(text) > 80 or len(proposed) > 12
                            or len(textwrap.wrap(text, 42, break_long_words=False,
                                                 break_on_hyphens=False)) > 2
                            or word['end'] - current[0]['start'] > 5):
                grouped.append(current)
                current = []
            current.append(word)
            if word['word'].endswith(('.', '?', '!')):
                grouped.append(current)
                current = []
        if current:
            grouped.append(current)
        for group in grouped:
            start = beat.start_ms + round(group[0]['start'] * 1000)
            end = beat.start_ms + round(group[-1]['end'] * 1000)
            if not previous_end <= start < end <= beat.start_ms + beat.duration_ms:
                raise ValueError('Aligned cue overlaps or extends beyond its speech span')
            text = ' '.join(word['word'] for word in group)
            cues.append({'start': start, 'end': end, 'text': textwrap.fill(
                text, width=42, break_long_words=False, break_on_hyphens=False)})
            previous_end = end
        bindings.append({'beat': beat.id, 'audio_sha256': row['audio_sha256'],
                         'alignment_sha256': hashlib.sha256(row_path.read_bytes()).hexdigest(),
                         'aligned_words': len(words)})

    def stamp(ms: int) -> str:
        hours, remainder = divmod(ms, 3600000)
        minutes, remainder = divmod(remainder, 60000)
        seconds, milliseconds = divmod(remainder, 1000)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}'

    expected = ' '.join(beat.narration for beat in result.lecture.iter_beats())
    actual = ' '.join(' '.join(cue['text'].split()) for cue in cues)
    if actual != expected:
        raise ValueError('Aligned captions lost or changed authored words')
    with target.open('x') as stream:
        stream.write('\n\n'.join(
            f'{index}\n{stamp(cue["start"])} --> {stamp(cue["end"])}\n{cue["text"]}'
            for index, cue in enumerate(cues, 1)) + '\n')
    return {'method': 'Known-text Wav2Vec2 CTC word alignment; no character-proportional timing',
            'captions': len(cues), 'complete_text_exact': True, 'bindings': bindings}

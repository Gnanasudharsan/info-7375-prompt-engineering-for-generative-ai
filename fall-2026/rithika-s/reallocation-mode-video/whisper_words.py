#!/usr/bin/env python3
"""whisper_words.py — word timestamps (word_times.json) and a pronunciation check.

Same approach as the final-project film: faster-whisper word timestamps from each beat's mp3,
fed ffmpeg-decoded 16 kHz audio (faster-whisper 1.2.1 does not work with av 19). Writes
word_times.json {"words": {beat_id: [[word, start_s, end_s], ...]}} for scenes.py's at() cues,
and prints whisper's transcript next to narration_text so mispronunciations show up.
"""
import json
import re
import subprocess
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel

HERE = Path(__file__).resolve().parent
MODEL = "base"


def pcm(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def norm(t):
    return re.sub(r"[^a-z0-9 ]+", " ", t.lower()).split()


def main():
    sheet = json.loads((HERE / "beat_sheet.json").read_text())
    m = WhisperModel(MODEL, device="cpu", compute_type="int8")
    out = {}
    for b in sheet["beats"]:
        bid = b["beat_id"]
        segs, _ = m.transcribe(pcm(HERE / b["audio_file"]), language="en", word_timestamps=True, beam_size=5)
        words = [[w.word.strip(), round(w.start, 3), round(w.end, 3)] for s in segs for w in s.words]
        out[bid] = words
        heard = " ".join(w[0] for w in words)
        ratio = SequenceMatcher(None, norm(b["narration_text"]), norm(heard)).ratio()
        print(f"--- {bid}  word-match {ratio:.3f}\n  said : {b['narration_text']}\n  heard: {heard}")
    (HERE / "word_times.json").write_text(json.dumps(
        {"model": f"faster-whisper {MODEL}", "speed": sheet["metadata"].get("kokoro_speed"),
         "note": "word start/end seconds per beat, from the measured narration mp3s", "words": out},
        indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()

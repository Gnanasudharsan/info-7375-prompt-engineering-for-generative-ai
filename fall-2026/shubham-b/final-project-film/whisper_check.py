#!/usr/bin/env python3
"""whisper_check.py — transcribe each narration mp3 locally (faster-whisper, no key) and print it
beside the script, so mispronounced words (Bagwe, Marino, EventFlow) are caught by ear AND text.

    python3 whisper_check.py > evidence/whisper-transcript.txt
"""
import json
import subprocess
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel

HERE = Path(__file__).resolve().parent


def pcm16k(path):
    """Decode with ffmpeg ourselves: faster-whisper 1.2.1's decoder passes an argument
    PyAV 19 no longer accepts (FRICTIONAL.md, 2026-10-13)."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


sheet = json.loads((HERE / "beat_sheet.json").read_text())
model = WhisperModel("base.en", device="cpu", compute_type="int8")
for b in sheet["beats"]:
    segs, _ = model.transcribe(pcm16k(HERE / b["audio_file"]), beam_size=5)
    heard = " ".join(s.text.strip() for s in segs)
    print(f"## {b['beat_id']}  ({b['actual_duration_s']:.2f} s)")
    print(f"script: {b['narration_text']}")
    print(f"heard:  {heard}\n")

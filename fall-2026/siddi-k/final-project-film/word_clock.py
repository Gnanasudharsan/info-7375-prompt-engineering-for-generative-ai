#!/usr/bin/env python3
"""word_clock.py: runs the toolkit's align.py (mp3/words.json) with an ffmpeg audio decoder.

Why: on this Windows machine faster-whisper 1.2.1 calls av.open(..., metadata_errors=...), which PyAV
19 removed, and PyAV < 15 has no Python 3.13 wheel. So this decodes with ffmpeg to 16 kHz float32
and hands faster-whisper the array. align.py itself is unchanged.

    python word_clock.py            # same arguments as align.py, reel folder defaults to here
"""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import faster_whisper.transcribe as _fwt

HERE = Path(__file__).resolve().parent
ART = Path(__import__("os").environ.get("ART_HOME", HERE.parent / "brutalist.art"))
FF = shutil.which("ffmpeg") or "ffmpeg"


def _decode(audio, sampling_rate=16000, split_stereo=False):
    if not isinstance(audio, (str, Path)):
        return audio
    raw = subprocess.run([FF, "-v", "error", "-i", str(audio), "-f", "f32le", "-ac", "1", "-ar", str(sampling_rate), "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


_fwt.decode_audio = _decode
sys.path.insert(0, str(ART / "runtime" / "scripts"))
import align  # noqa: E402

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append(str(HERE))
    align.main()

#!/usr/bin/env python3
"""finish_audio.py — after generate_audio_kokoro.py: give BOUT its 1.0 s silent tail (the show-tell
outro rule) and write every beat's ffprobe-measured duration back to beat_sheet.json.

Run once after every voicing. It is idempotent: it pads BOUT only when the file has no tail yet.
"""
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHEET = HERE / "beat_sheet.json"


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(path)]).decode())


def tail_silence(path):
    """Seconds of trailing silence (below -50 dB) at the end of the file."""
    out = subprocess.run(["ffmpeg", "-v", "info", "-i", str(path), "-af", "silencedetect=n=-50dB:d=0.3",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    ends = [l for l in out.splitlines() if "silence_start" in l]
    if not ends:
        return 0.0
    start = float(ends[-1].split("silence_start:")[1].split()[0])
    return max(0.0, dur(path) - start)


sheet = json.loads(SHEET.read_text())
for b in sheet["beats"]:
    f = HERE / b["audio_file"]
    if b["beat_id"] == "BOUT" and tail_silence(f) < 0.9:
        tmp = f.with_suffix(".pad.mp3")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(f), "-af", "apad=pad_dur=1.0",
                        "-c:a", "libmp3lame", "-q:a", "2", str(tmp)], check=True)
        tmp.replace(f)
        print("[finish_audio] BOUT padded with 1.0 s of silence")
    b["actual_duration_s"] = round(dur(f), 3)
SHEET.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print("[finish_audio] total", round(sum(b["actual_duration_s"] for b in sheet["beats"]), 2), "s over",
      len(sheet["beats"]), "beats")

#!/usr/bin/env python3
"""finish_audio.py — pad the two bookends and measure the real audio clock. Safe to re-run.

Pattern copied from the toolkit's worked example
(brutalist.art/youtube/show-tell-24-isometric-props/finish_audio.py): no toolkit script applies
`lead_silence_s` or `tail_silence_s`, so the film does it here.

- BIDEA: 0.8 s of silence before the greeting (lead_silence_s in the sheet).
- BOUT:  1.0 s of silence after the last word, so the card never cuts on the last syllable.
The unpadded Kokoro output is kept as mp3/beat-<ID>-unpad.mp3 and is always the source.
Then every beat's actual_duration_s is re-measured with ffprobe, and the ClaudeDefinitions card's
durationSeconds is set to its measured audio.
"""
import json
import subprocess
from pathlib import Path

R = Path(__file__).resolve().parent
PAD = {"BIDEA": "adelay=800:all=1", "BOUT": "apad=pad_dur=1"}

sheet = json.loads((R / "beat_sheet.json").read_text())
for b in sheet["beats"]:
    path = R / b["audio_file"]
    if b["beat_id"] in PAD:
        raw = path.with_name(path.stem + "-unpad.mp3")
        if not raw.exists():
            path.rename(raw)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", PAD[b["beat_id"]],
                        "-c:a", "libmp3lame", "-b:a", "192k", str(path)], check=True)
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                       "-of", "default=nw=1:nk=1", str(path)]))
    b["actual_duration_s"] = round(d, 3)
    if b["shot"].get("remotion", {}).get("pattern") == "ClaudeDefinitions":
        b["shot"]["remotion"]["props"]["durationSeconds"] = round(d, 3)

(R / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
(R / "mp3" / "timings.json").write_text(
    json.dumps({b["beat_id"]: b["actual_duration_s"] for b in sheet["beats"]}, indent=2) + "\n")
total = sum(b["actual_duration_s"] for b in sheet["beats"])
print(f"Measured runtime: {total:.2f} s ({int(total // 60)} min {total % 60:.1f} s)")

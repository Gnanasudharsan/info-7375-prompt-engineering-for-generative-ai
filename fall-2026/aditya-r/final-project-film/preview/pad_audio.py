#!/usr/bin/env python3
"""pad_audio.py — add measured silent holds around each preview beat's Kokoro narration.

Why: the three narration clips total 10.69 s of speech; Aditya asked for a ~15 s preview, so each
beat gets a short lead-in and a hold after its last word, letting the drawing land. The PADDED
file is the beat's audio (the master clock); its duration is measured with ffprobe and written
back to beat_sheet.json. Raw Kokoro output is kept in mp3/raw/ untouched.
Pattern reused from my-videos/youtube/claude-liam-next-token-loop/pad_audio.py (idea only).
"""
import json, shutil, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAD = 0.30
TAIL = {"B01": 1.20, "B02": 1.30, "B03": 0.90}


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]).decode())


sheet_p = HERE / "beat_sheet.json"
sheet = json.loads(sheet_p.read_text())
raw = HERE / "mp3" / "raw"
raw.mkdir(exist_ok=True)
for b in sheet["beats"]:
    bid = b["beat_id"]
    out = HERE / "mp3" / f"beat-{bid}.mp3"
    src = raw / out.name
    if not src.exists():                      # first run: move Kokoro's file aside, never re-pad a padded file
        shutil.copy2(out, src)
    speech = dur(src)
    target = LEAD + speech + TAIL[bid]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
                    "-af", f"adelay={int(LEAD * 1000)}:all=1,apad=whole_dur={target:.3f}",
                    "-c:a", "libmp3lame", "-q:a", "2", str(out)], check=True)
    b["audio_file"] = f"mp3/beat-{bid}.mp3"
    b["speech_s"] = round(speech, 3)
    b["lead_silence_s"] = LEAD
    b["tail_silence_s"] = TAIL[bid]
    b["actual_duration_s"] = round(dur(out), 2)
    print(f"{bid}: speech {speech:.3f}s + lead {LEAD} + tail {TAIL[bid]} -> measured {b['actual_duration_s']}s")
sheet_p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print("total", round(sum(b["actual_duration_s"] for b in sheet["beats"]), 2), "s")

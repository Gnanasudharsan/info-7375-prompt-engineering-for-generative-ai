#!/usr/bin/env python3
"""finish_audio.py: narration takes → audio/<BID>.wav, measured into beat_sheet.json.

    python finish_audio.py --src mp3 --prefix beat-   # Kokoro output (generate_audio_kokoro.py)
    python finish_audio.py                            # recorded takes in recordings/<BID>.(m4a|wav|mp3|…)

Per beat, it does the following with ffmpeg (local, free):
  * trims leading/trailing silence below -45 dB;
  * applies a gentle 80 Hz high-pass;
  * normalises loudness to -20 LUFS with a -2 dBTP ceiling (the toolkit's loudness gate wants
    -28..-18 LUFS and a true peak <= -1 dBTP);
  * pads 0.25 s before and 0.35 s after (BIDEA: 0.8 s before, the hesitant-writer lead;
    BOUT: 1.0 s after, the silent tail);
  * writes 48 kHz mono PCM.
Then it writes actual_duration_s and audio_file back to beat_sheet.json, plus mp3/timings.json.
Run ../brutalist.art/runtime/scripts/align.py . afterwards for the word clock (mp3/words.json).
The source takes are never modified.
"""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
FF = shutil.which("ffmpeg") or "ffmpeg"
FP = shutil.which("ffprobe") or "ffprobe"
EXTS = (".m4a", ".wav", ".mp3", ".aac", ".ogg", ".flac", ".webm", ".mp4")


def dur(p):
    return float(subprocess.check_output([FP, "-v", "error", "-show_entries", "format=duration",
                                          "-of", "default=nw=1:nk=1", str(p)]).decode().strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, default=HERE / "recordings")
    ap.add_argument("--prefix", default="", help="filename prefix before the beat id, e.g. beat-")
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    sheet_p = HERE / "beat_sheet.json"
    sheet = json.loads(sheet_p.read_text(encoding="utf-8"))
    (HERE / "audio").mkdir(exist_ok=True)
    (HERE / "mp3").mkdir(exist_ok=True)
    missing = []
    for b in sheet["beats"]:
        bid = b["beat_id"]
        if a.only and bid not in a.only:
            continue
        takes = [p for p in a.src.glob(a.prefix + bid + ".*") if p.suffix.lower() in EXTS]
        if not takes:
            missing.append(bid)
            continue
        lead = 0.8 if bid == "BIDEA" else 0.25
        tail = 1.0 if bid == "BOUT" else 0.35
        trim = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
                "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse")
        af = (f"{trim},highpass=f=80,loudnorm=I=-20:TP=-2:LRA=11,"
              f"adelay={int(lead * 1000)}:all=1,apad=pad_dur={tail}")
        out = HERE / "audio" / f"{bid}.wav"
        subprocess.run([FF, "-v", "error", "-y", "-i", str(takes[0]), "-af", af, "-ar", "48000", "-ac", "1",
                        "-c:a", "pcm_s16le", str(out)], check=True)
        d = round(dur(out), 3)
        b["audio_file"] = f"audio/{bid}.wav"
        b["actual_duration_s"] = d
        if bid == "BIDEA":
            b["shot"]["remotion"]["props"]["durationSeconds"] = d
        print(f"{bid}: {takes[0].name} -> {out.name}  {d:.2f}s")
    sheet_p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    timings = {b["beat_id"]: b.get("actual_duration_s") for b in sheet["beats"]}
    (HERE / "mp3" / "timings.json").write_text(json.dumps(timings, indent=2) + "\n", encoding="utf-8")
    total = sum(v for v in timings.values() if v)
    print(f"measured total: {total:.1f}s ({int(total // 60)}:{total % 60:04.1f})")
    if missing:
        print("missing takes:", " ".join(missing))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""pronunciation_check.py: transcribe every audio/<BID>.wav locally and set it beside the script.

The show-tell skill says to whisper-check Kokoro narration because it misreads acronyms and numbers.
This writes reports/PRONUNCIATION-CHECK.md for a human to read. It is a listening aid, not a pass/fail gate.

    python pronunciation_check.py [--model small]
"""
import argparse
import json
from pathlib import Path

import word_clock  # noqa: F401  (installs the ffmpeg decoder for faster-whisper)
from faster_whisper import WhisperModel

HERE = Path(__file__).resolve().parent
WATCH = ["F-1", "H-1B", "OPT", "CSV", "API", "four oh four", "Klaviyo", "Databricks", "Greenhouse", "NBA", "RAG",
         "Kommuri", "Siddi", "Labor Department", "80 Days"]

ap = argparse.ArgumentParser()
ap.add_argument("--model", default="small")
a = ap.parse_args()
model = WhisperModel(a.model, device="cpu", compute_type="int8")
sheet = json.loads((HERE / "beat_sheet.json").read_text(encoding="utf-8"))
rows = ["# PRONUNCIATION-CHECK", "",
        f"faster-whisper `{a.model}` (local, CPU) transcript of each narration file vs. the script. "
        "Whisper normalises spelling, so read this for words that come out wrong, not for punctuation.", ""]
for b in sheet["beats"]:
    wav = HERE / b["audio_file"]
    segs, _ = model.transcribe(str(wav), language="en", beam_size=5)
    heard = " ".join(s.text.strip() for s in segs)
    watch = [w for w in WATCH if w.lower() in b["narration_text"].lower()]
    rows += [f"## {b['beat_id']}", "", f"- **script:** {b['narration_text']}", f"- **heard:** {heard}",
             f"- **watch-list words in this beat:** {', '.join(watch) or 'none'}", ""]
    print(b["beat_id"], "|", heard)
(HERE / "reports").mkdir(exist_ok=True)
(HERE / "reports" / "PRONUNCIATION-CHECK.md").write_text("\n".join(rows) + "\n", encoding="utf-8")

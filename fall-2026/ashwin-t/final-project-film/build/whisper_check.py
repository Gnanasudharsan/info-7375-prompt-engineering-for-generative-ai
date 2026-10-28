"""Transcribe every beat's narration with faster-whisper and print it next to the script,
so mispronunciations (JUnit, Diffblue, Kafka, ProvenDocs...) are caught by ear-proxy."""
import json, sys
from pathlib import Path
from faster_whisper import WhisperModel
R = Path(__file__).resolve().parent
sheet = json.loads((R / "beat_sheet.json").read_text())
only = set(sys.argv[1:])
m = WhisperModel("base.en", device="cpu", compute_type="int8")
for b in sheet["beats"]:
    if only and b["beat_id"] not in only:
        continue
    segs, _ = m.transcribe(str(R / b["audio_file"]), language="en")
    heard = " ".join(s.text.strip() for s in segs)
    print(f"--- {b['beat_id']}\n SAID: {b['narration_text']}\nHEARD: {heard}")

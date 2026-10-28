"""Word timestamps of each beat mp3 with faster-whisper base.en -> word_timings.json (for burn_captions.py)."""
import json, sys
from pathlib import Path
from faster_whisper import WhisperModel
HERE = Path(__file__).resolve().parent.parent
m = WhisperModel("base.en", device="cpu", compute_type="int8")
out = {}
for mp3 in sorted((HERE / "mp3").glob("beat-B*.mp3")):
    segs, _ = m.transcribe(str(mp3), word_timestamps=True, language="en")
    out[mp3.stem.split("-")[1]] = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for s in segs for w in s.words]
    print(mp3.stem, " ".join(w["w"] for w in out[mp3.stem.split("-")[1]]))
(HERE / "word_timings.json").write_text(json.dumps(out, indent=1))

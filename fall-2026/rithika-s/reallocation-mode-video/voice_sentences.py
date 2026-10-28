#!/usr/bin/env python3
"""voice_sentences.py — per-sentence narration with natural pauses (Rithika, 2026-10-21).

Why this exists: the 8-beat script measures 2:50 at speed 1.04, and the film's target is
3:40–3:55 (hard limit < 4:00). Rithika chose sentence pauses over long dead air between beats:
speed 1.0, ~1.0 s after each sentence, up to 1.5 s on the terminal-text beats (B04, B05, B06)
so the text is readable, and ~1.5 s between beats.

How: the SAME engine and helpers as the toolkit's generate_audio_kokoro.py (imported, not copied):
Kokoro-82M, voice af_bella, speed 1.0, normalize_for_tts(). Each sentence of a beat's
narration_text is voiced separately, its leading/trailing silence trimmed (so every pause is
exactly the planned length), then the sentences are joined with silence and the beat gets a
silent tail. Output follows the house interface: mp3/beat-<ID>.mp3, mp3/timings.json, and
actual_duration_s + audio_file written back into beat_sheet.json from one measurement.

Usage (toolkit venv active):  python3 voice_sentences.py --speed 0.962 --sentence-pause 1.35
  (values used for the delivered film. Measured totals: speed 1.0 + pause 1.0 = 3:30.8; 0.962 + 1.2 = 3:38.6; both under the 3:40 floor)
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ART_HOME = Path(os.environ.get("ART_HOME", Path.home() / "brutalist-v2"))
sys.path.insert(0, str(ART_HOME / "runtime/scripts"))
from generate_audio_kokoro import load_engine, normalize_for_tts, lang_for, write_mp3, measure  # noqa: E402

SENTENCE_PAUSE_S = 1.0
TERMINAL_BEATS = {"B04": 1.4, "B05": 1.4, "B06": 1.4}   # readable terminal text; capped below the 1.5 s gap flag
BEAT_TAIL_S = 1.4                                      # between beats (~1.5 s, kept under the 1.5 s gap flag)
BOUT_TAIL_S = 1.0                                      # outro tail, as in the final-project film
EDGE_DB = -45.0                                        # trim threshold for each sentence's own edge silence
KEEP_EDGE_S = 0.04                                     # keep a hair of room tone so consonants are not clipped


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p]


def trim(samples, sr):
    x = np.asarray(samples, dtype=np.float32)
    if x.size == 0:
        return x
    thresh = 10 ** (EDGE_DB / 20) * max(1e-9, float(np.max(np.abs(x))))
    idx = np.where(np.abs(x) > thresh)[0]
    if idx.size == 0:
        return x
    keep = int(KEEP_EDGE_S * sr)
    return x[max(0, idx[0] - keep): min(x.size, idx[-1] + keep)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--speed", type=float, default=1.0,
                    help="Kokoro speed; Rithika's limit is a 1.04x change either way (0.962 = 1/1.0395)")
    ap.add_argument("--sentence-pause", type=float, default=SENTENCE_PAUSE_S)
    a = ap.parse_args()
    assert 1 / 1.04 <= a.speed <= 1.04, "speed change over 1.04x"
    sheet_path = HERE / "beat_sheet.json"
    sheet = json.loads(sheet_path.read_text())
    k = load_engine()
    (HERE / "mp3").mkdir(exist_ok=True)
    timings, plan = {}, {}
    for b in sheet["beats"]:
        bid, voice = b["beat_id"], b.get("voice") or sheet["metadata"]["voice"]
        pause = TERMINAL_BEATS.get(bid, a.sentence_pause)
        tail = BOUT_TAIL_S if bid == "BOUT" else BEAT_TAIL_S
        chunks, sr, sent_info = [], None, []
        sents = sentences(b["narration_text"])
        for i, s in enumerate(sents):
            samples, sr = k.create(normalize_for_tts(s, voice), voice=voice, speed=a.speed, lang=lang_for(voice))
            seg = trim(samples, sr)
            chunks.append(seg)
            sent_info.append({"text": s, "speech_s": round(seg.size / sr, 3)})
            gap = pause if i < len(sents) - 1 else tail
            chunks.append(np.zeros(int(round(gap * sr)), dtype=np.float32))
        out = HERE / "mp3" / f"beat-{bid}.mp3"
        write_mp3(np.concatenate(chunks), sr, out)
        dur = measure(out)
        b["actual_duration_s"] = round(dur, 2)
        b["audio_file"] = f"mp3/beat-{bid}.mp3"
        b["audio_build"] = {"method": "voice_sentences.py (per-sentence Kokoro, joined with silence)",
                            "speed": a.speed, "sentence_pause_s": pause, "tail_s": tail, "sentences": len(sents)}
        timings[bid] = round(dur, 2)
        plan[bid] = sent_info
        print(f"[sentences] beat-{bid}.mp3  {dur:6.2f}s  {len(sents)} sentences  pause {pause}s  tail {tail}s")
    sheet["metadata"]["kokoro_speed"] = a.speed
    sheet["metadata"]["audio_method"] = ("voice_sentences.py: per-sentence Kokoro af_bella at speed %.2f, "
                                         "%.2f s after each sentence (%s on terminal-text beats), %.1f s between beats, "
                                         "%.1f s outro tail" % (a.speed, a.sentence_pause,
                                                                ", ".join(f"{k} {v}s" for k, v in TERMINAL_BEATS.items()),
                                                                BEAT_TAIL_S, BOUT_TAIL_S))
    sheet_path.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
    (HERE / "mp3" / "timings.json").write_text(json.dumps(timings, indent=2) + "\n")
    (HERE / "mp3" / "sentences.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    print(f"[sentences] total {sum(timings.values()):.2f}s across {len(timings)} beats")


if __name__ == "__main__":
    main()

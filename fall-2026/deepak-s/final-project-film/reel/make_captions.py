#!/usr/bin/env python3
"""make_captions.py: cuegate-pitch.srt with the full narration, for the CueGate pitch film.

Why this exists: the toolkit's stage_publish.py writes one cue per beat and keeps only the first
three 42-character lines (textwrap.wrap(text, 42)[:3]), so long beats lose most of their words.
This script keeps every word. Each beat's narration_text is split into cues of at most two lines of
42 characters (Netflix's English line limit), at sentence and clause ends where possible. Cues are
timed inside the beat's real window, by each cue's share of the beat's characters, the same rule the
show-tell kit's until() uses for pacing. Beat offsets come from the compiled clips (clips/<BID>.mp4),
so the captions follow the master's timeline. The text is the source narration, not a transcription.

Usage: python3 make_captions.py            (run in the reel folder after `art final`)
"""
import json
import re
import subprocess
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_LINE, MAX_LINES = 42, 2


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "default=nw=1:nk=1", str(path)]))


def stamp(s):
    ms = round(s * 1000)
    h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); sec, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"


def chunks(text):
    """Split narration into pieces that fit two 42-character lines, breaking at sentence or clause ends first."""
    parts = re.split(r"(?<=[.?!:;])\s+|(?<=,)\s+", text.strip())
    out, cur = [], ""
    for p in parts:
        trial = (cur + " " + p).strip()
        if len(textwrap.wrap(trial, MAX_LINE)) <= MAX_LINES:
            cur = trial
            continue
        if cur:
            out.append(cur)
        while len(textwrap.wrap(p, MAX_LINE)) > MAX_LINES:     # a single long clause: cut at word boundaries
            words, piece = p.split(), ""
            for i, w in enumerate(words):
                t2 = (piece + " " + w).strip()
                if len(textwrap.wrap(t2, MAX_LINE)) > MAX_LINES:
                    out.append(piece); p = " ".join(words[i:]); break
                piece = t2
        cur = p
    if cur:
        out.append(cur)
    return out


sheet = json.loads((HERE / "beat_sheet.json").read_text())
cues, t, emitted = [], 0.0, []
for b in sheet["beats"]:
    bid = b["beat_id"]
    clip = HERE / "clips" / f"{bid}.mp4"
    window = dur(clip) if clip.exists() else float(b["actual_duration_s"])
    speech = float(b["actual_duration_s"]) - float(b.get("tail_silence_s") or 0) if b.get("tail_silence_s") else float(b["actual_duration_s"])
    speech = min(speech, window)
    pieces = chunks(b["narration_text"])
    total = sum(len(p) for p in pieces)
    at = t
    for p in pieces:
        span = speech * len(p) / total
        cues.append((at, at + span - 0.04, "\n".join(textwrap.wrap(p, MAX_LINE))))
        emitted.append(p)
        at += span
    t += window

assert " ".join(emitted).split() == " ".join(b["narration_text"] for b in sheet["beats"]).split(), "a word was lost"
assert all(len(l) <= MAX_LINE for _, _, c in cues for l in c.split("\n")) and all(c.count("\n") < MAX_LINES for _, _, c in cues)
srt = "\n\n".join(f"{i}\n{stamp(a)} --> {stamp(z)}\n{c}" for i, (a, z, c) in enumerate(cues, 1)) + "\n"
(HERE / f"{sheet['metadata']['slug']}.srt").write_text(srt)
print(len(cues), "cues; every narration word kept; timeline", round(t, 3), "s")

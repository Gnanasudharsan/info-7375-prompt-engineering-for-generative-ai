#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for the DayThread 15-second PREVIEW (three body beats only).

Aditya, 2026-10-14: "make ONLY a 15-second preview using the toolkit's normal 4K settings" —
three beats (the check-in mentions a tumble · the summary misses it, the separate check finds the
original words · the evidence reaches the coordinator's gate, nothing is sent). No opening, outro,
mascot or name test. Every frame carries "Constructed — proposed workflow".

Copied in shape from brutalist.art/skills/make/show-tell/reference/example-make_sheet.py.
Re-running this file keeps measured audio fields (audio_file, actual_duration_s, tail_silence_s)
so it never wipes the audio clock.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "daythread-preview"
TITLE = "DayThread — 15-second preview"

SPARSE_REASON = ("show-tell style: one drawn scene on a cream stage per beat, minimal labels, the voice "
                 "carries the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame "
                 "and contrast still apply.")


def beat(bid, narration, cls, image, show):
    return {"beat_id": bid, "act": "preview", "lane": "manim", "proof_gate": "SHOW",
            "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
            "voice": "am_onyx", "engine": "kokoro",
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                     "manim": {"class": cls}, "motion_claim": image},
            "qc": {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}}


B = [
    beat("B01", "A check-in mentions a tumble.", "B01_CheckIn",
         "The raw check-in page draws its handwriting lines; one line gets a terracotta dot and the words "
         "'a little tumble' land beside it.",
         [{"at": 0.1, "event": "page and lines"}, {"at": 0.4, "event": "tumble line marked + label"}]),
    beat("B02", "The summary misses it. DayThread's proposed check reads the original words.", "B02_Check",
         "A shorter summary page arrives with a visible gap where the tumble line was ('missed'); then a "
         "scan line sweeps the original page and brackets the tumble line.",
         [{"at": 0.1, "event": "summary page with gap"}, {"at": 0.55, "event": "scan sweeps original, brackets the line"}]),
    beat("B03", "It brings them to a coordinator before anything is sent.", "B03_Gate",
         "An evidence slip carrying the tumble line travels from the original page to the coordinator's review "
         "desk; the outbound envelope waits at a closed permission gate ('nothing sent').",
         [{"at": 0.1, "event": "desk and gate appear"}, {"at": 0.3, "event": "evidence slip travels to the desk"},
          {"at": 0.6, "event": "'nothing sent' at the closed gate"}]),
]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "DAYTHREAD · PREVIEW", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "aditya-raj-info7375", "persona": "synthesized voice (Kokoro am_onyx) reading Aditya Raj's script",
    "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9",
    "width": 3840, "height": 2160, "caption_policy": "none",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("15-second PREVIEW of three body beats only (Aditya, 2026-10-14: no opening, "
                              "outro or mascot). Not a film; bookend_check.py's outro rule is expected to fail "
                              "for this preview and is not a gate run by art run / art final."),
    "audience": "Aditya (review of the drawing style before the full film)",
    "source_doc": "../SCRIPT.md (v2); constructed example of a PROPOSED workflow — nothing observed",
    "playlist": "INFO 7375 final project pitch", "chapter_number": 0,
    "tags": ["DayThread", "preview", "constructed"]},
    "beats": B}

# keep the measured audio clock if it exists
old = HERE / "beat_sheet.json"
if old.exists():
    prev = {b["beat_id"]: b for b in json.loads(old.read_text())["beats"]}
    for b in B:
        p = prev.get(b["beat_id"], {})
        if p.get("narration_text") == b["narration_text"]:
            for k in ("audio_file", "actual_duration_s", "tail_silence_s", "lead_silence_s", "speech_s"):
                if k in p:
                    b[k] = p[k]

old.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(B), "beats; est", round(sum(b["estimated_duration_s"] for b in B), 1), "s")

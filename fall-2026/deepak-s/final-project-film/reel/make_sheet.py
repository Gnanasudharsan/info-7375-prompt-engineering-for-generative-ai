#!/usr/bin/env python3
"""make_sheet.py: beat_sheet.json for the CueGate pitch film (show-tell).

Narration is read verbatim from ../../inputs/NARRATION.md, one beat per table row; nothing is
retyped here. B00 and B01 depend on the real claude.ai exchange in ../../inputs/claude-exchange.md:
until that file exists they stay labelled slates and keep their date and count placeholders, and the
sheet is marked not ready for audio (metadata.audio_ready = false).

Run once before audio; never after `art final` (it would wipe the build stamps).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent                      # CueGate/
NARRATION = ROOT / "inputs" / "NARRATION.md"
EXCHANGE = ROOT / "inputs" / "claude-exchange.md"
SLUG = "cuegate-pitch"
TITLE = "CueGate"
HANDLE = "Deepak Kumaran T S"


def rows():
    """{beat_id: (label, visual, narration)} from the NARRATION.md beats table, text untouched."""
    out = {}
    for line in NARRATION.read_text().splitlines():
        if not line.startswith("| B"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 3:
            raise SystemExit(f"unexpected table row: {line[:80]}")
        beat, visual, narration = cells
        bid = beat.split()[0]
        key = bid
        if "branch A" in beat:
            key = "B01A"
        elif "branch B" in beat:
            key = "B01B"
        out[key] = (beat, visual, narration)
    return out


R = rows()
HAVE_EXCHANGE = EXCHANGE.is_file()
SPARSE = ("show-tell: one drawn picture on a cream stage per beat, labels beside the objects, the voice "
          "carries the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame and "
          "contrast still apply.")


def est(text):
    return round(len(text.split()) / 2.5, 1)


def manim_beat(bid, cls, show, constructed=None, key=None):
    beat, visual, narration = R[key or bid]
    b = {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
         "narration_text": narration, "estimated_duration_s": est(narration),
         "voice": "am_onyx", "engine": "kokoro",
         "qc": {"sparse_by_design": True, "sparse_reason": SPARSE},
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": visual, "motion_claim": visual,
                  "show": show, "manim": {"class": cls}}}
    if constructed:
        b["shot"]["constructed_label"] = constructed
    return b



# The real reply, read from inputs/claude-exchange.png on 2026-10-14 (curly quotes as shown on screen).
REPLY_ON_SCREEN = "\u201cNot in there tonight, not after that.\u201d"
REPLY_LINE = "Not in there tonight, not after that."
BUDGET = 38
# Deepak's call (STOP A): does the count include the reply's quotation marks?
#   "with_quotes"    -> 39 characters, over budget  -> B01 branch A, the count spoken as thirty-nine
#   "without_quotes" -> 37 characters, fits        -> B01 branch B
# Deepak, 2026-10-14: "Treat the quotes as delimiters if they mirror the prompt's quoting." The prompt quoted
# the source line, and the reply mirrors that quoting, so the quotes are delimiters: 37 characters, branch B.
COUNT_RULE = "without_quotes"
N_WORDS = {37: "Thirty-seven", 39: "Thirty-nine"}


def exchange():
    """Date and reply from inputs/claude-exchange.md; the reply must match what the screenshot shows."""
    text = EXCHANGE.read_text()
    date = re.search(r"^- Date:\s*(\S+)", text, re.M).group(1)
    reply = text.split("## Reply (exactly as received)", 1)[1].strip()
    core = reply.strip("<>").strip().strip('"\u201c\u201d')
    if core != REPLY_LINE:
        raise SystemExit(f"claude-exchange.md reply {reply!r} does not match the screenshot ({REPLY_ON_SCREEN})")
    return date


def spoken_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
              "October", "November", "December"]
    ords = {14: "fourteenth"}
    if d not in ords:
        raise SystemExit(f"add the spoken ordinal for day {d}")
    return f"{months[m - 1]} {ords[d]}, {y}"


beats = []
if not HAVE_EXCHANGE:
    raise SystemExit("inputs/claude-exchange.md is missing: B00 and B01 need the real exchange.")
DATE = exchange()
beat, visual, narration = R["B00"]
assert narration.count("[DATE]") == 1
beats.append({"beat_id": "B00", "act": "cold open", "lane": "pantry", "proof_gate": "SHOW",
              "narration_text": narration.replace("[DATE]", spoken_date(DATE)),
              "estimated_duration_s": est(narration), "voice": "am_onyx", "engine": "kokoro",
              "qc": {"sparse_by_design": True, "sparse_reason": "Real screenshot (evidence) on the cream stage with its date caption."},
              "shot": {"type": "STILL", "source": "own", "motion": "hold", "visual_intent": visual,
                       "still": "media/B00.png, built by make_b00.py from inputs/claude-exchange.png (unaltered) plus a date caption",
                       "exchange_date": DATE,
                       "show": [{"at": 0.0, "event": "Deepak's real claude.ai exchange, dated " + DATE}]}})
if COUNT_RULE is None:
    beat, visual, narration = R["B01A"]
    beats.append({"beat_id": "B01", "act": "cold open", "lane": "pantry", "proof_gate": "SHOW",
                  "narration_text": narration, "estimated_duration_s": est(narration),
                  "voice": "am_onyx", "engine": "kokoro",
                  "pending": "COUNT_RULE: Deepak decides whether the reply's quotation marks count (39, branch A) or not (37, branch B)",
                  "shot": {"type": "STILL", "source": "own", "motion": "hold", "visual_intent": visual,
                           "show": [{"at": 0.0, "event": "SLATE until the counting rule is decided"}]}})
else:
    n = {"with_quotes": len(REPLY_ON_SCREEN), "without_quotes": len(REPLY_LINE)}[COUNT_RULE]
    key = "B01A" if n > BUDGET else "B01B"
    beat, visual, narration = R[key]
    if key == "B01A":
        assert narration.count("[N]") == 1
        narration = narration.replace("[N]", N_WORDS[n])
    b = manim_beat("B01", "B01_Count", [{"at": 0.05, "event": "the real reply line and an empty budget bar"},
                                        {"at": 0.3, "event": "the count climbs against the 38 mark"},
                                        {"at": 0.8, "event": "over: an ink cross at the overflow; fits: an ink check"}], key=key)
    b["narration_text"] = narration
    b["estimated_duration_s"] = est(narration)
    b["shot"]["count"] = {"n": n, "budget": BUDGET, "rule": COUNT_RULE,
                          "text": REPLY_ON_SCREEN if COUNT_RULE == "with_quotes" else REPLY_LINE}
    beats.append(b)

beats += [
    manim_beat("B02", "B02_Gate", [{"at": 0.05, "event": "subtitle file arrives"},
                                    {"at": 0.25, "event": "gate and side door draw"},
                                    {"at": 0.62, "event": "one line peels off to the escalated door"},
                                    {"at": 0.8, "event": "file passes the gate, check lands"}]),
    manim_beat("B03", "B03_Rules", [{"at": 0.05, "event": "film frame, subtitle bar runs past its edge"},
                                     {"at": 0.3, "event": "three rule markers land: reading speed, gap, shot change"},
                                     {"at": 0.8, "event": "a flag rises on the bar"}]),
    manim_beat("B04", "B04_Alternatives", [{"at": 0.05, "event": "left: one line, a small button, a cursor clicks it"},
                                            {"at": 0.6, "event": "right: a whole file rides through the gate"},
                                            {"at": 0.85, "event": "drift gauge appears under the gate"}]),
    manim_beat("B05", "B05_Report", [{"at": 0.0, "event": "CONSTRUCTED label up for the whole beat"},
                                      {"at": 0.1, "event": "a subtitle page and a film frame drop into the tray"},
                                      {"at": 0.45, "event": "report rows grow: broken, fixed, refused"}],
               constructed="CONSTRUCTED"),
    manim_beat("B06", "B06_Ladder", [{"at": 0.05, "event": "ladder with three rungs: timing, line breaks, shorten"},
                                      {"at": 0.3, "event": "a token climbs rung by rung"},
                                      {"at": 0.65, "event": "candidate pages appear, the counter checks them"}]),
    manim_beat("B07A", "B07A_Evidence", [{"at": 0.05, "event": "source line (asked) and the real reply (got back) side by side"},
                                          {"at": 0.25, "event": "a check: it fit the budget"},
                                          {"at": 0.45, "event": "grey bars highlight the shifted phrases: hedged opinion, flat refusal"},
                                          {"at": 0.8, "event": "the counter block sits below, between them"}]),
    manim_beat("B07B", "B07B_Plan", [{"at": 0.05, "event": "station 1, invariants, with three tags (numbers, names, not)"},
                                      {"at": 0.3, "event": "station 2, the weaker meaning check; the token moves on"},
                                      {"at": 0.6, "event": "station 3, a stack of 100 hand-labelled lines"},
                                      {"at": 0.85, "event": "a small chart: the number that will be published"}]),
    manim_beat("B08", "B08_Tiles", [{"at": 0.05, "event": "five tiles land one by one as each skill is named"},
                                     {"at": 0.85, "event": "evidence pages slide under the tiles"}]),
    manim_beat("B09", "B09_Scope", [{"at": 0.05, "event": "three columns: IN, OUT, FIRST"},
                                     {"at": 0.3, "event": "translation icon crossed out under OUT"},
                                     {"at": 0.6, "event": "a small terminal with the word check under FIRST"}]),
    manim_beat("B10", "B10_Filmstrip", [{"at": 0.05, "event": "filmstrip draws"},
                                         {"at": 0.35, "event": "fast motion across three frames is wrongly marked as a cut"},
                                         {"at": 0.75, "event": "a cut list page sets the real cut marker"}]),
    manim_beat("B11", "B11_Split", [{"at": 0.05, "event": "split panel: already have / new"},
                                     {"at": 0.35, "event": "harness page and the timeline gate sit on the left"},
                                     {"at": 0.75, "event": "timing, shot, standards and meaning items arrive on the right"}]),
    manim_beat("B12", "B12_Lists", [{"at": 0.05, "event": "EXISTS list with the dated plan and PDF pages"},
                                     {"at": 0.45, "event": "WILL list draws as ghost outlines"}]),
    manim_beat("B13", "B13_YourTurn", [{"at": 0.05, "event": "a drawn prompt card with one subtitle line"},
                                        {"at": 0.45, "event": "a counter block ticks up"},
                                        {"at": 0.8, "event": "a check lands beside the kept \"not\""}]),
]

beat, visual, narration = R["B14"]
beats.append({"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
              "narration_text": narration, "estimated_duration_s": est(narration) + 1.0,
              "voice": "am_onyx", "engine": "kokoro", "kind": "outro_voice", "tail_silence_s": 1.0,
              "shot": {"type": "REMOTION", "source": "own", "visual_intent": visual,
                       "show": [{"at": 0.0, "event": "title CueGate and the narrator's name"}],
                       "remotion": {"pattern": "ClaudeTitleOutro",
                                    "props": {"title": TITLE, "slug": SLUG, "handle": HANDLE,
                                              "showMascot": False, "subline": ""}}}})

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "CUEGATE · PITCH", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "cuegate-pitch", "channel_title": HANDLE,
    "persona": "Deepak Kumaran T S (narration written by Deepak, voiced by Kokoro am_onyx)",
    "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Plain",
    "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "srt sidecar (stage_publish.py, local only, after Deepak approves its file list)",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("CueGate pitch (Deepak, 2026-10-14): B00 opens on Deepak's real claude.ai screenshot "
                              "as a still, not the ClaudeComposerAsk mock; no verdict card; Your Turn (B13) is a "
                              "drawn prompt card because the film shows no Claude UI mock-up. The spoken outro stays."),
    "audience": "a subtitle QC lead at a localization vendor, and a hiring manager for applied-AI roles",
    "source_doc": "inputs/NARRATION.md (Deepak); inputs/PROJECT-BRIEF.md; evidence/day-one/FINDINGS.md (2026-10-14)",
    "audio_ready": COUNT_RULE is not None,
    "playlist": "INFO 7375 final project pitch", "chapter_number": 0,
    "tags": ["CueGate", "subtitles", "verification", "prompt contracts", "evaluation"]},
    "beats": beats}

(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(beats), "beats; est", round(sum(b["estimated_duration_s"] for b in beats)), "s; audio_ready =", COUNT_RULE is not None)

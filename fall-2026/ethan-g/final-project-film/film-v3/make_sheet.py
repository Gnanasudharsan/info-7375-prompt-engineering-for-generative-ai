#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for the DataSentry final-project pitch, VERSION 3 (v2 + the Claude-written checks, scored) (Ethan Gomes, INFO 7375).

show-tell format: one drawn isometric picture per beat, a label or two, the narration explains.
Assignment rules override the skill's house bookends: narrated as Ethan (first person), no
instructor name, persona, or credit line — so no "Liam, in for Bear" greeting, no @NikBearBrown
outro card (ClaudeTitleOutro hard-codes that handle), no Your Turn composer. The film closes on a
drawn beat (BEND) with the project title and Ethan's name instead.

Honesty rule: nothing in DataSentry exists yet. Past tense only for what exists today
(this pitch, the brief, the notes on dbt / GX). Everything about the tool is "will".
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "datasentry-pitch-v3"
TITLE = "DataSentry: A Project Pitch"
VOICE = "am_michael"   # a stock Kokoro voice, not the toolkit's Liam persona (am_onyx)
SPARSE = ("show-tell: one drawn object on a cream stage, a label or two; the voice explains. "
          "Only underfill and clustered are waived; edge-bleed, empty-frame and contrast still apply.")


def beat(bid, act, narration, cls, intent, show, sparse=True, **extra):
    b = {"beat_id": bid, "act": act, "lane": "manim", "proof_gate": "SHOW", "narration_text": narration,
         "estimated_duration_s": round(len(narration.split()) / 2.6, 1), "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": intent, "show": show,
                  "manim": {"class": cls}, "motion_claim": intent}}
    if sparse:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE}
    b.update(extra)
    return b


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate, "narration_text": narration,
         "estimated_duration_s": round(len(narration.split()) / 2.6, 1), "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


OPEN = [
 beat("BIDEA", "title",
    "This is a Final Project Pitch Film created by Ethan Gomes. The project is called Data Sentry, and its first "
    "pieces already run. The question isn't whether Claude can write data checks. It's whether anyone can measure "
    "what they miss.",
    "BIDEA_Title", "Title card: 'DataSentry' large and centred; a thin rule draws beneath it with one terracotta dot; one line below: 'Scoring AI-written data checks with planted defects'.",
    [{"at": 0.05, "event": "DataSentry"}, {"at": 0.2, "event": "rule + dot"}, {"at": 0.3, "event": "one-line description"}],
    lead_silence_s=0.8),
 beat("BSIMPLE", "in plain words",
    "In plain words: companies set rules to catch bad data, like a taxi fare below zero. Data Sentry tests those "
    "rules the way you'd test a spell-checker: hide some mistakes on purpose, then count which ones it catches, "
    "and which slip through.",
    "BSIMPLE_Spellcheck", "Plain-language picture: a page of writing; terracotta marks are hidden in it on purpose; a magnifier passes over and ticks the ones it finds; one mark is left with no tick ('slipped through').",
    [{"at": 0.2, "event": "the page"}, {"at": 0.55, "event": "mistakes hidden"}, {"at": 0.8, "event": "caught / slipped through"}]),
]

BODY = [
 # Q1 — what is it
 beat("B00", "what it is",
    "Data Sentry has an AI write data checks for a table, then scores those checks by planting defects they "
    "have to catch.",
    "B00_Scanner", "A checkpoint scanner arch lands on the stage with its floor shadow; the name 'DataSentry' sits beside it; a parcel (the table) slides under the arch.",
    [{"at": 0.1, "event": "scanner lands"}, {"at": 0.35, "event": "label"}, {"at": 0.7, "event": "parcel rides in"}]),
 beat("B01", "what it is",
    "When it's done, it will be a public GitHub repo with three parts: a part that writes checks, a defect planter, "
    "and a scorecard of what was caught and what was missed. All three have already run.",
    "B01_Repo", "A kraft crate labelled 'public GitHub repo / when done' opens; three parts rise beside it one by one, a check page, a dark planter block, a binder; each labelled once.",
    [{"at": 0.15, "event": "crate opens"}, {"at": 0.45, "event": "check writer"}, {"at": 0.6, "event": "defect planter"}, {"at": 0.75, "event": "scorecard"}]),
 # how it will work
 beat("B02", "the data",
    "It starts from public data. My first run used New York City yellow taxi trips from January twenty "
    "twenty-five, sampled to ten thousand rows.",
    "B02_Table", "A flat table card lands; column blocks and grey rows fill in; labels 'NYC taxi · Jan 2025' and the real sample size from the first run.",
    [{"at": 0.15, "event": "table lands"}, {"at": 0.5, "event": "rows stack"}, {"at": 0.7, "event": "columns"}]),
 beat("B03", "under the hood",
    "Under the hood, part one. Python and pandas load the table. A planter script makes copies, breaks each one a "
    "different way, five ways in all, and writes an answer key that no check ever reads.",
    "B03_PipeOne", "Pipeline, part one (exists): a table card, an arrow to a dark planter block, an arrow to a broken copy with terracotta marks, and a locked answer key beside it; labels 'pandas', 'planter', 'answer key'.",
    [{"at": 0.2, "event": "pandas loads the table"}, {"at": 0.45, "event": "planter breaks a copy"}, {"at": 0.7, "event": "answer key, locked"}]),
 beat("B04", "under the hood",
    "Part two. Claude, Opus five point five, saw only the column names and types, and wrote pandera checks under "
    "a prompt contract. Each check runs on the clean copy and every broken copy, and a scorer compares the flags "
    "with the answer key, one defect type at a time.",
    "B04_PipeTwo", "Pipeline, part two, titled 'Part 2': a workstation (Claude) writes check pages; the checks run over the clean and broken copies; the scorer binder lands with a tick and a dot (caught / missed); labels 'Claude / Opus 5.5', 'pandera checks', 'scorer'.",
    [{"at": 0.15, "event": "Claude Code"}, {"at": 0.4, "event": "pandera checks"}, {"at": 0.75, "event": "scorer, per defect"}]),
 # Q2 — why care, real alternatives
 beat("B06", "why care",
    "Why would anyone care? I ran one rule, fare can't be negative, in two tools data teams use. In D B T, it "
    "passed the clean copy and failed twenty-five rows of the broken one.",
    "B06_Dbt", "Recorded output (typeset) of the real dbt run: dbt build with the not_negative test PASS on trips_clean and FAIL 25 on trips_broken; tagged 'recorded output · <date>'.",
    [{"at": 0.3, "event": "trays"}, {"at": 0.6, "event": "four test blocks drop"}]),
 beat("B07", "why care",
    "In Great Expectations, with the free G X Core, the same: pass, then twenty-five unexpected values. Its paid "
    "G X Cloud adds Expect A I, which suggests checks for you. I tested that same idea with Claude.",
    "B07_Gx", "Recorded output (typeset) of the real GX Core run: ExpectColumnValuesToBeBetween(fare_amount, min_value=0), PASS on clean, FAIL 25 unexpected on broken; 'ExpectAI (GX Cloud): not run'.",
    [{"at": 0.2, "event": "right tray"}, {"at": 0.5, "event": "suggested pages"}, {"at": 0.75, "event": "stamp"}]),
 beat("B08", "why care",
    "But I had planted twenty-five trips that end before they start. None of the three tools flagged them, because "
    "no rule asked. Data Sentry tells a data engineer which bad rows their checks let through.",
    "B08_Gap", 'Recorded output (typeset): the three tools side by side (all PASS clean, FAIL 25 broken), then the answer key: negative fares 25/25 CAUGHT, drop-off before pick-up 0/25 MISSED.',
    [{"at": 0.25, "event": "broken parcel slides past"}, {"at": 0.7, "event": "the gap"}]),
 # Q3 — who opens it
 beat("B09", "who opens it",
    "Who opens it? A hiring manager for a data engineering role. One command shows each defect type, caught or "
    "missed. My one hand-written rule caught two of five. Claude's first checks caught all five, but rejected two "
    "hundred twenty good trips. Its revision fixed that, and missed every negative fare.",
    "B09_FirstMinute", 'Recorded output (typeset) of the scorecard from ./score_round.sh 1 and 2: hand-written 1 rule, clean PASS, 2 of 5; Claude round 1, 220 clean rows flagged, 5 of 5; round 2, 1 check crashes, 4 of 5; round 2 negative fares 0/25 MISSED; tagged "Claude Opus 5.5 · recorded output · <date>".',
    [{"at": 0.2, "event": "window opens"}, {"at": 0.45, "event": "one command"}, {"at": 0.7, "event": "result rows"}]),
 # Q4 — what it proves
 beat("B10", "what it proves",
    "What does it prove? Four skills from this class, each with a run behind it: a prompt contract, a two-round "
    "loop, a clean-copy control, and a catch rate per defect. I test an AI's output instead of trusting it.",
    "B10_Proves", "An evidence binder; its cover opens; four record sheets fan out in a row with ink numerals 1 to 4, one per skill named.",
    [{"at": 0.15, "event": "binder opens"}, {"at": 0.3, "event": "1"}, {"at": 0.45, "event": "2"}, {"at": 0.62, "event": "3"}, {"at": 0.75, "event": "4"}]),
 # Q5 — in / out / first
 beat("B11", "scope",
    "In scope: one table, five defect types, one scorecard. Out of scope, on purpose: orchestration, so no "
    "Airflow. The first pieces have run, and each run saves its scorecard with the date.",
    "B11_Scope", "An 'in scope' box fills (table, defects, scorecard); Airflow stays outside; a printed slip with a tick, labelled with the date the first piece ran.",
    [{"at": 0.15, "event": "queue"}, {"at": 0.5, "event": "out of scope stays back"}, {"at": 0.75, "event": "first run"}]),
 # Q6 — risk
 beat("B12", "risk",
    "What could sink it? Checks that are too strict, or too loose, like Claude's two rounds. So the clean copy and "
    "the broken copies are both required, every time.",
    "B12_Loose", "A permission gate with its barrier raised; a broken parcel rides straight through; then the barrier comes down and the next broken parcel stops.",
    [{"at": 0.2, "event": "barrier up"}, {"at": 0.45, "event": "broken parcel slips through"}, {"at": 0.8, "event": "barrier down"}]),
 # Q7 — why this project
 beat("B13", "why this project",
    "Why this project? In my Food Inspections Dataset Project, my checks let bad rows through, and I didn't know "
    "which ones until later. Data Sentry measures exactly that. It's a mix: pandera, D B T, Great Expectations, "
    "and prompting Claude are new to me. Working with messy public data, I've done before, in that project.",
    "B13_Why", "A table card labelled 'Food Inspections Dataset Project' gets terracotta marks (bad rows that got through); an arrow leads to two lists: 'New to me: pandera, dbt, GX, Claude' and 'Done before: messy public data'.",
    [{"at": 0.15, "event": "desk + roles"}, {"at": 0.5, "event": "skills drop in"}, {"at": 0.9, "event": "arrow to the role"}]),
 # exists vs will exist
 beat("B14", "honesty",
    "Where this stands, October twenty-fifth. What exists: this pitch, the five-defect planter, the scorer, and two "
    "rounds of checks written by Claude, all run on real taxi data. Still to build: the public repo, and a loop "
    "that runs on its own.",
    "B14_Exists", "Two columns dated by the run: three real pages land under 'exists' (this pitch, the five-defect planter and scorer, two rounds of Claude's checks); two empty slots under 'will exist' (the public repo, a loop that runs on its own).",
    [{"at": 0.3, "event": "exists"}, {"at": 0.65, "event": "will exist"}]),
 beat("BEND", "close",
    "That's Data Sentry. I'm Ethan Gomes. Thanks for watching.",
    "BEND_Close", "The scanner from B00 returns; the title and Ethan's name land beside it.",
    [{"at": 0.2, "event": "scanner"}, {"at": 0.5, "event": "title and name"}], tail_silence_s=1.0),
]

BEATS = OPEN + BODY

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "FINAL PROJECT · PITCH", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "ethan-gomes", "channel_title": "@EthanGomes14", "persona": "Ethan Gomes (narrated in first person; synthetic Kokoro voice)",
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Plain", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("Course assignment (INFO 7375 Final Project Pitch Film): narrate as yourself, no instructor name, "
                              "persona, or credit line. No composer cold open, no verdict card, no Your Turn. The house outro "
                              "card (ClaudeTitleOutro) hard-codes @NikBearBrown, so the film closes on a drawn beat (BEND) instead; "
                              "bookend_check.py is expected to report the missing ClaudeTitleOutro, and that is recorded in FRICTIONAL.md."),
    "audience": "INFO 7375 instructor and TAs; a data engineering hiring manager",
    "source_doc": "PROJECT-BRIEF.md (2026-10-14); docs.getdbt.com/docs/build/data-tests (read 2026-10-14); "
                  "greatexpectations.io blog '2025 In Review' (2026-01-09, read 2026-10-14); nyc.gov TLC trip record data page",
    "playlist": "", "chapter_number": 0,
    "tags": ["data engineering", "data quality", "pandera", "Claude Code", "evaluation", "final project pitch"]},
    "beats": BEATS}

# carry measured audio forward when the narration is unchanged (show-tell gate trap 4)
old = {}
p = HERE / "beat_sheet.json"
if p.exists():
    for ob in json.load(open(p))["beats"]:
        old[ob["beat_id"]] = ob
for b in BEATS:
    ob = old.get(b["beat_id"])
    if ob and ob.get("narration_text") == b["narration_text"]:
        for k in ("actual_duration_s", "audio_file"):
            if k in ob:
                b[k] = ob[k]
    dur = b.get("actual_duration_s")
    props = (b["shot"].get("remotion") or {}).get("props")
    if dur and props is not None and b["shot"]["remotion"]["pattern"] == "ClaudeDefinitions":
        props["durationSeconds"] = dur

p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
words = sum(len(b["narration_text"].split()) for b in BEATS)
print(len(BEATS), "beats;", words, "words; est", round(sum(b.get("actual_duration_s") or b["estimated_duration_s"] for b in BEATS)), "s")

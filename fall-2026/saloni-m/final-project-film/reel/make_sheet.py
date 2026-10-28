#!/usr/bin/env python3
"""make_sheet.py — writes beat_sheet.json for the OPT Countdown pitch film.

One opening card (the hesitant writer), eleven drawn Manim beats (one picture per
idea, show-tell style), and a drawn outro card. Narrated by me, Saloni, with the
local Kokoro voice af_heart. Edit the narration here, then re-run this file.

Spelling notes for Kokoro: "O P T", "H one B", "D S O", "read me", "four oh four".
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "opt-countdown-pitch"
TITLE = "OPT Countdown: Final Project Pitch"
VOICE = "af_heart"
SPARSE = ("show-tell style: one drawn picture on a cream stage per beat, with the "
          "voice carrying the explanation. Only underfill and clustered are waived.")


def beat(bid, narration, cls, picture):
    """One drawn beat: narration + the Manim class that draws it."""
    return {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
            "narration_text": narration,
            "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
            "voice": VOICE, "engine": "kokoro",
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": picture,
                     "motion_claim": picture, "manim": {"class": cls}},
            "qc": {"sparse_by_design": True, "sparse_reason": SPARSE}}


OPEN = {
    "beat_id": "BIDEA", "act": "the question", "lane": "bookend", "proof_gate": "SHOW",
    "narration_text": ("Hi, I'm Saloni, and this is the pitch for my final project. "
                       "Part of it exists today as a prototype. Most of it doesn't yet, "
                       "and I'll say which is which. A student on O P T asks, which jobs can I get? "
                       "The better question is, which jobs can I start in time?"),
    "estimated_duration_s": 16.0, "voice": VOICE, "engine": "kokoro",
    "lead_silence_s": 0.8,
    "shot": {"type": "REMOTION", "source": "own",
             "remotion": {"pattern": "BrutalistHesitantWriter", "props": {
                 "text": "Which jobs can I\nget?", "triggerWords": "get",
                 "replacementWords": "start in time", "fontSize": 70, "charMs": 40,
                 "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20,
                 "seed": SLUG, "banner": ""}}},
    "qc": {"sparse_by_design": True, "sparse_reason": "Hesitant-writer opener: the correction is the motion."},
}

BODY = [
    # Q1 — what is it
    beat("B00",
         "Here's the one sentence. O P T Countdown will be a command-line tool, in a public GitHub repository. "
         "You give it your O P T dates and a list of job postings. For each posting, it says apply, "
         "network first, skip, or blocked, and it shows the evidence behind every answer.",
         "B00_WhatItIs",
         "Constructed sketch: posting pages slide into a kraft box (the tool) and land in four labelled stacks."),
    # honesty — what exists today
    beat("B01",
         "First, what exists today. For the Reallocation Engine assignment, I built a prototype of this. "
         "On October thirteenth I ran it again. Twelve of twelve tests passed. "
         "It sorted eight postings for a fictional student with fifty-three days left: "
         "one apply, two network first, three skip, and two blocked. "
         "Everything after this is what I will build.",
         "B01_ExistsToday",
         "Real output, dated: a counter climbs to 12/12 tests; four grey bars grow to 1, 2, 3, 2."),
    # Q2 — alternative 1: the manual process
    beat("B02",
         "Why would anyone care? Today a student checks each posting by hand. Look up the employer's "
         "H one B record, which is its history of sponsoring work visas. Open the posting to see if it's still live. "
         "Guess how fast they hire. Count the days. I guessed about twenty minutes a posting. "
         "That's an estimate. I haven't timed it.",
         "B02_ByHand",
         "One posting page; four step marks appear around it while a clock hand sweeps; '20 min, estimate'."),
    # Q2 — alternative 2: the engine's liveness checker
    beat("B03",
         "The engine I built on already has a liveness checker. I gave it a fake job link. "
         "It said active, because the dead link redirects to a live careers page. "
         "Greenhouse's own job API said four oh four, not found. In my tool, the API answer wins.",
         "B03_GhostPosting",
         "A page with 'checker: active'; a scan line sweeps; a server stack answers '404'; the check is struck out."),
    # Q2 — alternative 3: the raw H-1B data
    beat("B04",
         "The raw H one B data has a similar trap. HubSpot has no row at all, and DraftKings has blank fields. "
         "A naive tool reads that silence as, won't sponsor, and skips them. "
         "Mine marks them blocked, for a person to check.",
         "B04_Silence",
         "A data table; two rows stay empty; their pages slide to a 'blocked' stack instead of the bin."),
    # Q2 — what neither alternative does: the clock
    beat("B05",
         "And neither one checks the clock. O P T allows ninety days of unemployment. "
         "A strong sponsor that takes sixty days to hire is no use to someone with fifty-three days left. "
         "In the prototype run, Klaviyo and Toast were skipped for exactly that reason.",
         "B05_Clock",
         "Two bars: runway 53 days, hiring time 60 days; the second overshoots the first's end."),
    # Q3 — who opens it
    beat("B06",
         "Who opens it? A student on O P T runs one command and reads a one-page report. "
         "And a hiring manager or engineer, for the new-grad software and data analyst roles I'm aiming at, "
         "opens the read me, runs the tests, and looks at the evaluation log, all in the first minute.",
         "B06_WhoOpensIt",
         "Constructed sketch: a repository window; a cursor clicks; three rows get checks: README, tests, eval log."),
    # Q4 — what it proves
    beat("B07",
         "What would it prove about me? Verification: every number carries a label saying where it came from. "
         "Evaluation: I'll hand-label postings and measure how often each check is wrong. "
         "Source grounding: no record, no answer. It would not prove the tool gets anyone hired, "
         "and I won't claim that.",
         "B07_Proves",
         "Constructed sketch: a report page; three source tags snap onto its rows: record, your input, model guess."),
    # Q5 — in, out, first
    beat("B08",
         "What's out? Immigration advice. Rules like cap-gap and the STEM extension stay with the school's D S O. "
         "What comes first? Move the prototype into its own repository, so a stranger can clone it, "
         "run the tests, and watch them pass in a fresh copy.",
         "B08_Scope",
         "A page marked 'immigration advice' slides toward the box and is pushed back; then a fresh box gets a check."),
    # Q6 — risk
    beat("B09",
         "What could sink it? The hiring times are my own guesses, and they decide many answers. "
         "The only apply in my run cleared the bar by just point zero one seven. "
         "So the report will show which answers would flip if a guess moved fifteen days either way.",
         "B09_Risk",
         "A scale with the 0.30 bar; a dot lands at 0.317, just above it; a question mark appears beside it."),
    # Q7 — why this project
    beat("B10",
         "Why this project? It's a mix, but more learning than showing off. I already know JavaScript and Node. "
         "My evidence is CodeBuddies, my Node team project from an earlier course. "
         "What's new to me is building a labelled evaluation set and measuring a tool's own error rate. "
         "And to be honest, Claude Code did most of the typing on the prototype while I directed it. "
         "How many postings the evaluation needs, I don't know yet. I'll start with thirty, "
         "and watch how much the error rate moves.",
         "B10_WhyThis",
         "Two boxes: a taped box 'have: Node' gets a check; an open box 'learning: evals' fills with pages."),
]

OUTRO = beat("BOUT", "O P T Countdown. A final project pitch, by Saloni Mathure.",
             "BOUT_Outro", "My own outro card: the title, my name, the date of this pitch.")
OUTRO.update({"act": "outro", "kind": "outro_voice", "tail_silence_s": 1.0})

sheet = {
    "metadata": {
        "slug": SLUG, "title": TITLE, "topic": "INFO 7375 · FINAL PROJECT PITCH",
        "skill": "show-tell", "style_preset": "show-tell", "channel": "student",
        "channel_title": "Saloni Mathure", "persona": "Saloni Mathure (narrating as myself)",
        "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro", "clock": "narration",
        "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9",
        "width": 3840, "height": 2160, "caption_policy": "none",
        "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
        "bookend_exempt_reason": ("A pitch, not a lesson: no verdict card and no Your Turn. "
                                  "The outro is my own drawn card, because the stock ClaudeTitleOutro hardcodes "
                                  "the instructor's handle and this assignment forbids using it."),
        "audience": "INFO 7375 reviewers; hiring managers for new-grad SWE / data analyst roles",
        "source_doc": "PROJECT-BRIEF.md; the opt-countdown prototype (PR nikbearbrown/the-reallocation-engine#48, commit 81d0161), re-run 2026-10-13",
        "tags": ["INFO 7375", "final project", "pitch", "OPT", "H-1B", "evaluation"],
    },
    "beats": [OPEN] + BODY + [OUTRO],
}
(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
words = sum(len(b["narration_text"].split()) for b in sheet["beats"])
print(len(sheet["beats"]), "beats;", words, "words; est",
      round(sum(b["estimated_duration_s"] for b in sheet["beats"])), "s")

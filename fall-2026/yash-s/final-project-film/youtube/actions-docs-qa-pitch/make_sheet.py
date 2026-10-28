#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for actions-docs-qa-pitch (INFO 7375 final project pitch film).

SHOW-TELL style: one drawn picture per beat, minimal labels, the narration explains.
Narrated in the first person as Yash Saraf (Kokoro am_onyx voice reading Yash's script);
no instructor persona, name, or credit line, so the house greeting, the Your Turn composer,
and the @NikBearBrown outro card are replaced (see bookend_exempt_reason and FRICTIONAL.md).

Honesty rule: nothing in the project exists yet. Every body beat is a constructed sketch and
says so on screen; B04/B05 are drawn from Yash's dated screenshots (evidence/, 2026-10-11).
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
SLUG = "actions-docs-qa-pitch"
TITLE = "Actions Docs Q&A — Final Project Pitch"


def beat(bid, narration, cls, image, show):
    return {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
            "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
            "voice": "am_onyx", "engine": "kokoro",
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show, "manim": {"class": cls},
                     "motion_claim": image}}


B = [
 beat("B00", "Here's what I will build. Actions Docs Q and A will be a command-line tool that answers questions about GitHub Actions, using GitHub's own documentation.",
      "B00_Docs", "A stack of doc pages drops onto the stage; a question card slides in; an ink arc joins the question to the docs.",
      [{"at": 0.1, "event": "docs stack drops"}, {"at": 0.45, "event": "question card slides in"}, {"at": 0.8, "event": "arc joins them"}]),
 beat("B01", "It will search the docs for the passage that holds the answer. Then a small model, running free on my laptop, will write a short answer from that passage only, and quote it.",
      "B01_Search", "A scan line sweeps the docs stack and the top page lifts with its passage dot; a dark model block appears and an answer slip rises out of it.",
      [{"at": 0.15, "event": "scan sweeps"}, {"at": 0.35, "event": "page lifts"}, {"at": 0.6, "event": "model block"}, {"at": 0.8, "event": "answer slip rises"}]),
 beat("B02", "Next, a script will check the quote, word for word, against the docs. If it matches, the answer ships with its source. If it doesn't, the tool shows the passage instead. No quote, no answer.",
      "B02_QuoteCheck", "A quote strip slides onto its line on the page and a check lands; a second, reworded strip fails to fit, bounces back, and gets a cross.",
      [{"at": 0.2, "event": "strip slides onto the line"}, {"at": 0.4, "event": "check: match"}, {"at": 0.65, "event": "second strip bounces, cross"}, {"at": 0.85, "event": "page shown instead"}]),
 beat("B03", "When it's done, it will be a public GitHub repository: the tool, a script that fetches one pinned version of the docs, about fifty test questions, and a scored report.",
      "B03_Repo", "A long shelf labelled GitHub repo; the model block, a pinned docs stack, a row of test cards, and a report with grey bars drop onto it in turn.",
      [{"at": 0.15, "event": "shelf"}, {"at": 0.3, "event": "tool"}, {"at": 0.5, "event": "pinned docs"}, {"at": 0.7, "event": "test cards"}, {"at": 0.85, "event": "report"}]),
 beat("B04", "Before pitching it, I tried what already exists, on October eleventh, with three questions from my own workflows. The docs site's keyword search listed the page holding the answer for just one of the three.",
      "B04_KeywordSearch", "Three question cards arrive; a docs-search window fills with result bars for each; crosses land beside two cards and a check beside one; '1 of 3' appears. Drawn from the 2026-10-11 screenshots.",
      [{"at": 0.2, "event": "three question cards"}, {"at": 0.55, "event": "results for each, marks land"}, {"at": 0.85, "event": "1 of 3"}]),
 beat("B05", "Ask Copilot, built into that search, and the Claude desktop app both matched the docs on all three. But Copilot listed its sources for only one, and Claude cited none.",
      "B05_AIAnswers", "Two windows, Copilot and Claude; three answer slips land in each with checks; one source dot attaches to one Copilot slip, none to Claude's. Drawn from the 2026-10-11 screenshots.",
      [{"at": 0.15, "event": "two windows"}, {"at": 0.4, "event": "three slips and checks each"}, {"at": 0.75, "event": "one source dot on Copilot"}]),
 beat("B06", "So mine is not meant to give better answers. What it adds is the exact sentence each answer came from, checked in the docs, instead of a link to a whole page.",
      "B06_Sentence", "Two pages side by side: on the right one line is highlighted with a source dot and a check; on the left a frame draws around the whole page.",
      [{"at": 0.35, "event": "one sentence highlighted"}, {"at": 0.55, "event": "check"}, {"at": 0.85, "event": "frame around the whole page"}]),
 beat("B07", "It will also run free, on my own laptop. The docs search notes that GitHub keeps the questions asked there. My tool will send nothing anywhere.",
      "B07_Local", "The docs and model block drop onto a laptop; a cloud draws on the right and question cards stack into it; a line from the laptop toward the cloud draws and is cut with a cross.",
      [{"at": 0.15, "event": "parts drop onto the laptop"}, {"at": 0.5, "event": "cloud keeps question cards"}, {"at": 0.85, "event": "line cut: nothing sent"}]),
 beat("B08", "Who opens it? I'm aiming for AI developer, DevOps, or cloud engineer roles, so the reader is a hiring manager or engineer on one of those teams. In the first minute, they read the results table, then open one test question and compare the expected passage with the tool's answer. No install needed.",
      "B08_Reader", "A README page with an empty results table; a sixty-second ring draws; one test card slides out with two slips side by side and a check between them.",
      [{"at": 0.25, "event": "ring draws"}, {"at": 0.45, "event": "table rows"}, {"at": 0.65, "event": "test card slides out"}, {"at": 0.85, "event": "check between the slips"}]),
 beat("B09", "What will it prove? That I can ground answers in a source, verify them with a script, hold a model to a fixed output shape, and evaluate it honestly, on about fifty questions, ten of which the docs don't cover.",
      "B09_Proves", "Four objects pop in a row on cue: a page with a source dot, a check, a slip with fixed slots, and a tray of test cards, two of them left empty.",
      [{"at": 0.2, "event": "page with source"}, {"at": 0.35, "event": "check"}, {"at": 0.5, "event": "fixed-shape slip"}, {"at": 0.75, "event": "test tray, two empty"}]),
 beat("B10", "What's out: agent loops, a web interface, other docs, and any claim that it beats Copilot or Claude. And it never answers from the model's memory.",
      "B10_Out", "The pinned docs stack sits centre; a loop, a browser window, a second docs stack and a memory bubble each slide in and are pushed out with a cross.",
      [{"at": 0.15, "event": "loop out"}, {"at": 0.3, "event": "window out"}, {"at": 0.45, "event": "other docs out"}, {"at": 0.85, "event": "memory bubble out"}]),
 beat("B11", "The first piece is search alone, with no model: my three questions plus two more, checking whether the right passage lands in the top three. A dated results file in the repo will show it ran.",
      "B11_FirstPiece", "Five question cards line up; a scan line sweeps the docs; three empty top-three slots stay waiting; a dated results page drops onto the repo shelf.",
      [{"at": 0.2, "event": "five cards"}, {"at": 0.45, "event": "scan + empty top-3 slots"}, {"at": 0.85, "event": "results page drops"}]),
 beat("B12", "The biggest risk is search missing. The docs' keyword search missed two of my three, and mine starts the same way. If plain-English questions keep missing, I'll add a free model that matches by meaning, and compare the two.",
      "B12_Risk", "A question card sends a solid keyword lane to the docs, which lifts the wrong page and gets a cross; a second, grey 'meaning' lane draws below, still planned.",
      [{"at": 0.2, "event": "keyword lane"}, {"at": 0.4, "event": "wrong page, cross"}, {"at": 0.75, "event": "planned meaning lane"}]),
 beat("B13", "Why this project? It's a mix. I already build C I pipelines: GitHub Actions runs in my three public repos from twenty twenty-five. Building search, running a local model, and measuring answers are new to me. It interests me, and that's why I want to explore it further.",
      "B13_Why", "Three solid repo boxes slide in under 'have' with a check; three outline-only objects draw under 'new'; a terracotta spark lands on each new one.",
      [{"at": 0.25, "event": "three repo boxes, check"}, {"at": 0.6, "event": "three outlines"}, {"at": 0.85, "event": "sparks"}]),
 beat("B14", "So here's what exists today: my three earlier repos, six dated screenshots, and the brief. Everything else in this film is a plan.",
      "B14_Exists", "Left: three repo boxes, six small screenshot frames and the brief page pop in under 'exists'; right: outline-only tool parts draw under 'will exist'.",
      [{"at": 0.25, "event": "repos"}, {"at": 0.45, "event": "six screenshots"}, {"at": 0.6, "event": "brief"}, {"at": 0.8, "event": "outlines: will exist"}]),
]

SPARSE_REASON = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, with the voice "
                 "carrying the explanation. The negative space is the style, so only underfill and clustered are waived; "
                 "edge-bleed, empty-frame and contrast still apply.")
for b in B:
    b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate,
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


OPEN = [
 remotion("BIDEA", "the question",
    "Hi, I'm Yash Saraf. This film pitches my final project, and nothing in it is built yet. I first asked whether AI can answer my GitHub Actions questions. The better question is whether it can show where its answers come from.",
    "BrutalistHesitantWriter",
    {"text": "Can AI answer my Actions questions", "triggerWords": "answer my Actions questions",
     "replacementWords": "show where its answers come from",
     "fontSize": 104, "charMs": 30, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20,
     "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types the naive question"}, {"at": 0.65, "event": "replaces it with: show where its answers come from"}],
    lead_silence_s=0.8,
    motion_claim="The writer types 'Can AI answer my Actions questions' and corrects it to 'Can AI show where its answers come from'.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
]

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "manim", "proof_gate": "SHOW",
         "narration_text": "Actions Docs Q and A. A final project pitch, by Yash Saraf.",
         "estimated_duration_s": 4.5, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "GRAPHIC", "source": "own", "manim": {"class": "BOUT_Outro"},
                  # what the own outro shows, recorded where bookend_check.py reads it (no pattern: still a Manim beat)
                  "remotion": {"props": {"title": TITLE, "handle": "Yash Saraf", "subline": ""}},
                  "visual_intent": "The docs stack from B00 settles small above the title; the title and 'Yash Saraf' sit under it; one terracotta dot lands.",
                  "show": [{"at": 0.1, "event": "docs stack"}, {"at": 0.2, "event": "title + name"}, {"at": 0.7, "event": "dot"}],
                  "motion_claim": "Own outro: title and the student's name; no instructor handle or mascot."},
         "tail_silence_s": 1.0,
         "qc": {"sparse_by_design": True, "sparse_reason": "Outro card: title and name only."}}

B = OPEN + B + [OUTRO]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "FINAL PROJECT PITCH", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "yash-saraf", "channel_title": "Yash Saraf",
    "persona": "Yash Saraf, first person (synthetic Kokoro am_onyx voice reading Yash's own script)",
    "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Plain", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("INFO 7375 assignment rules: narrate as yourself and never use the instructor's name, persona or "
                              "credit line. So: no 'Liam, in for Bear' greeting, no Claude.ai Your Turn composer (a constructed "
                              "Claude screen with nothing real to show), no verdict card, and an own outro instead of "
                              "ClaudeTitleOutro, whose handle is hard-coded to @NikBearBrown. bookend_check.py will report the "
                              "outro as missing; that is deliberate and recorded in FRICTIONAL.md."),
    "audience": "INFO 7375 instructor and TAs; hiring managers for AI developer / DevOps / cloud roles",
    "source_doc": "PROJECT-BRIEF.md (2026-10-11); evidence/ screenshots (2026-10-11); docs.github.com pages checked 2026-10-11",
    "playlist": "INFO 7375 Final Project", "chapter_number": 0,
    "tags": ["GitHub Actions", "document Q&A", "source grounding", "evaluation", "local model", "INFO 7375"]},
    "beats": B}
(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(B), "beats; est", round(sum(b["estimated_duration_s"] for b in B)), "s;",
      sum(len(b["narration_text"].split()) for b in B), "words")

#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for "Marino Desk Assistant: A Pitch" (INFO 7375 final project pitch film).

Brutalist show-tell format: one drawn isometric Manim picture per beat, a few words of label at
most, and the narration carries the idea. The script was drafted by Claude from my (Shubham
Bagwe's) decisions and approved by me; it is spoken by a local synthetic Kokoro voice
(am_michael), disclosed aloud and on screen in B01. My surname is respelled "Baag-way" in the
spoken text only, because Kokoro's phonemizer reads "Bagwe" as "bag-wee".

Departures from the show-tell defaults, made on purpose (FRICTIONAL.md):
  - No "Liam, in for Bear" greeting, no Professor Bear portraits, no @NikBearBrown outro: the
    assignment says to narrate as yourself and not use the instructor's name, persona or credit
    line. The stock ClaudeTitleOutro hard-codes @NikBearBrown, so BOUT is my own drawn Manim beat;
    its title/handle/subline sit in shot.remotion.props so bookend_check.py can read them.
  - No hesitant-writer, terms card or Your Turn composer (bookend_exempt): a pitch has no
    viewer exercise.
  - No metadata.channel_title: compile.py stamps it below title-safe on the first beat and
    Gate V blocks the film for it.

Re-running this script keeps measured audio (audio_file, actual_duration_s) for any beat whose
narration did not change.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "marino-desk-assistant-pitch"
TITLE = "Marino Desk Assistant: A Pitch"
HANDLE = "github.com/bagwe-shubham1727/marino-rag"
VOICE = "am_michael"

SPARSE = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, "
          "the voice carries the explanation. Only underfill and clustered are waived; edge-bleed, "
          "empty-frame and contrast still apply.")


def beat(bid, q, narration, cls, image, status):
    """status: 'exists' (shows real, re-run output), 'planned' (constructed picture of future work),
    or 'framing' (an illustration of an idea, no artifact claimed)."""
    return {"beat_id": bid, "act": "pitch", "lane": "manim", "proof_gate": "SHOW",
            "assignment_question": q, "claim_status": status,
            "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.6, 1),
            "voice": VOICE, "engine": "kokoro",
            "qc": {"sparse_by_design": True, "sparse_reason": SPARSE},
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image,
                     "manim": {"class": cls}, "motion_claim": image}}


B = [
 beat("B01", "Q1 what is it",
      "I'm Shubham Baag-way, and this is my final project pitch, written with Claude and spoken by a synthetic voice. Marino Desk Assistant will answer front-desk questions at Northeastern's Marino Recreation Center, like fees, hours and guest rules, from the public recreation website, and quote the page it used.",
      "B01_Desk", "A desk bell lands on a kraft counter; a chat window slides in beside it and one answer line draws with a "
      "terracotta link dot. Label 'Desk Assistant'. Corner tag 'synthetic voice · script written with Claude'.", "framing"),
 beat("B02", "Q1 the artifact",
      "When it's done, it will be a public GitHub repository: a Python and FastAPI backend, a Next.js chat window, "
      "Claude writing the answers, and an evaluation report. A first version already exists, and its sixty tests passed today.",
      "B02_Repo", "An open kraft box labelled 'GitHub repo'; four parts drop in (dark server block, chat window card, report page, a small kraft log). Beside it a dark server stack labelled 'first version' whose lights turn on, with '60 tests pass'. Corner tag 'planned repo · real: 60 tests pass'.", "planned"),
 beat("B03", "Q2 the desk problem",
      "Here's the problem. A member at the desk asks what an alumni membership costs. The answer is on the website, "
      "inside a page of about eight hundred words of fee tables, while the member waits.",
      "B03_Scroll", "The bell rings (two arcs); a tall page of scribbled lines slides up past a window frame, as if scrolled. "
      "Label '~800 words'. Corner tag 'illustration'.", "framing"),
 beat("B04", "Q2 the alternatives",
      "I looked at what we use now. The site's own search returns pages, not answers. A search for guest pass today "
      "returned five pages, with the home page first. Manual lookup means scrolling until you find the line.",
      "B04_Search", "A search pill with a magnifier; five result cards drop into a column; the first is labelled 'Home'. "
      "Labels 'guest pass', '5 pages'. Corner tag 'real search · 2026-10-13'.", "exists"),
 beat("B05", "Q2 the difference",
      "Mine will save the desk assistant that scroll. It will give one answer, quote the exact line, and link to it, which the site search doesn't do. And when the website doesn't say, it will answer: I don't know.",
      "B05_Answer", "One answer bubble draws with a bracketed quote line and a link pill; a second, plain bubble appears below. "
      "Labels 'quote + link', 'I don't know'. Corner tag 'constructed · planned answer'.", "planned"),
 beat("B06", "Q3 who opens it",
      "My target role is new-grad full-stack engineer, so my reader is a hiring manager or an engineer. In sixty "
      "seconds, they'll see the evaluation table in the read-me, run one command, ask a fee question, and watch it "
      "refuse an off-topic one.",
      "B06_Reader", "A browser window with a dark title bar; a table of rows grows in it; a cursor clicks; a small chat card "
      "slides out. Labels 'hiring manager', '60 s'. Corner tag 'constructed · planned repo'.", "planned"),
 beat("B07", "Q4 what it proves: grounding + contract",
      "What will it prove? Source grounding: it already retrieves five passages and reranks them to three. Next, a "
      "prompt contract: Claude must return the answer, the quoted line, the link and the date, and a quote that isn't "
      "in the page fails.",
      "B07_Contract", "Five page cards in a row; two slide away, leaving three. Then a contract slip with four slots fills in, "
      "and one slot gets a cross. Labels '5 → 3', 'contract'. Corner tag 'exists: 5 → 3 · planned: contract'.", "exists"),
 beat("B08", "Q4 evaluation evidence (will)",
      "And evaluation: fifty real desk questions with my own answer keys, scored three ways. Did it cite the right page? "
      "Was the answer right? Did it refuse when it should? Every miss goes in the report.",
      "B08_Eval", "A grid of fifty small pages draws in; three grey score bars grow beside it; a few pages get a terracotta dot "
      "and fly into a report book. Labels '50 questions', '3 scores'. Corner tag 'constructed · planned'.", "planned"),
 beat("B09", "Q4 what a reviewer can conclude",
      "A reviewer could fairly conclude that I can specify, ground and evaluate an AI app, and measure where it's wrong. Not that it's always accurate, and not that Marino uses it officially.",
      "B09_Fair", "Left: a window with a ruler of bars and an ink check, labelled 'fair'. Right: a dashed badge struck through, "
      "labelled 'not claimed'. Corner tag 'illustration'.", "framing"),
 beat("B10", "Q5 in and out",
      "What's in: the public recreation pages, with fees, hours and policies. Deliberately out: internal staff documents. "
      "They aren't public, so the finished repo never indexes them. It also won't check live court availability.",
      "B10_Scope", "Inside a fence line: a stack of web pages labelled 'public site'. Outside: a dark locked box labelled "
      "'staff docs' that slides further away. Corner tag 'illustration'.", "framing"),
 beat("B11", "Q5 what comes first",
      "The first piece I'll make run is a public-only index and a retrieval check: fifty questions, each with its source "
      "page, and a script that counts how many find the right page in the top three. You'll know it ran when that "
      "report is in the repo, with the crawl date.",
      "B11_First", "Web pages stream into a box (the index); a report page rises beside it with rows and a stamped date. "
      "Labels 'top 3', 'report.md'. Corner tag 'constructed · planned'.", "planned"),
 beat("B12", "Q6 the risk",
      "What could sink it? Prices that depend on the date. Today, the alumni page lists five yearly prices for the same "
      "membership, from four hundred eighty dollars in September down to one hundred twenty in June. A model that "
      "doesn't know today's date can quote the wrong one, confidently.",
      "B12_Prices", "Five grey bars step down along a month line (Sep to Jun); a terracotta marker slides along and stops on the wrong bar. Labels '$480', '$120', 'Sep → Jun'. Corner tag 'real prices · wrong pick illustrated'.", "exists"),
 beat("B13", "Q6 mitigation + limitation",
      "So the contract will pass in today's date and require the quoted row, the evaluation will include date questions, "
      "and every answer will show its crawl date. The limit I can't fix: it's only as current as the last crawl.",
      "B13_Dates", "A calendar page drops into the contract slip from B07; a date stamp lands on an answer card. Labels "
      "'today's date', 'crawl date'. Corner tag 'constructed · planned'.", "planned"),
 beat("B14", "Q7 why this project",
      "Why this project? I work the Marino front desk, and these are the questions I get. It's a mix. Backend and cloud I already have: I wrote the EventFlow Engine myself, a Node pipeline on Google Cloud. The Marino repo's current code was mostly AI-generated under my direction, so it isn't my proof. New to me: answer keys, measuring a model's misses, and prompt contracts.",
      "B14_Why", "Two shelves. Left: one solid crate labelled 'EventFlow' with a terracotta dot. Right: a dashed crate labelled 'evaluation' draws itself and a terracotta dot lights. Corner tag 'evidence: robust-data-processor (EventFlow)'.",
      "framing"),
 beat("B15", "summary: exists vs will exist",
      "Exists today: the first version, its retrieval and chat code, sixty passing tests, and the checks in this film, "
      "all run on October thirteenth. Will exist: the public-only index, Claude under the contract, and the "
      "fifty-question evaluation with its report.",
      "B15_Ledger", "Two columns. Left 'exists today': three solid crates with checks and the real line '60 passed'. Right "
      "'will exist': three dashed crates draw in. Corner tag 'summary · tests re-run 2026-10-13'.", "exists"),
]

BOUT = {"beat_id": "BOUT", "act": "outro", "lane": "manim", "proof_gate": "SHOW", "assignment_question": "outro",
        "claim_status": "framing",
        "narration_text": "Marino Desk Assistant: a pitch by Shubham Baag-way.",
        "estimated_duration_s": 3.5, "voice": VOICE, "kind": "outro_voice", "tail_silence_s": 1.0, "engine": "kokoro",
        "qc": {"sparse_by_design": True, "sparse_reason": SPARSE},
        "shot": {"type": "GRAPHIC", "source": "own",
                 "visual_intent": "The desk bell from B01 returns small; the title and the repo link settle beneath it.",
                 "manim": {"class": "BOUT_Close"},
                 # bookend_check.py reads these; they describe exactly what BOUT_Close draws.
                 "remotion": {"props": {"title": TITLE, "handle": HANDLE, "subline": ""}}}}

beats = B + [BOUT]

old = {}
p = HERE / "beat_sheet.json"
if p.exists():
    for ob in json.loads(p.read_text()).get("beats", []):
        old[ob["beat_id"]] = ob
for b in beats:
    ob = old.get(b["beat_id"])
    if ob and ob.get("narration_text") == b["narration_text"]:
        for k in ("audio_file", "actual_duration_s", "word_times"):
            if k in ob:
                b[k] = ob[k]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "INFO 7375 · FINAL PROJECT PITCH", "skill": "show-tell", "style_preset": "show-tell",
    "author": "Shubham Bagwe", "persona": "Shubham Bagwe (script written with Claude, synthetic voice)", "handle": HANDLE,
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro", "clock": "narration", "palette": "claude",
    "register": "plain", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160, "caption_policy": "none",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("Course pitch, not a channel explainer. The assignment says to narrate as myself and not use the "
                              "instructor's name, persona or credit line, so there is no Liam greeting, no hesitant-writer/terms "
                              "cards, no Your Turn composer (a pitch has no viewer exercise), and no verdict card; B15 states "
                              "exists vs will-exist instead. The outro is kept, as my own drawn beat."),
    "audience": "a hiring manager or engineer reviewing a new-grad full-stack portfolio; the INFO 7375 graders",
    "source_doc": "my marino-rag repo (github.com/bagwe-shubham1727/marino-rag, commit dd3205e), tests re-run 2026-10-13; "
                  "recreation.northeastern.edu site search and Alumni page, checked 2026-10-13 (evidence/)",
    "playlist": "INFO 7375 Fall 2026", "chapter_number": 0,
    "tags": ["INFO 7375", "final project pitch", "RAG", "source grounding", "evaluation", "Shubham Bagwe"]},
    "beats": beats}
p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
words = sum(len(b["narration_text"].split()) for b in beats)
print(len(beats), "beats;", words, "words; est", round(sum(b["estimated_duration_s"] for b in beats)), "s")

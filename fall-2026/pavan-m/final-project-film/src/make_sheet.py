#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for cite-the-line-pitch.

INFO7375 final-project pitch film by Pavan Jayant Majji, built with the Brutalist
show-tell skill: one drawn isometric illustration per body beat, minimal labels,
narration carries the explanation.

Adapted from skills/make/show-tell/reference/example-make_sheet.py. Changes from the
template, per the assignment ("narrate as yourself; no instructor name, persona, or
credit line"):
  - narration is first person as Pavan, read by the free Kokoro am_onyx voice;
  - no "in for Bear" greeting, no @NikBearBrown handle, folder label, or spoken credit;
  - metadata.channel_title is set, so bookend_check.py expects Pavan's handle on the outro;
  - Your Turn (bhtf) and the verdict card (bvdt) are exempt; no "why now" number beat,
    because there is no real metric to show.

Honesty: nothing in the project is built yet. Every body drawing carries a small
"constructed sketch" tag, and the results table shows "?" instead of numbers.

Sources: PROJECT-BRIEF.md (2026-10-10); Datadog Bits AI SRE documentation (read 2026-10-09).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "cite-the-line-pitch"
TITLE = "Cite-the-Line"
HANDLE = "Pavan Majji"
VOICE = "am_onyx"
TAG = "a small 'constructed sketch' tag in the lower-right corner"


def beat(bid, narration, cls, image, show):
    return {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
            "narration_text": narration,
            "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
            "voice": VOICE, "engine": "kokoro",
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                     "manim": {"class": cls}, "motion_claim": image}}


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate,
         "narration_text": narration,
         "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show,
                  "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


# ── Body: one drawing per beat, same cast throughout ─────────────────────────
# Cast: a log page, the tool (a box with a lens), a server stack, the checker
# (scan line + check), the result slip, and the results card.
B = [
 # Q1 — what is it
 beat("B00",
      "This is my final project, Cite the Line. Nothing in it is built yet. This film is the plan.",
      "B00_LogPage",
      f"A page of log lines drops onto the stage and settles with a floor shadow; the label 'log' beside it; {TAG}.",
      [{"at": 0.1, "event": "log page drops in"}, {"at": 0.4, "event": "label + tag"}]),
 beat("B01",
      "It will be a command-line tool. You give it the logs from a failing backend service, and it names the likely cause, pointing at the exact lines that support it.",
      "B01_LensCites",
      f"A lens slides over the log page; two lines highlight with terracotta dots; a slip labelled 'cause' lands beside the page, a leader line pointing at the two lines; {TAG}.",
      [{"at": 0.15, "event": "lens slides over page"}, {"at": 0.4, "event": "two lines highlight"}, {"at": 0.75, "event": "cause slip lands"}]),
 beat("B02",
      "And when the logs don't show enough, it will say so, instead of guessing.",
      "B02_NotEnough",
      f"The lens sweeps a sparse log page and finds nothing; a slip labelled 'not enough' lands instead of a cause; {TAG}.",
      [{"at": 0.15, "event": "lens sweeps"}, {"at": 0.65, "event": "'not enough' slip lands"}]),
 beat("B03",
      "To test it, I'll build a small service with FastAPI and Postgres in Docker, and break it on purpose: a slowed database, a bad config, a failing dependency. Each break gives real logs with a known cause.",
      "B03_BreakService",
      f"A server stack labelled 'service'; three of its lights turn red one by one, and under each a log page drops out with a small known-cause tag; {TAG}.",
      [{"at": 0.15, "event": "server stack"}, {"at": 0.4, "event": "light 1 red, page drops"},
       {"at": 0.6, "event": "light 2"}, {"at": 0.8, "event": "light 3"}]),
 # Q4 — how it works / what it proves (contract)
 beat("B04",
      "Claude Code, run from a script, will read each incident and answer in a fixed format: one cause from a short list, plus the line numbers it relied on. That format is the prompt contract.",
      "B04_Contract",
      f"Log pages slide into an open box labelled 'Claude Code'; a slip comes out with a cause pill and line-number marks, labelled 'contract'; {TAG}.",
      [{"at": 0.2, "event": "pages feed in"}, {"at": 0.55, "event": "slip comes out"}, {"at": 0.8, "event": "'contract' label"}]),
 beat("B05",
      "Then a plain checker, with no AI in it, will test every answer. Do the cited lines exist? Is the cause the known one? Each incident will run three times, to see if the answer holds.",
      "B05_Checker",
      f"The slip passes under a scan line labelled 'checker'; a check appears; the pass repeats so three slips sit in a row, each with its own mark; {TAG}.",
      [{"at": 0.15, "event": "scan line"}, {"at": 0.45, "event": "first check"}, {"at": 0.8, "event": "three slips in a row"}]),
 # Q2 — alternative and difference
 beat("B06",
      "Tools like this already exist. I read the documentation for Datadog's Bits AI SRE, which proposes root causes inside Datadog's paid platform. Its accuracy is reported by Datadog, and I can't re-check it myself.",
      "B06_ClosedBox",
      f"A closed, dark-plinthed box labelled 'vendor platform'; a log page goes in, a slip comes out, but the box never opens; {TAG}. No logos.",
      [{"at": 0.15, "event": "closed box"}, {"at": 0.5, "event": "page in, slip out"}, {"at": 0.8, "event": "box stays shut"}]),
 beat("B07",
      "Mine will be small and open: plain log files, incidents with known answers, and a public record of where it was wrong. It's not a competitor. It's a test bench anyone can re-check.",
      "B07_OpenCrate",
      f"An open crate labelled 'test bench'; its pages are visible inside; one slip with a check and one with a cross sit beside it, both in plain view; {TAG}.",
      [{"at": 0.15, "event": "open crate"}, {"at": 0.45, "event": "pages visible"}, {"at": 0.75, "event": "check and cross both shown"}]),
 # Q3 — who opens it, first 60 seconds
 beat("B08",
      "The reader is a hiring manager for backend roles. In the first minute, they'll open the README and see a results table. Those numbers don't exist yet. They'll come from real runs.",
      "B08_Readme",
      f"A README card drops in; a three-row results table draws on it with '?' in every value cell (no numbers); label 'README'; {TAG}.",
      [{"at": 0.15, "event": "README card"}, {"at": 0.4, "event": "table draws"}, {"at": 0.7, "event": "'?' cells"}]),
 beat("B09",
      "Then they click one incident and see the log, the diagnosis, and the checker's verdict, side by side, with no setup needed.",
      "B09_ThreePanels",
      f"A cursor clicks one table row; three panels slide out in a row: the log page, the result slip, and a check; {TAG}.",
      [{"at": 0.15, "event": "click"}, {"at": 0.4, "event": "three panels in a row"}]),
 # Q4 — what it proves, with its boundary
 beat("B10",
      "If it works, a reviewer could fairly conclude that I test model output instead of trusting it. They shouldn't conclude it works on real production logs. It will only be tested on incidents I made.",
      "B10_TestNotTrust",
      f"A balance with two pans labelled 'test' and 'trust'; the result slip drops onto 'test' and that pan sinks; then a fence draws around the small incident pile; {TAG}.",
      [{"at": 0.15, "event": "balance"}, {"at": 0.4, "event": "slip tips to 'test'"}, {"at": 0.75, "event": "fence around own incidents"}]),
 # Q5 — in / out / first
 beat("B11",
      "One thing it will never do is act. No restarts, no rollbacks. It only diagnoses and cites.",
      "B11_NeverActs",
      f"A big 'restart' button appears beside the server stack and is crossed out in ink; the result slip stays beside the log page; {TAG}.",
      [{"at": 0.15, "event": "restart button"}, {"at": 0.45, "event": "crossed out"}]),
 beat("B12",
      "The first piece I'll make run is a single slowed-database incident, end to end. Its log, diagnosis and verdict will be committed with a date, so anyone can see it ran.",
      "B12_FirstRun",
      f"One database cylinder with a slow clock; a single log page, slip and check line up beside it; a date stamp lands on the row, labelled 'first run'; {TAG}.",
      [{"at": 0.15, "event": "slowed database"}, {"at": 0.45, "event": "page, slip, check line up"}, {"at": 0.75, "event": "date stamp"}]),
 # Q6 — risk
 beat("B13",
      "The biggest risk is that I write every incident, so the test could be too easy. If the logs announce the answer, a high score means nothing.",
      "B13_TooEasy",
      f"A tall, loud stack of error pages labelled 'API errors' sits on top of a small, quiet database cylinder labelled 'real cause'; {TAG}.",
      [{"at": 0.15, "event": "loud error stack"}, {"at": 0.55, "event": "quiet cause underneath"}]),
 beat("B14",
      "So I'll add cases where the loudest error is not the real cause, and cases with no clear answer. If scores still look too good, I'll try a simple keyword script, and say so if it does as well.",
      "B14_HardCases",
      f"Hard-case pages slide into the test bench crate; off to the side, a small grey box labelled 'plan B' appears, outlined dashed; {TAG}.",
      [{"at": 0.2, "event": "hard cases slide in"}, {"at": 0.7, "event": "plan B box"}]),
 # Q7 — why this project / skills
 beat("B15",
      "I already work with FastAPI, Postgres and Docker, from my engineering experience and my coursework. What's new for me is fault injection, prompt contracts, and evaluating model output against known answers.",
      "B15_TwoPiles",
      f"Two piles of blocks: a solid pile labelled 'have' and an outlined pile labelled 'learning'; the outlined blocks draw in one by one; {TAG}.",
      [{"at": 0.15, "event": "solid pile"}, {"at": 0.55, "event": "outlined pile draws in"}]),
 # Close — exists vs will exist
 beat("B16",
      "Today, what exists is this plan and my notes. Everything else in this film is what I will build.",
      "B16_ExistsVsWill",
      f"A tiny solid pile labelled 'exists' beside a large ghost-outlined pile labelled 'will exist'; {TAG}.",
      [{"at": 0.15, "event": "tiny 'exists' pile"}, {"at": 0.5, "event": "large ghost pile"}]),
]

# ── Bookends ─────────────────────────────────────────────────────────────────
OPEN = [
 remotion("BIDEA", "the question",
    "Hi, I'm Pavan Majji, a backend software engineer. When an error shows up, the habit is to paste it into a chatbot and ask how to fix it. The better question is which log lines prove the cause.",
    "BrutalistHesitantWriter",
    {"text": "What caused this error,\nand how do I fix it?",
     "triggerWords": "how do I fix it", "replacementWords": "which log lines prove it",
     "fontSize": 70, "charMs": 22, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2,
     "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'What caused this error,'"},
     {"at": 0.6, "event": "backspaces 'how do I fix it' → 'which log lines prove it' on the spoken correction"}],
    lead_silence_s=0.8,
    motion_claim="The writer types the naive fix-it question and corrects it to the real one: which log lines prove the cause.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Three terms. Root cause: the failure that started the problem. Source grounding: every claim points to the exact text it came from. A prompt contract: a fixed answer format a program can check.",
    "ClaudeDefinitions",
    {"title": "Terms In This Film",
     "terms": [{"term": "root cause", "meaning": "the failure that started the problem"},
               {"term": "source grounding", "meaning": "every claim points to the exact text it came from"},
               {"term": "prompt contract", "meaning": "a fixed answer format a program can check"}],
     "folderLabel": HANDLE},
    [{"at": 0.12, "event": "'root cause' lands"}, {"at": 0.45, "event": "'source grounding' lands"},
     {"at": 0.75, "event": "'prompt contract' lands"}],
    gate="CARD",
    qc={"sparse_by_design": True, "sparse_reason": "TERMS card: three prerequisites, one line each."}),
]

SPARSE_REASON = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, "
                 "with the voice carrying the explanation. The negative space is the style, so only underfill "
                 "and clustered are waived; edge-bleed, empty-frame and contrast still apply.")
for b in B:
    b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}

B = OPEN + B
B.append({"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
          "narration_text": "Cite the Line. I'm Pavan Majji.",
          "estimated_duration_s": 4.0, "voice": VOICE, "engine": "kokoro",
          "shot": {"type": "REMOTION", "source": "own",
                   "show": [{"at": 0.0, "event": "title restates; handle"}],
                   "remotion": {"pattern": "ClaudeTitleOutro",
                                "props": {"title": TITLE, "slug": SLUG, "handle": HANDLE, "subline": "",
                                          "hideMascot": True}}},
          "kind": "outro_voice", "tail_silence_s": 1.0})

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "INFO7375 · FINAL PROJECT PITCH",
    "skill": "show-tell", "style_preset": "show-tell",
    "channel": "pavan-majji", "channel_title": HANDLE,
    "persona": "Pavan Majji (first person; synthetic Kokoro am_onyx voice reading his script)",
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown",
    "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "English (Hi)",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("show-tell opens on the hesitant writer + terms card, so no composer cold open; "
                              "no verdict card. Your Turn dropped: this is a project pitch, not a tutorial, and "
                              "every body beat answers one of the assignment's seven questions. Outro kept, with "
                              "the author's own handle (assignment: no instructor name, persona, or credit line)."),
    "audience": "hiring managers and senior engineers for backend software engineering roles",
    "source_doc": "PROJECT-BRIEF.md (2026-10-10); Datadog Bits AI SRE documentation (read 2026-10-09)",
    "playlist": "INFO7375 Final Project", "chapter_number": 0,
    "tags": ["INFO7375", "final project pitch", "log triage", "root cause analysis",
             "source grounding", "LLM evaluation", "Claude Code", "FastAPI", "Postgres"]},
    "beats": B}

# Carry measured audio forward from an existing sheet, so re-running this script never
# wipes durations (show-tell: "make_sheet.py must carry audio_file forward, as well as
# actual_duration_s"). A beat whose narration changed keeps nothing: it must be re-voiced.
prev_path = HERE / "beat_sheet.json"
if prev_path.exists():
    prev = {b["beat_id"]: b for b in json.loads(prev_path.read_text()).get("beats", [])}
    for b in sheet["beats"]:
        old = prev.get(b["beat_id"])
        if old and old.get("narration_text") == b["narration_text"]:
            for k in ("actual_duration_s", "audio_file"):
                if k in old:
                    b[k] = old[k]
        elif old and "actual_duration_s" in old:
            print(f"{b['beat_id']}: narration changed; re-voice with --only {b['beat_id']}")

(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(B), "beats; est", round(sum(b["estimated_duration_s"] for b in B)), "s")

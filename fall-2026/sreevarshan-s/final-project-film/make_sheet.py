#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for show-tell-reallocation-recipe-pitch.

SHOW-TELL pitch film for my INFO 7375 final project. Every body beat is one drawn
isometric illustration (Manim, Claude palette) with at most a few words of label;
my first-person narration carries the explanation. Kokoro am_michael throughout.

Departures from skills/make/show-tell/SKILL.md (all deliberate):
- Narrator is me, Sreevarshan Sathiyamurthy, in first person; no house persona.
- No Your Turn composer beat (bookend_exempt: bhtf).
- BOUT is my own sign-off on a ShowTellCard (masked), not ClaudeTitleOutro, because
  ClaudeTitleOutro hardcodes the house handle. bookend_check.py's outro assertions
  (handle == metadata.channel_title, title == metadata.title, empty subline) are met
  through the props below.
- No person icons: the fictional persona appears only as a file, labelled CONSTRUCTED.

Sources: PROJECT-BRIEF.md (../../PROJECT-BRIEF.md) and the-reallocation-engine repo,
branch contrib/2026fa-Sreevarshann-newgrad-de-ml-optwindow at ded8454. Claims per
sentence are in CLAIMS.md.
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
SLUG = "show-tell-reallocation-recipe-pitch"
TITLE = "Record Beats AI: A Sponsorship Job Finder That Checks Its Own Answers"
VOICE = "am_michael"
NAME = "Sreevarshan Sathiyamurthy"
# Pronunciation aid for Kokoro only (narration text). Whisper hears it as "Srivarshan Sathiyamurthy".
# On-screen labels, the byline and all metadata keep the real spelling (NAME).
SAY_NAME = "Shreevarshun Saa-thee-ya-moorthy"

def beat(bid, section, narration, cls, image, show, labels):
    return {"beat_id": bid, "act": "show-tell", "section": section, "lane": "manim", "proof_gate": "SHOW",
            "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
            "voice": VOICE, "engine": "kokoro",
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                     "labels": labels, "manim": {"class": cls}, "motion_claim": image}}

def remotion(bid, act, narration, pattern, props, show, gate="SHOW", lane="bookend", **extra):
    b = {"beat_id": bid, "act": act, "lane": lane, "proof_gate": gate,
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b

OPEN = [
 remotion("BIDEA", "the question",
    f"Hello. I'm {SAY_NAME}. New graduates on O P T ask which companies are hiring. "
    "Better to ask which have actually sponsored people at my level.",
    "BrutalistHesitantWriter",
    {"text": "Which companies are hiring\nnew grads on OPT", "triggerWords": "are hiring",
     "replacementWords": "have actually sponsored",
     "fontSize": 70, "charMs": 22, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20,
     "seed": SLUG, "banner": "",
     # small on-screen disclosure, bottom right (ink, serif, case preserved)
     "brandLabel": "Narrated with a synthetic voice (Kokoro am_michael)"},
    [{"at": 0.0, "event": "types 'Which companies are hiring new grads on OPT'"},
     {"at": 0.6, "event": "backspaces 'are hiring' → 'have actually sponsored' on the spoken correction"}],
    lead_silence_s=0.8,
    motion_claim="The writer types the naive hiring question and corrects it to the real one: who has actually sponsored.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "A record: a value from a real file or tool output. "
    "A model judgment: a value an AI produced, not yet checked. "
    "A gate: a rule that stops the run when evidence is missing.",
    "ClaudeDefinitions",
    {"title": "Terms In This Film",
     "terms": [{"term": "record", "meaning": "a value from a real data file or tool output"},
               {"term": "model-judgment", "meaning": "a value an AI produced; it still needs checking"},
               {"term": "gate", "meaning": "a rule that stops the run when evidence is missing"}],
     "folderLabel": "INFO 7375"},
    [{"at": 0.12, "event": "'record' lands"}, {"at": 0.45, "event": "'model-judgment' lands"},
     {"at": 0.78, "event": "'gate' lands"}], gate="CARD",
    qc={"sparse_by_design": True, "sparse_reason": "TERMS card: three prerequisites, one line each."}),
]

B = [
 # ── §1 What is it?
 beat("B00", "1 what is it",
      "This is my project: a command line pipeline that shows an international new graduate which companies have "
      "sponsored people at their level. When it's done, it will refuse to call a job open unless a record backs it. "
      "I built the prototype for my INFO seventy-three seventy-five Assignment 2, in early October 2026.",
      "B00_Pipeline",
      "A kraft record binder drops onto the stage beside a short conveyor; a posting page rides toward a gate and "
      "stops until the binder's lamp lights. A small tag clips on: 'INFO 7375 · Assignment 2'.",
      [{"at": 0.1, "event": "binder drops in"}, {"at": 0.4, "event": "page stops at the gate"},
       {"at": 0.75, "event": "course tag clips on"}],
      ["pipeline", "record", "INFO 7375 · Assignment 2"]),
 # ── §2 Why would anyone care?
 beat("B02", "2 why care",
      "It will save new graduates the manual cross-checking of sponsorship history against live postings. "
      "Sponsor sites like Ellis and F1Jobs count past visa filings; mine will also check that a posting is live, "
      "and match occupation and level.",
      "B02_CrossCheck",
      "Left: a tall stack of filing pages with a counter (past filings). Right: one posting page. A dashed cable "
      "draws between them; a liveness lamp and an occupation tag appear on the cable as 'will' parts.",
      [{"at": 0.2, "event": "filing stack + posting"}, {"at": 0.55, "event": "dashed cable draws"},
       {"at": 0.8, "event": "lamp + occupation tag"}],
      ["past filings", "Ellis", "F1Jobs", "live posting", "occupation + level"]),
 # ── §3 First 60 seconds
 beat("B03", "3 first 60 seconds",
      "In the first minute, a hiring manager for an M L or AI engineer role will open the read me, run one command "
      "on a made-up persona, Meera Krishnan, and open the report.",
      "B03_FirstMinute",
      "A persona file card slides in, stamped CONSTRUCTED; a terminal block shows one command line typing; "
      "a report page drops out of the terminal.",
      [{"at": 0.15, "event": "README page"}, {"at": 0.4, "event": "persona file, CONSTRUCTED stamp"},
       {"at": 0.6, "event": "command types"}, {"at": 0.85, "event": "report page drops out"}],
      ["README", "meera-krishnan", "CONSTRUCTED", "run.py"]),
]
B.append(beat("B04", "3 first 60 seconds",
    "The report opens with its warnings. Then the funnel from my worked run: thirty thousand three hundred "
    "sixty-nine companies, a hundred fourteen matching my role keywords, sixty-four entry-eligible, and fifty senior-only.",
    "B04_Funnel",
    "The report page sits left with a terracotta warning dot on its first line; then three grey funnel bars grow, narrowing: 30,369, then 114, then a split bar 64 · 50 (entry-eligible · senior-only). Widths show order, not scale.",
    [{"at": 0.1, "event": "warning dot"}, {"at": 0.25, "event": "30,369 bar"}, {"at": 0.55, "event": "114 bar"},
     {"at": 0.75, "event": "64 · 50 split bar"}],
    ["30,369", "114", "64 · 50"]))
B += [
 beat("B05", "3 first 60 seconds",
      "Then a conflict row: an AI web search called an Amgen posting open, the liveness check "
      "returned H T T P four oh four, so the record won, and the role went back to be verified.",
      "B05_Conflict",
      "The AMGEN posting page rides up with an 'open' tag (model-judgment); a scan line sweeps it; a small terminal "
      "block prints 'HTTP 404'; the page slides back onto a 'verify' tray.",
      [{"at": 0.2, "event": "page + 'open' tag"}, {"at": 0.55, "event": "scan → HTTP 404"},
       {"at": 0.8, "event": "page to verify tray"}],
      ["AMGEN INC", "open?", "HTTP 404", "verify"]),
 # ── §4 What does it prove about me?
 beat("B06", "4 what it proves",
      "What does it prove? Every value is labelled record, model judgment, or your input.",
      "B06_Labels",
      "Three value chips drop onto the conveyor; each gets a tag that clips on in turn: record, model-judgment, your-input.",
      [{"at": 0.3, "event": "chips drop"}, {"at": 0.55, "event": "record tag"}, {"at": 0.7, "event": "model-judgment tag"},
       {"at": 0.85, "event": "your-input tag"}],
      ["record", "model-judgment", "your-input"]),
 beat("B07", "4 what it proves",
      "Gates are hard stops. I added rule R four: when an AI claim and a record disagree, the record wins. "
      "And R five: a human check wins a same-day tie with an AI check.",
      "B07_Rules",
      "A gate drops across the conveyor; a 'model-judgment' chip and a 'record' chip meet at it; the record chip "
      "passes and the other is set aside. A second, smaller gate lights for R5.",
      [{"at": 0.15, "event": "gate drops"}, {"at": 0.45, "event": "R4: record passes"}, {"at": 0.8, "event": "R5 gate lights"}],
      ["hard stop", "R4", "R5"]),
 beat("B08", "4 what it proves",
      "The evidence: the commit history, fifty-eight passing offline tests, and a break attempts log. "
      "One attempt crashed the run on a missing input file; I had it fixed, and it now halts cleanly.",
      "B08_Evidence",
      "An evidence binder opens: a commit strip, a test rack whose lamps light, a log page. A terminal block prints "
      "'Ran 58 tests — OK', then a 'HALT: input file not found' line under a check.",
      [{"at": 0.2, "event": "commit strip"}, {"at": 0.4, "event": "test lamps + 'Ran 58 tests OK'"},
       {"at": 0.75, "event": "HALT line + check"}],
      ["commits", "58 tests", "break log"]),
 beat("B09", "4 what it proves",
      "It doesn't prove model training; no model is trained here.",
      "B09_NotTraining",
      "A ghosted training-rig outline stays empty and dim; beside it the conveyor and gate stay lit.",
      [{"at": 0.3, "event": "empty rig outline"}, {"at": 0.7, "event": "conveyor + gate light"}],
      ["no training", "reliability"]),
 # ── §5 In, out, first
 beat("B10", "5 in / out / first",
      "It will never auto-apply to jobs, scrape behind logins, or use real personal data. Personas are fictional.",
      "B10_Out",
      "Three items slide toward the stage edge and stop at a closed gate: an Apply button, a login lock, a "
      "personal-data card labelled 'personal data'.",
      [{"at": 0.25, "event": "Apply button stopped"}, {"at": 0.5, "event": "login lock stopped"},
       {"at": 0.8, "event": "personal data label"}],
      ["auto-apply", "logins", "personal data"]),
 beat("B11", "5 in / out / first",
      "First will come an offline evaluation log comparing AI-sourced posting claims with liveness records. "
      "It's done when one command prints an agree and conflict table, and the tests pass in a clean environment.",
      "B11_EvalLog",
      "Two trays side by side: AI claims and records. Pages pair up across them; a dashed table grows row by row "
      "with agree / conflict marks (dashed: will exist); then a row of three test lamps lights for 'tests pass'.",
      [{"at": 0.2, "event": "two trays"}, {"at": 0.5, "event": "pages pair up"}, {"at": 0.8, "event": "table rows"}],
      ["AI claims", "records", "agree / conflict"]),
 # ── §6 What could sink it?
 beat("B12", "6 what could sink it",
      "What could sink it is entity resolution. In my run, HUMAN INC had thirteen eighty-two approvals, "
      "but I couldn't confirm it was HUMAN Security; its sponsored titles looked like enterprise IT.",
      "B12_EntityRes",
      "A record card 'HUMAN INC · 1382' and a company box; a cable starts to draw between them and stops with a "
      "question mark.",
      [{"at": 0.25, "event": "record card"}, {"at": 0.55, "event": "cable draws"}, {"at": 0.8, "event": "stops at '?'"}],
      ["HUMAN INC", "1382", "match?"]),
 beat("B13", "6 what could sink it",
      "So ambiguous matches will be labelled model judgment, confirmed by a human before scoring, "
      "and measured on a small hand-checked sample.",
      "B13_Confirm",
      "The '?' cable gets a model-judgment tag; a dashed human-review desk appears (no person icon); a small sample "
      "tray with a check-count appears (dashed: will exist).",
      [{"at": 0.2, "event": "tag"}, {"at": 0.5, "event": "review desk"}, {"at": 0.8, "event": "sample tray"}],
      ["model-judgment", "human confirm", "sample"]),
 # ── §7 Why this project?
 beat("B14", "7 why this project",
      "Why this project? Mostly new learning, and a real problem for students on O P T "
      "that I wanted to answer with records, not guesses.",
      "B14_WhyProject",
      "A loose pile of guess slips is swept aside; the record binder slides into its place.",
      [{"at": 0.3, "event": "guess slips"}, {"at": 0.7, "event": "binder in place"}],
      ["guesses", "records"]),
 beat("B15", "7 why this project",
      "New to me: hard-stop gates, labelled values, and catching an AI mistake against a record. "
      "I checked the Amgen and HUMAN approval counts by hand, in my own terminal.",
      "B15_HandCheck",
      "Gate, tag and scan line from earlier beats reappear in a row, unlabelled. Then two kraft record cards drop "
      "side by side, each with its value beside it: 'AMGEN INC 1882.0' and 'HUMAN INC 1382.0'; an ink check lands "
      "on each, and a small caption 're-run 2026-10-11' sits under the pair. Drawn, not a screenshot: "
      "evidence/hand-check-terminal.png stays off screen.",
      [{"at": 0.2, "event": "two record cards + values"},
       {"at": 0.8, "event": "checks + caption 're-run 2026-10-11'"}],
      ["AMGEN INC 1882.0", "HUMAN INC 1382.0", "re-run 2026-10-11"]),
 beat("B16", "7 why this project",
      "Claude and Claude Code drafted much of the code and documents; I reviewed them. "
      "Claude advised holding the recipe at draft, and I agreed. I chose to skip human posting checks in that run.",
      "B16_Decisions",
      "Draft pages slide onto a review desk; a check lands on each. A DRAFT stamp lands on the recipe page.",
      [{"at": 0.3, "event": "pages to review desk"}, {"at": 0.65, "event": "DRAFT stamp"}],
      ["drafted", "reviewed", "DRAFT"]),
 beat("B17", "status",
      "The recipe was held at draft with five open to-dos, and pull request thirty-two is "
      "still open. No human checked a posting, so nothing reached Apply.",
      "B17_Status",
      "The recipe page with a DRAFT stamp and five unchecked boxes; a PR tag '#32 open'; the Apply tray stays empty.",
      [{"at": 0.25, "event": "5 open boxes"}, {"at": 0.55, "event": "PR #32 tag"}, {"at": 0.8, "event": "Apply tray empty"}],
      ["DRAFT", "5 TODOs", "PR #32", "Apply: 0"]),
 # ── Why the evaluation log first (spine slot: the number, attributed)
 beat("B18", "why the eval log first",
      "In my worked run, the liveness tool contradicted both postings an AI had "
      "called open. Two is a sample, not a rate. The log will measure it properly.",
      "B18_WhyNow",
      "Two posting pages with 'open' tags; a scan line sweeps each and a counter lands on '2 of 2'. Caption under it: "
      "'per report.md, worked run 2026-10-02'. Then a dashed log page (will exist) slides in beside the counter.",
      [{"at": 0.2, "event": "two 'open' pages"}, {"at": 0.35, "event": "scans"}, {"at": 0.6, "event": "'2 of 2' + caption"},
       {"at": 0.85, "event": "dashed log page"}],
      ["2 of 2", "per report.md, worked run 2026-10-02"]),
]

SPARSE_REASON = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, with the voice "
                 "carrying the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame and "
                 "contrast still apply.")
for b in B:
    if b["lane"] == "manim":
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}

BOUT = remotion("BOUT", "outro",
    f"I'm {SAY_NAME}. This narration uses a synthetic voice. I drafted the script with Claude and checked every claim.",
    "ShowTellCard",
    {"kind": "masked", "heading": "RECORD BEATS AI · INFO 7375", "word": "Thanks.", "sub": NAME,
     "durationSeconds": 6,
     # read by bookend_check.py's outro assertions; not rendered by ShowTellCard
     "title": TITLE, "handle": NAME, "subline": ""},
    [{"at": 0.1, "event": "'Thanks.' fills from below"}, {"at": 0.35, "event": "my name lands"}],
    kind="outro_voice", tail_silence_s=1.0,
    qc={"sparse_by_design": True, "sparse_reason": "Sign-off card: one word and my name."})

B = OPEN + B + [BOUT]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "INFO 7375 · FINAL PROJECT PITCH", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "sreevarshan-sathiyamurthy", "channel_title": NAME, "persona": f"{NAME} (first person)",
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro",
    "kokoro_speed": 1.09,   # passed as --speed 1.09 to generate_audio_kokoro.py (CLI only; not read from here)
    "clock": "narration", "palette": "claude", "register": "Plain", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "folderLabel": "INFO 7375",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": "show-tell pitch film: opens on the hesitant writer + terms card, no verdict card, and no Your Turn "
                             "composer (dropped at the author's request); the outro is the author's own sign-off.",
    "audience": "hiring managers and engineers evaluating me for an ML / AI engineer role",
    "source_doc": "../../PROJECT-BRIEF.md; the-reallocation-engine @ ded8454 (branch contrib/2026fa-Sreevarshann-newgrad-de-ml-optwindow), "
                  "verified 2026-10-11 — see CLAIMS.md",
    "persona_note": "meera-krishnan is a fictional persona; labelled CONSTRUCTED on screen where she appears (B03). No real personal data.",
    "playlist": "INFO 7375 Final Project", "chapter_number": 0,
    "tags": ["INFO 7375", "OPT", "H-1B sponsorship", "LLM reliability", "entity resolution", "pipeline", "show-tell"]},
    "beats": B}
(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
words = sum(len(b["narration_text"].split()) for b in B)
print(len(B), "beats;", words, "words; est", round(sum(b["estimated_duration_s"] for b in B)), "s at 2.5 words/s")

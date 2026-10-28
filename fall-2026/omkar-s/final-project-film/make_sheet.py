#!/usr/bin/env python3
"""make_sheet.py — writes beat_sheet.json for the BiteCheck pitch film (Omkar Salian, INFO 7375).

Format: Brutalist show-tell (one drawn isometric picture per beat, minimal labels, the voice
explains). Deliberate deviations from the skill, required by the assignment ("Narrate as yourself.
Do not use the instructor's name, persona, or credit line"): no Liam persona or greeting, no
Professor Bear portraits, no @NikBearBrown outro, and no reconstructed Claude.ai composer (no
fabricated Claude responses). Every beat is Manim. See FRICTIONAL.md.

v2 (2026-10-21), after grading: adds who is building it (B00), a plain-language version (B01-B02,
smoke alarm) and the technical pipeline (B05-B06). Honesty tags: REAL (it ran / exists, dated),
PROPOSED (a constructed drawing of something not built yet), ANALOGY, SELF-REPORT, STATUS.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "bitecheck-pitch"
TITLE = "BiteCheck: Do Claude's API Tests Actually Catch Bugs?"
VOICE = "am_michael"


def beat(bid, cls, tag, narration, image, show):
    return {"beat_id": bid, "act": "pitch", "lane": "manim", "proof_gate": "SHOW",
            "narration_text": narration,
            "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
            "voice": VOICE, "engine": "kokoro",
            "honesty_tag": tag,
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                     "manim": {"class": cls}, "motion_claim": image},
            "qc": {"sparse_by_design": True,
                   "sparse_reason": "show-tell style: one drawn object per beat on a cream stage; only underfill/clustered are waived."}}


B = [
 beat("B00", "B00_Who", "WHO",
      "Hi, I'm Omkar Salian, a software engineering master's student at Northeastern. "
      "This is my final project, BiteCheck. I'm building it myself, with Claude Code as my coding assistant.",
      "A name card: Omkar Salian, MS Software Engineering, Northeastern; beside it a laptop box labelled 'me + Claude Code'.",
      [{"at": 0.1, "event": "name card"}, {"at": 0.6, "event": "laptop: me + Claude Code"}]),
 beat("B01", "B01_SmokeAlarm", "ANALOGY",
      "First, the simple version. How do you know a smoke alarm works? You blow a little smoke at it. "
      "If it beeps, good. If it stays quiet, it's broken, and you'd only find out in a real fire.",
      "Two smoke alarms; a puff of smoke drifts to each; the first sends beep waves and gets a check, the second stays silent and gets an X.",
      [{"at": 0.3, "event": "smoke puffs"}, {"at": 0.5, "event": "alarm 1 beeps"}, {"at": 0.7, "event": "alarm 2 silent, X"}]),
 beat("B02", "B02_TestsAreAlarms", "ANALOGY",
      "Software has alarms too. They're called tests. Claude can write hundreds of them, and they can all pass. "
      "BiteCheck is the smoke. It breaks one rule in the code on purpose, then checks which tests go off.",
      "A row of test pages, each with an alarm light; one bug block (the smoke) slides in; two pages beep, two stay silent.",
      [{"at": 0.2, "event": "test pages"}, {"at": 0.6, "event": "bug block slides in"}, {"at": 0.8, "event": "two beep, two silent"}]),
 beat("B03", "B03_Repo", "PROPOSED",
      "When it's done, BiteCheck will be a public GitHub repo with four parts: "
      "a prompt that tells Claude how to write tests, a list of planted bugs, a runner, and a one page report.",
      "A box labelled 'GitHub repo' opens; four parts rise out of it in turn: prompt page, bug block, runner server, report page.",
      [{"at": 0.15, "event": "box opens"}, {"at": 0.45, "event": "prompt, bugs"}, {"at": 0.8, "event": "runner, report"}]),
 beat("B04", "B04_LoanRun", "REAL",
      "It will test a loan API I built earlier with Claude's help, in TypeScript and Express, with made up applicants. "
      "On October twelfth, I ran it with Claude Code. An income of fourteen thousand, nine hundred and ninety nine rupees was rejected, "
      "fifteen thousand got an offer, and paying out too early was refused.",
      "Three synthetic applicant cards point at the loan API: X, check, and a stop bar with '409'.",
      [{"at": 0.4, "event": "card 1, X"}, {"at": 0.65, "event": "card 2, check"}, {"at": 0.85, "event": "card 3, 409"}]),
 beat("B05", "B05_PipelineA", "PROPOSED",
      "Here's how it will work. Step one: I write a numbered list of rules, and a list of mutants. "
      "A mutant is a copy of the code with one rule broken, like the income limit dropped to fifteen hundred. "
      "Step two: Claude Code writes the tests in TypeScript, and every test must name the rule it checks.",
      "Step 1: a rules page and a mutant block. Step 2: test pages, each with a cable to a rule.",
      [{"at": 0.2, "event": "rules page"}, {"at": 0.4, "event": "mutant block"}, {"at": 0.75, "event": "tests cabled to rules"}]),
 beat("B06", "B06_PipelineB", "PROPOSED",
      "Step three: the runner runs every test on the real API, where they must all pass, then on each mutant, where at least one should fail. "
      "A mutant nobody catches is a gap in the tests. A test that fails on the correct code is Claude's mistake, and it goes into a dated log.",
      "Two servers: 'real API' with all checks; 'mutant' with one X; a survivor flag and a log page below.",
      [{"at": 0.15, "event": "real API, all pass"}, {"at": 0.35, "event": "mutant, one fails"}, {"at": 0.6, "event": "gap"}, {"at": 0.8, "event": "log"}]),
 beat("B07", "B07_Alternatives", "MIXED",
      "Other tools exist. From their docs, Postbot generates test scripts, and Schemathesis checks an API against its schema. "
      "On October thirteenth, I ran Stryker on my loan rules with Claude Code. It made ninety two mutants, but none changed the fifteen thousand limit. "
      "BiteCheck adds those business rule bugs, one at a time.",
      "Postbot and Schemathesis boxes (docs only); the Stryker box with 92 and '15,000 changed: 0'; then the open BiteCheck box.",
      [{"at": 0.15, "event": "Postbot"}, {"at": 0.3, "event": "Schemathesis"}, {"at": 0.45, "event": "Stryker 92"}, {"at": 0.85, "event": "BiteCheck"}]),
 beat("B08", "B08_FirstMinute", "PROPOSED",
      "The reader is a hiring manager screening me for a new grad software or AI role. "
      "In one minute, they run one command and read one page: what passed, which bugs were caught, which slipped through, and where Claude was wrong.",
      "A terminal types one command; a report page slides out with four bars growing.",
      [{"at": 0.35, "event": "command"}, {"at": 0.55, "event": "report"}, {"at": 0.75, "event": "bars"}]),
 beat("B09", "B09_Proves", "PROPOSED",
      "It shows four skills from this course: a prompt contract, source grounding, an agent loop with limits, "
      "where Claude edits tests but never the API, and evaluation, a score plus every miss. It's measured on one API, not every API.",
      "Loop arrows between tests and the API; a lock on the API; a score bar fills.",
      [{"at": 0.3, "event": "loop"}, {"at": 0.55, "event": "lock"}, {"at": 0.75, "event": "score"}]),
 beat("B10", "B10_OutAndFirst", "CIRAN",
      "It won't be a tool for every API, and it will never fix the app's code. "
      "The first piece now runs. On October twenty second, GitHub Actions ran the income rule tests. "
      "They passed on the real rule, and caught both planted bugs: the one I chose, and Claude's.",
      "A wrench over the API is crossed out; one bug block rides a three-gate CI belt to a check.",
      [{"at": 0.15, "event": "wrench crossed out"}, {"at": 0.5, "event": "CI belt"}, {"at": 0.85, "event": "check"}]),
 beat("B11", "B11_Risk", "PROPOSED",
      "The biggest risk is me. I write the bugs, so I could make them too easy. "
      "So I'll commit the bug list before Claude writes any test, and report every bug that survived.",
      "A git timeline: the bug list commit lands first with a lock, then the tests commit; a survivors page slides out.",
      [{"at": 0.4, "event": "bug list + lock"}, {"at": 0.65, "event": "tests"}, {"at": 0.85, "event": "survivors"}]),
 beat("B12", "B12_WhyMe", "SELF",
      "Why this project? I've done API testing and CI gates at my last job, but that work is private. "
      "My public Reallocation Engine pull request shows the Claude workflow side. "
      "Mutation testing and evaluation design are new to me, so it's a mix.",
      "Two shelves: 'have' with API tests + CI gates (private) and PR #37 (public); 'new to me' with mutants, evals.",
      [{"at": 0.2, "event": "have"}, {"at": 0.5, "event": "PR #37"}, {"at": 0.75, "event": "new"}]),
 beat("B13", "B13_ExistsWill", "STATUS",
      "So, where it stands. The loan API exists, and it ran, and so did the Stryker check. "
      "Claude Code wrote the first income rule tests, I chose a second bug for them to catch, and GitHub Actions ran them all. "
      "Everything else is still to be built. I'm Omkar Salian, and this is BiteCheck.",
      "Two columns: 'exists' with solid blocks; 'will exist' with dashed outlines; the title and name land.",
      [{"at": 0.25, "event": "exists"}, {"at": 0.55, "event": "will exist"}, {"at": 0.85, "event": "title"}]),
]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "INFO 7375 · FINAL PROJECT PITCH",
    "author": "Omkar Salian", "skill": "show-tell", "style_preset": "show-tell",
    "channel_title": "Omkar Salian", "persona": "Omkar Salian (first person; synthetic Kokoro voice)",
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro", "clock": "narration",
    "palette": "claude", "register": "Plain", "fps": 24, "aspect_ratio": "16:9", "width": 1920, "height": 1080,
    "caption_policy": "none",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": "v2 2026-10-21. Course assignment forbids the instructor's name, persona or credit line and any fabricated Claude response, so the Liam greeting, the composer cards and the @NikBearBrown outro are dropped. The film closes on the narrator's own name in B13 instead of ClaudeTitleOutro.",
    "audience": "INFO 7375 graders; hiring managers screening new-grad SWE / AI engineers",
    "source_doc": "PROJECT-BRIEF.md (2026-10-12); evidence/los_smoke_test.txt",
    "tags": ["INFO 7375", "pitch", "mutation testing", "API testing", "Claude Code"]},
    "beats": B}

old = HERE / "beat_sheet.json"
if old.exists():   # keep measured audio across re-runs
    prev = {b["beat_id"]: b for b in json.loads(old.read_text())["beats"]}
    for b in B:
        p = prev.get(b["beat_id"])
        if p and p.get("narration_text") == b["narration_text"]:
            for k in ("actual_duration_s", "audio_file"):
                if k in p:
                    b[k] = p[k]
old.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(B), "beats; est", round(sum(b["estimated_duration_s"] for b in B)), "s")

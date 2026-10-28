#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for the DryRun final-project pitch film (v5, resubmission).

v5 (2026-10-23): narration unchanged, word for word. Only the picture plan changes: B02 shows the real
screenshot, B03 my own Terminal lines, B19 the real PR #33 test output, and the text-only beats (B01, B11, B12,
B14-B18, B20) get a prop.

v4 (2026-10-13): three rubric gaps closed in narration: what a reviewer could fairly conclude (B14), how
someone would know the first piece ran (B15), and real evidence for the skills I already have (B19).

v3 (2026-10-11): shorter intro that defines DryRun at once; every planned feature in future tense; no repeated
definition in the artifact beat.

v2 (2026-10-11): same approved narration, re-ordered so the real Claude reply comes first and then runs
through the mechanism as one continuous example (command -> predicted changes -> simulated changes ->
WARN -> report). On screen: short phrases (3-10 words) timed to the narration, honesty chips (REAL,
TESTED, CONSTRUCTED), and drawings only where they explain the mechanism.

Narrated in the first person from Pavithra Prasad's script with a synthetic Kokoro voice (af_heart, 0.95).
The toolkit's house intro and outro cards are left out: the assignment says to narrate as myself and not use
the instructor's name, persona or credit line.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "dryrun-pitch"
TITLE = "DryRun: See What an AI's Command Will Do"
VOICE = "af_heart"
SPARSE = ("Week 1-style phrase layout on a cream stage: short phrases timed to the narration, one drawing only "
          "where it explains the mechanism. Only underfill and clustered are waived; edge-bleed, empty-frame "
          "and contrast still apply.")

# (class name, narration, what the picture does) in film order; ids are assigned B00..B21 below.
SPEC = [
 ("Intro", "Hi, I'm Pavithra Prasad, and I'm aiming for backend and platform engineering roles. Dry Run will be a Python command-line tool that tests an AI-suggested command on a throwaway copy, and warns when the actual changes do not match the user's request.",
  "Title card: my name, target role, and what DryRun will do."),
 ("Problem", "AI assistants now suggest terminal commands, and coding agents run them. One wrong character can delete files, and reading a command is not the same as knowing what it will do.",
  "Four phrases build the problem; beside them the AI's workstation hands a command to your folder, and the files leave it."),
 ("RealReply", "On October eleventh, I asked Claude for a command to delete log files older than seven days. It gave me this, and told me to preview it first.",
  "REAL SCREENSHOT chip; the real screenshot, cropped: my request, then Claude's command outlined and its preview advice underlined as they are spoken."),
 ("Tested", "I tested the preview on a test folder on my Mac. A file seven and a half days old wasn't matched, even though it's older than seven days.",
  "MY TERMINAL chip; my own Terminal lines from 13 Oct, copied exactly; three file rows by age; the 7.5-day row is marked as missed."),
 ("Copy", "When it's done, it will be a GitHub repository with tests and an evaluation report.",
  "The artifact: GitHub repository, tests, evaluation report; drawing: your folder and its throwaway copy; design goal: real files never touched."),
 ("Contract", "The AI will have to answer in a fixed format: the command, plus its own prediction of what that command will change.",
  "Example step 1: command card and predicted-changes card (constructed example)."),
 ("Simulate", "Dry Run will run the command on the copy, inside a locked container with no network. Then it will compare every file before and after: what was created, changed, or deleted.",
  "Example step 2 (constructed simulation): planned locked container; before/after file list; the 8.5-day file struck out."),
 ("Gate", "It will check the real changes against the AI's prediction and the task's rules. Then it will allow, warn, or block. When it can't tell, it will say so.",
  "Example step 3: predicted 2 vs simulated 1; the task rule; drawing: the gate with ALLOW / WARN / BLOCK, WARN chosen."),
 ("Retry", "In a later phase, a blocked command's changes will go back to the AI, which will try again, up to three times.",
  "Later phase: changes go back to the AI; retry up to 3 times."),
 ("Report", "A hiring manager will be able to clone the repo, run a demo, and see the command, its predicted changes, and the real file differences. The tests and report will show where it works and where it fails.",
  "Example step 4: the report card (constructed mock-up) with the decision WARN, 1 file missed."),
 ("Traps", "To catch mistakes like that on purpose, I'll build trap folders: names with spaces, names that look like options, hidden files, files right at a time limit, and links that point outside.",
  "Trap-folder file chips appear as each is named."),
 ("Measure", "Then I'll measure it: tasks with known correct results, across every trap folder, comparing Claude with a free local model, and counting how often a command did too much or too little.",
  "Evaluation plan; a queue of tasks with known answers; empty counters marked NOT MEASURED YET."),
 ("Alternatives", "A tool called try already lets developers preview a command's file changes on Linux. Research benchmarks score AI commands offline.",
  "Two alternatives, one prop each: a checkpoint scanner for try, an evidence binder for the research benchmarks."),
 ("Different", "Dry Run will go one step further. It will compare the changes with your request and the AI's own prediction, and flag mismatches before you press Enter.",
  "What DryRun adds, in three phrases."),
 ("Skills", "Together, that will show the skills from this course: a prompt contract, verification that doesn't trust the AI's explanation, an agent loop, and an evaluation you can rerun. A reviewer could fairly conclude that I can check an AI's work and measure how often it's wrong, not that Dry Run makes commands safe.",
  "Four skill chips appear as each is named; then the fair conclusion beside a review desk the evidence is brought to, and what is not claimed."),
 ("Scope", "It will only check files and folders. Network calls, outside services, and databases are out of scope. The first piece I'll make run: one command, on one copied folder, listing what changed. You'll know it ran when its self-test finds exactly the changes it planted.",
  "In scope (a folder), out of scope, first piece, and how you will know it ran: a test bench where the self-test plants a sample."),
 ("Intent", "The hardest part will be knowing what you meant. I'll start with a small set of file tasks where the right result can be checked, and report uncertainty instead of guessing.",
  "The main risk and the plan; an inspection lamp lowers onto one checkable task."),
 ("MacLinux", "Another risk: my Mac's command-line tools differ from Linux tools, so the first version will target Linux behaviour.",
  "Second risk; comparison trays labelled Mac and Linux, the Linux sample lifted; Version 1 will target Linux behaviour."),
 ("Why", "I picked Dry Run to make my portfolio stronger. I've built web apps before, but nothing that checks an AI's work.",
  "Why this project; my portfolio shelf and the empty slot beside it."),
 ("Learning", "Python and testing I already know, from my internship and from my Reallocation Engine pull request, which has thirty-two passing tests. I've used Docker in a cloud project at Northeastern. Sandboxing, file diffing, and evaluation design are new to me, so this is mostly new learning.",
  "Already know, backed by PR #33's real test output, vs new to me."),
 ("Today", "Today, none of Dry Run exists yet. Everything in this film is what I will build, in four phases.",
  "No DryRun code yet; a sealed parcel; four phase chips."),
 ("Close", "Dry Run. See what an AI's command will do, before it touches your files.",
  "Title and name footer."),
]

B = []
for i, (name, narration, image) in enumerate(SPEC):
    bid = f"B{i:02d}"
    B.append({"beat_id": bid, "act": "pitch", "lane": "manim", "proof_gate": "SHOW",
              "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.6, 1),
              "voice": VOICE, "engine": "kokoro",
              "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image,
                       "manim": {"class": f"{bid}_{name}"}, "motion_claim": image},
              "qc": {"sparse_by_design": True, "sparse_reason": SPARSE}})

# v5: B02 shows a real dark-mode screenshot. GATE T's whole-frame contrast reads its dark-grey interface shapes
# (the message bubble on a near-black page) as dark text on dark; the toolkit's documented fix for real captured
# images is named text regions, each checked on its own. Together they cover every piece of text on screen.
B[2]["qc"]["contrast_regions"] = [
    {"label": "kicker and REAL SCREENSHOT chip", "box": [0.05, 0.06, 0.85, 0.255]},
    {"label": "the real claude.ai screenshot", "box": [0.095, 0.28, 0.905, 0.735]},
    {"label": "source footer", "box": [0.17, 0.84, 0.95, 0.915]}]
B[2]["qc"]["contrast_reason"] = ("Real dark-mode claude.ai screenshot (evidence/claude-reply-2026-10-11.png), shown unaltered. Its "
                                 "dark-grey bubble on a near-black page is interface, not text. Each region that holds text is "
                                 "checked on its own; every region must pass and all other checks still run.")

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "FINAL PROJECT PITCH · DRYRUN", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "pavithra-prasad", "channel_title": "Pavithra Prasad",
    "persona": "Pavithra Prasad, first person (synthetic Kokoro voice af_heart reading my script)",
    "voice": VOICE, "voice_kokoro": VOICE, "voice_speed": 0.95, "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "plain", "fps": 24, "aspect_ratio": "16:9",
    "width": 3840, "height": 2160, "caption_policy": "none",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("INFO 7375 Final Project Pitch Film: the assignment says 'Narrate as yourself. Do not use "
                              "the instructor's name, persona, or credit line.' So the house bookends are left out; "
                              "B00 is my own intro and B21 my own close."),
    "audience": "hiring managers and engineers for backend and platform roles; INFO 7375 reviewers",
    "source_doc": "PROJECT-BRIEF.md (this folder)",
    "honesty": ("Pitch, not a build: nothing of DryRun exists yet. B02 shows the real screenshot of Claude's reply "
                "(claude.ai, 2026-10-11), cropped; B03 my own Terminal lines from the 13 Oct re-run of the preview test, copied "
                "exactly; B19 PR #33's real test output (re-run 2026-10-23). "
                "B05 prediction, B06 simulation, B07 decision and B09 report are constructed and labelled on screen."),
    "tags": ["DryRun", "AI safety", "shell commands", "sandbox", "evaluation", "INFO 7375"]},
    "beats": B}

(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
words = sum(len(b["narration_text"].split()) for b in B)
print(len(B), "beats;", words, "words; est", round(sum(b["estimated_duration_s"] for b in B)), "s")

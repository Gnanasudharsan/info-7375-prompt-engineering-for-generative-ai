#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for the README Checker pitch film (Lavanya R, INFO 7375).

Format: Brutalist show-tell (one drawn picture per beat, the voice explains), with more on-screen
text than the skill's default after my first review (2026-10-13): a question header on every beat,
readable README steps, my real terminal output, and one key sentence per beat.

Changes from the show-tell defaults, made because the assignment says "narrate as yourself;
do not use the instructor's name, persona, or credit line":
  - first-person narration as me; no "Liam, in for Bear" greeting
  - the locked ClaudeTitleOutro card is NOT used (it hard-codes @NikBearBrown); B14 is my own outro
  - the terms card is drawn in Manim (BDEFS_Terms): the Remotion ClaudeDefinitions card's fixed
    text size failed GATE T's 41px floor
Pronunciation: my first name is spelled "Luh-vun-ya" in narration_text only, so Kokoro says it the
way I say it (picked from six samples, 2026-10-13). On screen it is spelled "Lavanya".
Honesty rule: past tense only for the two real README runs (2026-10-13) and the webapp repo.
Everything about the tool is "will". B05's report is labelled "constructed mock-up" on screen.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "readme-checker-film"
TITLE = "README Checker: Does the README Actually Work?"
VOICE = "af_bella"
NAME = "Lavanya R"
SAY = "Luh-vun-ya"   # how Kokoro should say my first name

SPARSE_REASON = ("show-tell style: one drawn picture per beat on a cream stage; the voice carries the "
                 "explanation. Only underfill and clustered are waived.")


def est(text):
    return round(len(text.split()) / 2.6, 1)


def beat(bid, cls, narration, image, show, sparse=True):
    b = {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
         "narration_text": narration, "estimated_duration_s": est(narration),
         "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                  "manim": {"class": cls}, "motion_claim": image}}
    if sparse:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}
    return b


HELLO = beat("BHELLO", "BHELLO_Intro",
             f"Hi, I'm {SAY}. This is a pitch for my final project, the README Checker. Nothing is built yet.",
             "Title picture: the README Checker name, 'final project pitch · Lavanya', and 'nothing is built yet', "
             "beside a README page and an open box.",
             [{"at": 0.1, "event": "title"}, {"at": 0.7, "event": "'nothing is built yet'"}])

IDEA = {"beat_id": "BIDEA", "act": "the question", "lane": "bookend", "proof_gate": "SHOW",
        "narration_text": "The question isn't how to fix a broken README. It's how to find out if it works.",
        "voice": VOICE, "engine": "kokoro",
        "shot": {"type": "REMOTION", "source": "own",
                 "show": [{"at": 0.0, "event": "types 'How do I fix a broken README'"},
                          {"at": 0.5, "event": "corrects 'fix' to 'find' as the voice says it"}],
                 "remotion": {"pattern": "BrutalistHesitantWriter",
                              "props": {"text": "How do I fix a broken README", "triggerWords": "fix",
                                        "replacementWords": "find", "fontSize": 110, "charMs": 60,
                                        "hesitateBetween": 4, "hesitateWithin": 1, "mistakeRate": 0,
                                        "jitter": 10, "seed": SLUG, "banner": ""}}},
        "motion_claim": "The writer types the naive question (fix) and corrects it to the real one (find).",
        "qc": {"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}}
IDEA["estimated_duration_s"] = est(IDEA["narration_text"])

DEFS = beat("BDEFS", "BDEFS_Terms",
            "Three terms. A README: a project's setup instructions. A container: a throwaway sandbox where "
            "commands run without touching my laptop. And an agent loop: run a step, read the result, decide the next one.",
            "Terms card drawn in Manim: README, container, agent loop, one line each.",
            [{"at": 0.05, "event": "README"}, {"at": 0.25, "event": "container"}, {"at": 0.6, "event": "agent loop"}])

B = [
    beat("B00", "B00_Problem",
         "A new engineer opens a README and follows the setup steps. A step fails, and they can't tell if the "
         "problem is them, or the instructions.",
         "A README page with readable steps (clone, install, migrate, start); a cursor walks down and an X lands on "
         "migrate. Key line: 'Is it me, or the instructions?'",
         [{"at": 0.1, "event": "README page"}, {"at": 0.4, "event": "cursor walks"}, {"at": 0.7, "event": "X lands"}]),
    beat("B01", "B01_MyRun",
         "On October thirteenth, I followed my own web app's README exactly as written, in a fresh copy. "
         "Here are its seven steps, and what happened at each one.",
         "My webapp README's seven real steps as readable rows; a mark lands beside each: placeholder warning, "
         "pass, fail, skipped, placeholder warning, fail, fail.",
         [{"at": 0.15, "event": "seven steps"}, {"at": 0.6, "event": "marks land"}]),
    beat("B01T", "B01T_Terminal",
         "The clone step had a placeholder instead of a real link. The database step failed on a missing config file. "
         "And the health check returned five oh three. I wrote that README, and it didn't work.",
         "A terminal panel with my real output from 2026-10-13: the migrate error and the 503 response.",
         [{"at": 0.2, "event": "migrate error"}, {"at": 0.65, "event": "503"}]),
    beat("B02", "B02_HerokuRun",
         "Then I tried Heroku's open source starter app, following its README the same way. "
         "It worked. The server started and the page loaded.",
         "The Heroku starter README's steps as readable rows; checks land on all of them.",
         [{"at": 0.15, "event": "steps"}, {"at": 0.6, "event": "checks"}]),
    beat("B02T", "B02T_Terminal",
         "But its README asked for the Heroku tool, which I didn't need, and never mentioned the npm version it "
         "wanted. So a good checker has to tell broken apart from mostly fine.",
         "A terminal panel with my real Heroku output: command not found, the npm engine warning, Listening on "
         "5006, 200 OK.",
         [{"at": 0.2, "event": "warnings"}, {"at": 0.65, "event": "200 OK"}]),
    beat("B03", "B03_WhatItIs",
         "So, the README Checker. A command line tool, in a public GitHub repo, that will run every README step "
         "inside a throwaway container.",
         "Open box (the container); the README drops in. Key line: 'Runs every README step in a throwaway container.'",
         [{"at": 0.2, "event": "box"}, {"at": 0.6, "event": "README drops in"}]),
    beat("B04", "B04_Loop",
         "It will run one step, read the real output, and decide what's next: continue, stop, or mark the step "
         "unclear. The AI picks the move, but every result comes from a command that actually ran.",
         "Run → read → decide loop beside the box; a dot travels the loop.",
         [{"at": 0.15, "event": "loop"}, {"at": 0.6, "event": "dot travels"}]),
    beat("B05", "B05_Report",
         "Then it will write a report: pass, warning, or fail for each step, with the README line and the real "
         "error. This one is a mock up. It isn't built yet.",
         "A readable report mock-up for my webapp README with README line numbers, stamped 'constructed mock-up'.",
         [{"at": 0.2, "event": "report"}, {"at": 0.6, "event": "rows"}]),
    beat("B06", "B06_NotCI",
         "Isn't that what CI does? My project's CI installs Node and the database with its own steps, separate from "
         "the README. CI tests the code, not the instructions a person reads.",
         "My real CI steps on one side, the README steps on the other; the CI run passes, the README is never touched.",
         [{"at": 0.2, "event": "CI steps"}, {"at": 0.6, "event": "CI passes, README untouched"}]),
    beat("B07", "B07_Reader",
         "I'm aiming for software engineer roles. A hiring manager will run one command on a sample project, and "
         "within a minute, see a report they can check against the README.",
         "A terminal window with the planned command (constructed); a report appears. Key line: one command, one minute.",
         [{"at": 0.2, "event": "command"}, {"at": 0.6, "event": "report"}]),
    beat("B08", "B08_Eval",
         "To prove it works, I'll build about ten sample projects, some with problems I plant, and some that work. "
         "I'll score how many problems it catches, and how many false alarms it raises. Those numbers don't exist yet.",
         "Ten sample boxes, planted bugs marked, a scan, and two empty score slots: caught ? / planted, false alarms ?.",
         [{"at": 0.2, "event": "boxes"}, {"at": 0.6, "event": "score slots"}]),
    beat("B09", "B09_Skills",
         "That will show five course skills: an agent loop, verification with real output, evaluation with a score, "
         "source grounding to README lines, and a prompt contract my code checks.",
         "Five labelled skills listed beside the box, each landing as it is named.",
         [{"at": 0.15, "event": "skills land one by one"}]),
    beat("B10", "B10_First",
         "It won't fix READMEs. It only reports. First, one sample README runs in a container and writes report dot md. "
         "If that file appears with a real exit code for every step, it ran.",
         "Out: a crossed-out pen ('won't fix'). First: README → box → report.md with exit codes.",
         [{"at": 0.15, "event": "won't fix"}, {"at": 0.6, "event": "report.md"}]),
    beat("B11", "B11_Risk",
         "The risk: a README can contain any command. So every step will run in a disposable container, with no "
         "secrets, deleted after each run. Vague steps get marked unclear, not guessed.",
         "A locked box swapped for a fresh one; a vague step marked 'unclear'.",
         [{"at": 0.2, "event": "lock"}, {"at": 0.6, "event": "fresh box, unclear"}]),
    beat("B12", "B12_Why",
         "Why this project? It's a mix. My public web app repo shows CI and cloud work: GitHub Actions, and AWS and "
         "GCP machine images. Docker I've used, but with no public proof yet. The agent loop, evaluation, grounding, "
         "and prompt contracts are new to me.",
         "Two labelled columns: skills I have (with the repo as proof), and skills that are new to me.",
         [{"at": 0.2, "event": "have"}, {"at": 0.6, "event": "new"}]),
    beat("B13", "B13_Exists",
         "What exists today: this pitch, my two README tests, and that repo. The tool, the samples, and the scores "
         "are what I will build.",
         "Two labelled shelves: exists today (solid) and will exist (dashed).",
         [{"at": 0.2, "event": "exists"}, {"at": 0.6, "event": "will exist"}]),
]

OUTRO = beat("B14", "B14_Outro",
             "README Checker. Does the README actually work?",
             "Own outro: box and title. Replaces the locked @NikBearBrown card.",
             [{"at": 0.2, "event": "title"}, {"at": 0.6, "event": "name"}])
OUTRO["tail_silence_s"] = 1.0

BEATS = [HELLO, IDEA, DEFS] + B + [OUTRO]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "README CHECKER · PITCH", "skill": "show-tell",
    "style_preset": "show-tell", "channel": "lavanya-r", "channel_title": NAME,
    "persona": NAME, "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Plain", "fps": 24, "aspect_ratio": "16:9",
    "width": 3840, "height": 2160, "caption_policy": "none",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("Opens on my own intro, then the hesitant writer; terms card drawn in Manim; no "
                              "verdict card or Your Turn (cut for the 2-4 minute limit). The locked "
                              "ClaudeTitleOutro is replaced by an own drawn outro (B14) because it hard-codes "
                              "@NikBearBrown, and the assignment forbids the instructor's credit line."),
    "audience": "hiring managers and engineers reviewing a Software Engineer candidate",
    "source_doc": ("PROJECT-BRIEF.md; two manual README runs on 2026-10-13 "
                   "(github.com/LavanyaRajesh24/webapp, github.com/heroku/node-js-getting-started)"),
    "playlist": "INFO 7375 Final Project Pitch", "chapter_number": 0,
    "tags": ["README", "developer tools", "agent loop", "evaluation", "Docker", "INFO 7375"]},
    "beats": BEATS}

if __name__ == "__main__":
    (HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
    words = sum(len(b["narration_text"].split()) for b in BEATS)
    print(len(BEATS), "beats;", words, "words; est", round(sum(b["estimated_duration_s"] for b in BEATS)), "s")

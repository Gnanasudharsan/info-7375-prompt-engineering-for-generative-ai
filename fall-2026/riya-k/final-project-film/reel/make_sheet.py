#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for riya-k-ground-truth-sql-v2 (INFO 7375 final project pitch, redo).

v2 answers the instructor's feedback on v1 (2026-10-19): the problem was not shown clearly, the
animations were weak, and there were no examples. So every beat is an animated Manim scene built
around one real example from Chinook, and the narration is plain everyday language (SQL is
explained once). Narrated in the first person as Riya with Kokoro af_bella (American female,
synthetic). Captions are burned in after the master (see burn_captions.py).

Every number spoken comes from evidence/run_slice.py output or a read-only query on Chinook,
re-run 2026-10-19, or from evidence/score_claude_runs.py and evidence/vanna_check.py, run 2026-10-21
(see FACTCHECK.md). The wrong queries were drafted with Claude and checked by Riya to copy common
text-to-SQL mistakes, and the film says so (B03). The only model output shown is the 2026-10-21 Claude run (B10).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "riya-k-ground-truth-sql-v2"
TITLE = "Ground Truth SQL"
HANDLE = "Riya Kapadnis"
VOICE = "af_bella"
SPARSE = ("Builds in step with the narration: each scene adds its parts on the spoken word and is full by the "
          "end, so the 50% sample shows a partly built picture. Only underfill and clustered are waived; "
          "edge-bleed, empty-frame and contrast still apply.")


def beat(bid, cls, narration, motion, show, lead=0.0):
    b = {"beat_id": bid, "act": "pitch", "lane": "manim", "proof_gate": "SHOW",
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.7, 1),
         "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": motion, "show": show,
                  "manim": {"class": cls}, "motion_claim": motion},
         "motion_claim": motion}
    if lead:
        b["lead_silence_s"] = lead
    b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE}
    return b


B = [
 beat("B01", "B01_Title",
    "Ground Truth SQL. I'm Riya Kapadnis, and this is my final project pitch. "
    "The problem: AI can write database code that runs with no errors, but gives the wrong answer.",
    "Title card: the project name writes on, Riya Kapadnis and the course fade in under it, then the one-line "
    "problem appears with a small 'no errors' tick next to a wrong number.",
    [{"at": 0.0, "event": "title"}, {"at": 0.25, "event": "name + course"}, {"at": 0.6, "event": "the problem line"}],
    lead=0.8),
 beat("B02", "B02_Problem",
    "Picture an analyst asking an AI: what is our revenue by country? The AI writes SQL, the language for asking a "
    "database questions. It runs. No errors. It says the USA made four thousand six hundred sixty seven dollars. "
    "The real answer is five hundred twenty three.",
    "A chat box: the question types in; an SQL panel types itself out; a 'ran · 0 errors' pill ticks; the result "
    "table shows USA 4,667.06; a terracotta strike crosses it and 523.06 drops in beside it.",
    [{"at": 0.1, "event": "question"}, {"at": 0.3, "event": "SQL types out"}, {"at": 0.5, "event": "0 errors"},
     {"at": 0.65, "event": "USA $4,667"}, {"at": 0.9, "event": "real answer $523"}]),
 beat("B03", "B03_Why",
    "Claude and I drafted that SQL to copy a common mistake, on a free sample music store database. One order from Reno, Nevada cost "
    "three ninety six, for four songs. The SQL joined the order to its songs, so the three ninety six was counted "
    "four times. Do that for every US order, and the total is almost nine times too high.",
    "Order card #16 ($3.96) on the left; four song rows slide out of it; the $3.96 copies onto every row; a running "
    "sum counts 3.96, 7.92, 11.88, 15.84; zoom out to 91 orders becoming 494 rows and 523 becoming 4,667.",
    [{"at": 0.2, "event": "order card"}, {"at": 0.4, "event": "four songs"}, {"at": 0.6, "event": "copied 4 times"},
     {"at": 0.85, "event": "91 orders -> 494 rows"}]),
 beat("B04", "B04_More",
    "It's not the only mistake. Mix up milliseconds and seconds: three thousand five hundred long songs, not one "
    "thousand sixty nine. Count purchases, not people: eight hundred thirty five rock buyers, in a store with fifty "
    "nine customers. Link the wrong columns: no answer at all. And no errors.",
    "Three cards flip in one after another, each with the wrong number (struck) and the right one; at the end all "
    "three get the same 'no errors' tick.",
    [{"at": 0.2, "event": "ms vs s"}, {"at": 0.5, "event": "purchases vs people"}, {"at": 0.78, "event": "wrong link"},
     {"at": 0.92, "event": "no errors x3"}]),
 beat("B05", "B05_RealLife",
    "Why does this happen? People ask data questions in plain English, so most never see the SQL. The AI doesn't "
    "know your data. And wrong SQL doesn't crash. It just gives a number people trust.",
    "Three reasons build left to right: a person who only sees the answer (SQL greyed out behind it); the AI at a "
    "database with question marks over its tables; a confident number landing on a meeting screen.",
    [{"at": 0.2, "event": "can't see the SQL"}, {"at": 0.5, "event": "doesn't know your data"},
     {"at": 0.8, "event": "a number people trust"}]),
 beat("B06", "B06_Others",
    "Other tools don't do this on your data. BIRD tests AI only on its own databases. Vanna's built-in answer test "
    "looks for words, not right numbers. On this data, it passed the answer that was nine times too high.",
    "Two panels: BIRD's shelf of its own databases with 'your data' outside it; Vanna's workstation with 'checks "
    "words, not numbers'; a pill 'USA 4,667 · passed' lands over it (real run of Vanna 2.0.2's OutputEvaluator, "
    "evidence/vanna_check.py, 2026-10-21); a gap opens between the panels.",
    [{"at": 0.25, "event": "BIRD"}, {"at": 0.55, "event": "Vanna"}, {"at": 0.8, "event": "passed 4,667"},
     {"at": 0.95, "event": "the gap"}]),
 beat("B07", "B07_WhatItIs",
    "Ground Truth SQL fills that gap. Give it your database and questions with "
    "checked answers. It runs the AI's SQL and the checked SQL, compares the results, and gives a report card: what "
    "the AI got wrong, and why.",
    "The gap closes into a pipeline: question -> AI's SQL and checked SQL -> both run on the database -> two result "
    "tables meet at a compare step -> a report-card line prints 'Revenue by country · WRONG · counted orders 4 times'.",
    [{"at": 0.15, "event": "question"}, {"at": 0.4, "event": "two SQLs"}, {"at": 0.6, "event": "run + compare"},
     {"at": 0.85, "event": "report card line"}]),
 beat("B08", "B08_WhereUsed",
    "Where will it be used? Anywhere people ask data questions in plain English: store sales, finance, hospitals, "
    "marketing, and AI data assistants. Analysts learn what to double check. Teams test a tool "
    "before buying. Engineers see what to fix.",
    "The report card sits in the middle; five places light up around it one by one (store, finance, hospital, "
    "marketing, AI assistant); then three people step in, each with a two-word takeaway.",
    [{"at": 0.12, "event": "store"}, {"at": 0.2, "event": "finance"}, {"at": 0.26, "event": "hospital"},
     {"at": 0.32, "event": "marketing"}, {"at": 0.4, "event": "AI assistant"}, {"at": 0.6, "event": "analysts"},
     {"at": 0.75, "event": "teams"}, {"at": 0.9, "event": "engineers"}]),
 beat("B09", "B09_HowJudges",
    "How does it judge? By results, not wording, since one answer can be written many ways. These two look different, "
    "but both give five hundred twenty three. On nine test queries, comparing wording judged six right. "
    "Comparing results: all nine.",
    "Two different SQL panels side by side; both run into the same result 523.06; a 'same wording?' check fails, "
    "a 'same results?' check passes; two bars grow to 6 of 9 and 9 of 9.",
    [{"at": 0.3, "event": "two SQLs"}, {"at": 0.5, "event": "both 523.06"}, {"at": 0.75, "event": "6/9"},
     {"at": 0.9, "event": "9/9"}]),
 beat("B10", "B10_Runs",
    "Claude then answered my eight questions about the music store, three times. The checker passed twenty two "
    "of twenty four. The two fails were a tie my question never settled. Claude wasn't wrong; my question was.",
    "A terminal window types the real score_claude_runs.py result (three blind Claude runs, 2026-10-21), shortened; "
    "the 22 / 24 line is underlined; the two Q02 fails light up; a card shows France 5 and Brazil 5: a tie.",
    [{"at": 0.1, "event": "command"}, {"at": 0.45, "event": "22 / 24"}, {"at": 0.65, "event": "two fails"},
     {"at": 0.85, "event": "a tie"}]),
 beat("B11", "B11_CaughtMe",
    "It also caught a mistake in my answer key. One question asked about twenty twenty three, but the data ends in twenty "
    "thirteen. The right answer was empty, so broken SQL returning nothing looked correct. Now the tool rejects empty "
    "answers.",
    "A timeline 2009-2013; a '2023' marker slides past the end; two empty result boxes show '=' ; a terracotta cross "
    "lands on the '='; a new rule card stamps on: 'empty right answer -> rejected'.",
    [{"at": 0.2, "event": "timeline"}, {"at": 0.45, "event": "empty = empty"}, {"at": 0.85, "event": "rule"}]),
 beat("B12", "B12_WhoLooks",
    "Who looks first? Hiring managers for AI engineers. They read the report card, rerun it with one command, and "
    "open one mistake. It shows I test AI instead of trusting it.",
    "A reviewer's screen: the report card page (marked planned), a one-line command, then one wrong row opens into "
    "the AI's SQL next to the checked SQL.",
    [{"at": 0.25, "event": "report card"}, {"at": 0.45, "event": "one command"}, {"at": 0.65, "event": "one mistake opens"}]),
 beat("B13", "B13_Scope",
    "The finished project will have one sample database, about fifty test questions, and Claude as the AI it "
    "tests. It won't be a chat app, and it never changes the data.",
    "Two columns fill: 'the finished project will have' (1 sample database · Chinook, ~50 test questions, Claude as "
    "the AI being tested) and 'it will not' (be a chat app, change any data · read-only).",
    [{"at": 0.15, "event": "will have"}, {"at": 0.65, "event": "will not"}]),
 beat("B14", "B14_Risk",
    "The risk: I write the questions, so the test could be too easy, and Claude getting every answer right "
    "suggests it is. So I check every answer a second way, and next I'll add harder questions.",
    "Three steps build down the frame: a risk card ('I write the test questions, so the test could be too easy'); an "
    "arrow to 'warning sign: Claude got all 8 right'; an arrow to 'what I'll do about it' with two ticks.",
    [{"at": 0.1, "event": "risk"}, {"at": 0.45, "event": "warning sign"}, {"at": 0.75, "event": "what I'll do"}]),
 beat("B15", "B15_WhyMe",
    "Why this project? I already use SQL, Python and AI at my co-op. Testing AI and understanding why it fails is "
    "what I want to learn.",
    "A heading 'why this project?' opens the beat; two shelves: 'already use' fills with three blocks; 'want to learn' "
    "has two empty slots that two blocks slide into.",
    [{"at": 0.0, "event": "heading"}, {"at": 0.3, "event": "already use"}, {"at": 0.75, "event": "want to learn"}]),
 beat("B16", "B16_Conclusion",
    "The problem: AI can give wrong answers that look right. Ground Truth SQL tests the AI on your own data and "
    "shows what's wrong, and why. Today the checker works; Claude's only fails were my question's fault. "
    "Next: fifty harder questions. Running SQL is easy. Being right is the test.",
    "Four recap rows build (problem / solution / today / next), each with its own heading; then they clear and the "
    "closing two lines write on alone.",
    [{"at": 0.1, "event": "problem"}, {"at": 0.3, "event": "solution"}, {"at": 0.5, "event": "today"},
     {"at": 0.65, "event": "next"}, {"at": 0.8, "event": "closing line"}]),
]

# Keep measured audio durations across regenerations of the sheet.
old = {}
if (HERE / "beat_sheet.json").exists():
    for b in json.loads((HERE / "beat_sheet.json").read_text())["beats"]:
        old[b["beat_id"]] = b
for b in B:
    o = old.get(b["beat_id"])
    if o and o.get("narration_text") == b["narration_text"]:
        for k in ("actual_duration_s", "audio_file", "render_duration_s"):
            if k in o:
                b[k] = o[k]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "INFO 7375 · FINAL PROJECT PITCH", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "riya-kapadnis", "channel_title": HANDLE, "persona": "Riya Kapadnis (synthetic voice, Kokoro af_bella)",
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Plain", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "burned-in after master (burn_captions.py), from narration_text with word timings",
    "bookend_exempt": ["cold-open", "bidea", "bdefs", "bvdt", "bhtf", "bout"],
    "bookend_exempt_reason": ("Course pitch redo, not a channel explainer. The instructor's feedback asked for the problem to be "
                              "shown first, so B01 is a narrated title card (project title + Riya's name + the problem) and "
                              "B02 shows the problem with a real example, replacing the hesitant writer and the terms card "
                              "(SQL is defined in the narration where it is first used). No Your Turn (a pitch has no viewer "
                              "task). No ClaudeTitleOutro: it hardcodes the instructor's handle, which the assignment forbids; "
                              "the film ends on its spoken conclusion B15."),
    "audience": "INFO 7375 instructor and TAs; a hiring manager screening AI Engineer candidates; anyone who uses AI to ask a database questions",
    "source_doc": "PROJECT-BRIEF.md; evidence/run_slice.py output and read-only Chinook queries (re-run 2026-10-19); "
                  "bird-bench.github.io (read 2026-10-09); Vanna 2.0.2 run on Chinook (evidence/vanna_check.py, 2026-10-21); "
                  "three blind Claude runs (evidence/claude_runs/2026-10-21)",
    "tags": ["text-to-SQL", "evaluation", "Claude", "INFO 7375"]},
    "beats": B}
(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(B), "beats; est", round(sum(b["estimated_duration_s"] for b in B)), "s;",
      sum(len(b["narration_text"].split()) for b in B), "words")

# Ground Truth SQL — final project pitch film

**Riya Kapadnis** · `kapadnis.ri@northeastern.edu`
INFO 7375 — Prompt Engineering for Generative AI · Final Project Pitch Film · **resubmission, 2026-10-21**

| | |
|---|---|
| **Working title** | Ground Truth SQL: an evaluation harness for text-to-SQL |
| **Target role** | AI Engineer (also readable for Data Analyst roles) |
| **Runtime** | **3:58 (237.8 s)** · 3840×2160 · 24 fps · 16 beats · burned-in captions |
| **Film** | [`riya-k-ground-truth-sql-v2.mp4`](riya-k-ground-truth-sql-v2.mp4), in this folder and in the Canvas zip (sha256 `569a8364…`). It is the verified master (`gate-reports/verified.json`, sha256 `da2d4f00…`) with captions burned in by `reel/burn_captions.py`. The root `.gitignore` excludes `*.mp4`, so it was added with `git add -f` |
| **Narration** | Written in the first person as me; voiced by a **synthetic** local voice (Kokoro `af_bella`), not a recording of my voice |
| **Cost** | $0.00. Kokoro, Manim, FFmpeg and faster-whisper, all local. No API key, no account, no upload |

## What changed since the first submission (commit `42d8c48`, 2026-10-14)

| Feedback | What I did | Where |
|---|---|---|
| Instructor: the problem was unclear, the animations were weak, there were no examples | Rebuilt the film (v2): it opens on one real wrong number, explains it with one real invoice, shows three more real mistakes, explains why it happens, and adds captions | the film, `reel/` |
| TA, P2: no record that I checked Vanna myself | Ran Vanna 2.0.2 on Chinook. Its built-in answer check passed the join-mistake answer (USA 4,667.06, nine times too high), while the row comparison failed it. The old claim ("no way to check") was wrong: Vanna has an evaluation module, but it checks words, tool calls or an LLM's opinion, not rows | `evidence/vanna_check.py`, B06, PROJECT-BRIEF §2 |
| TA, P6: "hand-written" variants were drafted by Claude | Now "drafted with Claude, checked by me" in the film (B02 tag, B03 narration), the brief and SOURCES.md | B02, B03, SOURCES.md |
| TA, next step: run Claude on the eight questions and save the raw output with its date | Three blind runs of Claude Opus 5.5, saved unedited. 22 of 24 passed by rows, 0 of 24 by SQL text. Both fails were a France/Brazil tie that my question never settled | `evidence/claude_runs/2026-10-21/`, B10 |
| TA, next step: a classmate checks two gold answers | No classmate was available, so every gold answer is instead recomputed a second way, in plain Python from the raw tables: 8/8 agree, and Q02 (tie) and Q04 (answer = every customer) are flagged. A second person's check is still planned | `evidence/cross_check.py`, B13 |
| TA, Frictional: entries need to be dated and in my own words | Entries from 2026-10-19 on are mine; the earlier, Claude-drafted ones are labelled | `FRICTIONAL.md` |

## What exists today

`evidence/run_slice.py` checks 8 gold questions over the public Chinook database and an
execution comparator on 9 variants (drafted with Claude, labels checked by me): 9/9.
`evidence/score_claude_runs.py` replays the three saved Claude runs offline: 22/24.
Everything else (about 50 harder questions, a direct Claude runner, the report card) is said
with "will" and tagged *planned* on screen. Full answers to the seven questions are in
[`PROJECT-BRIEF.md`](PROJECT-BRIEF.md).

| Beat | Question it answers | On screen |
|---|---|---|
| B01 | (title) | Title, my name, course, the problem in one line |
| B02–B04 | Q2 Why care | real example: a join mistake reports USA $4,667 vs $523, no error; three more real mistakes |
| B05 | Q2 Why care | why it happens in real life |
| B06 | Q2 Alternatives | BIRD (its own databases); Vanna's own check **passed** the $4,667 answer (real run) |
| B07 | Q1 What is it | the testing tool and its report card (planned) |
| B08 | Q3 Who uses it | where it will be used; analysts, teams, engineers |
| B09 | Q4 What it proves | judging by results, not wording: 6/9 vs 9/9 (real run) |
| B10 | Q5 What comes first | **real Claude run** on the 8 Chinook questions, 2026-10-21: 22/24, and the tie that caught my question |
| B11 | Q4 Evidence | the empty-answer bug in my answer key, and the rule that now rejects it |
| B12 | Q3 First sixty seconds | what a hiring manager opens first |
| B13 | Q5 In / out | what the finished project will have, and what it will not do |
| B14 | Q6 Risk | the test may be too easy; the warning sign; what I do about it |
| B15 | Q7 Why this project | what I already use vs what I want to learn |
| B16 | conclusion | problem, solution, today, next: "Running SQL is easy. Being right is the test." |

## Verify the evidence (offline, a few seconds)

```bash
cd evidence
python3 run_slice.py              # last lines: 9/9 and 6/9; exit code 0
python3 score_claude_runs.py      # replays the saved Claude SQL: 7/8, 7/8, 8/8 by rows; 0/8 by text
python3 cross_check.py            # every gold answer recomputed without SQL: 8/8 agree, 2 flagged
# optional, needs `pip install vanna==2.0.2` in a separate venv:
python vanna_check.py             # Vanna OutputEvaluator PASS on 4,667.06; row comparison FAIL
```

`data/Chinook_Sqlite.sqlite` sha256 `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a`.

## Rebuild the film

Commands and prompts are in [`BUILD-PROMPT.md`](BUILD-PROMPT.md) (Stages 5 and 6 for v2). Short
version, with a brutalist.art checkout at `22264a33` and its Python 3.11 venv:

```bash
cp -r reel/ <work>/riya-k-ground-truth-sql-v2/
cd <work>/riya-k-ground-truth-sql-v2
python3 make_sheet.py && cat _kit_header.py _body.py > scenes.py
<brutalist.art>/.venv/bin/python <brutalist.art>/runtime/scripts/generate_audio_kokoro.py .
cd <brutalist.art> && export PATH="$PWD/.venv/bin:$PATH"
./art run   <work>/riya-k-ground-truth-sql-v2
./art final <work>/riya-k-ground-truth-sql-v2
cd <work>/riya-k-ground-truth-sql-v2 && python3 _qc/make_word_timings.py
python3 burn_captions.py <brutalist.art>/renders/riya-k-ground-truth-sql-v2.mp4 riya-k-ground-truth-sql-v2.mp4
```

## Quality gates

Reports are in [`gate-reports/`](gate-reports/).

| Gate | Result | Report |
|---|---|---|
| Gate F (fact check, shot list, prompts present before render) | passed, render allowed | `FACTCHECK.md` |
| Gates L, A, W (beat mix, static pre-flight, contrast and margins) | passed | `run.log` |
| Layout audit | **CLEAN** | `layout_audit.md` |
| Gate V (frame QC, 32 frames) | **PASS**: 0 BLOCKER, 0 MAJOR | `gate-V-REPORT.md` |
| GATE T (type size, contrast, kerning, 16 beats) | **PASS**: 0 FAILs | `TYPECHECK.md` |
| Render integrity (`verified.json`) | **ready**, 237.8 s | `verified.json` |
| Bookend check | **1 failure, deliberate**: no `ClaudeTitleOutro` beat | `bookend_check.txt` |

The bookend failure is on purpose. The toolkit's `ClaudeTitleOutro` hardcodes "@NikBearBrown",
and the assignment forbids the instructor's credit line, so the film ends on its conclusion
beat (B16). It is a house-style check, not a render-integrity check. The run log's two SKIN LINT
lines (no ClaudeComposerAsk cold open, no ClaudeTitleOutro) come from the same choice.
Home-directory paths in the reports are shortened to `<INFO7375>/`.

## Folder

| File | What it is |
|---|---|
| `riya-k-ground-truth-sql-v2.mp4` | the rendered film, with captions |
| `riya-k-ground-truth-sql-v2.srt` | the captions as a subtitle file |
| `PROJECT-BRIEF.md` | the seven answers, plus "exists today" and "will exist" |
| `beat_sheet.json` | narration and visual plan (copy of `reel/beat_sheet.json`) |
| `BUILD-PROMPT.md` | prompts and commands that rebuild it |
| `SOURCES.md` | what I used, what I made, what Claude contributed, licences |
| `FRICTIONAL.md` | dated log |
| `evidence/` | the runnable slice, the saved Claude runs, the Vanna check, the cross-check, Chinook + licence |
| `reel/` | film source: `make_sheet.py`, `_body.py`, `scenes.py`, `burn_captions.py`, `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` |
| `gate-reports/` | toolkit gate outputs |

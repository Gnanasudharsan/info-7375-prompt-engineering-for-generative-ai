# SOURCES — DataSentry: A Project Pitch

Ethan Gomes · INFO 7375 · compiled 2026-10-14, updated 2026-10-25 for resubmission (film version 3)

## What I used (read, not copied)

| Source | What it supports | Read |
|---|---|---|
| dbt docs, "Add data tests to your DAG" — https://docs.getdbt.com/docs/build/data-tests | dbt's four built-in generic tests (unique, not_null, accepted_values, relationships); a test passes when its query returns zero failing rows. The page does not describe a report of what tests would miss. | 2026-10-14 |
| Great Expectations home page — https://greatexpectations.io/ | GX Core is open source under Apache 2.0. | 2026-10-14 |
| GX blog, "2025 In Review: Building Trust Into Your Data Work" (dated 2026-01-09) — https://greatexpectations.io/blog/2025-in-review-building-trust-into-your-data-work/ | ExpectAI, in GX Cloud, "analyzes real dataset patterns and generates suggested Expectations you can review, refine, and approve." No defect seeding or per-defect catch rate described. | 2026-10-14 |
| GX community forum, "Is there any alternative for GX v1 Data Profiler?" — https://discourse.greatexpectations.io/t/is-there-any-alternative-for-gx-v1-data-profiler/2083 | Background only: GX 1.0 removed the older profilers / Data Assistants. Not stated in the film. | 2026-10-14 |
| NYC TLC Trip Record Data — https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page | Yellow taxi trip records are published monthly as public data (Parquet). | 2026-10-14 |
| NYC TLC yellow trip data dictionary — https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf | Column names and types given to Claude (pick-up/drop-off time, passengers, distance, fare). | 2026-10-14 |
| pandera — https://github.com/unionai-oss/pandera | The check library used by the first piece and by Claude's checks. | 2026-10-14 |

**Alternatives named in the film.** dbt data tests, and Great Expectations (GX Core, and GX Cloud's ExpectAI feature).

## What I ran (hands-on, 2026-10-25)

All recorded output is unedited, in `first-run/results/2026-10-25/`. The film's terminal and scorecard panels
(B06–B09) typeset that output and are labelled "recorded output".

**1. The first piece and the dbt / GX comparison.** I ran `first-run/run_all.sh` on my own machine on 2026-10-25 at
06:16:54 (`compare.txt`, `first_piece.txt`, `dbt.txt`, `gx.txt`, `run.log`, `data.json`, `environment.json`).

| What | Detail |
|---|---|
| Data | NYC TLC yellow taxi trips, January 2025 — https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet (59,158,238 bytes, sha256 `9af277e4c0d3f9de…`). Clean sample: 10,000 rows, seed 7375 (sha256 `01c41a0277e88abb…`). |
| Planted defects | 25 negative fares + 25 drop-offs before pick-up, seed 25; answer key in `first-run/data/planted/` (never read by any check). |
| The rule | `fare_amount >= 0` |
| pandera 0.29.0 | clean PASS; broken: 25 rows flagged — negative fares 25/25 CAUGHT, drop-off before pick-up 0/25 MISSED, 0 false alarms |
| dbt-core 1.10.23 + dbt-duckdb 1.10.1 | custom generic test `not_negative` (dbt's four built-in tests have no range rule): clean PASS, broken FAIL 25 |
| GX Core 1.24.1 | `ExpectColumnValuesToBeBetween(fare_amount, min_value=0)`: clean PASS, broken FAIL, 25 unexpected values |
| Not run | GX Cloud's ExpectAI (a paid hosted feature) — described from the GX blog only |
| Found in the real month | 144,118 negative fares and 124 drop-offs before pick-up among 3,475,226 rows (`data.json`) |

Environment: Python 3.11.14, macOS-27.0.1-arm64-arm-64bit; pandas 2.3.3, pyarrow 26.0.0, duckdb 1.5.6.

**2. Claude writes the checks (two rounds, 2026-10-25).** I pasted each prompt, unchanged, into one new chat in the
Claude desktop app (no files, no Project; chat title set by the app: "NYC taxi trips data-quality checks"; model
**Opus 5.5**, effort "High", as shown in the app's model selector). Claude's replies are saved verbatim and dated in
`first-run/claude-checks/`; the `round*_checks.py` files are the code blocks, unedited.

| Round | Prompt | Claude's reply | What Claude was told |
|---|---|---|---|
| 1 | `PROMPT-round1.md` | `round1-reply-2026-10-25.md` → `round1_checks.py` | the five column names and types, and the prompt contract (pandera 0.29, one `schema`, one rule per property, a comment per rule, no hard-coded values). Never the data or the defects. |
| 2 | `PROMPT-round2.md` | `round2-reply-2026-10-25.md` → `round2_checks.py` | only which of its rules rejected good trips on the clean copy, and how many (from `explain_clean.py`). Nothing about the planted defects. |

**3. Scoring.** I ran `first-run/score_round.sh 1` and `./score_round.sh 2` myself on 2026-10-25. After the first
scoring, the scorer was corrected (a check that crashed had been counted as a catch, and the clean-copy explainer
over-counted table-level rules); I re-ran both rounds at 17:25, and those runs are the saved results.

| Checks | Clean copy | Defect types fully caught (of 5) | Files |
|---|---|---|---|
| Hand-written baseline (`checks/fare_check.py`) | PASS | 2 (negative fare, wrong type) | `hand-written-baseline.txt` |
| Claude, round 1 | FAIL: 220 rows flagged (false alarms) | 5 | `claude-round1.txt`, `claude-round1-clean-flags.txt` |
| Claude, round 2 | 0 rows flagged; one check (`fare_amount not finite`) raises `NotImplementedError` | 4 (negative fares 0/25 MISSED: the non-negative fare rule was dropped, its comment saying "refund adjustments may be negative") | `claude-round2.txt`, `claude-round2-clean-flags.txt` |

Each round was also scored on a second, held-out planting (seed 99, `claude-round*-heldout.txt`): same results.

## What I made

- `PROJECT-BRIEF.md` — the seven answers (my topic choice and my answer to Q7; drafted with Claude, see below).
- `film-v3/make_sheet.py` → `beat_sheet.json` — narration and visual plan, 17 beats.
- `film-v3/scenes_body.py` — the 17 drawn scenes (Manim), including the title card and four recorded-output panels.
- `first-run/` — the first piece, the dbt and GX comparisons, the five-defect planter, the scorer, the two Claude
  rounds, and my recorded runs.
- `film-v3/finish_audio.py`, `film-v3/build_scenes.sh`, `film-v3/embed_recorded.py` — small build helpers.
- The rendered film, and its subtitles (`.srt` / `.vtt` and the embedded track), timed from my narration.

## What Claude contributed

Two different uses of Claude, kept apart:

**Claude as the thing being tested** (Claude desktop app, Opus 5.5, 2026-10-25): wrote the two rounds of checks
described above. Its replies are shown only as scored results in the film (B09, labelled "Claude Opus 5.5 · recorded
output · 2026-10-25"), and saved verbatim and dated in `first-run/claude-checks/`.

**Claude as my build assistant** (Claude Code, model Opus 5.5, 2026-10-12, 2026-10-14 and 2026-10-25). Claude Code:

- suggested four candidate topics for data roles; **I chose** the data-quality test generator (topic 2);
- researched dbt and Great Expectations on the web and summarised what the pages say (above);
- drafted `PROJECT-BRIEF.md` from my choices and my answer to Q7;
- wrote the narration, the beat sheet, all scene code, and the build paperwork (`FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`);
- ran the toolkit's audio, render, and quality gates, looked at frames, and fixed what failed;
- built and embedded the subtitles (`film-v3/make_captions.py`);
- for the resubmission (2026-10-25): wrote the `first-run/` scripts (data, both planters, the dbt and GX comparisons,
  the scorer `score_checks.py`, `explain_clean.py`, `score_round.sh`) and drafted the two prompts
  (`PROMPT-round1.md`; `PROMPT-round2.md` from the clean-copy explainer's output). It test-ran the scripts once into a
  scratch folder (not submitted) to make sure they worked, and rebuilt the film around **my** recorded runs.

I chose the topic, the scope, and my reason for Q7 (my earlier Food Inspections Dataset Project). I ran `run_all.sh`
and both `score_round.sh` rounds myself, and I pasted the prompts into Claude and copied its replies back.

## Tools and third-party assets (all free, all local)

| Asset | Use | Licence |
|---|---|---|
| Brutalist toolkit (github.com/nikbearbrown/brutalist.art, commit 519fcbb, 2026-10-12) | pipeline, gates, show-tell drawing kit, the 25 approved original isometric props | No LICENSE file found in the repository at that commit; used as the course directs ("make a short film with Brutalist"). |
| Kokoro-82M via kokoro-onnx, voice `am_michael` | narration (a stock synthetic voice, speaking my script in first person) | Kokoro-82M model: Apache 2.0 (as stated in the toolkit's generate_audio_kokoro.py) |
| faster-whisper (`small.en`, `base.en`) | pronunciation check of each narration clip | MIT |
| Manim Community v0.20.1 | drawn scenes | MIT |
| EB Garamond | on-screen type | SIL Open Font License 1.1 (`runtime/fonts/EB_Garamond/OFL.txt`) |
| ffmpeg | audio padding, encode | LGPL/GPL |
| pandas, pyarrow | data handling in `first-run/` | BSD-3-Clause, Apache 2.0 |
| pandera | the first-piece check, and the checks Claude wrote | MIT |
| duckdb, dbt-core, dbt-duckdb | the dbt comparison | MIT, Apache 2.0, Apache 2.0 |
| great_expectations (GX Core) | the GX comparison | Apache 2.0 |
| NYC TLC trip record data | the first-run data | NYC open data, published by the TLC |

No paid generation, API keys, stock media, music, or third-party images were used. The Claude desktop app chat used my
own Claude account; no API key.

# SHOTLIST — DataSentry: A Project Pitch (version 3)

Every body beat is one drawn isometric Manim scene (show-tell). No ShowTellCard is used. B06–B09 show **recorded output**
from the first run (`first-run/results/2026-10-25/`), typeset in a terminal-style panel and labelled as recorded, per the
toolkit's executable-evidence rule. Bookends are a drawn title card and
the terms card; there is no composer, no verdict card, no Your Turn, and no @NikBearBrown outro (assignment rule:
no instructor name, persona, or credit line).

| Beat | Question | About | Lane | Picture | Why a card |
|---|---|---|---|---|---|
| BIDEA | — | opener: title card | Manim `BIDEA_Title` | "Final Project Pitch Film created by Ethan Gomes" (name in bold), "DataSentry", a drawn rule with one terracotta dot, and "Scoring AI-written data checks with planted defects" | — |
| BSIMPLE | — | in plain words (TA: explain to a non-technical person) | Manim `BSIMPLE_Spellcheck` | a page with hidden mistakes; a magnifier ticks the ones it finds; one "slipped through" | — |
| B00 | Q1 | what it is | Manim `B00_Scanner` | checkpoint scanner, parcel = the table | — |
| B01 | Q1 | the artifact | Manim `B01_Repo` | repo crate labelled "public GitHub repo / when done" opens, three parts | — |
| B02 | how | the public data, as used in the first run | Manim `B02_Table` | table card; "NYC taxi · Jan 2025"; the real sample size | — |
| B03 | how | under the hood, part one (runs today) | Manim `B03_PipeOne` | title "Part 1"; table → planter → broken copy, answer key locked; labels pandas / planter / answer key | — |
| B04 | how | under the hood, part two (ran: Claude Opus 5.5 wrote the checks) | Manim `B04_PipeTwo` | title "Part 2"; Claude · Opus 5.5 → pandera checks → clean + broken copies → scorer | — |
| B06 | Q2 | alternative 1: dbt, run for real | Manim `B06_Dbt` | **recorded output** (typeset) of `dbt build`: PASS clean, FAIL 25 broken | — |
| B07 | Q2 | alternative 2: GX Core, run for real; ExpectAI named, not run | Manim `B07_Gx` | **recorded output** (typeset) of the GX expectation: PASS clean, FAIL 25 unexpected | — |
| B08 | Q2 | the gap, shown | Manim `B08_Gap` | **recorded output**: three tools side by side, then the answer key: 25/25 CAUGHT, 0/25 MISSED | — |
| B09 | Q3 | who opens it + the real scorecard | Manim `B09_FirstMinute` | **recorded output**: hand-written 2 of 5 · Claude round 1 5 of 5 (220 clean rows flagged) · round 2 4 of 5 (negative fares 0/25) | — |
| B10 | Q4 | what it proves + what a reviewer could conclude | Manim `B10_Proves` | binder, four numbered sheets, "tested, not trusted" | — |
| B11 | Q5 | in / out / first | Manim `B11_Scope` | in-scope box, Airflow outside, first-run slip dated by the run | — |
| B12 | Q6 | risk: loose checks | Manim `B12_Loose` | gate up lets broken parcel through; gate down stops it | — |
| B13 | Q7 | why this project: in the Food Inspections Dataset Project my checks let bad rows through | Manim `B13_Why` | table "Food Inspections Dataset Project" with marks (bad rows that got through) → arrow → "New to me: pandera, dbt, GX, Claude" and "Done before: messy public data" | — |
| B14 | honesty | exists vs will exist | Manim `B14_Exists` | three real pages (pitch, planter + scorer, two Claude rounds) vs two empty slots (public repo, automatic loop) | — |
| BEND | — | close | Manim `BEND_Close` | scanner returns, title, name | — |

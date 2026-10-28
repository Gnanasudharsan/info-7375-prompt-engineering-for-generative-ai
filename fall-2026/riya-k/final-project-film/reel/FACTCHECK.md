# Fact check — Ground Truth SQL pitch film v2

## Executive summary

Every number and claim in the redone pitch film, with where it comes from. The Chinook numbers
were re-run on 2026-10-19 (read-only) and matched the saved 2026-10-09 output. Revised
2026-10-21 after the TA's feedback: the wrong queries are now described as drafted with Claude
and checked by Riya (they were not written by hand), the Vanna claim is replaced by a real run
of Vanna 2.0.2 on Chinook, and B10 now shows the first real Claude run (three blind runs,
2026-10-21). That is the only model output in the film.

Status: checked by Claude (Opus 5.5, Claude Code), 2026-10-19 and 2026-10-21, against the sources named. Revised again 2026-10-21 evening after Riya's review of the cut: B13 split into scope (B13) and risk (B14); old B14/B15 are now B15/B16. Riya Kapadnis's sign-off: APPROVED 2026-10-22, after watching the final 3:58 cut with sound.
Rule used: past tense only for what exists and can be shown; everything else is "will" / "planned".

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B02 | Wrong (fan-out) query reports USA revenue 4,667.06; Canada 2,689.96; France 1,722.10; runs with no error | PASS | `evidence/run_slice.py` Q03 wrong variant, output 2026-10-19 (`evidence-run_slice_2026-10-19.txt`) | On-screen tag: "example SQL · drafted with Claude, checked by me" (2026-10-21; was "written by me") |
| 2 | B02 | The real answer is 523.06 | PASS | Q03 gold | — |
| 3 | B03 | Invoice 16, Reno, Nevada (BillingState NV), total 3.96, four lines (Longview, Basket Case, She, Geek Stink Breath) at 0.99 | PASS | read-only query on Invoice/InvoiceLine/Track, 2026-10-19 | — |
| 4 | B03 | 91 US invoices become 494 joined rows; "almost nine times too high" | PASS | direct count 91 / 494; 4667.06 / 523.06 = 8.92 | — |
| 5 | B03 | Chinook is a free sample database of a music store | PASS | github.com/lerocha/chinook-database (MIT; `evidence/data/CHINOOK-LICENSE.md`) | — |
| 6 | B04 | ms read as seconds: 3,503 vs 1,069 tracks over five minutes | PASS | Q06 | narration says "three thousand five hundred" (rounded), card shows 3,503 |
| 7 | B04 | COUNT not COUNT DISTINCT: 835 vs 59; the store has 59 customers | PASS | Q04; `SELECT COUNT(*) FROM Customer` = 59 | — |
| 8 | B04 | Wrong join key returns empty; right answer Jane Peacock, 21 | PASS | Q05 | — |
| 9 | B05 | People ask in plain English and don't see the SQL; models don't know a schema's grain; wrong SQL doesn't crash | EXEMPT (general explanation, no figure) | the four real cases above show the last point | Worded as a general reason, no statistic |
| 10 | B06 | BIRD tests models on its own databases | PASS | bird-bench.github.io (12,751 pairs, 95 databases), read 2026-10-09; Riya checked the live page 2026-10-21: "over 12,751 unique question-SQL pairs, 95 big databases" | — |
| 11 | B06 | Vanna's built-in answer test looks for words, not right numbers; on this data it passed the answer nine times too high | CORRECTED | `evidence/vanna_check.py`, run 2026-10-21 with Vanna 2.0.2: its `OutputEvaluator` (expected words USA, Canada, France) gave PASS to both the gold rows (523.06) and the fan-out rows (4,667.06); the row comparison gave the fan-out FAIL. Vanna 2.0.2's other evaluators check tool calls, time/tokens, or ask an LLM judge (`vanna/core/evaluation/evaluators.py`) | The 2026-10-09 claim ("no way to check") was wrong for Vanna 2.0.2, which has an evaluation module; replaced. Vanna's LLM step was not run (needs a paid key). On screen: a cropped screenshot of Riya's own run of `vanna_check.py` (2026-10-21 17:43), labelled "my run · 2026-10-21" |
| 12 | B07, B12 | The harness, report card, one-command replay | EXEMPT (plan) | PROJECT-BRIEF.md §1, §3 | On-screen "planned" tags |
| 13 | B08 | Where it will be used (store sales, finance, hospitals, marketing, AI data assistants) and who it helps | EXEMPT (intended use, said as "will") | PROJECT-BRIEF.md §2–3 | No customers or deployments claimed |
| 14 | B09 | Two different SQL queries both return 523.06; on 9 test queries (3 correct rewrites, 6 with a mistake) comparing wording judged 6 right, comparing results 9 | PASS | Q03 equivalent variant; last two lines of run_slice.py output | — |
| 15 | B10 | Claude answered the 8 questions three times; the checker passed 22 of 24; both fails are Q02, where France and Brazil tie at 5 customers and the question sets no tie order | CORRECTED | `evidence/claude_runs/2026-10-21/` (prompt, three raw replies, `score_output.txt`); tie checked with a read-only query (Brazil 5, France 5) | B10 used to show run_slice.py; now shows score_claude_runs.py, shortened and reformatted (tag says so). "Claude wasn't wrong" = its rows are a valid answer to the question as written |
| 16 | B11 | First gold asked about 2023; data ends 2013 (InvoiceDate 2009-01-01..2013-12-22); empty gold let a broken query match; runner now rejects empty gold | PASS | `evidence/run_slice_output_v0_first_run.txt`; `run_slice.py` assert | — |
| 17 | B13, B14 | Scope (will have / will not) and risk; "Claude's first run suggests" the test is too easy; "every answer is checked a second way" | PASS | PROJECT-BRIEF.md §5–6; item 15 (every Claude answer was a correct answer); `evidence/cross_check.py` recomputes all 8 gold answers in plain Python from raw tables: 8/8 agree, Q02 and Q04 flagged (2026-10-21) | Replaces "a classmate checks some answers": the classmate check did not happen. Harder questions said as a plan |
| 18 | B15 | Riya uses SQL, Python and AI at her AI engineer co-op | EXEMPT (personal account, confirmed 2026-10-14) | Riya | No co-op code or metrics shown |
| 19 | B16 | "Today the checker works; Claude's only fails were my question's fault. Next: fifty harder questions"; on screen "tested Claude on 8 questions, 3 times each · 22 of 24 passed" | PASS | items 14–16 | Closing line "Running SQL is easy. Being right is the test." is a slogan, EXEMPT |
| 20 | B03 | "Claude and I drafted that SQL" | PASS | SOURCES.md: Claude drafted `gold_set.json`; Riya checked it | Replaces "I wrote that SQL myself" (TA feedback, 2026-10-14) |
| 21 | B11 | "It also caught a mistake in my answer key" | PASS | the Q08 error was in the Claude-drafted gold set Riya adopted (SOURCES.md) | Replaces "my own mistake" |

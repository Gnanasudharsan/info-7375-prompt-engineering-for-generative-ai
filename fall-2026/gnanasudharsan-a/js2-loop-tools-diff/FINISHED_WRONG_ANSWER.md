# A finished wrong answer (GATE §8) — SEEDED demonstration, 2026-11-06

**SEEDED, not a normal live run.** In mode A the ashby:notion response was constructed as a 200 `{"jobs": []}` by `scripts/seeded_run.py`. Every other response was real HTTPS. Runs live in `seeded/`, never in the real `state/`.
Predictions were committed before running: `evidence/seeded_prediction.txt` (593387a).

## What the agent reported
| run | agent exit | notion count | new | removed |
|---|---|---|---|---|
| 20261106T203850Z-SEEDED-A (notion constructed empty) | **finished, code 0** | 0 | 0 | **154** |
| 20261106T203859Z-SEEDED-B (all real, the next run) | **finished, code 0** | 154 | **154** | 0 |

Both runs ended cleanly and both are wrong. In A, 154 real postings were reported "removed" and notion's state was overwritten with `[]` (`evidence/seeded_state_after_A.json`). In B, because the state entry was `[]` and not missing, the board was not a baseline, so all 154 real postings came back as "new". The harm lasts beyond the bad run.

## What caught it: an independent check, not the agent's own report
`scripts/check_run.py` does not import jobwatch. It compares the report with the prior state and re-counts one board with its own request.
- A: `EMPTY-AFTER-NONEMPTY` (prior 154 -> 0) **and** direct recount 154 != reported 0 (`evidence/check_seeded_A.txt`)
- B: `ALL-NEW-AFTER-EMPTY-STATE` (prior [] -> 154 new) (`evidence/check_seeded_B.txt`)

## Why the agent could not see it
The loop checks shape, not plausibility. A 200 with a well-formed empty list passes `_parse_jobs`, the board is `ok`, and GATE §2 calls a run with no failed board `finished`. As GATE §2 says, "finished" means the loop ran to the end, not that the answer is right.

## Also observed (real, not seeded)
greenhouse:anthropic had 1 genuinely new posting in run A (670 -> 671).

## What it led to
The fix is decided in GATE Amendment 1 and implemented as the review-packet change (REVIEW_PACKET.md).

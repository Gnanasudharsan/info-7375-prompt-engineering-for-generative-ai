# Job-Search Agent 1 — The Contract and the Watch
INFO 7375 · Fall 2026 · Gnanasudharsan Ashokumar · `fall-2026/gnanasudharsan-a/js1-contract-and-watch/`

An agent that watches one public job board (Anthropic on Greenhouse), reports only postings new since the last run, and gives two labeled verdicts for each new posting: a recomputable **rule verdict (record)** and a **Claude verdict (judgment, not fact)**, judged for a **fictional persona** (Ananya Rao, `persona/ananya-rao.resume.json`).

## Language and toolchain
- Python **3.14.0** (the only version I tested). Dependencies pinned in `requirements.txt` (requests, jsonschema, pytest, anthropic).
- Claude judge backend used for every live call: `JOBWATCH_BACKEND=claude_cli` (Claude Code print mode, `claude -p`, with all tools disabled and a fresh empty temp folder per call), model `claude-opus-5-5`. Requires a logged-in Claude Code CLI. See CONTRACT.md Amendment 2.
- No API key is needed for the tests or for rule-only runs.

## Setup
```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Run the tests (offline, no network, no API key)
```
.venv/bin/python -m pytest -v
```

## Run the agent
A live run **updates `state/`**. To try the agent without changing the committed state, use a seeded run (writes only to `seeded/`):
```
# Seeded, rule judge only (no network, no Claude): labeled SEEDED
.venv/bin/python -m jobwatch watch --no-claude --from-file data/raw/anthropic_20261028T192103Z.json

# Live, rule judge only
.venv/bin/python -m jobwatch watch --no-claude

# Live, both judges (as used for run 2)
JOBWATCH_BACKEND=claude_cli JOBWATCH_MODEL=claude-opus-5-5 .venv/bin/python -m jobwatch watch --prompt prompts/judge_baseline.md
```

## Reproduce the experiment numbers (from saved runs, offline)
```
.venv/bin/python experiment/score_sampling.py experiment/runs/sampling_20261029T0445Z
.venv/bin/python experiment/score_run.py experiment/runs/exp_baseline_dev_20261029T0505Z dev
.venv/bin/python experiment/score_run.py experiment/runs/exp_revision_dev_20261029T0517Z dev
.venv/bin/python experiment/score_run.py experiment/runs/exp_baseline_heldout_20261029T0524Z heldout
.venv/bin/python experiment/score_run.py experiment/runs/exp_revision_heldout_20261029T0526Z heldout
```
New judge runs: `experiment/run_judge.py --split dev|heldout --prompt <file> [--ids ...] [--repeats N] --out <new folder>`.

## What ran (all past tense, all saved)
| When (UTC) | What | Result | Evidence |
|---|---|---|---|
| 2026-10-28 19:21 | Run 1, live baseline | 680 postings, 0 new | `data/raw/anthropic_20261028T192103Z.json`, `data/runs/20261028T192103Z.json`, commit `6baa583` |
| 2026-10-29 04:40 | Smoke test, 1 Claude call | Valid; NOT_RELEVANT vs my label RELEVANT | `experiment/runs/smoke_20261029T0440Z/`, `96de51f` |
| 2026-10-29 04:43 | Run 2, live, second calendar day, both judges | 679 postings, 2 new (both NOT_RELEVANT by rule and Claude), 3 removed; recomputed independently | `data/raw/anthropic_20261029T044359Z.json`, `evidence/run2_recomputation_2026-10-29.txt`, `b04c897` |
| 2026-10-29 04:45 | Sampling: 5 dev postings × 4 fresh calls | 11/20 agree with my labels; 4/5 unanimous | `experiment/SAMPLING_REPORT.md` |
| 2026-10-29 05:05–05:26 | Prompt experiment | Baseline dev 7/10, revision dev 10/10; held-out 10/10 for both | `experiment/EXPERIMENT_REPORT.md` |
| 2026-10-29 ~15:45–16:00 | Action-surface comparison, 3 modes | Chat RELEVANT, file RELEVANT, agent NOT_RELEVANT (all valid) | `experiment/ACTION_SURFACE.md` |

**Prompt the watch uses:** `prompts/judge_baseline.md`. I kept the baseline because the held-out set scored 10/10 for both prompts, so it gave no evidence that the revision generalizes.

## Files
- `CONTRACT.md`: the contract (written first, `fd949ad`) and Amendments 1–2.
- `jobwatch/`: watch, allow-listed fetcher, persona check, rule judge, Claude judge, validator.
- `tests/`: `test_rule_contract.py` (my contract's cases, written before the rule code), plus Claude Code's tests.
- `persona/`: the fictional persona and its labeled additions.
- `data/raw/`, `data/runs/`, `state/`: raw responses, run reports, seen ids from both runs.
- `prompts/`: `judge_baseline.md`, `judge_revision.md`.
- `experiment/`: labeling rule and notes, the 20 hand labels, selection, sampling, experiment, action surface, runs, scorers.
- `evidence/`: test outputs, run logs, recomputations, order checks, the generated prompt diff.
- `SOURCES.md` (what I used, wrote, and Claude contributed) · `FRICTIONAL.md` (honest log).
- Not included by design: my real résumé, any API key, Claude conversation transcripts.

## Sign-off — Job-Search Agent 1
**Checked:**
- The rule's two contract wrong versions are caught: `test_rejects_senior_titles`, `test_respects_negative_sponsorship_boilerplate` (fail on the wrong versions in scratch copies, pass on the real rule).
- The rule's data traps: `test_control_posting_is_relevant`, `test_irish_location_is_not_us`, `test_not_shipped_skills_do_not_count`, `test_ai_in_sales_title_is_not_a_role_match`, and the two Amendment 1 tests.
- New-since-last by id: run 2's 2 new ids and the state contents, recomputed directly from the two raw files (`evidence/run2_recomputation_2026-10-29.txt`).
- Allow-list refusal, persona refusal, validator rejections, seeded-state isolation: Claude Code's tests, run by me (`evidence/pytest_*.txt`).
- Judge isolation: smoke test showed `num_turns 1`, a temp working folder, reported model `claude-opus-5-5`.
- Every sampling and experiment number: recomputed from saved runs by `score_sampling.py` and `score_run.py`.

**How:** by a test written before Claude's code (`tests/test_rule_contract.py`, committed failing at `bbbafdf`; Amendment 1 tests failing at `c841810`; the wrong-version cases and expected verdicts come from my contract, while a Claude chat drafted the file, including the control posting values and three extra trap tests); by recomputation (run 2 ids, all scores); by hand (all 20 labels, the action-surface folder checks and tool logs); with Claude's help (Claude Code wrote the implementation and its own tests and ran the wrong-version scratch checks; a Claude chat drafted the scorers, helper scripts and experiment plan, and reviewed my documents — see SOURCES.md).

**Not checked:**
- Removed postings are not reported, and the state keeps removed ids, so a re-posted id would not be reported as new.
- Whether the revision prompt generalizes: held-out hit the ceiling for both prompts.
- Remote postings outside the US, and whether Research Engineer roles need research depth the rule does not test.
- Claude Code's behavior in default (non-auto) permission mode; only auto mode was observed.
- Python 3.10; the claude_cli and API backends against each other; any other job board.

**Not claiming:** that any verdict is right for a real person; that Claude's judgments are facts or better than the rule; that the revision prompt is better; that the agent monitors continuously (it runs only when invoked); that its relevance rule is complete.

**Signed or withheld:** Signed — Gnanasudharsan Ashokumar, 2026-10-29

## Driver's seat
| Part of the task | What Claude did | What I did | Why it stays mine | Where it shows |
|---|---|---|---|---|
| Contract and rule | Reviewed drafts, flagged gaps | Wrote CONTRACT.md and both amendments; made every rule decision | Defines what "relevant" means for this person | `fd949ad` before any code; `c841810`; `14c75ac` |
| Tests of the rule | A Claude chat drafted the test file, including the control posting values and three extra trap tests | Supplied the two wrong-version cases and expected verdicts from my contract, checked every case against my rule, and committed them failing first | Tests must come from the contract, not the code they test | `bbbafdf` (failing) → `b1f1e45` (passing) |
| Implementation | Claude Code wrote `jobwatch/` and its tests | Reviewed diffs, accepted 8 of 9 choices, modified #3, rejected an `rm -rf` command | I run and stand behind the code | `806f052`, `b1f1e45`; FRICTIONAL entries |
| Ground truth | — | Wrote the labeling rule and all 20 labels | The experiment measures Claude against my judgment | `187b985`, `4d5278c` |
| Prompt experiment | A Claude chat drafted the plan, the scorers, and the revision sentence's wording; Claude Code built the runner; Claude (Opus 5.5) produced the verdicts | Wrote the baseline prompt; chose the one change from the dev misses; committed the plan and revision before their runs; ran every judge call and scorer; wrote and corrected the report; kept the baseline after held-out | The choice of what to change, and the decision after held-out, are the experiment | `879b247`, `7cfc8e5`, `908b8f7`, `71830f9` |
| Live runs and evidence | — | Ran the baseline and run 2, recomputed run 2, checked the logs | Past tense only for what I ran | `6baa583`, `b04c897` |

# Mode Build assignment — daily data-role check, OPT + H-1B (Atharva H)

## Executive summary

**What this is.** My submission for the Reallocation Engine Mode Build assignment: a mode (recipe) for the engine, the one-page case for it, a real run with its output pasted in, the log entries, and the prototype script with its tests.

**Who it's for.** An international master's student on OPT with a fixed end date, looking for entry-level data roles: data analyst, data scientist, BI analyst, business analyst, analytics engineer and data engineer. The student needs an H-1B sponsor that's also in E-Verify.

**What it does.** Each morning it reads the student's own target companies' job boards (Greenhouse and Ashby) and returns the postings that match the student's requirements. For each one it shows the sponsorship, E-Verify and visa-clock evidence, and it lists every target-title posting it dropped, with the reason.

**What it found.** On two real days it read 8 real company boards. On 2026-10-20 it found 2,108 postings and 7 matches, all confirmed live. On 2026-10-21 it caught one posting that had closed overnight, and after I recorded my E-Verify and sponsorship statements, 4 roles came out as Apply.

**Claimed stage: RUNNABLE-LIVE**, not VERIFIED: nobody but me has run it.

## What is in this folder

The folder mirrors the paths in `nikbearbrown/the-reallocation-engine`, so the files can be copied into a clone of the engine unchanged.

| File | What it is |
|---|---|
| [`recipes/case-data-analyst-opt-h1b-15-2051.md`](recipes/case-data-analyst-opt-h1b-15-2051.md) | The mode file (RUNNABLE-LIVE, 8 open typed TODOs) |
| [`recipes/case-data-analyst-opt-h1b-15-2051.card.md`](recipes/case-data-analyst-opt-h1b-15-2051.card.md) | The same mode, written for the student |
| [`assignments/submissions/atharvahambir/DOMAIN-JUSTIFICATION.md`](assignments/submissions/atharvahambir/DOMAIN-JUSTIFICATION.md) | The one-page case: who, the information gap, the engine layers, failure modes |
| [`assignments/submissions/atharvahambir/WORKED-RUN.md`](assignments/submissions/atharvahambir/WORKED-RUN.md) | Both live days: real commands and output, verified vs. inferred, verification, attestation, reflection |
| [`assignments/submissions/atharvahambir/RUN_LOG-entry.md`](assignments/submissions/atharvahambir/RUN_LOG-entry.md) | The run-log entries (kept here, not in the engine's shared `logs/RUN_LOG.md`) |
| [`assignments/submissions/atharvahambir/PRESENTATION.md`](assignments/submissions/atharvahambir/PRESENTATION.md) | Talk track for the five-minute show-and-tell |
| [`assignments/submissions/atharvahambir/FRICTIONAL.md`](assignments/submissions/atharvahambir/FRICTIONAL.md) | What I tried, what broke, who decided what |
| [`assignments/submissions/atharvahambir/runs/`](assignments/submissions/atharvahambir/runs/INDEX.md) | Every saved terminal output, with an index of exact commands |
| [`logs/runs/`](logs/runs/2026fa-atharvahambir-4.md) | Detailed run logs 1–4 |
| [`scripts/contrib/2026fa/atharvahambir-reallocation-engine/`](scripts/contrib/2026fa/atharvahambir-reallocation-engine/README.md) | The prototype (`daily_check.py`, standard-library Python), 18 tests, 4 break mutants |
| [`search/examples/atharva/`](search/examples/atharva/) | The fictional persona the offline sample runs as |

## Run it

It reads the engine's data and calls the engine's scorer, so it runs inside a clone of the engine. It needs Python 3.10+ and Node 20+. The sample and tests make no network calls.

```bash
git clone https://github.com/nikbearbrown/the-reallocation-engine.git
cd the-reallocation-engine
cp -R <this folder>/recipes <this folder>/scripts <this folder>/logs <this folder>/assignments <this folder>/search .
npm install
python3 scripts/contrib/2026fa/atharvahambir-reallocation-engine/daily_check.py --sample
python3 scripts/contrib/2026fa/atharvahambir-reallocation-engine/test_daily_check.py
python3 scripts/contrib/2026fa/atharvahambir-reallocation-engine/break_attempts.py
```

## Not in this repository on purpose

The live runs used my real profile. My OPT end date, unemployment days, buffer and slack days are redacted from every file here. The raw job-board responses and the unredacted reports stay in a private, gitignored folder on my machine.

## Relation to my earlier submission

[`../reallocation-engine-recipe/`](../reallocation-engine-recipe/README.md) is my earlier (25-point) recipe-design submission, left as it was. This folder supersedes it for the Mode Build. The same files are in pull request [nikbearbrown/the-reallocation-engine#73](https://github.com/nikbearbrown/the-reallocation-engine/pull/73), opened 2026-10-21 from my fork. It only adds files under my own paths.

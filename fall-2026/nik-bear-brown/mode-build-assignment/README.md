# Mode Build assignment: Professor Bear's own version

## Executive summary

**What this is.** The instructor's worked example of the Reallocation Engine Mode Build assignment: a new recipe (a "mode") for the engine, the one-page case for it, a real run with its output pasted in, and the log entry. **Why it is here.** Professor Bear gives this assignment to students and does it himself, in the open, with the same honesty rule: say what ran, say what did not, and mark the recipe's stage by its evidence. **What it found.** The mode answers a question the engine's job-board checks cannot: where is the research money, for a teaching professor who wants part-time paid research? A first real run against two federal award databases found 349 awards at six Boston-area institutions, 223 of which could pay for work starting in January 2027. The mode is a **DRAFT**: it ran, but six decisions are still the professor's, so it does not claim a later stage. The run also found real problems in the engine itself (below).

## What is in this folder

| File | What it is |
|---|---|
| [`recipes/case-part-time-funded-research-lab.md`](recipes/case-part-time-funded-research-lab.md) | The mode file (status DRAFT, 6 open typed TODOs) |
| [`01-domain-justification.md`](01-domain-justification.md) | The one-page case: who, the information gap, the engine layers, two failure modes |
| [`02-worked-run.md`](02-worked-run.md) | The run: real commands and output, verified versus inferred, verification, reflection, attestation |
| [`03-run-log-entry.md`](03-run-log-entry.md) | The entry for the engine's `logs/RUN_LOG.md` |
| [`04-show-and-tell-notes.md`](04-show-and-tell-notes.md) | Notes for the five-minute in-class show and tell |
| [`scripts/funding/check-awards.py`](scripts/funding/check-awards.py), [`test_check_awards.py`](scripts/funding/test_check_awards.py) | The new ingest script and its 17 tests |
| [`runs/`](runs) | Every command's real output, and the script's JSON log and Markdown report |
| `make-zip.sh` | Builds the upload zip for the course site (not committed) |

## What the run found about the engine

- `npm run bls:local-wage` cannot run on a fresh copy: its `.venv` is not there and `data/bls/local-wage/` is not in the repository on `main`, though the recipe says the inputs are "already ingested".
- `npm run ats:liveness` returns `uncertain`, not `expired`, for a posting that does not exist.
- `npm run ats:scan` keeps a role on a title substring: `Director, Technical Revenue Accounting` matched "Account".
- With the lockfile's Playwright (1.62.1) the liveness command needs a browser build that a machine with an older cache does not have.

## Reproduce

```bash
python3 scripts/funding/test_check_awards.py            # 17 tests, no network
python3 scripts/funding/check-awards.py --orgs "NORTHEASTERN UNIVERSITY" --terms "single cell" \
  --fy 2026 --window-start 2027-01-01 --redact-ids --out-json out.json --out-md out.md   # live, public databases, about 6 seconds
```

The engine commands in the worked run were run on a fresh clone of the engine repository. This folder does not change that repository, and no pull request has been opened: that step is the student's, and for the professor it is his call.

## Not in this repository on purpose

The real award numbers and the principal investigators' names are written only to a private file outside this folder. This folder is public and carries no grant tracking numbers and no other person's name.

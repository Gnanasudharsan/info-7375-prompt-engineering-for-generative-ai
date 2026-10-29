# SOURCES — Job-Search Agent 1
Author: Gnanasudharsan Ashokumar

## What I used (starting material)
- **Course repo** (nikbearbrown/info-7375-prompt-engineering-for-generative-ai): the JS1 assignment and the course AI policy. No earlier JS1 submission was copied.
- **Persona**: `search/examples/ananya-rao/` from The Reallocation Engine (`resume.example.json`, `profile.yml`), fictional (@example.com, 555 numbers). I extended it with labeled additions: `target_roles`, `willing_to_relocate_us`, `needs_sponsorship` (2026-10-28), and "Research Engineer" under Amendment 1. The `_additions` field in the persona file records these.
- **Data**: the public Greenhouse job-board API for Anthropic (`boards-api.greenhouse.io/v1/boards/anthropic/jobs?content=true`), fetched 2026-10-28 and 2026-10-29; raw responses in `data/raw/`.
- **Tools**: Python 3.14.0, requests, jsonschema, pytest, the anthropic SDK (pinned in `requirements.txt`); Claude Code (Opus 5.5) for implementation; `claude -p` for the Claude judge; Claude.ai incognito chat for action-surface Mode 1.

## What I wrote
- `CONTRACT.md` (before any code, `fd949ad`) and Amendments 1 and 2.
- The rule decisions: board, persona, location, sponsorship, not-shipped skills, Amendment 1 variant choice, the claude_cli backend decision.
- `experiment/LABELING_RULE.md`, `experiment/LABELING_NOTES.md` (interpretations mine; notes wording drafted with help from a Claude chat).
- All 20 hand labels in `experiment/labels_dev.json` and `labels_heldout.json`.
- `prompts/judge_baseline.md`, and the choice of the one revision change in `prompts/judge_revision.md`.
- The reports: `experiment/SAMPLING_REPORT.md`, `experiment/EXPERIMENT_REPORT.md`, `experiment/ACTION_SURFACE.md` (corrections to match the evidence made with help from a Claude chat), and `FRICTIONAL.md` (entries mine; hashes, file names and ordering corrected with help from a Claude chat).
- The sign-off and driver's seat in `README.md`.

## What Claude contributed
- **Claude Code** wrote the implementation against my contract: `jobwatch/` (watch, fetcher, persona check, rule, validator, Claude judge, claude_cli backend), `experiment/run_judge.py`, `experiment/select_postings.py`, `evidence/amendment1_variants.py`, and its own tests (`tests/test_watch.py`, `tests/test_judges.py`, `tests/test_run_judge.py`, `tests/test_claude_cli_backend.py`, `tests/conftest.py`). It also ran the offline variant analysis and the wrong-version checks in scratch copies. Its choices and my accept/modify decisions are in `FRICTIONAL.md`.
- **A Claude chat** (claude.ai) guided the process: setup and data-exploration commands, the contract skeleton headings, reviews of my drafts, the `tests/test_rule_contract.py` file (cases and expected verdicts from my contract), the scoring scripts (`experiment/score_sampling.py`, `experiment/score_run.py`), `experiment/label_helper.py`, and the evidence-extraction commands.
- **The Claude judge** (Opus 5.5 via `claude -p`) produced every Claude verdict in `experiment/runs/` and in run 2; each is labeled "judgment (model output, not fact)".

## What is NOT in this repo (by design)
- My real résumé, API keys, and Claude conversation transcripts. Only extracted tool-call lists from two local Claude Code session logs are included (`experiment/action_surface/mode2_tool_summary.txt`, `mode3_tool_log.txt`).

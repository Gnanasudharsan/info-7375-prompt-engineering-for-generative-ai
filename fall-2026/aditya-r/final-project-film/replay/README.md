# DayThread two-day replay (resubmission, 2026-10-25)

The pitch film (submitted 2026-10-14) **proposed** this replay as the first thing to make run. It
did not exist then. It was built and run on 2026-10-25 during the class-wide resubmission, after
the TA asked for a build log that starts with a prediction made before the run.

**Synthetic data only.** Peg Hollis is a fictional client. Day 1 (2026-11-02) and day 2
(2026-11-03) are simulated conversation dates. Both days are replayed back to back in one command,
and every call is stamped with its real execution time.

## What it tests

1. Day 1: a fixed check-in transcript in which Peg mentions "just a little tumble"
   (`fixture/day1_transcript.txt`).
2. A summary of day 1, under two settings:
   - **normal**: a concise summary for the record;
   - **constrained**: exactly one sentence on mood, meals and daily activities. This is a
     deliberate stress test, not an estimate of normal failure rates.
3. Two day-two openings per summary, each from its own fresh session, with identical
   instructions:
   - **A**: the summary only;
   - **B**: the summary plus the full raw day-one transcript text.

The question is whether the summary keeps the fall, and whether day two follows up on it. The
prediction and the criteria were fixed first, in `PRE-RUN.md`.

**Not built here:** the separate transcript check, the review page, the executor, and the
permission test. These remain proposed.

## Files

| Path | What |
|---|---|
| `PRE-RUN.md` | Aditya's prediction, final criteria, run plan, input hashes. Written before the first call and not edited afterwards. |
| `fixture/` | Transcript (the exact text sent) and `fixture.json` (label, simulated dates, evaluation notes) |
| `prompts/` | System prompts and input templates, identical for every trial |
| `replay.py` | The runner: Python standard library + SQLite. Refuses to run if an input's hash changed. |
| `flags.py` | Keyword pre-flags. A preliminary aid only. |
| `make_review_sheet.py` | Builds the review sheet: auto flags, Claude's provisional scores, Aditya's blank final columns |
| `preflight/` | Non-experimental config check (a "ping" with the exact flags) |
| `runs/<run_id>/` | Everything from one run: `daythread.sqlite`, raw CLI JSON for every attempt (`calls/`), `run.log`, `manifest.json`, `flags.json`, `claude_provisional.json`, `REVIEW-SHEET.md` |

## Reproduce

Requirements:
- Python 3.12, standard library only.
- The Claude Code CLI (`claude`), logged in. The run used version 2.1.241, logged in through a
  claude.ai account; no API key.

```bash
cd replay
python3 -B replay.py --trials 5               # 30 calls; creates runs/<run_id>/
python3 -B flags.py runs/<run_id>
python3 -B make_review_sheet.py runs/<run_id>
```

Each call is:
```
claude -p --safe-mode --tools "" --no-session-persistence --output-format json \
  --model claude-opus-5 --effort medium --system-prompt "<prompt file>" "<filled input>"
```
- It runs from a new empty temporary directory.
- `--safe-mode` turns off CLAUDE.md, skills, plugins, hooks and MCP.
- With no tools, the model sees only the text it is given.
- Calls share no history.
- The CLI cannot set temperature, top-p or max output tokens, so these were left at the service's
  defaults.

Model output varies from run to run, so a rerun will not reproduce the same text. It should
reproduce the setup.

**Isolation limit:** a test call used 272 input tokens in total. That is consistent with very
little added context, but it does not prove exactly what hidden context, if any, the CLI adds.

# Assignment 01 — Randomness and Prompt Contracts: a controlled prompt experiment

**Course:** INFO 7375 Prompt Engineering for Generative AI (Fall 2026)
**Assignment:** [assignments/assignment-01-randomness-and-prompt-contracts.md](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/assignments/assignment-01-randomness-and-prompt-contracts.md) (100 points)
**Student:** Muse (AI agent), submitted at Professor Bear's direction as a pilot to evaluate how well Muse does course assignments
**Instructor:** Professor Bear (Nik Bear Brown)

## What this is

One controlled experiment in two parts:

- **Part A — sampling mechanics (actual runs):** softmax normalization with
  max-subtraction, temperature controls, and seeded sampling, implemented in
  `sampling.py` and exercised for real in `run_experiment.py` (E1–E3).
- **Part B — prompt contracts (fixture evaluation):** a baseline (v0) and a
  revised (v1) prompt contract in `prompts/`; the validator in `contracts.py`
  is executed for real against 5 development and 5 held-out **hand-written
  fixtures** (`fixtures/`). No model was called; no API was contacted.
  Fixtures are labeled `FIXTURE` at every level.

## Contents

| Path | What it is |
|---|---|
| `README.md` | This file |
| `FRICTIONAL.md` | Honest process log (dated entries) |
| `CONCLUSION.md` | Reproducible conclusion, separated by claim type |
| `sampling.py` | Softmax, temperature, seeded sampling, failure checks |
| `contracts.py` | Contract validator returning `(ok, reason)`; pass-rate with breakdown; template renderer |
| `run_experiment.py` | Runs E1–E3 and the fixture evaluations; writes `results/` |
| `prompts/baseline.md` | Baseline prompt contract (v0, superseded) |
| `prompts/revised.md` | Revised prompt contract (v1) |
| `prompts/CHANGELOG.md` | What changed v0 → v1 and why |
| `evidence/evidence.json` | The 4-item evidence set fixtures may cite |
| `fixtures/dev_cases.json` | 5 development fixtures (labeled FIXTURE) |
| `fixtures/heldout_cases.json` | 5 held-out fixtures (labeled FIXTURE) |
| `tests/test_sampling.py` | 12 tests beyond the lesson reference |
| `tests/test_contracts.py` | 9 tests beyond the lesson reference |
| `results/` | Raw outputs: 5 JSON result files + `RUN_LOG.md` |

## Setup / run / test

Requires Python 3.8+; standard library only, no dependencies.

```bash
python3 run_experiment.py                 # runs the experiment, writes results/
python3 -m unittest discover -s tests -v  # 21 tests
```

Expected: `Ran 21 tests ... OK`, and `run_experiment.py` prints E1/E2/E3
summaries plus dev/held-out pass rates (0.40 / 0.40).

## Key finding

Cooling a confidently-wrong distribution concentrates mass on the wrong
answer (E2: P(wrong) = 1.0 at t=0.1); and a well-formed falsehood with a
real source ID passes every format check (fixtures d5/h5). Temperature
changes the distribution, not the truth; validation checks the format,
not the facts.

## Credits and assistance

- Starting points: `lessons/01-randomness-and-first-prompts/` and
  `lessons/02-prompt-contracts-and-evaluation/` (reference `main.py` and
  tests) in
  [info-7375-prompt-engineering-for-generative-ai](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai).
  Differences from the references are documented in each module's docstring.
- Lesson 02's Anthropics links (Anthropic prompt-engineering tutorial, prompt
  evaluations course) informed the contract's evidence-boundary rule.
- All code, fixtures, prompts, and docs were written by Muse (the agent);
  Professor Bear directed the pilot and supplied the assignment. No other
  assistance.
- License: same as the course repository (see repo LICENSE).

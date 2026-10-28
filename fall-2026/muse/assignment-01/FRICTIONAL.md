# FRICTIONAL.md — honest process log

Student: Muse (AI agent). Context: Professor Bear directed this pilot on
2026-10-10 to evaluate how well Muse does his course assignments. Everything
below describes what actually happened; nothing is reconstructed.

## 2026-10-10 — reading the assignment and lessons

- **Date and what I was working on:** Read the assignment brief, both lesson
  docs (01 randomness, 02 prompt contracts), both reference `main.py` files,
  both reference test files, and the frictional / github-submission /
  ai-policy / relative-quartile prerequisites, all via the course repo.
- **I tried / expected:** Expected the brief to require live Claude runs; the
  brief says "distinguish actual Claude runs from fixtures."
- **What happened:** I have no API access in this environment, and the
  lessons state default commands "neither read credentials nor make API
  requests." Fabricating a Claude transcript was never an option under the
  AI policy.
- **What I did:** Designed Part B as a *fixture evaluation*: the validator
  runs for real, the responses are hand-written fixtures labeled FIXTURE at
  every level (fixture files, result files, run log, README, conclusion).
  The measured claim is validator behavior, not model behavior, and the
  conclusion says so plainly.
- **What I understand now:** The honest version of this assignment for an
  offline agent is smaller than the brief's maximum — no live A/B test of
  v0 vs v1 prompts against a model. That gap is disclosed, not hidden.

## 2026-10-10 — writing sampling.py and contracts.py

- **I tried / expected:** Implement softmax/temperature/sampling and the
  contract validator from scratch, using the references as starting points.
- **What happened:** Straightforward. Softmax with max-subtraction and
  seeded `random.Random` are standard; I verified behavior by running rather
  than by staring. No real friction here.
- **Decisions I made (not instructed):**
  - `contracts.validate()` returns `(ok, reason)` instead of a bare bool,
    because the experiment needs to report *which* clause failed. `is_valid()`
    keeps the reference's boolean interface.
  - Added `total_variation()` to quantify empirical-vs-theory agreement; the
    reference only eyeballs counts.
  - `sample()` uses a local generator and never touches global random state;
    added a test proving it.
- **What Claude/another person contributed:** Nothing beyond the lesson
  references, which are credited in README.md. Professor Bear set the task
  and the destination folder.

## 2026-10-10 — fixtures and the v0 → v1 contract revision

- **I tried / expected:** Wrote the baseline (v0) contract first, then 5 dev
  fixtures including adversarial ones, expecting the validator design to
  need at least one fix.
- **What happened:** The validator passed all dev expectations on the first
  run, but writing the fixtures exposed that v0 ("JSON is preferred", "cite
  your sources") could not adjudicate fixtures d3 (extra field) and d4
  (unknown source). That drove the v0 → v1 changelog: exact key set, legal
  source-ID set, named failure reasons, evidence boundary.
- **Friction:** Deciding whether to make the validator *reject* the false-claim
  fixtures (d5/h5). I kept them passing deliberately: a format validator that
  rejected false claims would be claiming semantic judgment it does not have.
  The passing falsehood is the experiment's key demonstration, with the human
  evidence check named as the missing piece.

## 2026-10-10 — tests and experiment run

- **I tried:** 21 tests (12 sampling, 9 contracts), each with a docstring
  stating what it can falsify; then `run_experiment.py` end to end.
- **What happened:** All 21 passed first run (`Ran 21 tests ... OK`).
  Experiment output matched predictions recorded beforehand: E2 wrong-peak
  P(wrong) → 1.0 at t=0.1; E3 same-seed counts identical; dev and held-out
  format-pass rates both 0.40 with every per-case expectation met.
- **What I checked:** Re-ran the suite after writing results; spot-read
  `contract_heldout.json` to confirm failure reasons (`type`, `empty`,
  `source`) matched the fixture designs. Confirmed no secrets, keys, or
  tokens anywhere in the folder (nothing to leak: no credentials were used).
- **Still unresolved:** Whether a grader would want the live-model v0-vs-v1
  comparison; noted in CONCLUSION.md as not run. Next step if asked: run the
  same fixture sets as *prompts* through Claude Code and compare format-pass
  rates for real — that would be actual runs, properly labeled.

## Rubric self-check

- Attempts: specific (listed above). Friction: the fixture-vs-live-run
  decision and the d5 reject-or-pass call. Human/AI split: stated.
  Learning: the v0→v1 revision was driven by fixture evidence, which is the
  lesson's "change one feature, compare" loop in miniature. Traceable:
  entries tie to files, test output, and result JSON in this folder.

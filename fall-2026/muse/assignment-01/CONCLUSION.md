# Conclusion — what the experiment establishes, by claim type

Reproduce: `python3 run_experiment.py` (stdlib only), then
`python3 -m unittest discover -s tests`. Raw outputs in `results/`;
run metadata in `results/RUN_LOG.md`.

## 1. Repeatability — established for the mechanism, bounded for sampling

- **Bitwise repeatable:** `sample()` with the same seed returns identical
  counts (E3: `same_seed_identical: true`). Anyone re-running with seed 7
  gets the same numbers in `results/sampling_temps.json`.
- **Statistically stable, not identical:** across seeds 7–11 (n=5000,
  t=0.5), total-variation distance from theory ranged 0.0026–0.0102. The
  distribution is repeatable; individual count vectors are not, and the
  spread is quantified rather than hand-waved.
- **Not established:** anything about a live model's sampling, which I did
  not call.

## 2. Format validity — established for the validator on both splits

- Dev format-pass rate 0.40 (2/5), held-out 0.40 (2/5); every per-case
  expectation met on both splits (`all_expectations_met: true`).
- Failure reasons observed: `not-json`, `schema` (extra field), `type`
  (non-string answer), `empty` (blank answer, empty sources), `source`
  (unknown ID). Each names the exact contract clause violated.
- The v0 → v1 revision was driven by dev fixtures: v0 could not adjudicate
  d3/d4; v1 names both failures. Held-out confirms the validator was not
  overfit to dev wording — including h1, a meaning-preserving paraphrase of
  q1, which passes.

## 3. Source support — checked for membership, NOT for entailment

- The validator guarantees every cited ID is a key of the evidence map.
  Fixture d4 (hallucinated `e99`) fails; no fixture with an unknown source
  passes.
- It does **not** check whether the cited text supports the answer's claim.
  Fixtures d5 and h5 state falsehoods, cite real source IDs, and **pass**
  every check. This is the experiment's central boundary result: citation
  membership is mechanical; source *support* needs a human evidence check
  (or a separate entailment step, not built here).

## 4. Correctness — not established, and shown to be out of reach here

- E2: with logits [4, 1, 1] where index 0 is stipulated wrong, cooling from
  t=2.0 to t=0.1 moves P(wrong) from 0.69 to 1.0. Lower temperature
  concentrates on the argmax regardless of its truth — the lesson's
  "confidently wrong" practice-lab result, reproduced with numbers.
- A passing test suite (21/21) establishes the tested behavior only: the
  validator accepts well-formed falsehoods by design, and no fixture
  response came from a model, so nothing here measures model correctness.
- **What would establish more:** running the v0 and v1 contracts as live
  prompts against Claude on the dev/held-out questions and comparing
  format-pass rates for real — actual runs, properly labeled. Not done;
  no API access in this environment.

## One-sentence summary

Seeded sampling is repeatable and temperature sharpens but never corrects;
the revised contract makes format failures nameable and holds on held-out
fixtures; but neither sampling controls nor format validation can see truth —
the false-claim fixtures pass everything, and that boundary is the finding.

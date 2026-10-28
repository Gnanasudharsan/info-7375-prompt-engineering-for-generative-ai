# Prompt contract changelog

## v0 -> v1 (2026-10-10)

Designed while running the dev fixtures through `contracts.validate()`.

| # | Change | Why (evidence) |
|---|---|---|
| 1 | Added explicit `inputs`: `question` (non-empty string) and `evidence` (source_id -> text map) | v0 said "a question (free text)" with no evidence input; fixture d4 (hallucinated source ID `e99`) showed citations cannot be checked without a declared legal set |
| 2 | Output format changed from "JSON is preferred" to an exact schema: exactly keys `answer`/`sources`, no extra fields | Fixture d3 (extra `confidence` field) is neither valid nor invalid under v0; v1 names it `schema` failure |
| 3 | Added validation rules with named failure reasons (`not-json`, `not-object`, `schema`, `type`, `empty`, `source`) | Without named reasons, failures cannot be counted or compared; results files report per-reason breakdowns |
| 4 | Added evidence boundary: answer only from supplied evidence; say so when evidence is silent | v0's "cite your sources" permits answering from memory with real-looking citations |
| 5 | Documented the validator's limit: format validity only, not truth | Fixtures d5/h5 (false claim + valid source ID) pass v1 validation; recorded as the key demonstration rather than a bug |

## What v1 still does not do

- It does not check whether a cited source's *text* supports the answer's
  claim (needs a human evidence check or a separate entailment step).
- It was not A/B tested against a live model; the measured comparison is
  validator behavior on dev vs held-out fixtures, not model behavior under
  v0 vs v1 prompts. Stated plainly in CONCLUSION.md.

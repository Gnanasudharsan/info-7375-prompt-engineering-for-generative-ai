# Baseline prompt contract (v0)

Status: superseded by revised.md. Kept to show what changed.

## Inputs

- A question (free text).

## Task

Answer the question. Cite your sources.

## Output format

Respond with the answer and where you got it. JSON is preferred.

## Validation

None stated. The contract does not say what counts as a valid response,
which source IDs are legal, or what happens when the evidence is silent.

## Known weaknesses (found while drafting the revised contract)

1. "Cite your sources" does not define the legal source-ID set, so a
   citation cannot be checked mechanically.
2. "JSON is preferred" is not a contract: a plain-text answer is neither
   valid nor invalid, so failures have no name.
3. No evidence boundary: the model may answer from memory when the evidence
   is silent, and the contract cannot tell the difference.
4. No required fields, so a consumer cannot rely on any key being present.

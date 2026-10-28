# Revised prompt contract (v1)

## Inputs (explicit)

- `question`: a single non-empty string.
- `evidence`: a map from `source_id` (string) to source text (string).
  Only these source IDs may be cited.

## Task

Answer the question using **only** the supplied evidence. If the evidence
does not contain the answer, the answer field must say so explicitly
(e.g. "The evidence does not answer this.") rather than guessing.

## Output format (exact)

Respond with exactly one JSON object and nothing else:

```json
{"answer": "<non-empty string>", "sources": ["<source_id>", "..."]}
```

Rules:
- The object must contain exactly the keys `answer` and `sources`.
  No extra fields, no missing fields.
- `answer` must be a non-empty string (whitespace-only is empty).
- `sources` must be a non-empty list of strings.
- Every entry of `sources` must be a key of the supplied evidence map.

## Worked example

Question: "What does temperature change?"
Evidence: softmax: "Softmax converts ... Temperature changes the distribution, not the truth of the answer."

Response:

```json
{"answer": "Temperature changes the probability distribution over continuations.", "sources": ["softmax"]}
```

## Validation (mechanical)

A response passes if and only if it satisfies every rule above, checked by
`contracts.validate()`. Failure reasons are named: `not-json`,
`not-object`, `schema`, `type`, `empty`, `source`. The validator checks
format validity only; it does not check whether the answer is true or
whether the cited evidence actually supports it. Those need a human
evidence check (see CONCLUSION.md).

## Evidence boundary

Cite only supplied source IDs. Do not cite from memory. A well-formed
response with a false claim and a real source ID still passes validation;
that case is fixture d5/h5 and is the experiment's key demonstration.

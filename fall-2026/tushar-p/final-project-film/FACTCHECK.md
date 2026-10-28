# FACTCHECK — agent-proving-ground

A pitch for a project that does not exist yet. Every sentence about Agent Proving Ground’s features is in future tense, or sits inside a sentence framed with ‘will’ or ‘you’ll’ (B04, B08). The only things described as existing are this plan and my public OmniSQL-Postgres project (B10, B11). B08’s opening line describes the plan’s first step, not something that has run. No numbers from outside sources appear on screen.

## Claims

| # | Beat | Claim (on screen or spoken) | Status |
|---|---|---|---|
| C1 | B04 | "E2B is a service that runs AI-generated code in sandboxes" · card "Sandboxes — E2B" | ** Done ** |
| C2 | B04 | "Langfuse is a tool that records LLM traces and scores them" · card "Traces & scores — Langfuse" | ** Done ** |
| C3 | B07 | "kind, which is Kubernetes inside Docker" | kind's own expansion is "Kubernetes IN Docker"; author to confirm wording |
| C4 | B10 | "I've already built LLM evaluation and cloud infrastructure with Docker, Terraform, and AWS, in a public project you can check on GitHub." · Have column "LLM evaluation · Docker · Terraform · AWS" · "Shown in my public project: OmniSQL-Postgres", github.com/tushar-patel28/omnisql-postgres | Self-attested by the author (PROJECT-BRIEF.md §7); the public repo is linked in SOURCES.md |
| C5 | B11 | "today, this is a plan. None of the code exists yet." | True as of this build |
| C6 | B04 | Pass/fail "from tests run inside the sandbox, not from another model's opinion" | A design commitment (will), not a result |
| C7 | — | OmniSQL-Postgres execution accuracy, 23% base → 69% fine-tuned on a 200-question held-out test set (PROJECT-BRIEF.md §7; no longer spoken or shown in B10) | Done · brief only, not in film |
| C8 | B02, B06 | An official Go SDK exists for the Claude API (the planned agent loop "in Go with the Claude API") | Done |

## Honesty rules this reel follows

- **Mock-ups are labelled.** B00, B02, B05 and B08 show "Constructed — not
  built yet." in the top rail for the whole mock-up. Their contents (the chat
  bubble, the repo tree, the results table rows, the illustrative PASS line
  and step list) are illustrations of the plan, not output of running code.
- **No Claude responses are shown.** If one is added, it must be real and dated.
- **Tense.** Every sentence about Agent Proving Ground’s features is in future tense, or sits inside a sentence framed with ‘will’ or ‘you’ll’ (B04, B08). The only things described as existing are this plan and my public OmniSQL-Postgres project (B10, B11). B08’s opening line describes the plan’s first step, not something that has run.
- **No brand marks.** B09's wheel is a generic ship's wheel, not the
  Kubernetes logo; no product logos, colours or channel names appear.

<!--
Paste-ready Canvas assignment description. Student-facing, self-contained, all links
absolute, since students reading it in Canvas cannot resolve repo-relative paths. Posted to
Canvas by the instructor after review (2026-10-11). Keep the Canvas text and this file in sync.
-->

# Job-Search Agent 5 — The Gate, the Register, and the Supervised Run

**Points: 100 · Due: Sunday, December 13, 11:59 pm ET · Chapters 13–15 · Submit: one .zip through Canvas, plus a matching GitHub folder**

Read the [course AI policy](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/ai-policy.md) and watch [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) before beginning graded work.

## What this assignment is

Your agent produces a shortlist. A shortlist is a **proposal**, and somebody has to be accountable for acting on it. This layer puts the human gate, the rules about people and data, and the whole supervised run in one packet. It applies Chapters 13–15: evaluation and human approval gates (Chapter 13), governance and ethics (Chapter 14), and the supervised capstone (Chapter 15). You finish with a decision about your own agent: **would you rely on it for your own search tomorrow?**

Build on all four earlier assignments. You may also use the [Reallocation Engine](https://github.com/nikbearbrown/the-reallocation-engine) and Madison (the personal-brand tool, [Madison repository link: instructor to confirm]) for a verified résumé source and, if you choose, outreach drafts. If you use Madison for anything you write about yourself, every claim must trace to a verified fact about you.

**Use any programming language you like.** Name it, give exact commands, and list your toolchain.

## Step 1 — The gate: approval before anything is approved

Write `APPROVAL.md` **before** you build the gate. A yes must be a yes to something specific:

- **The proposal.** The exact shortlist content, the scope (which boards, which date), and an expiry.
- **The approval predicate.** What must be true for an approval to count, who is allowed to give it, and what makes it stop counting.
- **A fingerprint.** Bind the approval to a fingerprint of the exact proposal, so a changed shortlist cannot ride on an old yes. Show what happens when one posting changes.
- **Refusal, deferral, escalation.** The gate must be able to say no, not yet, and "this needs someone else."
- **An evaluation set that can embarrass the proposal.** A list of postings your agent **should skip** (a dead posting, a location or authorization mismatch, a posting that merely matches keywords). A healthy run skips **at least half** of what it evaluates; report your skip rate and what you found when you tried to fool your own agent.
- **Attention budget.** How many items one review can honestly cover, and what the agent does when the queue is longer.

## Step 2 — The register: rules about data and people

Write `REGISTER.md`, a team-style AI-use register for your agent, with these questions answered in plain words:

- **Data:** each source and file, labeled public, synthetic, or personal by the real policy, plus where it is stored, how long it is kept, and how it is deleted.
- **Owners:** who decides what the agent may do, and who can pause it.
- **Never:** what the agent may never do (apply, email, message, scrape beyond the allow-list, store another person's data).
- **People:** any person whose data touches the project, how they consented, and how someone affected could contest a result. Simulated people are not consent.
- **Deferral:** one case where the responsible output is "stop and ask a person."

## Step 3 — The supervised run and the decision

1. **A controlled failure.** Before the run, write down **one failure you expect** and the independent check that should catch it. Then **trigger it on purpose** and show the check catching it and your reviewed recovery. Described-only earns nothing: the failure must be triggered and observed.
2. **A claim-to-evidence graph.** For the claims in your final report ("it skipped 61%," "every shortlisted job is live"), trace each to the record that supports it. Mark every claim with no record as unsupported, and show one orphan claim you removed.
3. **The packet.** Pull your earlier work into the ten documents of Chapter 15: `brief`, `data-boundary`, `action-surface map`, `plan`, `gates`, `premortem`, `evidence`, `artifact`, `audit-note`, `transfer-reflection`. Reuse earlier assignments' work and link between them; a link is a claim, so open each target and confirm it says what the link says.
4. **The audit note and the Gap Account.** Predict what a reviewer will find, then have a reviewer (a classmate, a TA, or Claude) look. Judge each finding genuine or false-positive yourself. Then write what a reviewer **of that kind** could never reach.
5. **The decision.** Ship, narrow, defer, or stop, for your own use of this agent, with the reasons. State one task you will hand to an agent more readily after this work, and one you will keep practicing yourself.

## Step 4 — The sign-off

```text
Sign-off — Job-Search Agent 5
Checked:      which properties, by which of my own tests (name them)
How:          by hand / by a test I wrote before reading Claude's code /
              by recomputation / with Claude's help (say which parts)
Cleared by:   who cleared which gate
Not checked:  at least three real items
Not claiming: what this agent does not show
Signed or withheld: ____________ (name, date)
```

If your evidence does not support signing, **withholding is an honest result** and can earn full credit. A signature the record does not support cannot.

## What to submit

Canvas file name: `LastName_FirstName_INFO7375_JS5.zip`
GitHub folder: `fall-2026/first-name-last-initial/js5-gate-register-run/`

`README.md` (language, toolchain, exact commands, what ran) · `APPROVAL.md` and the gate code and tests · `REGISTER.md` · the controlled-failure record · the claim-to-evidence graph · the ten-document packet · the audit note with the Gap Account · the decision and transfer reflection · the sign-off · `SOURCES.md` · `FRICTIONAL.md`. Include the GitHub folder link and final commit hash in Canvas. Leave out caches, credentials, and your real résumé.

## Grading — 100 points

| Component | Points |
|---|---:|
| Implementation and explanation | 60 |
| [Frictional](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/frictional.md) (honest log) | 10 |
| [GitHub version posting](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/github-submission.md) matching Canvas | 10 |
| [Relative Quartile](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/relative-quartile.md) | 20 |
| **Total** | **100** |

**Implementation and explanation (60)** — the approval gate: bound to a fingerprint, expiry and scope, refusal and deferral, an evaluation set that can embarrass the proposal, a skip rate reported (14) · the register: data, owners, never-list, people and consent, a deferral case (10) · the controlled failure: predicted first, triggered, caught by an independent check, recovered with review (12) · the claim-to-evidence graph, the linked packet, and the audit note with a Gap Account (12) · the decision and transfer reflection, honest and evidence-based (6) · sign-off with real "Not checked" entries and who cleared which gate (6).

**Frictional (10)** — specific, honest accounts (3) · what you checked, changed, or learned, including what is unresolved (3) · what you accepted, modified, or rejected from Claude (2) · traceability to commits, prompts, and tests (2). An unsuccessful attempt can earn full credit.

**GitHub posting (10)** — source and documentation posted in your folder (4) · Canvas names the exact commit and run instructions (3) · what you submit matches what is posted (3).

**Relative Quartile (20)** — an overall quality score compared with the whole class: specificity, real improvement, demonstrated understanding, evidence, honesty about verification, and usability. Top 25%: 16–20 · Second 25%: 10–15 · Third 25%: 5–9 · Bottom 25%: 0–4. Meeting the criteria earns the other 80 points; it does not guarantee these 20.

## The honesty rule

Past tense only for what you ran and can show. Label every simulation and seeded run. Any Claude response you show is one you actually got, with the date. A packet with ten documents and no working links between them is ten islands.

## Privacy and boundaries

Your real résumé, contacts, tracker, and conversation transcripts stay on your machine; use a fictional persona on GitHub and on screen. Public endpoints only, with an allow-list, and respect each site's terms of use. **The agent never applies, emails, messages, or logs in, and no draft it writes is sent without you.**

## AI use and responsibility

Use Claude as much as you like and name what it contributed in `SOURCES.md`. You remain responsible for what you submit. The instructor or a TA may ask you to explain any part of it. Not being able to explain your own submission reduces points, and misrepresenting what you verified is an academic integrity matter.

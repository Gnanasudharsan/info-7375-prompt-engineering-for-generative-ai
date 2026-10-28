<!--
Paste-ready Canvas assignment description. Student-facing, self-contained, all links
absolute, since students reading it in Canvas cannot resolve repo-relative paths. Posted to
Canvas by the instructor after review (2026-10-11). Keep the Canvas text and this file in sync.
-->

# Job-Search Agent 4 — The Plan, the Evidence, and the Memory

**Points: 100 · Due: Tuesday, December 1, 11:59 pm ET · Chapters 10–12 · Submit: one .zip through Canvas, plus a matching GitHub folder**

Read the [course AI policy](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/ai-policy.md) and watch [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) before beginning graded work.

**Heads up:** fall break is November 25–29. Nothing is due then, but this assignment is due the day after classes resume, so plan to start before the break.

## What this assignment is

Your agent filters, scores, and offers its work as a tool. Now it must **plan before it acts, verify what it claims, and remember across days without fooling itself.** It applies Chapters 10–12: planning before acting (Chapter 10), tool use and verification (Chapter 11), and memory and multiple agents (Chapter 12).

Build on your earlier work, the [Reallocation Engine](https://github.com/nikbearbrown/the-reallocation-engine) (its liveness check and run recipes), or the instructor's [Lectern](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/tree/main/fall-2026/nik-bear-brown/lectern). Say what you started from.

**Use any programming language you like.** Name it, give exact commands, and list your toolchain.

## Step 1 — The gate: the reviewed plan, written before the run

A search run is a plan. Write `PLAN.md` **before** you run the agent, and have it reviewed (by a classmate, a TA, or Claude as a first reviewer: say which, and verify its criticisms yourself). It must contain:

- **The steps**, with each step's inputs, outputs, and permissions.
- **Dependencies**, as a graph with **no cycles**, and an answer to "is this order actually executable?" (acyclic is not the same as runnable).
- **Evidence on the edges:** what each step must hand to the next, as a condition a stranger could test. "Looks good" is not a condition.
- **Stop conditions and refusal paths:** when the agent stops, when it declines to continue, and what it reports. A failed check is not an identical retry.
- **Budgets** and who can change them.
- **One counterexample** your review found that changed the plan.

A later finding can reopen an earlier decision. If that happens during the assignment, **say so** and log what changed and why; do not edit the plan to look as if you knew.

## Step 2 — Build

1. **A tool evidence matrix (Chapter 11).** List every claim your agent makes about a posting that you would rely on: still live, new, location or remote status, what the employer says about work authorization or sponsorship, pay. For each claim write: which check supports it, **what failure that check catches**, and why it **fails differently** from the thing that produced the claim (a model's reading is not a check on itself; a lookup against the source is). **Run** at least three of the checks, including one that catches a planted error: a claim in the agent's summary whose number or fact differs from the trace (a "42 in the trace, 99 in the claim" case).
2. **Memory with a revision rule (Chapter 12).** Your seen-postings state is shared memory. Give it a version, reject a stale write, and show it. Run the agent on **two days** (or a second run against a saved earlier response, labeled as seeded) and show the **diff**. Show one case where *fresh is not true*: a posting your memory lists as live that is gone. Label every remembered fact with where it came from.
3. **Two workers, one notes file (Chapter 12).** Run two watchers (two boards, or two scoring schemes) that write to the same notes. Say honestly whether they are **independent**: two copies of the same model reading the same text are not two opinions. Write the **premortem**: predict one way the shared memory will fail, then **trigger that failure on purpose** and show what your design did. If the notes file accepts text from a posting, show that it is treated as data, never as instructions.

## Step 3 — The sign-off

```text
Sign-off — Job-Search Agent 4
Checked:      which properties, by which of my own tests (name them)
How:          by hand / by a test I wrote before reading Claude's code /
              by recomputation / with Claude's help (say which parts)
Not checked:  at least three real items
Not claiming: what this agent does not show
Signed or withheld: ____________ (name, date)
```

Add a **driver's seat** table: what Claude should do, what you should do, and why deciding which check counts as independent stays yours.

## What to submit

Canvas file name: `LastName_FirstName_INFO7375_JS4.zip`
GitHub folder: `fall-2026/first-name-last-initial/js4-plan-evidence-memory/`

`README.md` (language, toolchain, exact commands, what ran) · `PLAN.md` with the review · the code and tests · the tool evidence matrix and the output of the checks you ran · the state file's versions, the stale-write rejection, and the two-day diff · the premortem and the failure you triggered · the sign-off and driver's seat · `SOURCES.md` · `FRICTIONAL.md`. Include the GitHub folder link and final commit hash in Canvas. Leave out caches, credentials, and your real résumé.

## Grading — 100 points

| Component | Points |
|---|---:|
| Implementation and explanation | 60 |
| [Frictional](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/frictional.md) (honest log) | 10 |
| [GitHub version posting](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/github-submission.md) matching Canvas | 10 |
| [Relative Quartile](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/relative-quartile.md) | 20 |
| **Total** | **100** |

**Implementation and explanation (60)** — the plan: written before the run, an executable acyclic order, evidence on every edge, stop and refusal paths, a counterexample from review (14) · the tool evidence matrix: every consequential claim covered, checks that fail differently from the generator, at least three run, one catching a planted error (14) · memory: versioned, a stale write rejected, a two-day diff, fresh-is-not-true shown, sources labeled (14) · two workers and the premortem: independence discussed honestly, a failure predicted then triggered, injection treated as data (12) · sign-off with real "Not checked" entries, and the driver's seat (6).

**Frictional (10)** — specific, honest accounts (3) · what you checked, changed, or learned, including what is unresolved (3) · what you accepted, modified, or rejected from Claude (2) · traceability to commits, prompts, and tests (2). An unsuccessful attempt can earn full credit.

**GitHub posting (10)** — source and documentation posted in your folder (4) · Canvas names the exact commit and run instructions (3) · what you submit matches what is posted (3).

**Relative Quartile (20)** — an overall quality score compared with the whole class: specificity, real improvement, demonstrated understanding, evidence, honesty about verification, and usability. Top 25%: 16–20 · Second 25%: 10–15 · Third 25%: 5–9 · Bottom 25%: 0–4. Meeting the criteria earns the other 80 points; it does not guarantee these 20.

## The honesty rule

Past tense only for what you ran and can show. Label every simulation and seeded run. Any Claude response you show is one you actually got, with the date. A premortem written after the failure is not a premortem.

## Privacy and boundaries

Your real résumé, contacts, tracker, and conversation transcripts stay on your machine; use a fictional persona on GitHub and on screen. Public endpoints only, with an allow-list, and respect each site's terms of use. **The agent never applies, emails, messages, or logs in.**

## AI use and responsibility

Use Claude as much as you like and name what it contributed in `SOURCES.md`. You remain responsible for what you submit. The instructor or a TA may ask you to explain any part of it. Not being able to explain your own submission reduces points, and misrepresenting what you verified is an academic integrity matter.

<!--
Paste-ready Canvas assignment description. Student-facing, self-contained, all links
absolute, since students reading it in Canvas cannot resolve repo-relative paths. Posted to
Canvas by the instructor after review (2026-10-11). Keep the Canvas text and this file in sync.
-->

# Job-Search Agent 2 — The Loop, the Tools, and the Diff

**Points: 100 · Due: Tuesday, November 10, 11:59 pm ET · Chapters 4–6 · Submit: one .zip through Canvas, plus a matching GitHub folder**

Read the [course AI policy](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/ai-policy.md) and watch [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) before beginning graded work.

## What this assignment is

Your job-search agent from Job-Search Agent 1 watches one board. This layer makes it an **agent in earnest**: a bounded loop that watches **several boards**, uses tools under a **permission policy you wrote**, and changes only through code you **reviewed**. It applies Chapters 4–6: the agent loop and its exits (Chapter 4), tools and permissions (Chapter 5), and Claude Code with evidence-based diff review (Chapter 6).

Build on your Job-Search Agent 1 work. You may also start from the [Reallocation Engine](https://github.com/nikbearbrown/the-reallocation-engine) (its ATS providers and the `greenhouse-watch` skill) or the instructor's collector, [Lectern](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/tree/main/fall-2026/nik-bear-brown/lectern), which reads 18 boards across three applicant-tracking systems. Say what you started from.

**Use any programming language you like.** Name it, give exact commands, and list your toolchain. A TA must be able to run it from a fresh clone.

## Step 1 — The gate: write the exits and the policy first

Before Claude Code touches the code, write `GATE.md`:

- **Exits.** Every way your loop can end, and what each one reports: finished, incomplete, budget-exhausted, error. A loop that stops is not a loop that succeeded.
- **Budgets.** The maximum boards, requests, and seconds per run, and who may change them (a budget changes only by a new written decision).
- **Repeat rule.** What counts as "the same" action, and what the loop does about it.
- **Error policy.** What the loop does on a failed board: stop, retry (how many times, and why a retry here is sound), or escalate to you.
- **Permission policy.** Which hosts the agent may call, which folders it may write, and what it may never do (apply, email, message, log in).
- **Wrong versions.** Plausible-but-wrong implementations your tests must catch.

## Step 2 — Build

1. **The loop (Chapter 4).** Watch **at least three boards, at least two different applicant-tracking systems**. Keep a budget, an exit status, and a record of every observation. Include **one board that fails on purpose** (a bad name, an empty response, a timeout) and show your error policy handling it without inventing a value.
2. **A finished wrong answer.** Show a run that **ends cleanly and is wrong** (for example, an empty board reported as "no new jobs"). Show the independent check, not the agent's own report, that catches it.
3. **The permission policy, in code (Chapter 5).** Enforce the policy in the program, not in a prompt. Your boundary tests must include at least 10 cases: a host off the allow-list, a path that escapes your output folder (`..`, a prefix trick like `jobs-evil` beside `jobs`, a symlink), a read request versus a write request, and a write that needs your approval. For each, state what should happen *before* you run it.
4. **The review packet (Chapter 6).** Choose one non-trivial change you asked Claude Code to make. Show: the defect reproduced and your test written **before** the patch; the diff read as a change in behavior; whether the change stayed in scope; the commands you ran yourself; and your decision to **accept, revise, or reject**, with the evidence. Name one case your test would still miss.

## Step 3 — The sign-off

```text
Sign-off — Job-Search Agent 2
Checked:      which properties, by which of my own tests (name them)
How:          by hand / by a test I wrote before reading Claude's code /
              by recomputation / with Claude's help (say which parts)
Not checked:  at least three real items
Not claiming: what this agent does not show
Signed or withheld: ____________ (name, date)
```

Add a **driver's seat** table: for the loop and for the review, what Claude should do, what you should do, and why that part stays yours. Point to evidence in your transcript or diff.

## What to submit

Canvas file name: `LastName_FirstName_INFO7375_JS2.zip`
GitHub folder: `fall-2026/first-name-last-initial/js2-loop-tools-diff/`

`README.md` (language, toolchain, exact commands, what ran) · `GATE.md` · the code and tests · the **agent trace** of one real run, including the deliberate failure · the finished-wrong-answer demonstration · the permission policy and boundary-test table · the review packet · the sign-off and driver's seat · saved raw responses · `SOURCES.md` · `FRICTIONAL.md`. Include the GitHub folder link and final commit hash in Canvas. Leave out caches, credentials, and your real résumé.

## Grading — 100 points

| Component | Points |
|---|---:|
| Implementation and explanation | 60 |
| [Frictional](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/frictional.md) (honest log) | 10 |
| [GitHub version posting](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/github-submission.md) matching Canvas | 10 |
| [Relative Quartile](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/relative-quartile.md) | 20 |
| **Total** | **100** |

**Implementation and explanation (60)** — the loop: exits, budgets, repeat rule, three boards across two systems (12) · the trace, with the deliberate failure handled and a finished-wrong-answer caught by an independent check (12) · the permission policy enforced in code with at least 10 predicted boundary cases (14) · the review packet: reproduce first, test first, scope, decision on evidence (14) · sign-off with real "Not checked" entries, and the driver's seat (8).

**Frictional (10)** — specific, honest accounts (3) · what you checked, changed, or learned, including what is unresolved (3) · what you accepted, modified, or rejected from Claude (2) · traceability to commits, prompts, and tests (2). An unsuccessful attempt can earn full credit.

**GitHub posting (10)** — source and documentation posted in your folder (4) · Canvas names the exact commit and run instructions (3) · what you submit matches what is posted (3).

**Relative Quartile (20)** — an overall quality score compared with the whole class: specificity, real improvement, demonstrated understanding, evidence, honesty about verification, and usability. Top 25%: 16–20 · Second 25%: 10–15 · Third 25%: 5–9 · Bottom 25%: 0–4. Meeting the criteria earns the other 80 points; it does not guarantee these 20.

## The honesty rule

Past tense only for what you ran and can show. Label every simulation and seeded run. Any Claude response you show is one you actually got, with the date. Do not weaken a test to get a green report.

## Privacy and boundaries

Your real résumé, contacts, tracker, and conversation transcripts stay on your machine; use a fictional persona on GitHub and on screen. Public endpoints only, with an allow-list, and respect each site's terms of use. **The agent never applies, emails, messages, or logs in.**

## AI use and responsibility

Use Claude Code as much as you like and name what it contributed in `SOURCES.md`. You remain responsible for what you submit. The instructor or a TA may ask you to explain any part of it. Not being able to explain your own submission reduces points, and misrepresenting what you verified is an academic integrity matter.

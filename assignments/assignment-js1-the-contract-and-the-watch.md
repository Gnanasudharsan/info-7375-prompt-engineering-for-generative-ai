<!--
Paste-ready Canvas assignment description. Student-facing, self-contained, all links
absolute, since students reading it in Canvas cannot resolve repo-relative paths. Posted to
Canvas by the instructor after review (2026-10-11). Keep the Canvas text and this file in sync.
-->

# Job-Search Agent 1 — The Contract and the Watch

**Points: 100 · Due: Saturday, October 31, 11:59 pm ET · Chapters 1–3 · Submit: one .zip through Canvas, plus a matching GitHub folder**

Read the [course AI policy](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/ai-policy.md) and watch [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) before beginning graded work.

## What this assignment is

From here to the final project, every assignment builds **one thing in layers: your own job-search agent.** An agent that watches job boards, decides which new postings are worth your time, and tells you why. You decide where it goes, you check what comes back, and your name goes on it. Claude is very good at writing the code and the drafts. It cannot tell you whether a job is worth a day of your life.

This first layer is the smallest honest slice: **one board, one résumé, new postings only, every verdict justified.** It applies Chapters 1–3: what a model's answer is and is not (Chapter 1), the contract an answer must meet (Chapter 2), and how much autonomy the agent needs (Chapter 3).

**Use any programming language you like.** Name it, give the exact commands, and list your toolchain. A TA must be able to run your work from a fresh clone; anything we cannot run is unverified.

## Step 1 — The gate: write the contract before you build

Before you ask Claude to write anything, write `CONTRACT.md`. It must say:

- **In:** what the agent takes in (a board name, a résumé as JSON), and what it needs.
- **Out:** what it returns for each new posting: a verdict (relevant or not) and a justification that names the résumé fields and the posting fields behind it.
- **Refuses:** what it will not do. At minimum: fetch any host not on your allow-list, show a real résumé on screen or on GitHub, or present a model's judgment as a fact.
- **The rule:** how a posting is judged relevant, written so a TA could predict your verdict on a posting by hand.
- **Wrong versions:** two plausible-but-wrong implementations your tests must catch (for example, labels paired with the wrong postings, or a justification that cites nothing).
- **What a failure looks like:** one dated sentence, written *before* you run anything.

Then have Claude Code implement against your contract. Run your tests on what it returns, yourself.

## Step 2 — The watch

Your agent fetches **one public job board** (the public JSON endpoints of Greenhouse, Ashby, Lever, or SmartRecruiters are fine; name the host and keep an allow-list). It saves the raw response as evidence, remembers the posting ids it has seen, and reports only postings **new since the last run**. The first run is a baseline that reports none as new. Show two runs with a real change between them: a second calendar day, or a second run against a saved earlier response, clearly labeled as seeded.

The résumé is JSON. Use a **fictional persona**, not yourself, on GitHub and on screen. The [Reallocation Engine](https://github.com/nikbearbrown/the-reallocation-engine) ships four in `search/examples/`; you may invent one with `@example.com` addresses and 555 phone numbers. Your real résumé stays on your own machine.

## Step 3 — Two judges, labeled

For each new posting, produce two verdicts: one from your written rule (a **record**: anyone can recompute it) and one from Claude under a **prompt contract** (a **judgment**: label it as one). The Claude step needs a fixed output format and a validator that rejects anything else.

## Step 4 — The three Chapter artifacts, applied to your agent

1. **Sampling report (Chapter 1).** Pick 5 postings. Ask Claude your contract about each one in **fresh conversations, at least 4 times per posting**. Record every verdict. Report how much they vary and what you can and cannot conclude. Repeating the same verdict proves repeatability, not correctness: compare against your own hand label.
2. **Prompt experiment (Chapter 2).** Hand-label **20 real postings** (10 development, 10 held-out) using a labeling rule you wrote first. Run a baseline prompt contract and **one** revision that changes **one thing** on the development set, then on the held-out set you did not look at until the end. Report pass rates and be honest about how little ten cases can show.
3. **Action-surface comparison (Chapter 3).** Do the same task three ways: paste one posting into a chat; give Claude a file to read; let an agent fetch and write its own state file. For each, list what it can read, write, and send, what authority it needs, and what could go wrong. Choose the **least autonomy that suffices** and defend it.

## Step 5 — The sign-off

End your README with a sign-off you could put your name to. Claude can draft the words in seconds; the part that matters is what it can't know: what you did not test.

```text
Sign-off — Job-Search Agent 1
Checked:      which properties, by which of my own tests (name them)
How:          by hand / by a test I wrote before reading Claude's code /
              by recomputation / with Claude's help (say which parts)
Not checked:  at least three real items
Not claiming: what this agent does not show
Signed or withheld: ____________ (name, date)
```

Add a short **driver's seat** table: for this task, what Claude should do, what you should do, and why that part stays yours. Point to the transcript line or edit that shows the split really happened.

## What to submit

Canvas file name: `LastName_FirstName_INFO7375_JS1.zip`
GitHub folder: `fall-2026/first-name-last-initial/js1-contract-and-watch/`

`README.md` (language, toolchain, exact commands, what ran) · `CONTRACT.md` · the code and tests · saved raw responses and the state file from your two runs · the sampling report · the prompt experiment (prompts, labels, results) · the action-surface comparison · the sign-off and driver's seat · `SOURCES.md` (what you used, what you wrote, what Claude contributed) · `FRICTIONAL.md`. Include the GitHub folder link and your final commit hash in Canvas. Leave out caches, credentials, and your real résumé.

## Grading — 100 points

| Component | Points |
|---|---:|
| Implementation and explanation | 60 |
| [Frictional](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/frictional.md) (honest log) | 10 |
| [GitHub version posting](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/github-submission.md) matching Canvas | 10 |
| [Relative Quartile](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/relative-quartile.md) | 20 |
| **Total** | **100** |

**Implementation and explanation (60)** — the contract, written first, with testable wrong versions and applied as written (12) · the watch: allow-listed fetch, raw response saved, new-since-last by id, baseline then a real second run, validated persona résumé (12) · sampling report: repeated verdicts, spread, an honest conclusion (10) · prompt experiment: one change at a time, development versus held-out, honest limits (12) · action-surface comparison and the autonomy choice (8) · sign-off with real "Not checked" entries, and the driver's seat (6).

**Frictional (10)** — specific, honest accounts of what you tried and what happened (3) · what you checked, changed, or learned, including what is unresolved (3) · what you accepted, modified, or rejected from Claude (2) · traceability to commits, prompts, and tests (2). An unsuccessful attempt can earn full credit. Invented struggle earns nothing.

**GitHub posting (10)** — source and documentation actually posted in your folder (4) · Canvas names the exact commit and run instructions (3) · what you submit matches what is posted (3).

**Relative Quartile (20)** — an overall quality score compared with the whole class: specificity, real improvement, demonstrated understanding, evidence, honesty about verification, and usability. Meeting the criteria earns the other 80 points; it does not guarantee these 20. Top 25%: 16–20 · Second 25%: 10–15 · Third 25%: 5–9 · Bottom 25%: 0–4. The instructor and TAs review everyone's work before assigning it.

## The honesty rule

Past tense only for what you ran and can show. Label every simulation, seeded run, and constructed example. Any Claude response you show is one you actually got, with the date. No invented postings, results, or metrics.

## Privacy and boundaries

Your real résumé, contacts, application tracker, and conversation transcripts stay on your machine. Use public endpoints only, with a host allow-list. **The agent never applies, never emails or messages anyone, and never logs in anywhere.** Respect each site's terms of use.

## AI use and responsibility

Use Claude as much as you like. Name what it contributed in `SOURCES.md`. You remain responsible for what you submit. The instructor or a TA may ask you to explain any part of it, including why any posting was judged relevant. Not being able to explain your own submission reduces points, and misrepresenting what you verified is an academic integrity matter.

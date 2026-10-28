# PROJECT-BRIEF — SponsorScout

Akshit Verma · INFO 7375 Final Project Pitch · drafted 2026-10-12, revised 2026-10-14
Target role: **Data Analyst / Data Engineer**

> Tense rule: past tense = exists and can be shown today. "Will" = proposed.

## 1. What is it?

**SponsorScout** will be a Claude Code workflow that tells an international student looking for data
jobs, company by company, whether to **apply, network, check by hand, or skip**,
and cites the record behind every verdict. When done it will be a **repository**:
a Reallocation Engine recipe, a Python prototype, offline tests, a hand-checked
evaluation log, and a one-page run report a reader can trace row by row.

**Stack:** Python 3 (standard library only); Node 20 to call the engine's
existing `role-scorer.mjs`; Claude Code as the runtime that follows the recipe.
Data: the 80 Days to Stay sponsorship CSV, SEC Form D samples, and the public
Greenhouse, Lever and Ashby job-board APIs. All of it is public, and the job seeker is fictional.

## 2. Why would anyone care?

It will save an F-1 student targeting data roles the hours spent applying to
sponsors that have no entry-level data opening today. Instead of dropping those
sponsors, it puts them on a short **networking** list (the prototype already
does this: run-2, NETWORK 1). Alternatives:

- **The Reallocation Engine's own scorer** (Claude Code ran it at my request,
  2026-10-03, `runs/engine-baseline`): a strong sponsor with no live posting
  gets a closed liveness gate, scores 0.000, and is **Skipped**. Mine keeps that
  company and says *network here*.
- **MyVisaJobs** (I looked at it on 2026-10-07): it lists H-1B sponsors and
  their past job counts. It doesn't take a sponsor with nothing open today
  and tell you to network there instead. That routing is what mine adds.

## 3. Who opens it, and what do they do?

I'm targeting Data Analyst and Data Engineer roles, so the reader is a **hiring
manager for a data team** (and the end user, a job seeker). In the first sixty
seconds they will run one offline command, open the report, pick one NETWORK
row, and trace its numbers back to the source CSV row and board response.

## 4. What does it prove about me?

Source grounding: every value is labelled `record` or `your-input`. Verification gates: boards that
couldn't be resolved never reach the scorer, because the scorer treats a missing
liveness value as 1.0. An agent loop with human gates: Claude Code follows the
recipe (a prompt contract) and stops for my sign-off. Evaluation: still to come.
Evidence today: 25 offline tests, two logged runs, a false positive that was
caught and pinned by a test, and my gate sign-offs. Evidence to come: the evaluation log.

## 5. In, out, first

- **In:** the four verdicts, each with its source record; the repository above.
- **Out:** it will never apply, email, or contact anyone, and it will not score
  résumé fit (no real résumé is used).
- **First piece:** a **board resolver** for the 107 companies that currently have
  no mapped job board. You'll know it ran because board coverage is reported
  as a number (today 16/123), with each new mapping saved with its raw API
  response and a test.

## 6. What could sink it?

**Board coverage.** Many of the 107 unmapped companies may have no public job
board, and I don't know yet how many. If most don't, most verdicts stay
MANUAL-CHECK. What I will do: use only the three public APIs, never scrape, and
report coverage as a number even if it's low.

I don't know yet whether **recent funding predicts hiring**. It is a labelled
hypothesis. How I will find out: re-check NETWORK targets' boards after 14 days
and log whether a posting appeared.

## 7. Why this project?

I picked it because I'm job hunting too, and I wanted a smarter, more efficient
strategy than sending 100–200 applications a day.
It's a mix. **What I already have is judgment, not code.** Claude Code wrote most
of the Assignment 1 prototype under my direction. I set its rules (for example,
I made recent funding a requirement for NETWORK and recorded why, in Assignment 1
FRICTIONAL, 2026-10-03), and I signed its human gates G1 and G3.
**New to me:** building a hand-labelled evaluation set and measuring verdict
accuracy; resolving job boards at scale.

---

### Exists today
- Recipe v0.1.1 + card, prototype, fixtures (prototype written mostly by Claude Code under my direction). PR #44 opened 2026-10-04, **open, not merged**.
- 25 offline tests: passed, re-run 2026-10-12.
- run-1 (2026-10-03): false APPLY-TAILOR on contract student-worker postings, found by Claude on first read of the output; fix decided by me; a v0.1.1 test pins it.
- run-2 (2026-10-03, 16 boards): 123 candidates → APPLY-TAILOR 2 · NETWORK 1 · MANUAL-CHECK 107 · SKIP 13.

### Will exist
- Board resolver and a coverage number above 16/123.
- Hand-labelled evaluation set and an evaluation log of wrong verdicts.
- 14-day board re-check of NETWORK targets.
- A README with a sixty-second verification path.
- A write-up of where Claude's output was wrong and how it was caught.

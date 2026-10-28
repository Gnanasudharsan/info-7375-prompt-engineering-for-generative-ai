# PROJECT-BRIEF — Sponsor Triage (working title)

Siddi Kommuri · INFO 7375 Fall 2026 · Final project pitch · 2026-10-14

> **Status of this draft:** Claude Code drafted it from my repositories and recipe, and from my answers on 2026-10-14. Every sentence about my own reasons and skills (sections 4 and 7) is mine to confirm or rewrite before I submit. Past tense = exists and can be shown. "Will" = proposed.

## 1. What is it?

**Sponsor Triage is an agent that checks each job posting three ways for an F-1 student looking for data roles: has this company sponsored a *data* role, is the posting still live, and is there time left on my OPT.**

When it is done it will be a **GitHub repository**: a Node.js command-line agent, its tests, a hand-labelled evaluation set, a run log in which every value carries its source (file and line), and a Markdown report for the person deciding. It will grow from my Reallocation Engine recipe `data-role-sponsor-match` (DRAFT, 2026-10-03).

## 2. Why would anyone care?

It saves an F-1 data student hours they would otherwise spend on postings that look promising and are not. Two alternatives I compared against, both in the course's Reallocation Engine repo:

- **Company-wide approval counts** (the 80 Days CSV's `Total Approvals`, which the repo's sponsorship scorer uses). Databricks has 1,640 H-1B approvals (CSV line 7249), but its five recorded top sponsored titles are software and solutions roles. None is a data role. Sponsor Triage tiers a company by its **titles**, not its count.
- **The repo's page-level liveness check** (`npm run ats:liveness`). On 2026-10-03 the recipe gave it a Klaviyo job id that does not exist, on purpose (`.../jobs/1000000001`). The page check said `active`, and Greenhouse's job API returned `404`. Sponsor Triage lets the API result win.

I have not compared it against commercial sponsor-lookup sites. If I do, I will log what I find in FRICTIONAL.md and will not claim a difference I have not checked.

## 3. Who opens it, and what do they do in the first sixty seconds?

- **Target role:** data engineer / analytics engineer (early career).
- **Readers:** (a) a hiring manager or engineer on a data team, and (b) the end user, an F-1 student like me, deciding where this week's hours go.
- **First sixty seconds:** clone the repo, run one offline command, and read the report: **Apply / Consider / Skip / Unresolved** per posting, with every number traced to a file and line. No API key and no network needed for the worked run.

## 4. What does it prove about me?

The skills, tied to the course:

- **Agent loops:** observe → decide → act → record → stop, with a tool-call budget and a stop condition that is not "the model said it was done".
- **Verification:** two independent liveness checks, with a stated rule for when they disagree.
- **Source grounding:** every value in the log is `{value, source}`.
- **Evaluation:** a held-out set and planted failure cases.
- **Prompt contracts:** only if Claude earns a place (see section 5).

A reviewer could fairly conclude that I can build a small, bounded agent and say what it cannot know. They could *not* conclude that it predicts sponsorship.

The evidence I will produce:

- About 40 hand-labelled public postings, with a held-out split I do not look at until the end.
- At least five deliberate failure cases (fake job id, blank sponsorship row, ambiguous company name, keyword drift, OPT already past).
- Test output and the run log.

## 5. What is in, what is out, what comes first?

- **In:** the loop; tools for the CSV lookup, the Greenhouse job API and the OPT timeline; a permission policy in code (read the CSV, call only `boards-api.greenhouse.io`, write only to its output folder); and a **human gate** where I approve, refuse or defer every Apply and every Unresolved after seeing its evidence rows.
- **Out, deliberately:**
  - It will **not** say whether a particular opening will be sponsored this year. The data is company-level and historical.
  - It will never apply to a job or message anyone.
- **Not decided yet:** whether Claude helps decide if a job title is a data role. I will find out by scoring Claude against my hand labels and the recipe's title patterns on the same postings, and keep whichever is more accurate.
- **First piece:** the loop, offline, over the seven postings of the 2026-10-03 worked run (two of them constructed test cases).
- **How you would know it ran:** it exits 0, stays under its budget, and reaches the same decisions as the current recipe: 1 Apply, 2 Consider, 1 Skip, 3 Unresolved.

## 6. What could sink it?

**Thin data.**

- Of the 1,552 companies in the CSV with H-1B approvals, 862 (55.5%) list just one sponsored title, and 1,510 list five or fewer (`evidence/csv-title-coverage-2026-10-14.txt`).
- In the 2026-10-03 run, of the five *real* postings, two came out Unresolved (DraftKings: blank sponsorship columns; Absci: two matching company rows) and two more only reached the "Likely" tier (Databricks, Toast).
- If most real postings land there, the agent is honest but not useful.

**What I would do about it:**

- Measure the Unresolved rate on real postings first (Update 1).
- If it is too high, go back to the public data the CSV was built from: the Department of Labor's LCA disclosure data, which has a `JOB_TITLE` field on every H-1B labor condition application (DOL OFLC record layout). An LCA is not an approved petition, so I will label it as weaker evidence than an approval.

## 7. Why this project?

It is my own problem. I am on an F-1 visa looking for data roles, so I will notice when the agent is wrong. It is a **mix**:

- **Already have** (with evidence):
  - Python data work and a RAG app for NBA game analysis (Streamlit + Pinecone + Gemini, with a Hit@K retrieval evaluation): `github.com/kommurisi/Advances-in-Data-Science---Final-Portfolio-Project---NBA-Rag-App`, December 2025.
  - Small CI and model-provider fixes on a team project's resume parser (5 commits, March 2026).
- **New to me:**
  - agent loops with budgets and permission policies;
  - held-out evaluation;
  - owning agent code I did not write.
- **Honest starting point:** in the recipe this builds on, Claude wrote all the code and tests, and I accepted them without changes (recipe SOURCES.md). In the final project I will write the contract and tests before Claude implements anything, and I will hand-check CSV rows myself.

## Exists today (can be shown)

- Recipe `data-role-sponsor-match` (DRAFT): code, 12 offline tests, a worked run (2026-10-03), and four named failure modes. Fork `kommurisi/the-reallocation-engine`, branch `contrib/2026fa-kommurisi-data-role-sponsor-match`, PR nikbearbrown/the-reallocation-engine#31.
- The 12 tests passed again on 2026-10-14 (`evidence/recipe-tests-2026-10-14.txt`).
- The worked-run report with the numbers used above (`evidence/worked-run-report-2026-10-03.md`).
- This film and its gate reports.

## Will exist (proposed)

- The agent loop with a budget and stop conditions.
- The enforced tool permission policy.
- The human-gate approval file.
- The ~40-posting labelled evaluation set with a held-out split.
- At least five deliberate failure cases.
- The Claude-vs-patterns title comparison.
- The Unresolved-rate measurement, and possibly the DOL LCA source.
- The README that survives a stranger run.

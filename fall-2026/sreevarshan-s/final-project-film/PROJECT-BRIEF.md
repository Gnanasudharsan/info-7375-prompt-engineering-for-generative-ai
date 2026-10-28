# Record Beats AI: A Sponsorship Job Finder That Checks Its Own Answers

**Sreevarshan Sathiyamurthy** · INFO 7375 · Target role: **ML / AI engineer** · Stack: Python (standard library, `unittest`), the course's Reallocation Engine, Claude and Claude Code. Built on my Assignment 2 recipe (early October 2026).

## 1. What is it?
A command-line pipeline that shows an international new graduate on OPT which companies have actually sponsored people at their level, and refuses to call a job "open" unless a record backs it. When done, it will be a repository (a recipe and Python prototype in the Reallocation Engine) with one run command, tests, a readable `report.md`, and an evaluation log.

## 2. Why would anyone care?
It will save a new graduate the manual cross-checking of sponsorship history against live postings. I looked at **Ellis** and **F1Jobs** for Amgen on Oct 11, 2026. Both show past filing counts; F1Jobs itself says its counts are not job openings. On the pages I looked at, neither checks whether a specific posting is live or filters by occupation code and level. Mine will do both.

## 3. Who opens it, and what do they do in the first 60 seconds?
A hiring manager or engineer for an ML / AI engineer role. They will open the README, run one command on a fictional persona, and read `report.md`: warnings first, then the funnel, then a conflict row where an AI search called a posting open and the record said the page was dead (HTTP 404).

## 4. What does it prove about me?
That I can build an LLM-assisted pipeline that stays honest: every value is labelled `record`, `model-judgment` or `your-input`, gates are hard stops, and when an AI claim and a record disagree, the record wins (rule R4). Evidence: commit history, 58 offline tests, a break-attempts log, the worked run. It does **not** prove model training; no model is trained here.

## 5. What is in, what is out, what comes first?
**Out:** no auto-applying, no scraping behind logins, no real personal data (personas are fictional). **First:** an offline evaluation log comparing AI posting claims with liveness records. You'll know it ran when one command prints an agree / conflict table and the tests pass in a clean environment.

## 6. What could sink it?
Entity resolution. `HUMAN INC` had 1382 approvals, but I couldn't confirm it was HUMAN Security. Wrong matches make every later decision wrong. I'll label ambiguous matches `model-judgment`, require a human to confirm them, and measure errors on a small hand-checked sample.

## 7. Why this project?
Mostly new learning. Sponsorship is a real problem for students on OPT, and I wanted to answer it with records, not guesses. **New to me:** hard-stop gates, labelled values, and catching an AI mistake against a record. **What I did versus Claude:** Claude and Claude Code drafted most of the code and documents and proposed R4; I accepted R4, agreed to hold the recipe at DRAFT, chose to skip human posting checks in that run, and checked the AMGEN and HUMAN counts by hand in my own Terminal. **Skills I already had:** I'm not claiming any I can't back with evidence.

## Exists today (checked against the repo, Oct 10–11, 2026)
- Prototype runs end to end on fictional persona `meera-krishnan`
- Funnel: 30,369 → 114 → 64 entry-eligible / 50 senior-only companies
- Rules R4 (`6202dc8`) and R5 (`806ce8a`); 58 offline tests pass
- AMGEN conflict: AI said open, liveness check returned HTTP 404
- AMGEN INC 1882.0 and HUMAN INC 1382.0 checked by hand (re-run Oct 11)
- Break-attempts log; recipe at DRAFT (5 TODOs); PR #32 open
- **Not done:** no human posting check, nothing reached Apply, CI never ran

## Will exist
- Offline evaluation log of AI claims vs. records (first piece)
- Human posting-check step to clear gate G4
- Entity-resolution check with human confirmation
- README a stranger can follow in five minutes

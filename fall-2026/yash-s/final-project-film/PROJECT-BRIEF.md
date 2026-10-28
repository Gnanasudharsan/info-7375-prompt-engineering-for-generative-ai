# Project Brief — actions-docs-qa

**Yash Saraf · INFO 7375 · Final Project Pitch · 2026-10-11**
**Target role:** AI Developer / DevOps / Cloud Engineer · **Stack:** Python, BM25 search, a small local model via Ollama, pytest. No paid API.

Nothing in this project exists yet; everything about it below is a plan.

## 1. What is it?
A command-line tool that will answer GitHub Actions questions from GitHub's own docs, quoting the exact passage each answer came from, or saying "not found." Done, it will be a public GitHub repo: the tool, a script that fetches one pinned version of the docs, about 50 test questions, an evaluation script, `REPORT.md` and `FAILURES.md`.

## 2. Why would anyone care?
It is for an engineer fixing a workflow who needs an answer and its source. On 2026-10-11 I tried three questions from my own workflows (screenshots in `evidence/`, answers checked against the docs):
- **docs.github.com search:** keyword results listed the answer page for 1 of 3. Its built-in Ask Copilot matched the docs on all 3 but listed sources for only 1.
- **Claude desktop app (Sonnet 5.5):** matched the docs on all 3, with no sources.

Mine is not meant to give better answers. It will add the exact sentence each answer came from, checked word for word against the docs; a published score on a fixed test set; and it runs free on my laptop (the docs search says GitHub keeps the questions asked there).

## 3. Who opens it, and what do they do?
A hiring manager or engineer on a DevOps, platform or AI tooling team. In the first minute they read the results table, then open one test question and compare the expected passage with the tool's answer. No install needed.

## 4. What does it prove about me?
Source grounding (answers only from a retrieved passage), verification (a script checks every quote), a prompt contract (fixed JSON: answer, quote, source, or "not found"), and evaluation (about 50 questions, 10 the docs don't cover, repeated runs). A reviewer could conclude I can build a grounded Q&A tool and measure it honestly, not that it beats Copilot or Claude, works on other docs, or shows agent loops.

## 5. In, out, first
- **In:** the Actions docs only, pinned to one version; command line; about 50 questions.
- **Out:** it never answers from the model's memory. No quote, no answer. No web interface.
- **First piece:** search alone, no model: my 3 questions plus 2 more, checking whether the right passage lands in the top 3. A dated results file in `evals/results/` will show it ran.

## 6. What could sink it?
**Risk:** search misses the right passage. The docs' keyword search missed 2 of my 3, and mine starts with keyword search too. If plain-English questions keep missing, I will add a free local embedding model and compare.
**Limitations:** a small model (my Mac has 8 GB RAM) may reword quotes; the check will catch it and the report will count it. Pinned docs go stale. And some answers live in shared snippet files, not the page files (true for my first question), so the fetch script must fill those in.

## 7. Why this project?
A mix. **Existing:** GitHub Actions CI/CD and Python/pytest, shown in my public repos marketpulse-service (June 2025) and, from CSYE 6225 coursework, webapp and tf-aws-infra (Jan–Apr 2025). **New:** search over documents, local models with Ollama, source-grounded test sets, and measuring answers. I picked it because it interests me, and because it is new to me, which is why I want to explore it further.

## Exists today
- My three public repos above (past work, not part of this project)
- Six dated screenshots of the alternatives (`evidence/`, 2026-10-11)
- This brief; GitHub's public Actions docs (third-party, CC BY 4.0)

## Will exist
- Docs fetch script (pinned), keyword search, local-model answer step with its JSON contract
- Quote checker with tests; about 50 test questions; evaluation script, `REPORT.md`, `FAILURES.md`

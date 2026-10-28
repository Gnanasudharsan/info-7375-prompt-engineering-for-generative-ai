# PROJECT-BRIEF — Seeded Faults (working title)

**Author:** Atharva C · **Course:** INFO 7375 · **Drafted:** 2026-10-09
**Target role:** Data Engineer / BI Engineer (entry level)
**Stack (planned):** Python, DuckDB, dbt-core with dbt-duckdb, Claude Code, public NYC TLC trip data

> Status as of 2026-10-09: this is a pitch. No project code exists yet. Every "will" below is a plan.

## 1. What is it?
Seeded Faults will be a Claude Code workflow that writes data-quality tests for a table, then measures those tests by planting known faults in a copy of the data and counting which faults the tests catch.

When it is done, it will be a **public GitHub repository** containing: the workflow (prompt contract + scripts), a fault-injection script, a small dbt project on DuckDB, an evaluation log, and a written failure analysis.

## 2. Why would anyone care?
A data engineer who adds tests to a new table usually has no way to know whether those tests would catch the problems that actually happen. AI-generated tests make this worse: they look complete and pass on clean data.

Alternatives I checked on 2026-10-09 (details in FRICTIONAL.md):
- **Great Expectations, GX Core 1.24.0 (free library).** I wrote each check by hand. The "Create an Expectation" docs page describes choosing and configuring checks yourself, and I found no automatic suggestion feature in the installed library. A not-null check passed on clean data and caught all 50 nulls I planted. *Not checked: GX Cloud.*
- **dbt tests (dbt-core 1.12.5) and dbt-expectations (metaplane fork, v0.10.10).** Same result with tests I wrote in YAML. dbt-expectations adds about 60 more test types, which you still write by hand; its README says nothing about generating tests or measuring what they would miss.

In each tool, a test only checks what the person thought to write, and nothing reported which faults the tests would miss. The difference I am aiming for: Seeded Faults will **score** a test suite against a fixed catalogue of planted faults and report what was caught and what was missed. It saves a data engineer from trusting a test suite that has never been shown to fail.

## 3. Who opens it, and what do they do?
- **Reader:** a data engineering hiring manager or a senior data engineer reviewing my GitHub.
- **First 60 seconds:** they open the README and see one table — each planted fault, whether the generated tests caught it, and why not when they did not. One command (`make eval`) reproduces that table.

## 4. What does it prove about me?
- **Prompt contracts:** the test-generation prompt will have a written contract (inputs, output format, what it must not do).
- **Verification:** generated tests are not trusted; they are run against clean and faulted data.
- **Evaluation:** a fixed fault catalogue and a catch-rate / false-alarm log, rerunnable.
- **Data engineering:** dbt, SQL, data-quality testing, dimensional thinking about keys and grain.

A reviewer could fairly conclude: "This person checks whether their checks work." The evidence will be the evaluation log and the failure analysis in the repo — not a claim in the film.

## 5. In, out, first
- **In:** one public table (a NYC TLC trip sample), one fault catalogue (~15–20 fault types), generated dbt tests, an evaluation report.
- **Out (deliberately):** it will **not** repair data, run in production, or connect to any live warehouse.
- **First piece to run:** the fault-injection script on the trip sample, plus one generated test. You will know it ran because `make eval` prints a caught/missed table and writes it to `eval/results.md`.

## 6. What could sink it?
**Risk:** Claude may write tests that are tuned to the clean sample (pass everything, catch little), or tests so strict they flag clean data. Either would make the catch rate meaningless.
**What I will do:** measure false alarms on clean data as well as catches on faulted data; keep the fault catalogue fixed before generating any tests so I cannot tune it to the output; log every miss by fault type in the failure analysis.

## 7. Why this project?
A mix of showing off and learning.
- **Skills I already have:** SQL, relational modelling, data pipelines. *Evidence (public repos, checked 2026-10-09):*
  - [github.com/Arc-211/DMDD_FinalProject](https://github.com/Arc-211/DMDD_FinalProject) — Crime Rate Management System, an Oracle schema with PL/SQL, permissions, transactions and a `testing.sql` script. Solo work.
  - [github.com/Arc-211/Chinook_ADF](https://github.com/Arc-211/Chinook_ADF) — an Azure Data Factory pipeline (pipeline, dataflow, dataset and linked-service JSON).
- **Skills that are new to me:** prompt contracts, LLM evaluation, agent workflows in Claude Code, fault injection / mutation-style testing, dbt on DuckDB.

---

### Exists today (2026-10-13)
- This brief, the beat sheet, and the submission files in this folder.
- The rendered pitch film (`seeded-faults-pitch.mp4`, 3:36) and the toolkit's gate reports (`gate-reports/`).
- One hand-run planted-fault test (50 nulls in one column, caught by a hand-written check in Great Expectations and in dbt). Scripts and logs in `evidence/2026-10-09-first-planted-fault/`.

### Will exist
- The Seeded Faults repository: a fault-injection script covering the full fault catalogue, the dbt project, the prompt contract, an evaluation log, and the failure analysis.

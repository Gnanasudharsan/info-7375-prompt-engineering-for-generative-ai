# Cite-the-Line — Project Brief

**Author:** Pavan Jayant Majji · **Course:** INFO7375 · **Target role:** Backend Software Engineer · **Status:** proposed, nothing built yet

## 1. What is it?
A command-line tool that reads logs from a failing backend service and proposes a root cause, quoting the exact log lines that support it, or saying plainly when the evidence isn't enough. When done, a public GitHub repository will contain: a small FastAPI + Postgres service run with Docker Compose that can be broken on purpose; around ten incident scenarios, each with captured logs and a labelled true cause; the triage CLI, which sends logs to Claude Code in headless mode and returns a JSON diagnosis with cited line numbers; a checker that verifies every cited line exists; and an evaluation report covering correct, wrong, and correctly declined diagnoses.

## 2. Why would anyone care?
Commercial agents such as Datadog's Bits AI SRE already propose root causes from telemetry, but they run inside a paid platform and their accuracy is reported by the vendor. This project will be small and open: plain log files, a public set of incidents with known causes, a checker that rejects any diagnosis citing lines that don't exist, and a published record of where it was wrong. It will let an engineer see, on evidence they can re-check, how far an LLM's root-cause claims can be trusted. It is not a competitor to Datadog; it is a transparent test bench for the same idea.

## 3. Who opens it, and what do they do?
A hiring manager or senior engineer hiring for backend roles. In the first sixty seconds they will open the README, see a results table at the top, then click one incident to see the raw log, the diagnosis with cited lines, and the checker's verdict side by side. No setup needed; every diagnosis will be saved and dated. With Docker and Claude Code access, one command will reproduce a run.

## 4. What does it prove about me?
That I can write a prompt contract with a checkable output, ground model claims in source lines, verify them mechanically, and evaluate them against known answers across three runs per incident. A reviewer could fairly conclude that I treat LLM output as something to test, not trust. Evidence: the contract, checker verdicts, saved diagnoses, and results table. The harness is an evaluation loop with validate-and-retry, not an autonomous agent. A reviewer should **not** conclude it works on real production logs or matches commercial tools; it will be tested only on incidents I created.

## 5. In, out, first
**In:** one service, ~10 scenarios, CLI, checker, 3 runs each, results and failure write-up. **Out (deliberately):** it will never take action — no restarts, rollbacks, or changes. Also out: real production logs, real-time monitoring, multi-service systems. **First:** one "database slowed" incident end to end — start the service, slow Postgres, capture logs, run one diagnosis, check it. Proof it ran: the dated log, raw diagnosis, and checker verdict committed with the commands that produced them.

## 6. What could sink it?
The test set may be too easy because I write every scenario and know every answer. I will include scenarios where the loudest error is not the real cause, and scenarios with no clear answer. Plan B, if results look suspiciously good: score a simple keyword-matching script on the same incidents; if it does about as well, I will report the test set as too easy rather than present the score as success.

## 7. Why this project?
In development work, the habit is often to paste an error into a chatbot and act on the answer without checking it against the actual logs, which can send debugging in the wrong direction. This project is a mix. **Existing skills:** FastAPI, Postgres, and Docker, from my software engineering experience and from my coursework in Network Structures & Cloud Computing, Object-Oriented Design, Software Quality, and Web Design & User Experience. **New skills:** fault injection, prompt contracts with checkable outputs, mechanical verification of model claims, LLM evaluation against known answers, and running Claude Code from a script.

## Exists today (as of 2026-10-13)
- This brief and the project decisions in it
- This pitch film (3:04), its script, beat sheet, and quality-gate reports
- My reading of the Datadog Bits AI SRE documentation (read 2026-10-09)

## Will exist
- FastAPI + Postgres service with fault injection (Docker Compose)
- ~10 incident scenarios with labelled causes
- Prompt contract and triage CLI (Claude Code headless)
- Citation checker and evaluation harness (3 runs per incident)
- Results table, saved diagnoses, and failure write-up
- Keyword baseline, only if needed (plan B)

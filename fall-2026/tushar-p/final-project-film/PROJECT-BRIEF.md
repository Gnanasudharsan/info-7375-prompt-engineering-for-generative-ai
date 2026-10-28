# PROJECT-BRIEF — Agent Proving Ground (working title)

Tushar Patel · INFO7375 Final Project · Target role: early-career Software Engineer, AI agent infrastructure / platform

## 1. What is it?
Agent Proving Ground will run an AI coding agent on small tasks inside an isolated Kubernetes sandbox, record every step it takes, and check whether it actually did the task.
When done, it will be a public GitHub repository. It will hold a Go harness, a suite of 10–20 synthetic coding tasks with automatic pass/fail checks, saved traces of every run, an evaluation log, and a failure analysis.

## 2. Why would anyone care?
An agent saying "done" is not the same as the task being done. This project will give an engineer one local command that answers three questions: did the agent's change pass the checks, did it stay inside the sandbox, and did the latest prompt or model change make the results worse?
Alternatives I looked at: E2B provides sandboxes for running AI-generated code, and Langfuse records LLM traces and scores. Each covers one piece. Mine will join sandbox, trace, and verification into one small, self-hostable loop. Pass/fail will come from checks that run inside the same sandbox, such as tests and file state, not from another model's opinion.

## 3. Who opens it, and what do they do?
The reader is a hiring manager or engineer on an agent-infrastructure or platform team. In the first sixty seconds they will read the README, run one command, and see a results table (task, pass/fail, steps, reason). They can then open one trace to see exactly what the agent did.

## 4. What does it prove about me?
- **Agent loops:** I will write the loop myself in Go, using Anthropic's official Go SDK with tool use.
- **Prompt contracts:** each task will give the agent a fixed contract (goal, allowed tools, required output).
- **Verification:** results will come from deterministic checks, not from the agent's own report.
- **Evaluation:** a repeatable suite, with pass rates compared across runs.

A reviewer could fairly conclude that I can build and evaluate an agent system end to end. It will be built for one laptop, not for production traffic, so they should not conclude that I have run agents in production. The evidence will be the repository, its tests, the saved traces, the evaluation log, and the failure analysis.

## 5. What is in, what is out, what comes first?
- **In:** a Go codebase, local sandboxing on `kind` (Kubernetes in Docker), one agent, synthetic tasks, traces stored as JSON files, and an evaluation report.
- **Out:** it will not be a hosted or multi-user service. It will run locally only. Cloud deployment (EKS) and OpenTelemetry can be added in the future; they are not part of this course project.
- **First:** one task, run once in one container, producing one trace file and one PASS/FAIL line. Someone will know it ran because the command prints the result and the trace file exists, with its steps listed.

## 6. What could sink it?
Learning Go and Kubernetes at the same time could eat my time, so the evaluation part never gets built. To prevent that, I will build the harness and checks against plain Docker first, then move them onto `kind`, with a fixed cutoff date for the switch. If the switch misses that date, I will submit the Docker version and log the reason in FRICTIONAL.md.

## 7. Why this project?
It is a mix, by choice.
- **Skills I already have**, shown in a public project a reviewer can check:
  - **OmniSQL-Postgres:** https://github.com/tushar-patel28/omnisql-postgres (live demo: https://omnisql-postgres.vercel.app).
  - **LLM evaluation:** I fine-tuned OmniSQL-7B for PostgreSQL and built the evaluation that measured it. Execution accuracy went from 23.0% to 69.0% on a 200-pair held-out test set, with the same decoding settings for both. The README's iteration log shows each change, including fixing the evaluator itself.
  - **Docker, Terraform, AWS:** the repo includes its Dockerfile, docker-compose, and Terraform infrastructure.
- **Skills that are new to me:** Go, Kubernetes, sandbox isolation (network and credential limits), and trace design.

I want to work on the infrastructure that AI agents run on, and building this is how I will learn it.

## Exists today
- This brief.
- My public OmniSQL-Postgres project (section 7), as evidence of existing skills.
- Nothing of Agent Proving Ground's code yet.

## Will exist
- Harness and agent loop.
- Sandbox on `kind`.
- Task suite with checks.
- Traces.
- Evaluation log.
- Failure analysis.
- README with a one-command demo.

Stack: Go, Anthropic Go SDK (Claude API), Docker, kind/kubectl. The coding tasks the agent solves will be small Python repos checked with pytest. Data: synthetic tasks I write myself; no private data.

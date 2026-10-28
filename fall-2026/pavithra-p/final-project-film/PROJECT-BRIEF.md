# PROJECT-BRIEF — DryRun

**Pavithra Prasad** · INFO 7375 · Final Project Pitch · 2026-10-13
**Target role:** software engineer, backend / platform (new grad, December 2026)
**Stack (all free):** Python, Docker + Docker SDK, pytest, Claude Code headless (`claude -p`); later Ollama, SQLite, GitHub Actions.

> Nothing of DryRun is built yet. Everything below is what I **will** build, except the two lists at the end.

## 1. What is it?

DryRun will test an AI's terminal command on a throwaway copy of your folder, before it touches your real files, and tell you whether it did only what you asked. When done, it will be a public GitHub repository: a Python command-line tool (`dryrun`), a Docker sandbox runner with a before/after file diff, a trap-folder benchmark and an evaluation report.

## 2. Why would anyone care?

AI assistants and coding agents suggest and run shell commands, and reading a command is not the same as knowing what it will do. **Real example (2026-10-11):** Claude gave me `find logs -type f -name "*.log" -mtime +7 -delete` for "delete .log files older than 7 days". Its suggested preview did not match a 7½-day-old file on my Mac (`evidence/`).

**Alternatives (checked 2026-10-11):** reading the command and hoping; `try`, which previews a command's file changes on Linux but does not check them against the request; InterCode-Bash and NL2SH, research benchmarks that score AI commands offline. **What DryRun adds:** it compares the real changes with **your request** and **the AI's own prediction**, then allows, warns or blocks.

## 3. Who opens it, and what do they do in the first sixty seconds?

A hiring manager or engineer for backend and platform roles. They read the README's one-line summary, run `dryrun demo`, see a command flagged with the files it would have changed, then open `REPORT.md`.

## 4. What does it prove about me?

| Course skill | How DryRun will show it | Evidence |
|---|---|---|
| Prompt contracts | The AI must return JSON: the command plus its predicted effect | Contract file, rejected replies |
| Verification | Decisions come from the real diff, never the AI's explanation | `tests/` with planted changes |
| Agent loops | A blocked command's diff goes back to the AI, up to 3 tries | Run logs |
| Evaluation | Tasks with correct end states, across trap folders, Claude vs a local model | Results JSON, `REPORT.md`, failure gallery |

**A reviewer could fairly conclude:** I can build a checking layer around an AI and measure how often it is wrong. **Not:** that DryRun makes commands safe.

## 5. What is in, what is out, what comes first?

- **In:** one shell command's effect on files and folders, Linux behaviour.
- **Out:** network calls, outside services, databases, remote servers.
- **First piece:** `dryrun run "<command>" --dir <folder>` copies the folder into a locked container, runs the command and lists what was created, changed and deleted. **You'll know it ran** when its self-test finds exactly the changes it planted.

## 6. What could sink it?

- **Knowing what the user meant.** A diff shows what changed, not whether it was intended. I will start with file tasks whose correct result can be checked, and report "can't tell" instead of guessing.
- **Mac vs Linux tools** (e.g. `sed -i`). Version 1 will target Linux behaviour.

## 7. Why this project?

**A mix, mostly new learning.** My portfolio is mostly web apps; I want one project that shows I can build a system around an AI and check its output.

- **Already have:** Python and unit tests (software engineer internship at MyEdMaster: Python, Flask); Python with offline tests in this course ([PR #33](https://github.com/nikbearbrown/the-reallocation-engine/pull/33), 32 passing tests); Docker, AWS and Terraform (cloud web application project at Northeastern).
- **New to me:** sandboxing commands in containers, a snapshot-and-diff engine, Claude Code hooks and agent loops, evaluation design.

## Exists today

- This brief, the beat sheet and the pitch film (resubmitted cut, October 2026, 3:53; first cut 2026-10-13).
- One real Claude reply (screenshot, 2026-10-11) and my test of its preview (`evidence/`, re-run 2026-10-13).
- Evidence for the skills I already have: PR #33 in the Reallocation Engine, 32 passing tests (re-run 2026-10-23, `evidence/`).
- No DryRun code, tests, results or users.

## Will exist

- The `dryrun` tool, the Docker sandbox runner and the file diff, with their own tests
- The trap-folder generator and a task set with correct end states
- The Claude Code hook and the retry loop
- The evaluation (Claude vs a local model), `REPORT.md` and a failure gallery

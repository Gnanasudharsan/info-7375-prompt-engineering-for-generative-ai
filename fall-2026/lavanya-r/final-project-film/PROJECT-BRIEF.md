# PROJECT-BRIEF — README Checker

**Lavanya R · INFO 7375 · Final project pitch · Written 2026-10-13**
**Working title:** README Checker: "Does the README actually work?"
**Target role:** Software Engineer
**Stack (planned):** Python, Claude, Docker

Nothing in the README Checker has been built yet. Everything described below as the tool is planned work, written as "will."

## 1. What is it?
A command-line tool that will run a project's README setup steps, one at a time, inside a throwaway Docker container, and report which step broke and why.

When it is done, it will be a **public GitHub repository** containing:
- the Python CLI tool
- about 10 small sample repos with problems I plant on purpose
- an evaluation log that scores how many of those problems the tool catches

## 2. Why would anyone care?
It will save an engineer joining a project the time spent finding out, by trial and error, which README setup step is wrong.

**Alternatives I looked at:**
- **Following the README by hand.** On 2026-10-13 I followed my own `webapp` README exactly as written, in a fresh clone, and did not get a working setup:
  - Step 1 uses a placeholder, `git clone <repository-url>`.
  - Step 3 (`yarn sequelize db:migrate`) failed: `Cannot find config/config.json`. The README never mentions that file.
  - Step 4 needs DBeaver, a GUI app, so I skipped it.
  - Step 5 uses a placeholder, `docker start <container-name>`, and never says how to create the container.
  - Step 6 (`node app.js`) started the server, but the database connection failed ("The server does not support SSL connections"). The code connects to AWS RDS, which the README does not mention. The README's expected output ("Database synced!") never appeared.
  - Step 7 (`GET /healthz`) returned `503 Service Unavailable`.

  It took about 5 minutes to hit these problems, and I wrote that README myself.
- **Following a well-kept open-source README by hand.** On 2026-10-13 I followed the "Running Locally" steps of [`heroku/node-js-getting-started`](https://github.com/heroku/node-js-getting-started) the same way. **It worked**: `npm start` printed `Listening on 5006`, and `GET /` returned `200 OK`. It had small gaps:
  - It lists the Heroku CLI as required. I don't have it, and the app still ran locally.
  - `npm install` warned that the project wants npm 12, while I have 10.9. The README doesn't mention this.
  - The clone URL in the README (`nodejs-getting-started`) doesn't match the repo name. GitHub redirected it.

  Doing it by hand only finds a problem when a person happens to hit it, and it takes a person's time for every README.
- **CI pipelines (GitHub Actions).** My `webapp` repo has a CI workflow (`ci.yml`) that installs Node 18 and starts PostgreSQL itself, using steps I wrote separately from the README. So CI can pass while the README is wrong. CI tests the code. It does not test the instructions a new person follows.

**What mine will do that these don't:** follow the README exactly as written, in a clean container, and point to the exact README line that failed, alongside the real error output.

## 3. Who opens it, and what do they do?
- **Reader:** a hiring manager or engineer reviewing me for a Software Engineer role.
- **In the first 60 seconds:** they open the repo, run one command against an included sample repo, and get a pass/fail report for each step. Each failure cites a README line and shows the real error text.

## 4. What does it prove about me?
| Course skill | How the project will show it | Evidence a reviewer can check |
|---|---|---|
| Agent loop | Run a step, read the output, decide the next step | Run logs in the repo |
| Verification | Every pass/fail is backed by real command output, not the model's opinion | Saved outputs beside each report |
| Evaluation | About 10 sample repos with planted problems and a known answer key, **plus working READMEs**, so I also measure false alarms | Evaluation log with a catch score and a false-alarm count |
| Source grounding | Every finding cites the README line it came from | Line numbers in each report |
| Prompt contracts | A fixed output format the model must return, which the code checks | Contract file plus tests that reject bad output |

**A reviewer could fairly conclude:** I can build a small, honest, testable developer tool and measure where it fails.
**They could not conclude:** that it works on every README, or on any project that needs secrets or paid services.

## 5. In, out, first
- **In:** public or sample repos, setup steps in shell commands, Docker sandbox, pass/fail report, evaluation log.
- **Out (deliberately):** it will **not fix** the README. It only reports problems.
- **First piece to run:** take one sample README, run its steps in a Docker container, and write a pass/fail line for each step to `report.md`. **You will know it ran** because `report.md` will exist and will show the real exit code for each step.

## 6. What could sink it?
- **Risk:** a README can contain any command, so running unknown commands is unsafe.
  **What I will do:** every step runs only inside a disposable container with no secrets and no access to my files. The container is deleted after each run.
- **Second risk: false alarms.** My Heroku test worked despite small warnings. A tool that flags every warning as "broken" would be useless, so the report will separate **pass**, **warning** and **fail**, and the evaluation will count false alarms on working READMEs.
- **Limitation:** some READMEs are too vague to run ("set up your database"). The tool will mark those steps **"unclear"** instead of guessing. How common this is, I don't know yet. The evaluation set will tell me.

## 7. Why this project?
It is a **mix** of skills I already have and skills I'm learning.
- **Already have (with proof):**
  - **CI/CD:** GitHub Actions workflows in my public repo <https://github.com/LavanyaRajesh24/webapp> (`ci.yml`, `packer-build.yml`, `packer-ci.yml`).
  - **Cloud (AWS/GCP):** the same repo, which uses Packer machine images and CloudWatch.
  - **Docker:** I have used it, but I have no public proof yet. This project will be the first.
- **New to me:** building an AI agent loop, writing an evaluation test set, source grounding, and prompt contracts.

---

## Exists today (2026-10-13)
- This brief and the pitch film, made with Brutalist show-tell.
- My public `webapp` repo, the CI/CD and Cloud evidence above (last updated 2025-04-19).
- My two manual README tests (2026-10-13): my `webapp` README (did not work) and `heroku/node-js-getting-started` (worked, with small warnings).

## Will exist
- The README Checker CLI tool (Python + Claude + Docker)
- The Docker sandbox runner
- About 10 sample repos with planted problems, plus an answer key
- The prompt contract and its tests
- The evaluation log with a catch score
- A write-up of where Claude was wrong and how I caught it

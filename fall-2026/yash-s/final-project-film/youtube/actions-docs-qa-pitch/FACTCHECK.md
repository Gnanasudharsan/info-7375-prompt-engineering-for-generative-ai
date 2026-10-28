# FACTCHECK — actions-docs-qa-pitch

Every factual claim in the narration, checked against the source named. Claims about the
project itself are plans, spoken in the future tense; they are EXEMPT from fact-checking
because nothing has been built (honesty rule), and the film says so on screen.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | BIDEA | Nothing in the project is built yet | PASS | `PROJECT-BRIEF.md` "Exists today" list; no project code exists | — |
| 2 | B04 | The alternatives were tried on October 11 | PASS | `evidence/*.png` file times and menu-bar clocks, 2026-10-11 13:56–14:16 | — |
| 3 | B04 | Three questions came from my own workflows | PASS | marketpulse-service `ci.yml` (secrets on `pull_request`); `dockerbuild.yml` and webapp `packerbuild.yml` (`closed` + `merged == true`); marketpulse `ci.yml` service containers and webapp's "Wait for MySQL" step | — |
| 4 | B04, B12 | The docs keyword search listed the answer page for only 1 of 3 (missed 2) | PASS | `evidence/github-docs-1.png`: top 4 lacks "Using secrets in GitHub Actions"; `-2.png`: top 4 unrelated; `-3.png`: #1 is "Creating PostgreSQL service containers" | Said "listed", since only the top 4 shown were checked |
| 5 | B05 | Ask Copilot is built into that search | PASS | `evidence/github-docs-*.png` ("Ask Copilot" panel under the results) | — |
| 6 | B05 | Copilot and the Claude desktop app both matched the docs on all three | PASS | Answers compared with the docs pages fetched 2026-10-11: "With the exception of GITHUB_TOKEN, secrets are not passed to the runner when a workflow is triggered from a forked repository."; "To run a workflow when a pull request merges, use the pull_request closed event type along with a conditional that checks the merged value of the event."; PostgreSQL example `--health-cmd pg_isready` | — |
| 7 | B05 | Copilot listed its sources for only one | PASS | `github-docs-1.png` shows "Relevant docs" and "Copilot Sources"; `-2` and `-3` show none | — |
| 8 | B05 | Claude cited none | PASS | `evidence/claude-1/2/3.png`: no links or sources; model shown as Sonnet 5.5 | — |
| 9 | B07 | The docs search notes that GitHub keeps the questions asked there | PASS | Footer in every docs screenshot: "GitHub will retain questions and answers generated in the Docs search function." | — |
| 10 | B13 | GitHub Actions runs in my three public repos from 2025 | PASS | github.com/iyashsaraf/marketpulse-service (`ci.yml`, `dockerbuild.yml`; commits June 2025); CSYE6225CloudSpring2k25/webapp (`webapp.yml`, `packerbuild.yml`, `packerstatus.yml`; Jan–Apr 2025); CSYE6225CloudSpring2k25/tf-aws-infra (`terraform.yml`; Feb–Apr 2025) | — |
| 11 | B13 | Search, local models and measuring answers are new to me | EXEMPT | Yash's own statement (PROJECT-BRIEF.md §7) | — |
| 12 | B14 | Six dated screenshots exist | PASS | `evidence/` holds six PNGs | — |
| 13 | B00–B03, B06–B11 | What the tool will do, contain and prove | EXEMPT | Plans, future tense, labelled "constructed sketch · not built yet" on screen | — |
| 14 | B01, B07 | The model will run free on my laptop | EXEMPT | Plan: Ollama and open-weight models are free to run locally; laptop has 8 GB RAM (brief §6) | — |
| 15 | B09 | About fifty questions, ten not covered by the docs | EXEMPT | Plan (brief §4) | — |

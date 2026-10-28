# SOURCES — Final Project Pitch Film

Yash Saraf · INFO 7375 · 2026-10-11

## What I used

| Tool or source | Version / date | Licence | Used for |
|---|---|---|---|
| Brutalist toolkit (`github.com/nikbearbrown/brutalist.art`) | local checkout, commit `b21f625` | no licence file in the checkout | show-tell skill, iso drawing kit, render pipeline and quality gates |
| Manim Community | 0.19.2 | MIT | every body beat and the outro, drawn in code (`scenes.py`) |
| Remotion | 4.x (toolkit's `runtime/remotion`) | Remotion License (free for individuals) | the opening hesitant-writer beat (`BrutalistHesitantWriter`) |
| Kokoro TTS via `kokoro-onnx` | 0.6.1, voice `am_onyx`, run locally | upstream licences not re-checked here | narration: a synthetic voice reading my script |
| ffmpeg | Homebrew build | LGPL/GPL | audio padding, frame checks |
| EB Garamond font | installed locally | SIL Open Font License | all on-screen type |
| GitHub Docs source (`github.com/github/docs`) | checked 2026-10-11 | content CC BY 4.0, code MIT | checking the three answers; no docs text is shown in the film |

Docs pages used to check the answers (fetched 2026-10-11):
- "Using secrets in GitHub Actions": *"With the exception of GITHUB_TOKEN, secrets are not passed to the runner when a workflow is triggered from a forked repository."*
- "Events that trigger workflows": *"To run a workflow when a pull request merges, use the pull_request closed event type along with a conditional that checks the merged value of the event."*
- "Creating PostgreSQL service containers": the example's `--health-cmd pg_isready` health-check options.

## What I made

- The project choice (document Q&A over the GitHub Actions docs) and the three test questions, taken from patterns in my own workflows.
- Six screenshots in `evidence/`, captured 2026-10-11 between 13:56 and 14:16:
  - `github-docs-1/2/3.png`: docs.github.com search and its built-in Ask Copilot answer, one question each, cropped to the search panel.
  - `claude-1/2/3.png`: the Claude desktop app (Sonnet 5.5), no docs attached, a fresh chat per question.
- My answers in `PROJECT-BRIEF.md` about my target role, my reasons for picking the project, my existing skills and my Mac's RAM.
- Review and approval of each step, and every entry in `FRICTIONAL.md`.
- My public repos referenced as evidence (2025): `iyashsaraf/marketpulse-service`, `CSYE6225CloudSpring2k25/webapp`, `CSYE6225CloudSpring2k25/tf-aws-infra`.

## What Claude contributed

**Claude Code (Claude Opus 5.5, in VS Code), 2026-10-10 to 2026-10-11:**
- Summarised the assignment and proposed project options; I chose document Q&A after rejecting ideas that needed a paid API.
- Read my public repos and summarised what they show.
- Drafted `PROJECT-BRIEF.md` from my answers; I approved each change.
- Confirmed the GitHub Docs licence and checked the three AI answers against the docs pages above.
- Drafted the narration and beat plan (`make_sheet.py` → `beat_sheet.json`) from the brief, wrote every drawing (`scenes.py`), wrote `FACTCHECK.md`, `SHOTLIST.md` and `PROMPTS.md`, ran the Brutalist pipeline and its gates, and drafted this file, `README.md` and `BUILD-PROMPT.md`.
- Formatted my notes into `FRICTIONAL.md` (grammar and layout only); the predictions and reflections in it are mine.

**Claude desktop app (Sonnet 5.5), 2026-10-11:** the three answers I compared against are real responses I got, shown in the film as drawings and kept as screenshots in `evidence/`.

## Third-party material in the film

| Material | Where | Status |
|---|---|---|
| docs.github.com search results and Ask Copilot answers | B04, B05 | redrawn as labelled constructed sketches from my own screenshots; the screenshots are GitHub's pages, captured by me as evidence |
| Claude desktop app answers | B05 | redrawn as a labelled constructed sketch from my own screenshots |
| GitHub, Copilot, Claude names | B04, B05 | named only as the alternatives I tested; no logos or branding are reproduced |

Not used: no instructor portraits, persona, voice name or credit line; no generated images or video; no paid service; no API key.

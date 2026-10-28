# SOURCES — BiteCheck pitch film

## What I used
| Item | What it is | Licence / terms | When |
|---|---|---|---|
| [brutalist.art](https://github.com/nikbearbrown/brutalist.art) @ `b21f625` | Film toolkit: show-tell drawing kit (pasted into `scenes.py` minus the portrait helpers), Kokoro audio script, `art run` / `art final`, QC gates | course toolkit (see its repo) | cloned 2026-10-12 |
| Kokoro-82M (`kokoro-onnx`, voice `am_michael`) | Free local text-to-speech for the narration | Apache-2.0 | 2026-10-12 |
| Manim Community v0.18.1 | Renders every drawing | MIT | 2026-10-12 |
| EB Garamond, Menlo | On-screen type | SIL OFL (EB Garamond); Menlo ships with macOS | — |
| ffmpeg | Encoding / frame sampling | LGPL/GPL | — |
| [Schemathesis docs](https://schemathesis.readthedocs.io/en/stable/) | What Schemathesis does (B06) | read only | read 2026-10-12 |
| [StrykerJS docs](https://stryker-mutator.io/docs/) | What Stryker does (B06) | read only | read 2026-10-12 |
| StrykerJS 8.7.1 (`@stryker-mutator/core`) + TypeScript 5.5.4 | **Ran** on a scratch copy of the InstaLoan rules files, 2026-10-13 (`evidence/stryker/`) | Apache-2.0 | 2026-10-13 |
| Whisper-tiny (`mlx-community/whisper-tiny`, via `mlx-whisper` 0.4.2) | Pronunciation check of the narration (`evidence/pronunciation_check.txt`) | MIT | 2026-10-13 |
| [Postman Postbot page](https://getpostman.com/product/postbot/) plus hands-on reviews ([NashTech](https://blog.nashtechglobal.com/postbot-in-postman/), [DEV](https://dev.to/lengochoangminh/simplify-api-testing-with-postbot-postmans-ai-assistant-56b)) | What Postbot does (B06) | read only | read 2026-10-12 |

## What I made or decided
- 2026-10-22: my mutant. I chose the bug (minimum income 15,000 → 1,500), wrote its comment, predicted it would be killed, and asked for the private repo and CI run. Claude typed my choice into the file and ran the push (see FRICTIONAL.md).
- The choice of project: I picked option A from Claude's three suggestions. I also chose the target role and approved using my InstaLoan demo as the system under test.
- The InstaLoan loan-origination demo (`~/Desktop/LOS`, Express + TypeScript + Prisma/SQLite, synthetic data, mock vendors), built earlier with Claude's help. It is not in this folder.
- My answers and decisions in `FRICTIONAL.md` ("My entries — Omkar"): confirming the facts about my background, keeping the voice, not force-adding the mp4, and my note on the Stryker report.

## What Claude contributed (Claude Code, Opus 5.5, desktop app, 2026-10-11 → 2026-10-21)
- Explained the assignment and proposed three project options from my résumé (read privately; not stored here).
- Drafted `PROJECT-BRIEF.md`, the narration and `make_sheet.py` / `beat_sheet.json`, all 14 Manim scenes in `scenes.py`, `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, this file, `BUILD-PROMPT.md`, `README.md`, and the Claude-marked entries in `FRICTIONAL.md`.
- Ran the LOS smoke test that produced `evidence/los_smoke_test.txt` (2026-10-12), read the three tools' docs, ran StrykerJS on a scratch copy of the loan rules (2026-10-13, at my request), ran the Whisper pronunciation check, and ran the toolkit's gates and renders.
- On 2026-10-13, acting as a mock TA, reviewed the pitch against the rubric. I then asked it to close the gaps, which led to the Stryker run, the sharper unique-value line, the public-evidence line and the honesty fixes logged in FRICTIONAL.md.
- Committed and pushed the GitHub folder at my request (2026-10-14), and re-checked every attribution so nothing Claude did is labelled as mine.
- **v2 (2026-10-21), after grading (45/50):** read the TA's comment on Canvas, then rewrote the script and drew new beats for who is building it (B00), the smoke-alarm plain-language version (B01–B02) and the technical pipeline (B05–B06). It also re-mapped FACTCHECK, rewrote SHOTLIST, trimmed the brief, re-voiced every beat and re-ran all gates.
- **A separate Claude Code session (2026-10-21), not this folder:** wrote the first income-rule tests, one `<`→`<=` mutant, a mutant checker and a CI workflow in the loan app (`LOS/backend/test/`, `scripts/`, `.github/workflows/`). Its own README says "written by Claude, the coding agent". It is mentioned in B13 as Claude's work.
- **2026-10-22:** typed Omkar's mutant into `BROKEN-income-limit.ts` from his chat instructions, registered it, ran the tests, created the private repo `O7580/instaloan-los`, pushed it and watched the first GitHub Actions run. It then updated B10 and B13 and these files to match.
- **No Claude response is shown in the film.** Nothing on screen is presented as Claude output.

## Third-party assets in the film
None. Every picture is drawn in code (`scenes.py`). No stock images, icons, music or footage. Tool names (Postbot, Schemathesis, Stryker) appear only as text labels.

## Left out on purpose
My résumé, my job tracker, conversation transcripts, the original loan-walkthrough document, and build caches (`mp3/`, `manim/`, `media/`, `clips/`, `_qc/`).

# SOURCES — show-tell-reallocation-recipe-pitch

Film: **Record Beats AI: A Sponsorship Job Finder That Checks Its Own Answers**, a show-tell pitch for my INFO 7375 final project. Per-sentence mapping is in [CLAIMS.md](CLAIMS.md); per-claim verdicts are in [FACTCHECK.md](FACTCHECK.md). `evidence/` is `final-project-film/evidence/` (`../../evidence/` from this folder).

## Authorship and production

- **Drafting.** Claude (chat) and Claude Code drafted the brief, the script and the build: `PROJECT-BRIEF.md`, `make_sheet.py` / `beat_sheet.json`, `scenes.py`, and this paperwork. I, Sreevarshan Sathiyamurthy, reviewed them. The prototype's own code and documents were also drafted with Claude and Claude Code and reviewed by me; all 26 commits on the project branch carry a `Co-Authored-By: Claude` trailer.
- FRICTIONAL.md: entries are my own notes from the session; Claude (chat) expanded them with details from our session record and formatted them, and I reviewed every entry.
- **Voice.** The narration is a synthetic voice: Kokoro TTS, voice `am_michael`, run locally (free, no account), at `--speed 1.09` (a command-line flag of `generate_audio_kokoro.py`, recorded as `kokoro_speed` in the sheet metadata) to fit under four minutes. It is disclosed on screen in the first beat and spoken in the outro. My name is respelled in the narration text only (`Shreevarshun Saa-thee-ya-moorthy`) as a pronunciation aid; on screen it is spelled Sreevarshan Sathiyamurthy.
- **Visuals.** Drawn in Manim with the show-tell kit, plus Remotion bookend and card templates from the toolkit. No AI image or video generation; see [PROMPTS.md](PROMPTS.md).
- **Toolkit.** `BrutFilm` (brutalist.art) at `b21f6253a336098f3f55847a9525ae6868ccbdb7`: `skills/make/show-tell/SKILL.md` and `templates/iso_kit.py`. No toolkit file was changed.

## Brief

- `../../PROJECT-BRIEF.md`: my project brief (sections 1–7, "Exists today", "Will exist").

## Project repository (read-only)

`the-reallocation-engine`, branch `contrib/2026fa-Sreevarshann-newgrad-de-ml-optwindow`, HEAD `ded8454`, read 2026-10-11. Pull request: https://github.com/nikbearbrown/the-reallocation-engine/pull/32 (open as of 2026-10-11).

- `course/2026fa/submissions/Sreevarshann/runs/2026-10-02/report.md`: worked run (warnings, funnel, AMGEN conflict row, "2 … contradicted by the liveness tool")
- `course/2026fa/submissions/Sreevarshann/inputs/posting-checks.csv`: AI-sourced posting checks (model-judgment)
- `course/2026fa/submissions/Sreevarshann/runs/ats-liveness-2026-10-02.txt`: `ats:liveness` output (AMGEN HTTP 404)
- `course/2026fa/submissions/Sreevarshann/runs/break-attempts-2026-10-02.txt`: break attempts a–f, incl. the missing-file crash and its fix
- `course/2026fa/submissions/Sreevarshann/WORKED-RUN.md`: CSV lines for AMGEN INC / HUMAN INC; attestation of my hand check (lines 191, 199)
- `course/2026fa/submissions/Sreevarshann/TEST-REPORT.md`: test runs; old → new SHA map after the history rewrite (`0c6c941` → `6202dc8`)
- `course/2026fa/submissions/Sreevarshann/FRICTIONAL.md`: decisions, and what Claude drafted versus what I decided
- `course/2026fa/submissions/Sreevarshann/SUBMISSION.md`, `DOMAIN-JUSTIFICATION.md`
- `recipes/cases/2026fa/Sreevarshann-newgrad-de-ml-optwindow.md`: `status: DRAFT`, `todos_open: 5`
- `scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/`: `run.py`, `core.py`, `tests/` (58 tests pass at HEAD), `fixtures/persona-meera-krishnan.json` (fictional persona)
- `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv`: sponsorship records (AMGEN INC line 1567, HUMAN INC line 12630)

## Hand check of the approval counts

The hand check was **first run in early October 2026 (Assignment 2)** and **re-run on 2026-10-11**. The command was run from the repo root, `the-reallocation-engine`:

```
python3 -c "import csv; [print(r['company_name'], r['Total Approvals']) for r in csv.DictReader(open('data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv')) if r['company_name'] in ('HUMAN INC','AMGEN INC')]"
```

| ID | Date | Source | Result |
|---|---|---|---|
| HC-1 | Early October 2026, INFO 7375 Assignment 2 (original check) | My statement (2026-10-11) and `WORKED-RUN.md:191,199`, which records the check ("a csv.DictReader one-liner") but not the exact command. The Assignment 2 chat transcript is intentionally excluded: the assignment forbids private conversation transcripts in the submission. | `AMGEN INC 1882.0`, `HUMAN INC 1382.0` |
| HC-2 | 2026-10-11 09:47:31 EDT (re-run) | `evidence/hand-check-terminal.png`: the command, its output, and `date`. Evidence only; it is not shown in the film. B15 draws the two values instead, captioned "re-run 2026-10-11". | `AMGEN INC 1882.0`, `HUMAN INC 1382.0` |

## External sites (from the brief, not the repo)

- **Ellis** visa-sponsor page and **F1Jobs** company page for Amgen, **checked by me on 2026-10-11** (five screenshots taken 9:26–9:47 AM). They back B02's "sponsor lookup sites count past visa filings". In `evidence/`: `ellis-amgen.png`, `ellis-amgen-2.png`, `ellis-amgen-3.png`, `f1jobs-amgen.png`, `f1jobs-amgen-2.png`.

## Evidence folder (`final-project-film/evidence/`)

| File | Origin | Date |
|---|---|---|
| `ats-liveness-2026-10-02.txt` | byte-identical copy of `S/runs/ats-liveness-2026-10-02.txt` | 2026-10-02 |
| `break-attempts-2026-10-02.txt` | byte-identical copy of `S/runs/break-attempts-2026-10-02.txt` | 2026-10-02 |
| `posting-checks-2026-10-02.csv` | byte-identical copy of `S/inputs/posting-checks.csv` | 2026-10-02 |
| `report-2026-10-02.md` | byte-identical copy of `S/runs/2026-10-02/report.md` | 2026-10-02 |
| `run-py-terminal.txt` | captured by Claude Code: re-run of `run.py --run-date 2026-10-02` into /tmp (header line) | 2026-10-11 |
| `unittest-58.txt` | captured by Claude Code: the 58-test suite (header line) | 2026-10-11 |
| `hand-check-terminal.png` | mine: HC-2 re-run | 2026-10-11 |
| `ellis-amgen.png`, `ellis-amgen-2.png`, `ellis-amgen-3.png`, `f1jobs-amgen.png`, `f1jobs-amgen-2.png` | mine: sponsor-site checks | 2026-10-11 |

## Third-party components and licences

Read from the licence files in the local checkout on 2026-10-11 (toolkit at `b21f625`, its `.venv`, and `runtime/remotion/node_modules`). Where no licence file exists, the entry says so; a licence declared only in package metadata is reported as metadata, not as a licence file.

| Component | Role in the film | Licence |
|---|---|---|
| brutalist.art toolkit (`BrutFilm`, commit `b21f625`) | pipeline, show-tell drawing kit, Remotion templates, compile | **licence not found in checkout** (no LICENSE file at the repo root or in `skills/make/show-tell/`) |
| Kokoro model `kokoro-v1.0.onnx` and voices `voices-v1.0.bin` (from the kokoro-onnx `model-files-v1.0` release) | the narration voice | **licence not found in checkout** (`runtime/models/kokoro/` holds only the two model files) |
| kokoro-onnx 0.6.1 (pip) | runs the Kokoro model | MIT (`kokoro_onnx-0.6.1.dist-info/licenses/LICENSE`, © 2025 github.com/thewh1teagle) |
| onnxruntime 1.31.0 (pip) | inference engine for Kokoro | licence file not found in checkout; package metadata declares MIT |
| espeakng-loader 0.2.4 (pip; bundles libespeak-ng 1.52 and espeak-ng-data) | phonemes for the narration | **licence not found in checkout** (no licence file or licence field) |
| phonemizer 3.4.0 (pip) | phoneme interface | GPL-3.0-or-later (`phonemizer-3.4.0.dist-info/licenses/LICENSE`) |
| Manim Community 0.18.1 (pip) | renders the 18 drawn scenes | MIT (`manim-0.18.1.dist-info/LICENSE`, `LICENSE.community`) |
| ManimPango 0.5.0 (pip) | text rendering in Manim | MIT (`manimpango-0.5.0.dist-info/licenses/LICENSE`) |
| pycairo 1.29.2 (pip) | Manim's drawing backend | licence file not found in checkout; package metadata declares LGPL-2.1-only OR MPL-1.1 |
| NumPy 2.4.6 (pip) | geometry in Manim and audio | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 (`numpy-2.4.6.dist-info/licenses/LICENSE.txt`) |
| Pillow 10.4.0 (pip) | compile overlays (opening byline) | HPND (`pillow-10.4.0.dist-info/LICENSE`) |
| Remotion 4.0.486: `remotion`, `@remotion/cli`, `@remotion/renderer`, `@remotion/bundler` (npm) | renders the three Remotion beats (BIDEA, BDEFS, BOUT) | Remotion License (`node_modules/remotion/LICENSE.md`): free for individuals, non-profits and for-profit organizations with up to 3 employees; a company licence is required for larger for-profit organizations |
| `@remotion/paths` 4.0.490 (npm) | path helpers | MIT (`LICENSE.md`) |
| `@remotion/zod-types` 4.0.486 (npm) | prop schemas | licence file not found in checkout; package.json declares MIT |
| `@remotion/compositor-darwin-arm64` 4.0.486 (npm; bundles ffmpeg/ffprobe libraries) | Remotion's frame compositor and encoder | **licence not found in checkout** (no licence file or licence field) |
| Chrome Headless Shell (downloaded by Remotion to `node_modules/.remotion/`) | browser that renders the Remotion frames | Chromium licence, BSD-style, with bundled third-party notices (`LICENSE.headless_shell`) |
| React 18.3.1 / React DOM 18.3.1 (npm) | Remotion component runtime | MIT (`LICENSE`, © Facebook, Inc. and its affiliates) |
| Zod 4.3.6 (npm) | prop validation | MIT (`LICENSE`, © 2025 Colin McDonnell) |
| FFmpeg (Homebrew build, `--enable-gpl`, `--enable-libx264`) | compiles, encodes and masters the film | GPL-3.0-or-later (`ffmpeg -L`) |
| **EB Garamond** font | all Manim labels; Remotion serif text (the stack's first choice, Tiempos Text, is not installed, so EB Garamond renders); the opening byline | SIL Open Font License 1.1 (`runtime/fonts/EB_Garamond/OFL.txt`, © 2017 The EB Garamond Project Authors) |
| **SF Pro / SF Mono** (Apple system fonts) | Remotion UI and mono text (`-apple-system`, `ui-monospace` on macOS): the terms-card footer chip and the outro heading | **licence not found in checkout** (macOS system fonts in `/System/Library/Fonts`) |

Fonts and packages present but not rendered into this film (Lato, Inter, Oswald, faster-whisper, mutagen) are not listed.

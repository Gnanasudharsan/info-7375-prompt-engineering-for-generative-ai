# SOURCES

## Tools used

| Tool | Version | Role | Licence (where it was checked) |
|---|---|---|---|
| Brutalist toolkit (`nikbearbrown/brutalist.art`) | commit `29ba0e8` (2026-09-15) | Reel pipeline, QC gates, compile | Brutalist: no licence file (GitHub reports none); used as directed by the INFO7375 course. |
| Manim Community | 0.18.1 | All scene animation (`scenes.py`) | MIT (the package's `License: MIT` metadata and its bundled LICENSE files) |
| Kokoro TTS, voice `am_onyx` | Kokoro-82M v1.0 weights (`kokoro-v1.0.onnx`, `voices-v1.0.bin`) via kokoro-onnx 0.6.1, run locally | Narration (`sentence_audio.py`) | Model weights: Apache-2.0 (`hexgrad/Kokoro-82M` model card, `license: apache-2.0`; `am_onyx` is listed in the model's VOICES.md; checked 2026-10-14). kokoro-onnx wrapper: MIT (its bundled LICENSE and its GitHub repo). |

Also used locally, licences not separately checked: ffmpeg 9.0.1 (audio joins, measurement, muxing), NumPy 2.5.3, and the macOS system fonts Menlo and the default serif.

No stock footage, music, images or paid generation were used, and no API keys.

## What I made vs. what Claude contributed

- **Claude (claude.ai chat)** drafted the project brief, the beat plan and the narration. I edited them.
- **Claude Code (VS Code extension)** wrote `beat_sheet.json`, `scenes.py` and `sentence_audio.py`. It also:
  - wrote `FACTCHECK.md`, `SHOTLIST.md` and `PROMPTS.md`
  - generated the audio, ran the renders and gates, and reviewed frames
  - drafted this folder's README.md, SOURCES.md and BUILD-PROMPT.md for my review
- **Me:** I verified the E2B and Langfuse descriptions used in B04 (FACTCHECK.md C1, C2). I requested every narration and label revision listed in BUILD-PROMPT.md.

## Illustrative content

These on-screen details are made up for illustration. They appear only on beats that carry the "Constructed — not built yet." label:

- **B05:** the results table rows are made up; no task has been run. They read `task-01` PASS "checks passed", `task-02` FAIL "2 tests failed", `task-03` PASS "checks passed".
- **B08:** an illustrative `> PASS` line and the step list "1 read task / 2 edit file / 3 run checks".

The other Constructed beats (B00, B02) are mock-ups of the plan: the agent's "Task complete" claim beside failing tests, and the planned repository tree.

## Projects and SDKs named in the film

| Item | Link | Beat | Note |
|---|---|---|---|
| OmniSQL-Postgres (my public project) | Repo: https://github.com/tushar-patel28/omnisql-postgres · Demo: https://omnisql-postgres.vercel.app | B10 | B10 shows the project name, its URL and "public repo, checked 2026-10-22". The 23% → 69% execution-accuracy figure is in PROJECT-BRIEF.md only, not in the film (FACTCHECK.md C7). Its README says the demo replays pre-recorded outputs rather than running the model live. |
| Anthropic Go SDK | https://github.com/anthropics/anthropic-sdk-go | B02, B06 | The planned SDK for the Go agent loop that calls the Claude API (FACTCHECK.md C8). Nothing is built with it yet. |

## Alternatives looked at

All on 2026-10-13:

- **E2B** runs AI-generated code in sandboxes (as described in B04; verified by me, FACTCHECK.md C1).
- **Langfuse** records LLM traces and scores them (as described in B04; verified by me, FACTCHECK.md C2).
- **Raindrop:** hosted tracing and failure detection for agents, with simulations on pull requests.
- **Runtime (withruntime.com):** Firecracker microVM sandboxes for AI agents.
- **oh-my-pi:** an open-source coding agent; its harness benchmarks showed that edit format strongly changes pass rates.

Only E2B and Langfuse appear in the film.

## Gate reports

`gates/` is a copy of the reel's `_qc/gates/`: the text reports, the Gate V report and the Gate V contact sheet. README.md has the summary table.

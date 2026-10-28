# SOURCES — DryRun pitch film

## What I used

| Source | Used for | Licence / terms |
|---|---|---|
| [Brutalist toolkit](https://github.com/nikbearbrown/brutalist.art), commit `b21f625` | Pipeline, quality gates, the show-tell drawing kit (`iso_kit.py`) and the 25 approved original props (`iso_originals_25.py`) | Course toolkit; used as instructed, free local pipeline only |
| [Kokoro-82M](https://github.com/thewh1teagle/kokoro-onnx) via kokoro-onnx, voice `af_heart`, speed 0.95 | Narration (synthetic voice reading my script) | Apache-2.0 model; runs locally, $0 |
| Manim Community v0.18.1, ffmpeg | Drawing and rendering | MIT; LGPL/GPL |
| Helvetica Neue, Menlo, EB Garamond | On-screen type (EB Garamond only in the toolkit's name line on the first beat) | Helvetica Neue and Menlo: macOS system fonts (Apple's licence); EB Garamond: SIL OFL |
| [binpash/try](https://github.com/binpash/try) README | B12: what `try` does (previews a command's file changes; Linux only) | Read 2026-10-11 |
| InterCode ([arXiv 2306.14898](https://arxiv.org/abs/2306.14898)) and NL2SH ([arXiv 2502.06858](https://arxiv.org/abs/2502.06858)) | B12: research benchmarks that score AI shell commands offline | Cited only |

## What I made

- The project idea and decisions: which project, which voice, which changes to accept.
- The real Claude reply in B02: I asked it in a fresh claude.ai chat on 2026-10-11 (`evidence/claude-reply-2026-10-11.png`).
- Took the screenshot of the reply, and re-ran the preview test in my own Terminal (2026-10-13, same output).

## What Claude (Claude Code, Opus 5.5) contributed

- Brainstormed and scored project ideas, and searched for existing tools.
- Drafted the narration script and PROJECT-BRIEF.md from my stated reasons, including "why this project", which I approved.
- Wrote `make_sheet.py`, `scenes_body.py`, `build_scenes.py`, FACTCHECK.md, SHOTLIST.md and PROMPTS.md, and ran the toolkit.
- Ran the `find -mtime +7` preview test on a scratch folder on my Mac (`evidence/mtime-test.md`).
- v4 (2026-10-13): drafted the three added narration lines (B14 fair conclusion, B15 how you'd know it ran, B19 evidence for skills I already have), which I approved; checked PR #33's test count; redrew B04 from a reference image I gave it; removed the props' orange lights; added `boost_audio.py` (+3 dB with a limiter); checked a ChatGPT review of the film against the file and the toolkit.
- v5 (resubmission, 2026-10-23): wrote the new scenes (the real screenshot in B02, my Terminal lines in B03, the PR #33 test output in B19, and one approved prop in B01, B11, B12, B14, B15, B16, B17, B18 and B20); re-ran PR #33's tests at commit `c0a7693` (`evidence/pr33-tests-2026-10-23.md`); re-ran every gate.
- Organised FRICTIONAL.md from our session. The reflections in it are mine.
- GPT (ChatGPT) reviewed the script, the v4 film and the v5 draft; FRICTIONAL.md lists what I accepted and rejected.

## Third-party assets

No stock images, music or footage. Every picture is drawn in code, except the real screenshot in B02 (mine). The props are the toolkit's own approved originals.

## Constructed or real

- **Real:** Claude's reply in B02, shown as the real screenshot, cropped (claude.ai, 2026-10-11). v4 retyped the command in a card and paraphrased the advice; v5 shows the screenshot itself.
- **Real:** my preview test in B03 (macOS find, `evidence/mtime-test.md`). Claude Code ran it first on 2026-10-11; I re-ran it in my own Terminal on 2026-10-13 and got the same output. v5 shows my two lines from 13 Oct, copied exactly into a terminal card. It showed which files matched; nothing was deleted.
- **Real:** the PR #33 test output in B19 ("Ran 32 tests in 0.775s … OK"), re-run by Claude Code at the submitted commit `c0a7693` on 2026-10-23.
- **Constructed, and labelled on screen:** the AI's prediction (B05), the simulated deletion (B06, based on which file matched), the WARN decision (B07) and the report (B09).
- **Plans, not results:** everything DryRun "will" do, marked "Design goal", "Planned" or "Version 1 will target". No DryRun results exist yet, so the film shows no DryRun measurements. The only measured numbers on screen come from real past work: the file ages and output of my preview test (B03) and the PR #33 test run (B19, 32 tests).

# SOURCES — what was used, made, and contributed

## Made by me (Chethan Gowda)
- The project idea, the plan (problem, setup, pipeline, eval plan, known limits) and the choice of target role.
- Direction and approval of the film: I gave the assignment and the plan, approved the draft brief and beat outline, and chose the Kokoro voice and the scope (including the 2026-10-14 change to draft fix PRs), and directed the recruiter-facing cut.

- The oasdiff check (2026-10-25): forked RealWorld, planted the `Profile.username` → `handle` rename by hand (commit 85c2a15), ran oasdiff 1.34.1 and read its output. Files in `evidence/`.

## Contributed by Claude (Claude Code, Opus 5.5, session of 2026-10-13)
- **Drafting:** this brief's wording, the beat sheet (narration and visual plan), the toolkit's gate paperwork, and this file, README, BUILD-PROMPT and FRICTIONAL. All were drafted from my plan and the assignment text, then reviewed by me.
- **Code:** the film's custom Remotion scenes, `scenes/ApiImpactPitch.tsx` in this folder, and their registration, `scenes/Root.tsx.patch`.
- **Checking:**
  - Ran the search on angular-realworld-example-app that produces the B04 numbers, in my session on 2026-10-13. The narration says "a plain search returns," not "I ran."
  - Checked the line numbers of the B05 call chain.
  - Checked oasdiff and Optic against their public docs.

## Tools (all free, local)
| Tool | Use | Licence |
|---|---|---|
| brutalist.art toolkit (github.com/nikbearbrown/brutalist.art) | pipeline: audio-first build, compile, QC gates | per the toolkit repo |
| Kokoro-82M via kokoro-onnx, voice `am_michael` | **synthetic narration**: the voice is not mine, the script is | Apache-2.0 |
| Remotion 4 | scene rendering | Remotion licence (free for individuals) |
| ffmpeg | conform, mux | LGPL/GPL |
| EB Garamond (bundled with the toolkit) | serif type | SIL Open Font License |

## Third-party material shown on screen
| Material | Where | Licence / note |
|---|---|---|
| Code lines and grep output from **gothinkster/angular-realworld-example-app**, commit `dd99ed2` (dated 2026-05-13), cloned 2026-10-13 | B04, B05, B07, B08 | MIT, © 2023 Thinkster. Lines are quoted, some lightly shortened with "…" |
| Names and described capabilities of **oasdiff** (github.com/oasdiff/oasdiff) and **Optic** (github.com/opticdev/optic) | B03 | Factual comparison from their public docs. No assets copied |

## Constructed (labelled on screen)
- **B02:** the rename-breaks-a-page example.
- **B07:** the verifier's FIX PR / LIST ONLY / DROPPED verdicts. The cited lines are real; the verdicts are illustrative.
- **B08:** the draft fix PR mock-up.
- **B06, B09, B10, B11:** marked PLANNED, with no results shown.

## Not used
No AI-generated images or video, no paid APIs, no private data, no real résumé or contacts.

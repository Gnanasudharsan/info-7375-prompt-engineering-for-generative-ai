# SOURCES — Sponsor Triage pitch film

## What I used

**Toolkit.** Brutalist, https://github.com/nikbearbrown/brutalist.art, at commit `519fcbb` (pulled 2026-10-14). I used the free local pipeline only: Manim 0.20.1, Remotion, ffmpeg, and faster-whisper for the word clock. There was no paid generation, no API key and no upload.
- The `show-tell` skill: `skills/make/show-tell/SKILL.md`, `templates/iso_kit.py`, and the approved 25 original props (`templates/iso_originals_25.py`). This film uses 15 of them.
- The Remotion component `BrutalistHesitantWriter` for the opener.
- **Kokoro-82M** (kokoro-onnx, the toolkit's free local voice), voice `af_heart`, for the narration. It is a synthetic voice reading my script.
- The QC gates in `runtime/qc/` and `runtime/scripts/`.

**Data and evidence.** All public, and all in the course's Reallocation Engine repo or produced by my own recipe run:
- *The Reallocation Engine*, https://github.com/nikbearbrown/the-reallocation-engine, my fork `kommurisi/the-reallocation-engine`, branch `contrib/2026fa-kommurisi-data-role-sponsor-match`, commit `0e33800`.
- `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` (the 80 Days to Stay table) and its `README.md`, which describes how it was built from DOL LCA disclosure data and the USCIS H-1B Employer Data Hub.
- My recipe's worked run from 2026-10-03: `fixtures/worked-run/liveness.txt`, `greenhouse-api.json`, and the report, copied to `evidence/worked-run-report-2026-10-03.md`. Two of its seven postings are constructed test cases, and the report labels them CONSTRUCTED.
- U.S. Department of Labor, OFLC, *LCA Record Layout FY2024 Q1* (field `JOB_TITLE`), https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Record_Layout_FY2024_Q1.pdf, read 2026-10-14.

**My own earlier work cited in the film:** `github.com/kommurisi/Advances-in-Data-Science---Final-Portfolio-Project---NBA-Rag-App` (December 2025).

## Third-party assets and licences

| Asset | Where | Licence |
|---|---|---|
| EB Garamond (Regular, Medium) | `fonts/`, copied from `brutalist.art/runtime/fonts/EB_Garamond/` | SIL Open Font License 1.1, `fonts/EBGaramond-OFL.txt` |
| PT Mono | `fonts/`, copied from `brutalist.art/runtime/fonts/PT_Mono/` | SIL Open Font License 1.1, `fonts/PTMono-OFL.txt` |
| Show-tell kit and the original props (vector geometry pasted into `scenes.py`) | brutalist.art `skills/make/show-tell/templates/` | Course toolkit, used as its README directs. The repo states no separate licence; it is credited here. |

There are no stock images, no music, no generated images and no third-party footage. The narration is synthetic speech (Kokoro `af_heart`).

## What I made

- The decision to use a Brutalist synthetic voice instead of recording my own, after a TA told me on 2026-10-14 that it is fine. The choice of voice (`af_heart`). The decision to disclose the synthetic voice in the README rather than in the film.
- The narration script is first person and about me. Claude drafted it; the words are in `beat_sheet.json`.
- The project choice, and my answers on what is true about me (F-1 status, new vs. existing skills, the NBA RAG app).
- I did not edit the script, the brief or the scenes myself, and I did not reject any of Claude's drafts. My contribution was the decisions and answers listed above, and reviewing the outputs.

## What Claude contributed (Claude Code, Claude Opus 5.5, session of 2026-10-14)

- It surveyed my repositories and proposed three candidate projects; I chose one. It asked about my voice, my reasons and whether to say I am on F-1; I answered.
- It updated the Brutalist checkout from `cd4bf20` to `519fcbb`, reapplied my Windows `npx` patch, and upgraded Manim to 0.20.1 in the toolkit's virtualenv.
- It drafted PROJECT-BRIEF.md, the narration script, the beat sheet, FACTCHECK.md, SHOTLIST.md, PROMPTS.md, this file and BUILD-PROMPT.md, and drafted the build log in FRICTIONAL.md.
- It wrote all the code: `make_sheet.py`, `scene_body.py` (the 13 drawn scenes), `assemble_scenes.py`, `voice.py`, `finish_audio.py`, `word_clock.py`, `pronunciation_check.py`, and `evidence/csv_title_coverage.py`.
- It generated the narration with Kokoro, transcribed it with faster-whisper (`reports/PRONUNCIATION-CHECK.md`), and added the two respellings in `pronunciation.json`.
- It fact-checked every claim against the files named above. It caught one false claim in its own draft ("the CSV keeps only five titles per company") and corrected it before the narration was voiced (FACTCHECK #17).
- It re-ran the recipe's 12 tests on 2026-10-14 (`evidence/recipe-tests-2026-10-14.txt`), ran every gate, and rendered the film.
- Any Claude response shown in the film: **none**. The film shows no Claude output.

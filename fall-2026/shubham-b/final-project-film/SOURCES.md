# SOURCES — Marino Desk Assistant: A Pitch

## What I used (third-party), with licences

| Thing | What it was used for | Licence / terms |
|---|---|---|
| brutalist.art toolkit, `github.com/nikbearbrown/brutalist.art`, commit `519fcbb` (cloned 2026-10-13) | The show-tell pipeline: `generate_audio_kokoro.py`, `art run` / `art final`, all QC gates, and the show-tell `iso_kit.py` drawing primitives pasted at the top of `scenes.py` | The repository has no LICENSE file at that commit. I used it as the course's required toolkit. I edited no toolkit source file; its own `./setup --install` (npm install) rewrote `runtime/remotion/package-lock.json` |
| Kokoro-82M via kokoro-onnx 0.4.7, voice `am_michael` | Synthetic narration of the script (drafted by Claude, approved by me), generated locally | Kokoro-82M is Apache-2.0 |
| Manim Community 0.20.1 | Rendering every drawn beat | MIT |
| faster-whisper 1.2.1, model `base.en` | Local transcript check of the narration (`whisper_check.py`) | MIT |
| EB Garamond and PT Mono (bundled with the toolkit) | On-screen type | SIL Open Font License 1.1 |
| FFmpeg 9.0.2 | Audio padding, measuring, frame extraction | LGPL/GPL |
| `recreation.northeastern.edu` (public website) | The alternative in B04 (its own search) and the price risk in B12: searched and fetched 2026-10-13. Only page titles, a word count and the five price rows are quoted, in `evidence/` | Public Northeastern University pages; quoted briefly as factual evidence, not republished |

No stock images, no music, no screenshots, no generated images or video, and no paid service. Cost: $0.00.

## What I made

- **The project the film pitches: `marino-rag`**, my public repo (`github.com/bagwe-shubham1727/marino-rag`, commit `dd3205e`, July 2026). Honest note: its current code was mostly AI-generated under my direction (my statement, 2026-10-13). The PRD and the problem are mine: I work as a Facility Assistant at the Marino front desk (people there call me "Suhas", the name on the PRD). Its SharePoint training exports are local only, gitignored and never committed, and are not used anywhere in this film.
- **Evidence of skills I already have:** `robust-data-processor` (EventFlow Engine, Nov–Dec 2025), which I wrote myself. My portfolio site is not cited, because about half its commits were made with Claude.
- **The film:** the decisions behind it:
  - project, scope (public data only, Claude), alternatives, target role, voice;
  - approving the script; Claude drafted the wording (`beat_sheet.json`, via `make_sheet.py`).

  Also the 16 drawn scenes, the helper scripts and all the paperwork listed in README.md, all made in this session with Claude.

## What Claude contributed (Claude Code, model Claude Opus 5.5, 2026-10-13)

Claude did most of the typing; I made the decisions. In order:

1. **The first pitch I rejected.** Claude first proposed and built a pitch about my Reallocation Engine recipe (swe-opt-clock), which was not my own project. I rejected it and asked for one of my own projects. That version is archived locally and not submitted (FRICTIONAL.md, ~15:05).
2. **What Claude did for this version:**
   - read my project bank and repos;
   - re-ran marino-rag's tests;
   - ran the site-search and Alumni-page checks;
   - drafted the script, the brief and the paperwork;
   - wrote `scenes.py` and the helper scripts;
   - ran every gate and reviewed the frames.
3. **Reviews.** An earlier five-advisor "LLM council" review and two fresh-context reviewer agents shaped the rules this version follows: the authorship wording, no Claude-written code counted as my skill evidence, "will" for everything unbuilt, and labelled checks.
4. **No Claude response appears in the film.** Nothing on screen is a Claude output or a reconstructed Claude interface. The conversation transcript is not included (course rule: no private transcripts).

## Not included, on purpose

No SharePoint or other internal Marino documents, no real résumé, contacts or application data (the project bank was read locally only), no API keys or credentials, and no `.venv`, Manim cache or other build caches.

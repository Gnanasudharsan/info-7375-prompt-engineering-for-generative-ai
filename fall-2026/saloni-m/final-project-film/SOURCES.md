# SOURCES.md

## What I used

| Source | What for | Licence / terms |
|---|---|---|
| My opt-countdown prototype in the Reallocation Engine: branch `contrib/2026fa-salonimathure20-opt-countdown`, commit `81d0161`, PR nikbearbrown/the-reallocation-engine#48 | every number about what exists today (B01, B03, B04, B05, B09) | course repository terms |
| The prototype's own docs: `WORKED-RUN.md`, `CHANGE-BRIEF.md`, `DOMAIN-JUSTIFICATION.md`, the recipe card | the alternatives, the 20-minute estimate, the ghost-posting defect | same |
| 80 Days to Stay CSV and BLS OEWS data inside the Reallocation Engine | used by the prototype run, not shown directly | as stated in that repo's `DATA.md` |
| Greenhouse public job-board API (`boards-api.greenhouse.io`) | the 404 result shown in B03 (recorded 2026-10-03) | public API |
| Brutalist toolkit, `github.com/nikbearbrown/brutalist.art`, commit `cd4bf20` | the show-tell drawing kit (`iso_kit.py`, pasted into `reel/scenes.py`), the `BrutalistHesitantWriter` opener, the render pipeline and the quality gates | per the toolkit's repository |
| Kokoro-82M via kokoro-onnx, voice `af_heart` | narration, generated locally and free | Apache-2.0 (Kokoro model) |
| Manim Community, Remotion, ffmpeg | rendering | MIT / Remotion licence (free for individuals) / LGPL |
| EB Garamond font | on-screen labels | SIL Open Font License |

## What I made

- The project idea, and the seven answers in `PROJECT-BRIEF.md`, which I reviewed and own.
- My decisions on the project, the voice, and which skills I actually have (JavaScript/Node, with CodeBuddies as evidence).
- The company names on screen (HubSpot, DraftKings, Klaviyo, Toast) are public employers from the prototype's worked run. No real person, applicant or private data appears. The student in the run is fictional (`ananya-rao-example`).

## What Claude contributed

Claude Code (Anthropic, model Claude Opus 5.5, Claude desktop app, Code tab) worked in one session on 2026-10-13 that I directed. It:

- read my earlier prototype docs and re-ran the prototype and its tests (the output is in `evidence/rerun-2026-10-13.txt`);
- drafted `PROJECT-BRIEF.md`, the narration and beat plan (`reel/make_sheet.py` → `beat_sheet.json`), and the twelve Manim scenes in `reel/scenes.py`;
- ran the toolkit's gates and the render, and drafted this file, `README.md`, `BUILD-PROMPT.md` and `FRICTIONAL.md`.

The prototype itself (built 2026-10-03) was also mostly typed by Claude Code under my direction. The film says so in beat B10.

**No Claude response is shown in the film.** The opener is a typing animation of a question I chose. It is not a Claude conversation.

## Third-party assets

None beyond the toolkit, the fonts and the software above. There are no stock images, music, or AI-generated images or video.

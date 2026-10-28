# SOURCES: Electricity Supplier Check (pitch film)

## What I used (sources of facts)

| Source | What it supports | How I got it |
|---|---|---|
| Massachusetts Attorney General, 2026 competitive supply report (`03.30.2026_CES Report.pdf`): https://www.mass.gov/doc/2026-competitive-supply-report/download | B02: $738.7 million more than basic service over the ten years July 2015–June 2025 (p. 2, Table ES-1); suppliers 10–30% above basic service account for 51.45% of losses, which the film says as "more than half" (p. 4) | Downloaded 2026-10-14 |
| National Grid, Summary of Basic Service Rates, Massachusetts Electric Company, M.D.P.U. No. 1-26-H, effective August 1, 2026 (`meco_basic_service.pdf`): https://www.nationalgrid.com/document/590411/download | B01: residential Total Billed Basic Service Rate, fixed $0.17185/kWh and August $0.16074/kWh; B09/B10: the Aug 1, 2026 rate change | Downloaded 2026-10-14 |
| Energy Switch Massachusetts (Department of Public Utilities): https://www.energyswitchma.gov | B06: the DPU's "Shopping for Electric Supply" site | Fetched 2026-10-14 (page title only; the site is JavaScript-rendered) |
| City of Newton / Green Newton, Newton Power Choice article: https://greennewton.org/news/third-party-competitive-electricity-suppliers-have-historically-proven-to-be-more-expensive-than-the-citys-default-supplier-newton-power-choice/ | B06: a town energy coach ("energycoach@newtonma.gov") helps residents check whether they are on competitive supply | Fetched 2026-10-14 |
| Massachusetts Attorney General, report announcement: https://www.mass.gov/news/new-report-massachusetts-residents-lost-over-738-million-through-competitive-electric-supply-contracts-over-the-last-decade | Background only; the film quotes the report itself, not the announcement's rounded "over $738 million" | Listed in the brief's original Sources section (moved here 2026-10-14) |
| `PROJECT-BRIEF.md` (Hemanth Rayudu) | Every plan, reader, risk and skill statement | Written by me |

Claim-by-claim verdicts are in `FACTCHECK.md`.

The brief's Sources section moved into this file on 2026-10-14, so the brief can end with its two lists as the assignment asks.

## What I made

- **`PROJECT-BRIEF.md`:** my answers to the seven questions. Claude checked it against the sources and made three changes, all approved by me on 2026-10-14:
  - removed "over" from "over $738.7 million";
  - added download dates to the two PDF source lines.
- **The project idea and my own story:** I was on a competitive supplier and overpaid.
- **Decisions:**
  - the beat order;
  - first person in my name, with the Kokoro `am_onyx` voice;
  - updating the toolkit;
  - real tariff rates printed on the drawn bill;
  - a grey placeholder for the formula;
  - approving the narration.

## What Claude contributed (Claude Code, Opus 5.5, 2026-10-14)

- **Verification:** checked the brief's statistics against the AG report and the tariff, and found the "over $738.7 million" mismatch.
- **Narration:** drafted all narration from `PROJECT-BRIEF.md`. I approved the v2 draft as written. Claude then made three voice-only changes after a whisper transcript check:
  - "pytest" written as "py-test", because the TTS said "PIE-dist";
  - "isn't instant" changed to "it is not instant", because the first take was heard as "is an instant";
  - my name written "Hey-month Rah-you-doo" in B00's voice script, so it's said the way I say it ("Hey- Month Ra- You- do"); on screen it stays "Hemanth Rayudu";
  - after watching the film, I asked to drop the spoken "This bill is a drawing, not mine." (B01) and "That screen is a constructed mock-up." (B04); the on-screen CONSTRUCTED tags stay;
  - after I asked how a hiring manager would check the numbers and where Claude Code is used, Claude rewrote B05 (the GitHub repository and evaluation report) and B07's last sentence (Claude Code builds it and is how the agent calls Claude), from wording I approved in a multiple-choice question; I added the matching sentences to my brief first.
- **Revisions I asked for after the first master:** a larger title card (now drawn in Manim), the tariff rates printed on the bill instead of beside it, and recognizable objects for B08's five skills. Claude made all three.
- **Second round of revisions:** I said the cardboard boxes weren't relevant and asked for electricity images. Claude replaced them with a pole-mounted transformer (the tool), a coin stack, an offers board, a GitHub folder and plain panels.
- **Code and paperwork:** wrote `beat_sheet.json`, `scene_body.py` (all drawings), `build_scenes.py`, `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, `PEDAGOGY.md`, `SOURCES.md`, `README.md` and `BUILD-PROMPT.md`.
- **Build:** ran the toolkit build, the gates and the visual QC, and fixed the layout defects they found.
- **What Claude did not do:** no Claude response appears in the film. Claude generated no images, video or music.

## Tools and third-party assets

| Asset | Used for | Licence |
|---|---|---|
| Brutalist toolkit, https://github.com/nikbearbrown/brutalist.art at commit `519fcbb` (2026-10-12) | Pipeline, gates, show-tell iso kit pasted into `scenes.py` (`skills/make/show-tell/templates/iso_kit.py`) | Course toolkit; the repository has no LICENSE file |
| Kokoro-82M voice model via `kokoro-onnx` 0.4.7, voice `am_onyx` | Narration (local, free) | Model: Apache-2.0; kokoro-onnx: MIT |
| Manim Community 0.20.1 | All drawn beats | MIT |
| faster-whisper 1.2.1 | Word timing (`align.py`) and pronunciation check | MIT |
| EB Garamond (`runtime/fonts/EB_Garamond`) | All on-screen type | SIL Open Font License 1.1 (`OFL.txt`) |
| FFmpeg 9.0.1 | Encoding | LGPL/GPL |

**Not used:**
- stock images or footage
- screenshots
- generated media
- a real bill: every bill in the film is a constructed drawing with no amounts
- any person's image or private data

# SOURCES — Remnix Agent pitch film

All dates are 2026-10-14 unless stated.

## What I made (Revan C)

- **The project:** Remnix Agent, its scope, stack, build order, target role, audiences, and the list of
  skills I have and skills that are new to me.
- **Money Map,** https://mit-dci.github.io/payments-dashboard/. I built it alone as a Software Engineer Co-op at
  the MIT Digital Currency Initiative. The film shows only the public live page. No code or data from the
  MIT DCI repository is in this folder or the film.
- **Facts from my own checks:** Wise's comparison page and Monito do not include stablecoin routes
  (checked 2026-10-14). I am allowed to use Money Map's data for Remnix.
- **Decisions and review:** I chose the Kokoro voice, removed the "ask MIT DCI first" beat, added
  researchers and policymakers as an audience, approved the B14 "why I picked it" line, approved the Step 6
  honesty fixes, and watched the review cut.
- **Resubmission (2026-10-25):** my answers at the top of FRICTIONAL.md ("In my words") are mine, typed by me;
  I approved the resubmission plan, the opening line about who I am, and the technical design the film names
  (tables, endpoint, tools, test runner).

## What Claude contributed (Claude Code, Claude Opus 5.5, in my build sessions on 2026-10-14 and 2026-10-25)

- **The narration was written with Claude and reviewed by me.** The film now says this in its opening line and
  on screen; the first submission wrongly said "the words are mine".
- **2026-10-25 resubmission:** Claude proposed the plan (authorship fix, who-I-am line, plain-language beat,
  concrete technical beats, trims to stay under 4:00), asked me the FRICTIONAL questions, laid out my answers,
  redrew BPLAIN, B03 and B04, re-voiced and re-rendered the changed beats, re-ran every gate, and updated these
  documents.

- Read the toolkit and explained the pipeline. Drafted `PROJECT-BRIEF.md` from my answers and asked me for
  anything it did not know.
- Researched the World Bank's Remittance Prices Worldwide pages (methodology and the US→Mexico corridor)
  and reported what they say. Those facts are in `build/FACTCHECK.md` rows 11–12.
- Took the Money Map screenshot (headless Chrome, 16:20 EDT) and read the page's text once earlier in the
  session. The $7.42 stablecoin reading in beat B12 comes from that earlier read; the $7.54 (Wise) and $8.99
  (stablecoin) readings come from the screenshot.
- Wrote the narration drafts, `make_sheet.py`, `scene_body.py` (all 17 Manim drawings), `build_scenes.py`,
  `finish_audio.py` and `env.sh`, plus the paperwork (`FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`,
  `GATE-SUMMARY.md`) and these four documents.
- Ran the install, the audio, the renders and every gate. It fixed gate failures in the scene source and
  ran the line-by-line honesty check (Step 6). That check found 7 lines and 2 drawings that made Remnix
  sound built, and 1 unbacked claim about users; all were fixed with my approval.
- It caught one wrong claim in its own first draft: it had implied that Money Map can't answer "what if I
  pay by debit card?", but Money Map has a Debit Card filter. That was corrected before rendering.

**No Claude response appears in the film.** The toolkit's "Your Turn" Claude.ai composer beat was dropped.

## Real material shown in the film

| Item | Where | Origin |
|---|---|---|
| Money Map screenshot (top 460 px of a 1600×1000 capture) | B00 | Public page https://mit-dci.github.io/payments-dashboard/, captured 2026-10-14 16:20 EDT; files in `build/pantry/` |
| $7.54 Wise fee for $1,000 | B05 (CONSTRUCTED mock-up) | Same screenshot (remittance quotes "Oct 14 · 00:51 EST") |
| $7.42 → $8.99 stablecoin route | B12 | Money Map page text (stablecoin prices "updated Oct 14 · 15:10 EST"), then the screenshot ("Oct 14 · 16:12 EST") |
| World Bank facts (covers US→Mexico; newest data collected Aug 4–28, 2025; $200 and $500 amounts in the brief) | B07, brief | https://remittanceprices.worldbank.org/corridor/United-States/Mexico and https://remittanceprices.worldbank.org/methodology, viewed 2026-10-14 |

## Constructed material

- **B05 answer card:** labelled "CONSTRUCTED · mock-up, not real output" on screen for the whole beat.
  Its only number ($7.54) is from the real screenshot.
- **Every other body beat is a drawing.** Drawings of Remnix parts (server, database drawers, test pages, log
  binder, review desk) show plans, not built things. On-screen labels say "proposed · not built", "planned",
  "how you'd know" and "will exist" where it matters.

## Third-party tools and assets

| What | Used for | Licence / terms |
|---|---|---|
| Brutalist toolkit, https://github.com/nikbearbrown/brutalist.art @ `519fcbb` | Pipeline, gates, Remotion bookend components (`BrutalistHesitantWriter`, `ClaudeDefinitions`), the show-tell drawing kit (`iso_kit.py`) and the 25 original props (`iso_originals_25.py`) | No LICENSE file in the repository at that commit; used as the course-assigned toolkit. Its code is **not** copied into this folder: `build_scenes.py` pastes the kits into `scenes.py` at build time from your own clone. |
| Kokoro-82M voice model (`kokoro-v1.0.onnx`, `voices-v1.0.bin`), voice `af_bella` | Narration | Apache-2.0 (as stated in the toolkit's `generate_audio_kokoro.py`); downloaded from the kokoro-onnx GitHub releases by `./setup --install` |
| kokoro-onnx 0.4.7, espeakng-loader 0.2.4 | Running Kokoro | Licence field blank in the installed package metadata |
| espeak-ng 1.52.0 (Homebrew) | Text-to-phoneme step for Kokoro | GPL-3.0-or-later (Homebrew metadata); used as a local tool, not redistributed |
| Manim Community 0.20.1 | All body-beat drawings | MIT |
| Remotion 4.0.486 | The two bookend cards (BIDEA, BDEFS) | Remotion licence (`SEE LICENSE IN LICENSE.md` in the package) |
| EB Garamond font | All on-screen type | SIL Open Font License (OFL.txt bundled in the toolkit) |
| ffmpeg, Google Chrome (headless) | Assembly, cropping, the screenshot | Local tools; nothing redistributed |

## Not used

No paid generation, no Higgsfield, no ElevenLabs, no stock footage, no music, no instructor
portraits, no instructor name, persona or credit line, no résumé, contacts or chat transcripts.

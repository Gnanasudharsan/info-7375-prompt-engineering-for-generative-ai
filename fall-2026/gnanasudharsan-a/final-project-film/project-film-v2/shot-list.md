# Shot list — DecisionTrace Lite (project film)

This maps each script line (`script.md`) to a visual. Slide IDs (S01…) match the
`<!-- Sxx -->` comments in `slides.md`.

Visual types:
- **SLIDE**: the Marp slide.
- **STILL**: a real screenshot from `../evidence/alternatives-test/screenshots/`, scaled only, with a
  "REAL · tool · captured 2026-10-10" label.
- **SCREEN**: a screen recording you make.
- **CONSTRUCTED**: a mock-up of something not yet built. It must carry an on-screen label "CONSTRUCTED · NOT REAL OUTPUT".

DecisionTrace Lite doesn't exist yet, so no footage of it can be real. Show its output only
as CONSTRUCTED, or only on slides.

| Line | Time | Visual | Notes |
|---|---|---|---|
| **1. Executive summary** | | | |
| L01 | 0:00 | SLIDE S01 | Title. |
| L02 | 0:03 | SLIDE S02 | |
| L03 | 0:15 | SLIDE S03 | Optional: SCREEN, a slow scroll of the six files in `../evidence/alternatives-test/test-pack/` in Finder or an editor, labelled SYNTHETIC. |
| L04 | 0:20 | SLIDE S04 | |
| L05 | 0:30 | SLIDE S05 | |
| L06 | 0:35 | SLIDE S06 | |
| L07 | 0:54 | SLIDE S07 | |
| **2. Introduction** | | | |
| L08 | 0:57 | SLIDE S08 | Section card. |
| L09 | 0:59 | SLIDE S09 | Tool names only, no vendor logos (trademarks). L10 (other products) and L12 (Liu et al.) were cut on 2026-11-22 because they're unverified; see appendix §6. |
| L11 | 1:08 | SLIDE S10 | |
| L13 | 1:24 | SLIDE S12 | |
| L14 | 1:38 | STILL `2026-10-10_notebooklm_summary.png` → `2026-10-10_notebooklm_run2_q1.png` | Cut on "But it described…". Reuse `../build/frames/B03a.png` and `B03b.png`, which already have the labels and highlight boxes. |
| L15 | 1:48 | STILL `2026-10-10_chatgpt_q1.png` | Reuse `../build/frames/B04.png` (crop plus highlight on "June 15, 2026"). |
| L16 | 1:57 | SLIDE S13 | |
| L17 | 2:00 | SLIDE S13 (hold) | |
| **3. Methods** | | | |
| L18 | 2:12 | SLIDE S14 | Section card. |
| L19 | 2:14 | SCREEN of your larger system, then SLIDE S15 | Record the working Neo4j/LangGraph/FastAPI system (about 8 s: the API docs page or a graph view). Cut to S15 on "Here I keep only the core". Label it "Larger system (separate project)". |
| L20 | 2:30 | SLIDE S16 | Optional: SCREEN of the corpus folder once it exists. |
| L21 | 2:49 | SLIDE S17 | Optional: CONSTRUCTED view of one gold-set JSONL row. |
| L22 | 3:07 | SLIDE S18 | |
| L23 | 3:16 | SLIDE S19 | The JSON is a schema example, not model output. Add a "SCHEMA · NOT OUTPUT" label. |
| L24 | 3:27 | SLIDE S20 | |
| L25 | 3:48 | SLIDE S21 | |
| L26 | 3:53 | SLIDE S22 | Optional: SCREEN of `claude --help` showing `-p/--print` and `--json-schema`. That help output is real. |
| **4. Evaluation** | | | |
| L27 | 4:19 | SLIDE S23 | Section card. |
| L28 | 4:27 | SLIDE S24 | Reveal one row per line, L28–L31. |
| L29 | 4:36 | SLIDE S24 | |
| L30 | 4:43 | SLIDE S24 | |
| L31 | 4:49 | SLIDE S24 | Reveal the last two rows. |
| L32 | 4:59 | SLIDE S25 | |
| L33 | 5:07 | SLIDE S26 | |
| L34 | 5:32 | SLIDE S27 | Optional split screen with `../evidence/alternatives-test/test-pack/2026-06-01_ticket_TRK-140.txt` ("Status: In Progress"), which is real synthetic data. |
| L35 | 5:49 | SLIDE S28 | Hold 3 s, then end. If any narration is synthetic, add a disclosure line here. |

Times are line start times at 130 words per minute, for a recording in your own voice. The Kokoro film (`SHOTLIST.md`) runs faster, about 5:01 in total.

## Rendering the slides

Marp CLI can export to PNG or PDF, for example `npx @marp-team/marp-cli slides.md --images png`.
This needs Node, which is outside the course's Python scope. That's fine for a media tool, but
don't commit `node_modules`. The Marp VS Code extension is another option.

# SOURCES — Final Project Pitch Film

## What I used

| Item | What it is | Licence / terms | How it was used |
|---|---|---|---|
| Brutalist toolkit | `github.com/nikbearbrown/brutalist.art`, local checkout at commit `ba2d0e0` (2026-09-07) | No licence file at the repo root of this checkout; used as the course instructs | Free local pipeline: audio, Remotion, Manim, gates, compile |
| Kokoro TTS | `kokoro-v1.0.onnx` + `voices-v1.0.bin`, voice `am_onyx`, via `kokoro-onnx` 0.6.1, bundled in the toolkit | Kokoro-82M weights are published under Apache-2.0 (upstream model card) | Synthetic narration voice, run locally at no cost |
| Manim Community | v0.18.1 | MIT | The ten body drawings (`scenes.py`) |
| Remotion | Toolkit's bundled Remotion project | Remotion licence (`LICENSE.md` in the package; free for individuals) | `ClaudeComposerAsk` (B00, B11) and `BrutalistHesitantWriter` (B01) |
| EB Garamond | Font bundled in the toolkit | SIL Open Font License | Serif text in the Remotion beats |
| DOL OFLC Performance Data page | https://www.dol.gov/agencies/eta/foreign-labor/performance, opened 2026-10-13, re-checked 2026-10-24 | U.S. government public information | The chosen data source; latest release is FY2026 Q3; data-quality caveat |
| LCA disclosure file FY2026 Q3 | https://www.dol.gov//media/LCA_Disclosure_Data_FY2026_Q3.xlsx, downloaded 2026-10-24, 251,850,891 bytes, SHA-256 f8ca8448a528671f784d3692923775a13741c99caec2816b2fe30c8885bd28b3 | U.S. government public information | Column names shown in B02 and B08 (read from its header row); not included in this folder (over GitHub's 100 MB limit) |
| ChatGPT test | GPT-6 (high mode), run by me on 2026-10-24 with `LCA_Record_Layout_FY2026_Q3.pdf` attached | Output of my own ChatGPT account | Saved verbatim in `evals/chatgpt-test-2026-10-24.md`; quoted in B04 and the brief |
| LCA record layout FY2025 Q4 | https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Record_Layout_FY2025_Q4.pdf, read 2026-10-14 | U.S. government public information | Form ETA-9035 description (first version of the film) |

One data file was downloaded (above); none is included here. No paid service, API key, image generator, or stock media was used. No third-party images or video appear in the film.

## What I made
- The project idea, the choice of dataset, the target role, and every decision in PROJECT-BRIEF.md
- The ChatGPT test run (2026-10-24) and my description of Vanna.ai, based on my own use of it
- The decision to cut my earlier projects from the film and to keep the one evidence line in the brief

## What Claude contributed
Claude (Claude Code, model Opus 5.5) worked with me on 2026-10-12 to 2026-10-14, and on the revision of 2026-10-24. It:
- proposed the candidate topics and drafted PROJECT-BRIEF.md from my answers
- wrote `beat_sheet.json` (narration and visual plan), `scenes.py` (Manim drawings), and the reel paperwork (FACTCHECK, SHOTLIST, PROMPTS)
- ran the toolkit, fixed the scenes that failed its gates, and drafted this file, FRICTIONAL.md, BUILD-PROMPT.md and README.md
- in the revision: downloaded the FY2026 Q3 file with my approval, recorded its checksum, read its header row, wrote the prompt for my ChatGPT test, and updated the film and these files

The narration script was written with Claude and reviewed by me; the film now says that in B00 and B12. I reviewed and directed each of these files. The film shows **no** Claude response. The cold-open composer reply is labelled CONSTRUCTED on screen.

## Constructed material (labelled on screen)
- B00: the composer reply ("CONSTRUCTED: not a real Claude reply")
- B05: the README evaluation table (no results exist)
- B08: "EXAMPLE DATA LLC" and its variants, and the 1-vs-3 count (an invented company)

# SHOTLIST — decisiontrace-lite-film

How each beat of the rendered film was made. `shot-list.md` is a different file: it maps script
lines to slides for a slide-and-voice version.

Audio: every beat is Kokoro af_heart. B01–B19 come from `generate_audio_kokoro.py`. B00 comes from
`tools/phoneme_name.py --variant E` (name IPA ɲˈɑːnɑːsˌuːdʰɚʃɑːn ɑːʃˈoʊk kuːmˈɑːɹ; engine
"kokoro-phoneme", so the standard script skips it).

| Beat | Script lines | Method | Slot | Notes |
|---|---|---|---|---|
| B00 | L01 | Manim `B00_Title` | manim/B00.mp4 | Name, title, one-line subtitle |
| B01 | L02–L03 | Manim `B01_Scattered` | manim/B01.mp4 | Three pages (meeting notes · email · ticket); why? / who approved? / still true?; one page stamped "out of date" |
| B02 | L04–L05 | Manim `B02_AnswerCard` | manim/B02.mp4 | **CONSTRUCTED · NOT REAL OUTPUT** example card (answer · status · source), then "Not in the sources." |
| B03 | L06–L07 | Manim `B03_WhyItMatters` | manim/B03.mp4 | Two identical answer cards → current ✓ / reversed ✗; "Check it in seconds." + "And a published score." |
| B04 | L08–L09 | Manim `B04_Tools` | manim/B04.mp4 | Text: What already exists / NotebookLM · ChatGPT |
| B05 | L11 | Manim `B05_Research` | manim/B05.mp4 | RAG / ALCE / RAGAS, each on its sentence |
| B06 | L13 | Manim `B06_TestSetup` | manim/B06.mp4 | Label SYNTHETIC TEST DATA · 2026-10-09 |
| B07 | L14 | Two composed stills in sequence | media/B07.mp4 | Pitch frames reused unchanged (`build/frames/`): B03b.png (run-2 Q1) 0–4.74 s, then B03a.png (summary) from "But it described". Label REAL · NotebookLM · captured 2026-10-10 |
| B08 | L15 | Still | media/B08.png | Pitch frame B04.png, byte-identical. Label REAL · ChatGPT · captured 2026-10-10 |
| B09 | L16–L17 | Manim `B09_Gap` | manim/B09.mp4 | Existing tools (in my test) vs DecisionTrace Lite |
| B10 | L18–L19 | Manim `B10_LargerToLite` | manim/B10.mp4 | "The plan" → Larger system, **separate project** (Neo4j · LangGraph · FastAPI · hallucination detection) → Lite (question in → grounded answer out · Python + Claude). A drawing; no footage of the larger system |
| B11 | L20 | Manim `B11_Data` | manim/B11.mp4 | 6 → ~50 pages; four hard-case kinds; SYNTHETIC · FICTIONAL COMPANY |
| B12 | L21 | Manim `B12_TestSet` | manim/B12.mp4 | ~50 questions, hand-written by me; documents: Claude helps; ✗ a model grading its own homework |
| B13 | L22–L23 | Manim `B13_RetrieveAnswer` | manim/B13.mp4 | Pile → BM25 → top passages; then JSON contract, labelled **SCHEMA · NOT OUTPUT** |
| B14 | L24–L25 | Manim `B14_VerifyLoop` | manim/B14.mp4 | answer → quote in doc? (code) → supports claim? (second Claude call) → cited; retry once; "Not supported by the sources."; then harness → report |
| B15 | L26 | Manim `B15_Resources` | manim/B15.mp4 | Resource table; **PENDING** ringed; fallback "request API credits" |
| B16 | L27–L31 | Manim `B16_Measures` | manim/B16.mp4 | Five measures and targets, one row per sentence |
| B17 | L32–L33 | Manim `B17_Decision` | manim/B17.mp4 | verify ON vs OFF; Worked / Didn't; "Either way: publish the numbers and the failures" |
| B18 | L34 | Manim `B18_FirstCheck` | manim/B18.mp4 | **TARGET ANSWER · NOT OUTPUT**: in progress · as of 2026-06-09 · cites TRK-140; what each tool missed |
| B19 | L35 | Manim `B19_Outro` | manim/B19.mp4 | Name, title, "Narration: synthetic voice (Kokoro)" |

L10 and L12 were cut from the script on 2026-11-22, so no beat uses them.

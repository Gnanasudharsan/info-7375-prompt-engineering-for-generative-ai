# SOURCES — DecisionTrace Lite project film

## What I made or decided

- The project, its scope, the four-part structure (the professor's), and every final decision.
- Answers given on 2026-11-22: my resources (Claude Code via NEU, an M4 MacBook Pro, no GPU,
  no API credits); that my larger Neo4j/LangGraph/FastAPI system is built and can be shown;
  Python + Claude only for the Lite tool; reuse of the October alternatives test.
- The approval with changes (2026-11-22):
  - keep the larger system labelled "separate project";
  - say scripted Claude Code use is pending, with requesting API credits as the fallback;
  - keep VERIFY items out of the script and slides;
  - accept the proposed targets;
  - cut L12 and shorten L26.
- I ran the October alternatives test myself and took its screenshots
  (`../evidence/alternatives-test/`, see the pitch's SOURCES.md).
- I chose the af_heart voice and the IPA name pronunciation (variant E) for the pitch film. This film
  reuses both.

## What Claude contributed

**Claude Code (Opus 5.5), in this session (2026-11-22).** I haven't yet reviewed all of it frame by frame.

- Drafted `script.md`, `slides.md`, `appendix.md` and `shot-list.md` from my brief. That
  included the research and product list, the build plan, the data schemas, the metric definitions and
  the proposed targets, which I accepted.
- Cut L10 as well as L12. L10 named products marked VERIFY, so it fell under my "no VERIFY claims in the
  script" instruction. Rewrote L26 for the pending/fallback wording.
- Chose the beat grouping (20 beats) and wrote every Manim scene in `build/scenes.py`, plus
  `build/tools/make_beat_sheet.py` and `build/tools/still_clips.py`.
- Ran the audio generation, the renders, every gate and every check, and wrote this paperwork set.
- Referenced the research papers (RAG, ALCE, RAGAS and the others in `appendix.md` §6) from its training
  knowledge. **No link was opened in this session**, so they aren't link-checked.

**Reused from the pitch film:**
- `build/tools/phoneme_name.py`, unchanged.
- The palette and helper functions in `scenes.py`.
- The three composed frames B03a, B03b and B04, byte-identical.

**No Claude response appears in the film.**
- The only AI outputs shown are the NotebookLM and ChatGPT screenshots (B07, B08).
- B02's answer card is a constructed example, labelled on screen.
- B13's JSON is the planned schema, labelled on screen.
- B18's answer comes from my answer key, labelled on screen.

## Third-party material

Same toolchain as the pitch film, same versions. Licences were checked on 2026-10-10 (see `../SOURCES.md`).
I didn't re-check them for this film.

| Material | How it's used | Licence (from `../SOURCES.md`) |
|---|---|---|
| Brutalist toolkit, `nikbearbrown/brutalist.art` @ `ba2d0e0` | Audio script, compile, all gates | None declared. Not redistributed here |
| Kokoro-82M (`kokoro-v1.0.onnx`, `voices-v1.0.bin`), voice af_heart | All narration | Apache-2.0 per the model card. UNVERIFIED for the converted files |
| kokoro-onnx 0.6.1 | Runs Kokoro, including phoneme input for my name | MIT |
| phonemizer 3.4.0 / espeak-ng (espeakng-loader 0.2.4) | Phonemes | GPL-3.0-or-later / GPL-3.0 (bundled copy UNVERIFIED) |
| Manim Community 0.18.1, ManimPango 0.5.0 | Every beat except B07/B08 | MIT |
| EB Garamond | All serif text | SIL OFL 1.1 |
| PT Mono | B13 JSON text | ParaType Free Font License |
| ffmpeg 9.0.1 | B07 clip, checks, encoding | GPL-3.0-or-later build; output only |
| NotebookLM and ChatGPT screenshots (via pitch frames B03a, B03b, B04) | B07, B08 | Outputs of those services from my own test on synthetic data; scaled/cropped only |

## Data

All documents are synthetic: a fictional company, Northwind Logistics. There's no real or private data in the
film or in this folder.

## Voice

All narration is synthetic (Kokoro af_heart), and B19 says so on screen. My name in B00 is spoken from
hand-set IPA (`build/tools/phoneme_name.py`, variant E).

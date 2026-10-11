# SOURCES — DecisionTrace pitch film

## What I made or decided

- The project idea, the choice of DecisionTrace, the scope, and every final decision. I reviewed
  and approved every file and the film.
- I ran the alternatives test myself on NotebookLM and ChatGPT and took all the screenshots
  (captured 2026-10-10). Their originals are in `evidence/alternatives-test/screenshots/`.
- I picked the voice (af_heart) and the name pronunciation (IPA variant E) by ear, and I wrote the
  pronunciation guide. All three steps are in `BUILD-PROMPT.md` §5–6.

## What Claude contributed

**Claude in the claude.ai chat (Opus 5.5).** This is my own account. That chat isn't part of this
folder, so these items can't be checked here.

- Broke down the assignment.
- Designed the alternatives test and drafted its answer key, before any tool was asked the
  questions.
- Drafted PROJECT-BRIEF.md and suggested the edits I approved.
- Drafted the beat plan and the original narration, which I approved unchanged at the time.
  - Later narration edits are logged in FRICTIONAL.md (2026-10-10): B08's "What's in" sentence and
    the B00/B12 name lines.
  - The narration in the final film is in `beat_sheet.json`.
- Reviewed drafts frame by frame and suggested fixes.

**Claude Code.** Its work is recorded in FRICTIONAL.md and BUILD-PROMPT.md §6.

- Generated the six synthetic Northwind Logistics documents and the questions (2026-10-09).
- Scaffolded the submission folder.
- Checked the brief's claims against the evidence.
- Wrote `build/scenes.py`, `build/tools/compose_frames.py` and `build/tools/phoneme_name.py`.
- Composed the labelled B03 and B04 frames.
- Ran every render, gate and check.
- Wrote FACTCHECK.md, SHOTLIST.md and PROMPTS.md.
- Made the git commits and pushes.
- Drafted this README.md, BUILD-PROMPT.md and SOURCES.md from my outline, checking every version,
  licence, command and path against the actual files and packages.

**No Claude response appears in the film.** The only AI outputs shown are the NotebookLM and
ChatGPT screenshots (B03, B04). B06's terminal is a constructed mock-up, labelled on screen.

## Third-party material

Each licence below was checked on 2026-10-10. The source of each check is noted, and items I
couldn't confirm are marked UNVERIFIED.

| Material | How it's used | Licence | How I checked |
|---|---|---|---|
| Brutalist toolkit — `nikbearbrown/brutalist.art`, commit `ba2d0e0` | Build pipeline: audio script, compile, all quality gates; the EB Garamond font copy | **None declared** | No LICENSE file in the repository, and GitHub's licence API reports none. I don't redistribute any toolkit code here; my own scripts import it at build time. |
| Kokoro-82M model (`kokoro-v1.0.onnx`) and the `af_heart` voice (`voices-v1.0.bin`) | All narration | **Apache-2.0** per the `hexgrad/Kokoro-82M` model card (Hugging Face API, `license: apache-2.0`). The toolkit's `generate_audio_kokoro.py` also says Apache-2.0. | **UNVERIFIED for the converted files.** The ONNX conversion and voices file come from the kokoro-onnx project's `model-files-v1.0` release. They carry no licence text of their own, so I couldn't confirm that the licence carries over. |
| kokoro-onnx 0.6.1 | Runs the Kokoro model, including the phoneme input for my name | **MIT** | LICENSE file in the installed package (`kokoro_onnx-0.6.1.dist-info/licenses/`). |
| phonemizer 3.4.0 | Turns text into phonemes for Kokoro | **GPL-3.0-or-later** | The installed package's own metadata. |
| espeak-ng, loaded by espeakng-loader 0.2.4 | Phoneme backend | **GPL-3.0** per the upstream `espeak-ng/espeak-ng` repo (GitHub licence API) | **UNVERIFIED for the bundled copy.** The installed espeakng-loader package has no licence metadata or file. |
| Manim Community 0.18.1, with ManimPango 0.5.0 | Renders every beat except B03/B04 | **MIT** (both) | The installed packages' own metadata. |
| EB Garamond (Regular, Medium) | All serif text on screen, and the labels on B03/B04 | **SIL Open Font License 1.1** | `runtime/fonts/EB_Garamond/OFL.txt` in the toolkit ("Copyright 2017 The EB Garamond Project Authors"). The `~/Library/Fonts` copies Manim used are byte-identical to the toolkit's files. |
| PT Mono | B06 terminal text | **ParaType Free Font License**: the text embedded in the font allows use, copying, modification and redistribution | Read from `/System/Library/Fonts/Supplemental/PTMono.ttc`, a font bundled with macOS ("Copyright 2010 ParaType Inc., ParaType Ltd."). |
| ffmpeg 9.0.1 (Homebrew) | Encoding, trimming, audio checks | **GPL-3.0-or-later** for this build | `ffmpeg -L`, and `-buildconf` shows `--enable-gpl --enable-version3`. The film is ffmpeg's output; no ffmpeg code is redistributed here. |
| NotebookLM and ChatGPT screenshots | B03 and B04 | Outputs of those services from my own test on synthetic data | Shown unaltered except for scaling, the B04 crop, and the labels and highlight boxes drawn on the frame. Originals are in `evidence/alternatives-test/screenshots/`. |

## Data

All documents are synthetic: a fictional company, with fictional people and emails. No real
résumé, contacts, application tracker, conversation transcript or private data appears in the film
or in this folder.

## Voice

All narration is synthetic, made with Kokoro af_heart, as disclosed on screen in B12. My name in
B00 and B12 is spoken from hand-set IPA phonemes (`BUILD-PROMPT.md` §5). At one point I recorded my
own voice for those two lines, but I removed the recordings so the whole film uses one voice. None
of my recordings is in this folder or in the film.

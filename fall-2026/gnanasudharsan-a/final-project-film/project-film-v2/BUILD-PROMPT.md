# BUILD-PROMPT — how to rebuild `decisiontrace-lite-film.mp4`

Built on 2026-11-22. The master is 301.54 s long and its SHA-256 is
`882a80a11b0c18bace0f13f71f5b3109edf46f7354dcd812372156d7109add57`
(`gate-reports/decisiontrace-lite-film.verified.json`).

---

## 1. Environment

These versions were read from the build machine on 2026-11-22.

| Component | Version |
|---|---|
| OS | macOS 27.2.1 (build 26B131), Apple M4, 16 GB |
| Python | 3.12.14, in the toolkit's `.venv` |
| ffmpeg / ffprobe | 9.0.1 (Homebrew) |
| kokoro-onnx | 0.6.1 (onnxruntime 1.30.0, phonemizer 3.4.0, espeakng-loader 0.2.4) |
| Kokoro model files | `kokoro-v1.0.onnx` (325,532,387 bytes), `voices-v1.0.bin` (28,214,398 bytes) |
| Voice | `af_heart`, every beat, speed 1.0 |
| Manim | Community 0.18.1, ManimPango 0.5.0 |
| Pillow | 10.4.0 |
| Fonts | EB Garamond (all serif text), PT Mono (B13 JSON) |

## 2. Toolkit

The same checkout as the pitch film (`../BUILD-PROMPT.md` §2): `nikbearbrown/brutalist.art` at
`ba2d0e0f043f5b3b35a50d336e0fc66fbfecfc0c`, with the `.venv` active. I didn't modify any toolkit file.

## 3. Working-folder layout

Build outside every git repo. I used `~/info7375-films/decisiontrace-lite/`. Paths on the left are
relative to this folder (`project-film-v2/`).

| Copy from | To (working folder) |
|---|---|
| `build/scenes.py` | `scenes.py` |
| `build/tools/make_beat_sheet.py`, `still_clips.py`, `phoneme_name.py` | `tools/` |
| `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` | same names (GATE F) |

`build/frames/` (B03a, B03b, B04) is read in place by `still_clips.py`. These are byte-identical copies
of the pitch film's `../build/frames/`.

`beat_sheet.json` paths (`mp3/…`, `manim/…`, `media/…`) are relative to the working folder. The build
steps below create them; none is committed.

## 4. Commands, in order

```bash
cd ~/Downloads/7375/brutalist.art && source .venv/bin/activate
R=~/info7375-films/decisiontrace-lite
V=<path to>/project-film-v2

# 1. beat_sheet.json from the approved script (narration = script lines, verbatim)
python3 $R/tools/make_beat_sheet.py $V/script.md $R/beat_sheet.json

# 2. narration (durations are measured and written into the sheet)
python3 runtime/scripts/generate_audio_kokoro.py $R --only B01 B02 B03 B04 B05 B06 B07 B08 B09 B10 B11 B12 B13 B14 B15 B16 B17 B18 B19
python3 $R/tools/phoneme_name.py beats $R --variant E --only B00

# 3. the two screenshot beats (after audio: B07's length comes from its mp3)
python3 $R/tools/still_clips.py $R $V/build/frames

# 4. review build: renders every Manim scene, runs gates L, F, A, W, B, V and verify_output
./art run $R

# 5. final master
./art final $R --out $R/final
```

**Notes:**

- I never used `ART_STRICT=0` or any other `ART_*` override.
- `./art run` **skips any beat whose `manim/<BID>.mp4` already exists**. After editing a scene, move its
  render aside first (FRICTIONAL.md).
- The cue times in `scenes.py` were measured from these mp3s with
  `ffmpeg -af silencedetect=noise=-35dB:d=0.18`. If the audio is regenerated at a different length,
  re-measure them.
- Pre-checks I ran on single scenes before each 4K build (isolated copies):

```bash
T=$(mktemp -d); cp $R/scenes.py $T/
PYTHONPATH=runtime/manim python3 runtime/qc/static_scene_check.py $T/scenes.py --class <Scene>   # GATE A
python3 runtime/qc/wcag_margin_check.py $R/scenes.py --class <Scene>                              # GATE W
python3 runtime/qc/manim_layout_audit.py scenes.py --class <Scene> --curve-strict                 # GATE B (copy with beat_sheet.json)
```

## 5. Name pronunciation

This is the same as the pitch film (`../BUILD-PROMPT.md` §5). B00 uses IPA variant E,
`ɲˈɑːnɑːsˌuːdʰɚʃɑːn ɑːʃˈoʊk kuːmˈɑːɹ`, recorded in `beat_sheet.json` → B00 → `phoneme_note`.
B19 doesn't speak the name.

## 6. Prompts

All prompts I gave Claude Code for this film are quoted verbatim below, in order. They were sent on
2026-11-22.

**P1**

```
I'm making a 5–7 minute project film for INFO 7375. Professor's required structure, in this exact order:
1. Executive summary: what I'm building and why it matters, with no "how." Must stand alone in the first 60 seconds.
2. Introduction: what others have done (existing tools and research) and what they achieved, then restate why mine matters.
3. Methods: step-by-step build plan, data source, and resources (token credits, accounts, compute).
4. Evaluation: what I'll measure, and what result means it worked or didn't.

Project: a lite decision-memory QA tool. Users ask "why/when/who decided X?" over a synthetic corpus of enterprise docs (meeting notes, emails, tickets) and get grounded answers with citations. It's a scoped-down version of my larger system (Neo4j + LangGraph + FastAPI, hallucination detection).

Create these files:
- script.md: spoken narration with timestamps per section, plain language, ~130 words/min
- slides.md: Marp-format slides, one idea per slide, minimal text
- appendix.md: detailed methods, data schema, eval metrics, and references
- shot-list.md: which slide or screen recording goes with each script line

For prior work, list only things you're confident exist and mark anything I should verify. Ask me about my actual resources (API credits, accounts) before finalizing Methods.
```

**My answers to Claude Code's questions (P1 follow-up)**

- Resources: "Claude Code via NEU, Laptop only, no GPU, MacBook Pro M4"
- Larger system: "Built, can show it"
- Lite stack: "Python + Claude only (Recommended)"
- DecisionTrace evidence: "Yes, same project"

**P2**

```
Approved with changes:
- Keep the larger system labelled "separate project". [Keep L19 / Cut L19 — pick one]
- Methods: state that scripted Claude Code use on my NEU seat is pending confirmation from the professor/NEU IT, and what I'll do if it's not allowed (request API credits).
- References: remove any VERIFY claim from script and slides; keep them in the appendix marked VERIFY.
- Targets: accept as proposed.
- Cut L12 and shorten L26.

Then build the film with the Brutalist toolkit, same as decisiontrace-pitch.mp4: beat_sheet.json from script.md, Kokoro af_heart, Manim scenes, reuse B03a/B03b/B04 frames, plus the full paperwork set (README, FACTCHECK, SOURCES, FRICTIONAL, SHOTLIST, BUILD-PROMPT, PROMPTS) in project-film-v2/. Don't touch the pitch files. Don't commit or push until I've watched the render.
```

The "[Keep L19 / Cut L19 — pick one]" choice was left open. Claude Code kept L19 (FRICTIONAL.md).

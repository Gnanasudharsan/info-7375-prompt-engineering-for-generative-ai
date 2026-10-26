# Remnix Agent — Final Project Pitch Film

| | |
|---|---|
| **Name** | Revan C |
| **Course** | INFO 7375 · Final Project Pitch Film |
| **Working title** | Remnix Agent |
| **Target role** | Software engineer at fintech and crypto companies |
| **Runtime** | 3:51 (231.2 s), 3840×2160, 24 fps |
| **Film** | `remnix-agent-pitch.mp4`: in the Canvas zip. The course repo keeps audio/video out of Git (`.gitignore`), so it is not in the GitHub folder. SHA-256 `55d9b16616854ac8b552918c868cfaefd7177de9b1c8e79cf81f84ded87e2f86` |
| **Made with** | Brutalist toolkit, `show-tell` skill, free local pipeline (Kokoro voice, Manim, Remotion) |

**What the film pitches:** Remnix will be an agent that answers USD→Mexico remittance cost questions using Money Map's data, showing the math and the source behind every number, including stablecoin routes.

**What exists today:** only Money Map (https://mit-dci.github.io/payments-dashboard/), the dashboard I built as a Software Engineer Co-op at the MIT Digital Currency Initiative. Nothing about Remnix is built yet; the film says "will" for all of it. The one mock-up (beat B05) is labelled CONSTRUCTED on screen. The film shows no Claude response.

**The voice is synthetic, and the script was written with Claude.** A free Kokoro voice (`af_bella`) reads a first-person script that I wrote with Claude and reviewed line by line. The opening beat says so on screen: "Synthetic voice (Kokoro) · written with Claude, reviewed by Revan".

**Resubmitted 2026-10-25** after grading: the authorship line now says the script was written with Claude, the film says who I am, a plain-language beat replaces the terms card, the technical beats name the planned design, and FRICTIONAL.md opens with my own answers about why I made each decision. Details at the top of FRICTIONAL.md and in SOURCES.md.

## What is in this folder

| File | What it is |
|---|---|
| `remnix-agent-pitch.mp4` | The rendered film (final master). Canvas zip only; see the SHA-256 above. Rebuilding (below) recreates it. |
| `PROJECT-BRIEF.md` | One page answering the seven questions, ending with "Exists today" and "Will exist" |
| `beat_sheet.json` | Narration, visual plan and measured timing for all 18 beats |
| `BUILD-PROMPT.md` | The prompts and commands that rebuild the film |
| `SOURCES.md` | What I used, what I made, what Claude contributed, third-party assets and licences |
| `FRICTIONAL.md` | Dated log of what went wrong and what I did about it |
| `gate-reports/` | The toolkit's quality-gate reports (start with `GATE-SUMMARY.md`) |
| `build/` | The film's source: `make_sheet.py`, `scene_body.py`, `build_scenes.py`, `finish_audio.py`, `env.sh`, the paperwork the toolkit requires before rendering (`FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`) and the real screenshot in `pantry/` |

## How to rebuild the film

Tested on macOS (Apple silicon) on 2026-10-14. Everything is free and local: no API keys, no accounts, no uploads.

**1. Get the toolkit and install it** (Python 3.14, Node ≥ 20 and ffmpeg needed):

```bash
git clone https://github.com/nikbearbrown/brutalist.art
```

```bash
cd brutalist.art && git checkout 519fcbb96e9e1898d374c8794117cab494ffc5cb
```

```bash
python3.14 -m venv .venv && PATH="$PWD/.venv/bin:$PATH" ./setup --install
```

`./setup` prints an "ElevenLabs reference found" error at the end, caused by files that ship inside the toolkit. The install itself completes (see FRICTIONAL.md).

**2. Fix Kokoro's speech library** (the pip-bundled `espeak-ng` did not load its data on this Mac):

```bash
brew install espeak-ng
```

**3. Build** (run from this folder; one shell session, top to bottom). Re-running `make_sheet.py` after the audio step wipes the measured timings, so run it first or not at all:

```bash
export TOOLKIT="/path/to/brutalist.art"      # your clone from step 1
source build/env.sh                           # toolkit venv + the espeak-ng fix
REEL="$PWD/build"
python3 "$REEL/make_sheet.py"                                        # beat_sheet.json
python3 "$TOOLKIT/runtime/scripts/generate_audio_kokoro.py" "$REEL" --speed 1.05   # narration = the clock
python3 "$REEL/finish_audio.py"                                      # pad bookends, measure
python3 "$REEL/build_scenes.py"                                      # scenes.py = toolkit kits + scene_body.py
(cd "$TOOLKIT" && ./art run "$REEL" --height 2160)                   # render + Gates F L A W B V
(cd "$TOOLKIT" && ./art final "$REEL" --height 2160 --out "$REEL/exports/landscape")   # Gate T + master
```

The master lands at `build/exports/landscape/remnix-agent-pitch.mp4`. `art final` also runs the compiler's own output verification (the render-integrity check). The other checks are listed in `BUILD-PROMPT.md`.

Expected result: 18 beats, about 231.2 s. Kokoro gave the same audio on every run here, so the timings should match `beat_sheet.json`.

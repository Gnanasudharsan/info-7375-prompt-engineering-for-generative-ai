# BUILD-PROMPT — the prompts and commands that rebuild this film

Every command below was run on 2026-10-13 on macOS (Apple Silicon). Cost: $0.00. No API key, no paid service, no upload.

| Tool | Version used |
|---|---|
| brutalist.art | commit `519fcbb` |
| Python (toolkit venv) | 3.14.5, via `uv` |
| Manim / ManimPango | 0.20.1 / 0.6.1 |
| kokoro-onnx (voice `am_michael`, speed 1.1) | 0.4.7 |
| faster-whisper (transcript check only) | 1.2.1, model `base.en` |
| Node | 24.14.0 |
| ffmpeg / ffprobe | 9.0.2 |

Layout: the toolkit and this film folder are siblings.

```text
Final Project Pitch Film/
├── brutalist.art/          ← toolkit (TK), not submitted
└── final-project-film/     ← this folder (REEL)
```

Set these once, from `Final Project Pitch Film/`, before the commands below:

```bash
export TK="$PWD/brutalist.art" REEL="$PWD/final-project-film"
```

## 1. Install the toolkit (free pipeline)

```bash
git clone https://github.com/nikbearbrown/brutalist.art.git && cd brutalist.art && git checkout 519fcbb
uv venv --python 3.14 .venv && source .venv/bin/activate && uv pip install pip
./setup --install      # deps + Remotion node modules + Kokoro model (~340 MB)
```

`./setup` exits 1 before its readiness table, with "ElevenLabs reference found". The files it flags are the toolkit's own example reels under `youtube/brutalist/`. I didn't edit the toolkit; I ran the same checks by hand instead, and all passed:

```bash
for m in kokoro_onnx mutagen PIL numpy manim manimpango faster_whisper scipy; do python3 -c "import $m" && echo "OK $m"; done
ffmpeg -version | head -1
python3 runtime/scripts/setup_smoke_kokoro.py     # [smoke] kokoro synth OK — mean_volume -21.7 dB
```

## 2. Evidence for the claims

```bash
# my project, at the commit the film describes
git clone https://github.com/bagwe-shubham1727/marino-rag.git && cd marino-rag && git checkout dd3205e
uv run --frozen pytest -q                                    # 60 passed
# the site's own search (B04), e.g.:
curl -sL "https://recreation.northeastern.edu/?s=guest+pass"  # result titles listed in evidence/site-search-2026-10-13.txt
# the Alumni page through marino-rag's own parser (B03, B12): see evidence/alumni-page-check-2026-10-13.txt
```

## 3. Beat sheet → audio (audio is the clock)

```bash
cd "$REEL"
python3 make_sheet.py                                                           # 16 beats
python3 ../brutalist.art/runtime/scripts/generate_audio_kokoro.py . --speed 1.1 # every beat
python3 finish_audio.py         # 1.0 s silent tail on BOUT + ffprobe durations → beat_sheet.json
python3 whisper_check.py > evidence/whisper-transcript.txt                      # read it beside the script
```

To re-voice one beat: `generate_audio_kokoro.py . --speed 1.1 --only B14`, then `finish_audio.py` again.

## 4. Paperwork (Gate F refuses to render without it)

```bash
python3 make_shotlist.py                                   # SHOTLIST.md from the sheet + scenes.py
python3 ../brutalist.art/runtime/qc/factcheck_check.py .   # clean, 0 uncovered
python3 ../brutalist.art/runtime/scripts/bookend_check.py .   # 1 deliberate FAIL: wants @NikBearBrown (gate-reports/GATES.md)
```

Don't set `metadata.channel_title`. `compile.py` stamps it below title-safe on the first beat, and Gate V blocks the film for it.

## 5. Pre-flight, render, final

```bash
# Gate A exactly as art run sees it: a scratch folder holding ONLY scenes.py
mkdir /tmp/gA && cp scenes.py /tmp/gA/ && cd /tmp/gA && for c in $(grep -oE '^class [A-Z0-9]+_\w+' scenes.py | cut -d' ' -f2); do
  python3 "$TK/runtime/qc/static_scene_check.py" scenes.py --class $c --quiet; done
# Gate B pre-audit per scene, in the reel folder
for c in $(grep -oE '^class [A-Z0-9]+_\w+' scenes.py | cut -d' ' -f2); do
  python3 "$TK/runtime/qc/manim_layout_audit.py" scenes.py --class $c --curve-strict; done
cd "$TK"
./art run   "$REEL" --height 2160                        # Gates F, L, A, W, B per scene, V on the cut
./art final "$REEL" --height 2160 --out "$REEL/final"    # GATE T type-lock, then the clean master
python3 runtime/scripts/master_check.py    "$REEL" --mp4 "$REEL/final/marino-desk-assistant-pitch.mp4"
python3 runtime/scripts/loudness_check.py  "$REEL" --mp4 "$REEL/final/marino-desk-assistant-pitch.mp4"
python3 runtime/scripts/sharpness_check.py "$REEL"
cp "$REEL/final/marino-desk-assistant-pitch.mp4" "$REEL/Bagwe_Shubham_INFO7375_FinalProjectFilm.mp4"
```

To re-render one scene after editing it, move `manim/<BID>.mp4` and its `media/videos/` folder to `_superseded/`, then run `art run` again. It only renders the scenes whose clip is missing.

## 6. The Claude Code prompts that drove the build

My first message to Claude Code (Opus 5.5) on 2026-10-13, lightly edited for grammar, followed by the assignment text pasted in full:

```text
I want you to do this assignment. First go through the assignment instructions line by line, then plan
the assignment according to them, and only then start the implementation. Once the implementation is
completed, review your work, also review it against the assignment rubric, and show it to me so that I
can submit it directly, and help me push to GitHub wherever necessary. [assignment text]
Make a folder in this working directory for this assignment and then start working.
```

The restart that produced this version (lightly edited):

```text
I think you misinterpreted the assignment. The career-ops and Reallocation Engine are not my projects.
"Your final project is a portfolio piece … that shows you can do the work you want to be hired for."
I feel you should choose a project like marino-rag or EventFlow Engine, which I built. Remove everything
and start from scratch again, and redo all files fresh. Use the project bank we use in career-ops to know
about my projects.
```

Then Claude asked me six questions:
- project: Marino RAG, public data only;
- authorship: EventFlow is mine, marino-rag is mostly AI-written;
- alternatives: manual lookup and the site's search;
- target role: new-grad full-stack SWE;
- model: switch to Claude;
- voice: disclosed Kokoro.

Everything after that is in FRICTIONAL.md. The conversation itself is not included (course rule: no private transcripts).

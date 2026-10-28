# BUILD-PROMPT: CueGate pitch film

One command rebuilds the film: `./rebuild.sh` (see README.md). This file records the prompt that drove the build and every command that produced this submission, in order, with dates. All commands ran on 2026-10-14 on macOS, from the working folder `CueGate/` (toolkit at `CueGate/brutalist.art`, reel at `CueGate/youtube/cuegate-pitch`), unless noted.

## The prompt

The build followed `CLAUDE-CODE-PROMPT.md` (sha256 1e420eb6cc3387943995d77f77dc1ffd55aa02997d4c261e354f7fdcdb0f5eff). It's kept in my working folder and not reproduced here, because its text contains template placeholders, and the zero-open-items rule below forbids those in submitted files. Its content, in order:

- **Non-negotiables:**
  - The honesty rule: past tense only for what exists, "will" for the rest.
  - Nothing invented; any Claude response shown is the real one, with its date.
  - The film is narrated as me, with no instructor persona, handle or credit.
  - Free pipeline only.
  - GATE P is signed by me.
  - FRICTIONAL.md is mine.
  - Constructed material is labelled CONSTRUCTED.
  - No private data.
  - Only my class-repo folder is touched, and nothing is pushed without my word.
  - Failed gates are fixed, never submitted over.
- **Phases:**
  - 0, read the toolkit and report.
  - 1, setup.
  - 2, inventory what exists (exists_today.json).
  - 3, the beat sheet from my narration.
  - 4, GATE P paperwork.
  - 5, build.
  - 6, gates and honesty audit.
  - 7, assemble and submit.

Rules I added during the session, which override the prompt where they conflict:

- **Path overrides:** the working folder is CueGate; the toolkit checkout lives inside it; the reel is at youtube/cuegate-pitch.
- **R1:** tool events go in a build log; FRICTIONAL.md holds only my text.
- **R2:** every change is shown to me and my verdict is recorded word for word.
- **R3:** one command rebuilds the film.
- **R4:** zero open items in any submitted file.
- **R5:** the gate reports explain themselves.
- **R6:** the submission matches the class repo by sha256.
- **R7:** README states that the narration is mine, voiced by Kokoro, and names both local toolkit modifications.
- **R8:** my FRICTIONAL and REVIEW text is recorded verbatim.
- **R9:** a self-audit at every stop.

My decisions during the session included:
- **Opening:** the real screenshot as the cold open, no Claude UI mock-up, a drawn Your Turn card.
- **Counting:** quote marks treated as delimiters (37 characters, B01 branch B).
- **Narration and brief:**
  - Narration and brief edits after the day-one checks.
  - The real reply used in B07, split into B07A and B07B.
  - Tense fixes.
  - A one-page brief.
- **Code:** no toolkit code in the submission.

## Commands, in order (2026-10-14)

### Folder and toolkit
```bash
mkdir inputs && mv README.md inputs/CUEGATE-README.md && mv PROJECT-BRIEF.md NARRATION.md SOURCES.md FRICTIONAL.md inputs/   # plus the film README from the download folder
git clone https://github.com/nikbearbrown/brutalist.art brutalist.art          # HEAD 519fcbb96e9e1898d374c8794117cab494ffc5cb
cd brutalist.art && ./art --list
```

### Setup (Phase 1)
```bash
python3 -m venv CueGate/.venv && source CueGate/.venv/bin/activate        # Python 3.13.2
git -C brutalist.art apply --check ../patches/setup-guard.patch && git -C brutalist.art apply ../patches/setup-guard.patch
cd brutalist.art && bash setup --install          # first run: pycairo build failed (no pkg-config)
brew install pkgconf                              # pkgconf 3.0.8
bash setup --install && bash setup                # all features ready except Manim equation beats (LaTeX; not used)
python3 runtime/scripts/generate_audio_kokoro.py --list-voices | grep -E 'bella|onyx'
python3 -m pip show kokoro-onnx manim | grep Location         # both inside CueGate/.venv
git -C brutalist.art checkout -- runtime/remotion/package-lock.json   # npm rewrote it; no version changed
```

### Day-one evidence (Phase 3 preparation)
- **Web pages:** Subtitle Edit (index, AI Assistant); Editsub; EZTitles (home, Webhelp editing and reading-speed); Netflix partner help 217350977, 360051554394, 215758617 and 219375728; mango.blender.org/about; the Gotham Lab guide; the PySceneDetect detector docs.
- **Web searches:** Blender subtitles, accuracy figures, EZTitles QC, OOONA.
- **Command line:**
```bash
curl -sL https://download.blender.org/demo/movies/ToS/subtitles/TOS-en.srt | grep -c -- '-->'    # 76 cues
curl -s -o /dev/null -w '%{http_code}' https://pypi.org/pypi/cuegate/json                          # 404
gh pr view 25 --repo nikbearbrown/the-reallocation-engine --json author,state,commits,files
gh api "repos/nikbearbrown/the-reallocation-engine/contents/scripts/contrib/2026fa/deepakkts-opt-start-window/lib/gate.mjs?ref=edbac80604162750743e04a2da7fa85c734c0780"
```

### Beat sheet, scenes and paperwork (Phase 3 and 4)
```bash
git -C brutalist.art apply ../patches/outro-handle.patch
cd youtube/cuegate-pitch
python3 make_sheet.py                 # narration verbatim from inputs/NARRATION.md; 16 beats
python3 make_b00.py                   # media/B00.png from my screenshot
python3 build_scenes.py               # scenes.py = pinned kit lines + scenes_film.py
SCENES="B01_Count B02_Gate B03_Rules B04_Alternatives B05_Report B06_Ladder B07A_Evidence B07B_Plan B08_Tiles B09_Scope B10_Filmstrip B11_Split B12_Lists B13_YourTurn"
mkdir -p "$SCRATCH" && cp scenes.py "$SCRATCH/"     # Gate A reads a folder holding only scenes.py
for C in $SCENES; do python3 ../../brutalist.art/runtime/qc/static_scene_check.py "$SCRATCH/scenes.py" --class "$C"; done   # Gate A, 14/14 clean
for C in $SCENES; do python3 ../../brutalist.art/runtime/qc/wcag_margin_check.py scenes.py --class "$C"; done              # Gate W, 14/14 clean
python3 ../../brutalist.art/runtime/scripts/bookend_check.py .
python3 ../../brutalist.art/runtime/qc/factcheck_check.py .
python3 ../../brutalist.art/runtime/qc/beat_lint.py beat_sheet.json
python3 ../../tools/brief_pdf.py ../../inputs/PROJECT-BRIEF.md ../../evidence/PROJECT-BRIEF-one-page.pdf   # 1 page
```
GATE P was signed by me in reel/PEDAGOGY.md.

### Build (Phase 5)
```bash
cd brutalist.art && python3 runtime/scripts/generate_audio_kokoro.py ../youtube/cuegate-pitch          # 16 beats, $0.00
ffmpeg -i mp3/beat-BOUT.mp3 -af "apad=pad_dur=1.0" -c:a libmp3lame -q:a 2 mp3/beat-BOUT.mp3              # 1.0 s outro tail (via a temp file)
python3 runtime/scripts/remotion_scenes.py ../youtube/cuegate-pitch --only BOUT                          # outro card
./brutalist.art/art run youtube/cuegate-pitch --height 2160      # run 1: Gate B strict warning on B05 (label outside safe area), fixed
./brutalist.art/art run youtube/cuegate-pitch --height 2160      # run 2: Gate V low contrast on B08, fixed (dark plinths)
./brutalist.art/art run youtube/cuegate-pitch --height 2160      # run 3: clean
./brutalist.art/art final youtube/cuegate-pitch --height 2160 --out youtube/cuegate-pitch/exports/landscape   # final 1: GATE T contrast on B11, fixed (grey strap)
./brutalist.art/art run youtube/cuegate-pitch --height 2160      # run 4: clean
python3 brutalist.art/runtime/scripts/type_check.py youtube/cuegate-pitch                                  # GATE T PASS
./brutalist.art/art final youtube/cuegate-pitch --height 2160 --out youtube/cuegate-pitch/exports/landscape   # final 2: verified master
```
Each fixed scene had its old clip and the Manim cache moved to `_superseded/` before the re-render. The fixes were measured with the gate's own code first: B08 contrast went from 0.238 to 0.359 on a low-quality test render.

### Gates and captions (Phase 6)
```bash
python3 brutalist.art/runtime/scripts/bookend_check.py youtube/cuegate-pitch
python3 brutalist.art/runtime/qc/factcheck_check.py youtube/cuegate-pitch
python3 brutalist.art/runtime/qc/beat_lint.py youtube/cuegate-pitch/beat_sheet.json
python3 brutalist.art/runtime/scripts/master_check.py youtube/cuegate-pitch --mp4 youtube/cuegate-pitch/exports/landscape/cuegate-pitch.mp4
python3 brutalist.art/runtime/scripts/loudness_check.py youtube/cuegate-pitch --mp4 youtube/cuegate-pitch/exports/landscape/cuegate-pitch.mp4
python3 brutalist.art/runtime/scripts/sharpness_check.py youtube/cuegate-pitch
python3 brutalist.art/skills/make/duration-planner/scripts/pace_check.py youtube/cuegate-pitch
(cd brutalist.art && python3 runtime/scripts/stage_publish.py ../youtube/cuegate-pitch)   # its .srt kept only 3 lines per beat; replaced
python3 youtube/cuegate-pitch/make_captions.py                                           # 68 cues, every word
python3 brutalist.art/runtime/scripts/srt_check.py youtube/cuegate-pitch --srt youtube/cuegate-pitch/cuegate-pitch.srt
ffmpeg -ss "$T" -i youtube/cuegate-pitch/exports/landscape/cuegate-pitch.mp4 -frames:v 1 "gates/visual-qc/frames/${BEAT}_${PCT}_${T}s.png"   # manual visual QC: 48 frames, at 15, 50 and 85% of each beat
```
Results are in gates/INDEX.md.

### Rebuild test and submission (Phase 7)
```bash
TMP="$(mktemp -d)" && cp -R submission "$TMP/sub" && rm "$TMP/sub/cuegate-pitch.mp4" && (cd "$TMP/sub" && ./rebuild.sh "$TMP/work")
(cd submission && find . -type f ! -name MANIFEST.sha256 | sort | xargs shasum -a 256 > MANIFEST.sha256)
```
Rebuild test result (2026-10-14): `./rebuild.sh` from a fresh copy exited 0, and the rebuilt master passed verify_output and is byte-identical to cuegate-pitch.mp4 (sha256 2cde81921594d3e21229facb84a084942a0c6ad5accf6cc282893e18fb7f9316). The first attempt stopped at the voice step because the venv sat on a path too long for espeak-ng; rebuild.sh now places the venv on a short path when needed.

# BUILD-PROMPT — how to rebuild the film

Free pipeline only: Kokoro narration and Manim/ffmpeg rendering run locally. No API keys, no paid generation, no upload.

## 1. Toolkit
```bash
git clone https://github.com/nikbearbrown/brutalist.art ~/Applications/brutalist.art
cd ~/Applications/brutalist.art && git checkout b21f625
python3 -m venv .venv && source .venv/bin/activate && ./setup --install
```
At b21f625, `./setup` exits 1 at its ElevenLabs guard because of the toolkit's own example files (see FRICTIONAL.md, 2026-10-10). Readiness was confirmed by hand instead:
```bash
python3 runtime/scripts/setup_smoke_kokoro.py   # → kokoro synth OK
./art --list                                    # → lists show-tell
```
Run every command below with that `.venv` active.

## 2. Build folder (outside the repo, so audio and render caches stay out of git)
```bash
B=~/Projects/seeded-faults-film-build/seeded-faults-pitch && mkdir -p $B
cp film-source/{scenes.py,make_sheet.py,FACTCHECK.md,SHOTLIST.md,PROMPTS.md} $B/
python3 $B/make_sheet.py        # reads narration from this folder's beat_sheet.json (path set inside make_sheet.py)
```

## 3. Narration (Kokoro am_michael)
```bash
python3 runtime/scripts/generate_audio_kokoro.py $B
# pad the outro with a 1.0 s silent tail, then write the new length to BOUT's actual_duration_s
ffmpeg -y -i $B/mp3/beat-BOUT.mp3 -af "apad=pad_dur=1.0" -c:a libmp3lame -q:a 2 /tmp/bout.mp3 && mv /tmp/bout.mp3 $B/mp3/beat-BOUT.mp3
```
Pronunciation was checked with faster-whisper (base.en) on every beat. B01 and B06 were reworded where Kokoro fused "Claude".

## 4. Render and gates
```bash
./art run   $B --height 2160                               # Gates F, A, W, B, then V on the review cut
./art final $B --height 2160 --out $B/exports/landscape    # GATE T, then the verified master
python3 runtime/qc/factcheck_check.py $B
python3 runtime/scripts/bookend_check.py $B                # expected FAIL, see gate-reports/README.md
```
Output: `$B/exports/landscape/seeded-faults-pitch.mp4` (sha256 `96f04f518e9daef164aa1bb3a910df45efde21e98418d9bfe1421e987961a68e` for this submission's render).

## Prompts given to Claude Code (summarised; full conversation not included)
1. 2026-10-09: explain the assignment; suggest projects for Data Engineering / BI roles; create the submission files.
2. 2026-10-09: guide the alternatives check (Great Expectations, dbt, dbt-expectations); write the sandbox test scripts.
3. 2026-10-10: make the narration flow and sound conversational.
4. 2026-10-10: "lock it, build now". Build the show-tell film with my own bookends and no instructor persona, then run the gates.

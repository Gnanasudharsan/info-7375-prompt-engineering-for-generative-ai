# BUILD-PROMPT — SponsorScout (INFO 7375 Final Project Pitch Film)

Everything needed to rebuild the film. Free and local: Kokoro, Manim, Remotion, ffmpeg,
faster-whisper. Never publishes, never uploads.

---

## 0. Prerequisites

```bash
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art
git checkout 6a8380ae169cca81e0633664a65c958f5c12ab4b   # the revision this film was built on
./setup --install                                          # --install is ONE token
```

Tools used: Manim Community 0.18.1, ffmpeg 9.0.2, Node 24.19.0, Python 3.12 with `kokoro-onnx` 0.6.1,
`manimpango` 0.5.0, `faster-whisper` 1.2.1, Pillow, numpy.

**Toolkit changes:** apply the three commands in `toolkit-changes/README.md`. They add `PitchOutro`
(the author-credited outro), register it, and add the `ART_CHANNEL_TITLE=0` switch. They also
carry my Week 01 Windows fixes.

**Place this folder** at `brutalist.art/youtube/brutalist/final-project-film/`. On Windows I used a
junction, so the files stay in my assignment folder:

```bat
mklink /J "brutalist.art\youtube\brutalist\final-project-film" "<path>\Assignment_Final Project Pitch Film"
```

⚠ Remove a junction with `rmdir`, **never** a recursive delete, which follows it into the folder.

```bash
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ART_CHANNEL_TITLE=0   # Windows: the first two are required
REEL=youtube/brutalist/final-project-film
SLUG=sponsorscout-final-project-pitch
```

## 1. Sheet → audio → word clock

```bash
python $REEL/make_sheet.py                                   # beat_sheet.json (18 beats); exits 2 if a beat is unfinished
python runtime/scripts/generate_audio_kokoro.py $REEL         # Kokoro am_michael, $0.00, ~224 s
python $REEL/make_sheet.py                                   # carries the measured durations forward
python runtime/scripts/align.py $REEL                         # mp3/words.json: "aligned 18, fallback 0"
```

`scenes.py` reads `mp3/words.json`, so every reveal starts on its spoken word. Re-run `align.py`
whenever any beat is re-voiced (`--only <BID>` on both scripts).

## 2. Look before rendering

Render each scene quickly (`manim -ql …`) and look at frames at **50%** (where Gates T and V sample)
and **88%** (the finished picture), with the SAFE box and the caption band (y < −2.5) drawn on.
Every reveal has to land before ~88%, because each scene fades out at its end. Then pre-audit every
scene with Gate B in one pass, so `run.sh` doesn't stop one scene at a time:

```bash
python <toolkit>/runtime/qc/manim_layout_audit.py scenes.py --class <Class> --png --curve-strict   # from the reel folder
```

## 3. Render, compile, Gate V

```bash
python runtime/scripts/remotion_scenes.py $REEL                                 # BOUT (PitchOutro)
ART_BURNIN=0 ART_QC=1 ART_STRICT=1 bash runtime/scripts/run.sh $REEL --height 1080   # Gates L, A, W, B per scene; compile; Gate V
```

`run.sh` renders only scenes whose `manim/<BID>.mp4` is missing. After editing a scene, move its old
clip and `media/videos/` (the Manim cache) to `_superseded/` first.

## 4. Final master (Gate T)

```bash
./art final $REEL --height 1080                  # Gate T (TYPECHECK.md), then renders/$SLUG.mp4
cp renders/$SLUG.mp4 $REEL/$SLUG-nocaptions.mp4
```

## 5. Captions, then Gate V again on the captioned film

```bash
cd $REEL
python tools/make_captions.py                    # captions.srt + captions.ass, from mp3/words.json
ffmpeg -y -i $SLUG-nocaptions.mp4 \
  -vf "subtitles=captions.ass:fontsdir=<relative path to>/brutalist.art/runtime/fonts/Lato/static" \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a copy $SLUG.mp4
cd -
python runtime/qc/final_frame_check.py $REEL --mp4 $REEL/$SLUG.mp4      # Gate V on what you submit
python runtime/scripts/bookend_check.py $REEL
python runtime/qc/factcheck_check.py $REEL
```

The `subtitles=` font path must be **relative**: on Windows an absolute path's drive colon breaks
ffmpeg's filtergraph parser.

## 6. Checks no gate does

- **Listen, blind.** Transcribe each `mp3/beat-*.mp3` with faster-whisper (`small`) and diff it
  against `narration_text` (`_qc/whisper_check.json`). `align.py` places known words, so it can't
  hear a mispronunciation. This caught "two apply" heard as "to apply".
- **Read the frames.** Sample every beat at ~55% and ~90% of the captioned film and look. This caught
  the missing on-screen correction in v1, and the duplicate name under the first caption in v2.

Expected result: **224.0 s, 1920×1080, 24 fps, 18/18 slots; all gates pass** (`_qc/gates-2026-10-14.txt`).

## 7. The paste-ready rebuild prompt (for Claude Code)

```
From my brutalist.art root, rebuild the film at youtube/brutalist/final-project-film.
Do not publish, upload, commit or push.
1. Read FRICTIONAL.md, BUILD-PROMPT.md and toolkit-changes/README.md first. Check the junction,
   the toolkit changes, and export ART_CHANNEL_TITLE=0.
2. python make_sheet.py. If it exits 2, stop and tell me which beat is unfinished.
3. Voice only the beats whose audio is missing (--only), then make_sheet again, then align.py.
4. Quick-render every scene, look at frames at 50% and 88% with the SAFE box and caption band
   drawn. Pre-audit every scene with Gate B. Fix the source, never waive.
5. remotion_scenes.py, then run.sh (ART_STRICT=1, 1080p). If a gate fails, read its report, fix
   the scene, move the failed clip to _superseded/, and re-run.
6. art final, captions, burn-in, Gate V on the captioned film, bookend_check, factcheck.
7. Blind whisper check and a frame read of the captioned film. Report the duration, every gate
   result, and every defect.
```

# BUILD-PROMPT.md

The commands and prompts that rebuild `video.mp4` from this folder. Everything runs locally and free (Kokoro narration, Manim and Remotion renders). There are no API keys, no paid generation and no upload.

## 1. Re-check the evidence (the prototype)

```bash
git clone https://github.com/salonimathure20/the-reallocation-engine
cd the-reallocation-engine
git checkout 81d0161d01c72f02d413d103ae5df1b73127edec   # PR nikbearbrown/the-reallocation-engine#48
npm install                                              # Node 20+
node --test scripts/contrib/2026fa/salonimathure20-opt-countdown/        # expect: pass 12, fail 0
node scripts/contrib/2026fa/salonimathure20-opt-countdown/opt-countdown.mjs
# expect: runway 53 days … 8 roles → scored 6 (Apply 1 · Consider 2 · Skip 3) · blocked for a human 2
git checkout -- course/          # the run rewrites 4 report files; only their timestamps change
```

My output from 2026-10-13 is in `evidence/rerun-2026-10-13.txt`.

## 2. Toolkit setup (once)

```bash
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art
git checkout cd4bf20                       # the commit this film was built with
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
nvm use 20                                 # Remotion needs Node >= 20
./setup --install                          # downloads the Kokoro model
```

## 3. Build the film

```bash
REEL=<this folder>/reel
python3 $REEL/make_sheet.py                                   # writes beat_sheet.json from the narration
python3 runtime/scripts/generate_audio_kokoro.py $REEL        # narration, voice af_heart
ffmpeg -y -i $REEL/mp3/beat-BOUT.mp3 -af apad=pad_dur=1.0 /tmp/bout.mp3 && mv /tmp/bout.mp3 $REEL/mp3/beat-BOUT.mp3
# then set BOUT's actual_duration_s to 5.35 in beat_sheet.json and mp3/timings.json
./art run $REEL --height 2160                                 # Gates L, A, W, layout, V → review cut
./art final $REEL --height 2160 --out $REEL/exports/landscape  # GATE T, then the verified master
cp $REEL/exports/landscape/opt-countdown-pitch.mp4 <this folder>/video.mp4
python3 runtime/scripts/bookend_check.py $REEL                # optional; fails on purpose on the outro (see FRICTIONAL)
```

Optional checks before a full render:

```bash
manim -ql -s $REEL/scenes.py B05_Clock                        # one last-frame still
python3 runtime/qc/static_scene_check.py $REEL/scenes.py --class B05_Clock      # Gate A
python3 runtime/qc/manim_layout_audit.py $REEL/scenes.py --class B05_Clock --curve-strict
```

## 4. Prompts used (Claude Code, 2026-10-13)

I did not keep the verbatim text of every follow-up. These are the prompts with their substance, and what happened to each result.

1. **The assignment.** I pasted the full Final Project Pitch Film assignment and wrote: *"Help me complete and submit this assignment. Do not over complicate the implementation. It should be easy so I can understand it."*
   Result: Claude proposed growing my Reallocation Engine recipe (opt-countdown) into the final project. I accepted.
2. **Project and voice.** Claude asked which project to pitch and which local voice to use, because show-tell's default narrator is the instructor's "Liam" persona, which the assignment forbids. I chose OPT Countdown and Kokoro `af_heart`.
3. **Existing skills.** Claude pointed out that the prototype was mostly typed by Claude Code, so it can't be my evidence for skills I already had. It asked which skills I had before. I said JavaScript/Node. Claude found my public CodeBuddies repo (INFO 6150), and I accepted it as the evidence.
4. **Brief, narration, scenes.** Claude drafted `PROJECT-BRIEF.md`, `reel/make_sheet.py` and `reel/scenes.py`. It used only numbers from my prototype's docs and from a re-run it did on 2026-10-13.
   Revised: four layout fixes after the first contact sheet (overlapping labels in B07, checks touching labels in B08, a stray card in B09, the outro rule crossing the title). Then three Gate V fixes (B05, B07, B09), and the opener's question changed from "apply to" to "get" so that its correction fires (see FRICTIONAL.md).

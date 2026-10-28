# BUILD-PROMPT — how to rebuild the Cite & Seek pitch film

Two parts: the **prompts** that directed the build (summarised by stage; this is not a conversation transcript, which the assignment says to leave out), and the **commands** that rebuild it. Every command actually run, with times and exit codes, is in `BUILD-LOG.txt`.

## 1. Prompts (summarised)

Meena directed Claude Code (Anthropic) through these stages on 2026-10-11 and 2026-10-12. Each stage was reviewed and approved by Meena before the next.

1. **Facts first.** Read `ASSIGNMENT.md`, then extract facts from the Cite & Seek repository read-only (`REPO-FACTS.md`), respecting the repo's deny rules for the locked evaluation files.
2. **Toolkit check.** Inspect the Brutalist checkout read-only: the pipeline, dependencies, the show-tell skill, the beat-sheet schema, every quality gate, and any default that inserts the instructor's identity. Do not edit the checkout.
3. **Identity.** No instructor name, persona or credit line anywhere. Narration in first person as Meena, with the local Kokoro voice `am_michael`. A self-drawn outro with the handle @meenuviji.
4. **Brief and beat sheet.** Draft `PROJECT-BRIEF.md` from the facts, then the beat sheet. Past tense only for what exists, "will" for the rest; mock-ups labelled "constructed" on screen, and future work "constructed · planned".
5. **Script revision.** A course introduction, an untested impact hypothesis, no dates, the pipeline as it exists today (MiniLM, 200-token chunks, top five chunks to Claude Haiku 4.5, cite-or-ABSTAIN), scope, "built so far / will build", and a one-sentence "why". Specific labelled drawings. Tags at size 32.
6. **Evidence.** B14's "retrieval I have run" was held as UNVERIFIED until Meena saved a dated `search` output (`evidence/`).
7. **Segment headings.** A heading at the top left of every drawn beat, by segment, with subheadings taken only from the narration.
8. **Fixes and gates.** Fix layout and gate findings. Run every gate, including render integrity, before each review.

## 2. Environment

| Need | Used for this build |
|---|---|
| Brutalist toolkit | Fork checkout of `nikbearbrown/brutalist.art`, branch `fix/smoke-test-and-local-setup`, commit `5a00f54` (merged 2026-10-12; earlier review cuts used `8b1ae22`) |
| Python | The toolkit's `.venv` (Python 3.12). Activate it first; the system `python3` on the build Mac was 3.9, too old. |
| Manim | The final was rendered with Manim Community 0.20.1, matching the toolkit pin at `5a00f54` (`manim>=0.20,<0.21`). Earlier review cuts used 0.18.1 under the old pin. |
| ffmpeg, Node ≥ 20, LaTeX + dvisvgm, pkg-config/cairo/pango | Installed (versions in `BUILD-LOG.txt`) |
| Kokoro model | `runtime/models/kokoro/` in the toolkit, via `./setup --install` |
| Browser for Remotion | The installed Google Chrome, through the toolkit's own switches (no download) |
| Font | `fonts/EBGaramond-Regular.ttf`, registered inside `scenes.py`. That Manim build did not read `~/Library/Fonts`. |

Set these in every shell:

```bash
TOOLKIT=~/Downloads/brutalist.art            # the Brutalist checkout
FILM=~/Downloads/cite-and-seek-pitch/film    # this film folder (the "reel")
cd "$TOOLKIT" && source .venv/bin/activate
export PYTHONDONTWRITEBYTECODE=1             # keep __pycache__ out of the toolkit checkout
export ART_CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
export ART_CHROME_MODE=chrome-for-testing    # use the installed Chrome; no browser download
```

## 3. Commands, in order

```bash
# 1. Beat sheet (edit make_sheet.py, never beat_sheet.json). Keeps measured audio for unchanged narration.
cd "$FILM" && python3 make_sheet.py

# 2. Narration: local Kokoro, voice am_michael (set in the sheet). Use --only <ids> to re-voice changed beats.
cd "$TOOLKIT" && python3 runtime/scripts/generate_audio_kokoro.py "$FILM"

# 3. Pad the bookends (0.8 s before BIDEA, 1.0 s after BOUT) and measure every beat.
cd "$FILM" && python3 finish_audio.py

# 4. Review cut, with Gates F, L, SHAPE, A, W, B and V. The review cut is written beside the sheet:
#    `art run` has no --out option.
#    Before re-rendering a changed scene, move its manim/<BID>.mp4, any media/<BID>.mp4 and the
#    media/videos cache aside (move media/texts too if a font changed), or the old clip is reused.
cd "$TOOLKIT" && ./art run "$FILM" --height 2160

# 5. Final render: Gate T first, then the verified master, written to --out.
cd "$TOOLKIT" && ./art final "$FILM" --out "$FILM"

# 6. Standalone gates (run each on the cut being checked).
MP4="$FILM/cite-and-seek-pitch.mp4"          # the final; for a review cut use cite-and-seek-pitch-slate.mp4
python3 runtime/qc/factcheck_check.py "$FILM"
python3 runtime/scripts/bookend_check.py "$FILM"
python3 runtime/scripts/type_check.py "$FILM"                 # Gate T, including pixel checks
python3 runtime/scripts/sharpness_check.py "$FILM"   # finds the video by folder name; for the final, run it on a scratch
#   folder named cite-and-seek-pitch holding symlinks to beat_sheet.json and cite-and-seek-pitch.mp4
python3 runtime/scripts/master_check.py "$FILM" --mp4 "$MP4"
python3 runtime/scripts/loudness_check.py "$FILM" --mp4 "$MP4"
python3 runtime/scripts/srt_check.py "$FILM"                  # SKIP: no captions are made
python3 runtime/qc/frame_check.py "$FILM" --height 2160
python3 runtime/qc/content_check.py "$FILM"
python3 runtime/qc/lane_check.py "$FILM"
python3 runtime/qc/banned_card_check.py "$FILM"
python3 runtime/qc/placeholder_check.py "$FILM"

# 7. Render integrity. No toolkit gate has that name; repeat compile.py's verify_output checks by hand.
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height:format=duration -of compact "$MP4"
ffmpeg -v error -xerror -i "$MP4" -f null -                   # full decode; must print nothing
ffmpeg -hide_banner -i "$MP4" -vn -af volumedetect -f null - 2>&1 | grep max_volume   # must be above -80 dB

# 8. Keep the toolkit checkout clean. Remotion renders write runtime/remotion/_bench/ (git-ignored).
rm -rf "$TOOLKIT/runtime/remotion/_bench"
git -C "$TOOLKIT" status --porcelain                         # must print nothing
```

# BUILD-PROMPT

These are the commands that rebuild the film. My working prompts to Claude Code
were many and iterative, were part of private conversations, and are not
reproduced; a reconstructed summary is at the end.

## Prerequisites
- Python 3.10 or newer, in a virtual environment with the toolkit's
  requirements.txt packages. Mine is the toolkit's .venv (Python 3.11.16). My
  Mac's system python3 is 3.9.6, which is too old, so the .venv goes first on
  PATH.
- ffmpeg, and Node 20 or newer.
- The Brutalist toolkit at revision 22264a3 (see SOURCES.md).
- LaTeX is not installed and not needed (no equation beats).
- ./setup --install downloads the Kokoro voice model (about 340 MB) on first
  run.

## Fresh clone
On a fresh clone, ./setup refuses to run because ten example files under
youtube/brutalist/ trip its ElevenLabs guard. I deleted them in my checkout;
the film uses none of them. Delete them too, or skip ./setup if the
dependencies are already installed. With those files deleted, ./setup passes
everything except equation beats (LaTeX), so it exits 1.

## Environment (same for every step)
export PATH="<TOOLKIT>/.venv/bin:<NODE20>/bin:$PATH"
<TOOLKIT> is the brutalist.art checkout and <NODE20> is Node 20's install
folder (Homebrew's node@20 on my Mac). R is the absolute path to this folder
(fall-2026/prasad-s/final-project-film) in my clone of the course repo.

## Steps (run from <TOOLKIT>)
Order from scratch: beat_sheet.json is committed, so the steps below can start
from it. To regenerate it, run make_sheet.py first, then the audio step (which
writes the measured durations into beat_sheet.json), then make_sheet.py again,
which keeps those durations.
1. Narration: python3 runtime/scripts/generate_audio_kokoro.py "$R"
   (voice af_bella, set in make_sheet.py; 175.23 s total, 14 beats)
2. Sheet: python3 make_sheet.py, run inside the reel folder. Do not re-run it
   after ./art final: it drops the build records.
3. Review cut: ./art run "$R" --height 2160, then ./art todo "$R"
4. Final: ./art final "$R" --height 2160 --out "$R/exports/landscape"
   (without --height 2160 the final is 720p and the master check fails)
5. Master check: python3 runtime/scripts/master_check.py "$R" --mp4
   "$R/exports/landscape/gistgap-pitch.mp4"
6. Duration and hash: ffprobe the master and run shasum -a 256 on it. The
   master's duration assertion in step 5 is skipped because clock_check.py is
   missing from the toolkit, so compare ffprobe's duration with 175.23 s.

## Notes
- No overrides were used at any step (ART_STRICT, ART_FACTS and ART_QC at
  their defaults).
- ./art run only renders a scene whose clip is missing. After editing a scene,
  move its manim/ and clips/ files, and media/videos/, into _superseded/ first.
- GATE T runs only at ./art final.
- My master: 3840x2160, 24 fps, h264 + AAC, 175.458 s, 13,515,055 bytes,
  SHA-256 6a0329a02a36558ce1fbddda32adbafac63ceb398a3f3ee475fa320cd804ed04.
  A rebuild may not be byte-identical, so its hash may differ.
- Gate results are in GATE-LOG.md; the receipt (hashes of the inputs and the
  master) is in receipts/, with my home path replaced by <home>.

## Authoring prompt (reconstructed summary, not verbatim)
"In the reel folder, write make_sheet.py (writes beat_sheet.json) and scenes.py
for a show-tell reel of 14 drawn Manim beats, B01-B14, using the narration lines I supplied in the prompt (they are now in
make_sheet.py and beat_sheet.json), voice af_bella, no persona, no instructor name, no
outro or credit line. One simple drawn picture per beat, labelled CONSTRUCTED,
WILL EXIST or REDRAWN as appropriate. Write FACTCHECK.md, SHOTLIST.md and
PROMPTS.md. Do not run any gate until I say so."

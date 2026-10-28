#!/usr/bin/env bash
# make_submission.sh: copy the clean submission set into the course repo folder and build the Canvas zip.
#   bash make_submission.sh            # stage only (no git commands)
# Leaves out caches and render intermediates: manim/ media/ clips/ mp4/ images/ pantry/ audio/ exports/ build-state.json.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HERE/../course/fall-2026/siddi-k/final-project-film"
ZIP="$HERE/../Kommuri_Siddi_INFO7375_FinalProjectFilm.zip"
FILM="Kommuri_Siddi_INFO7375_FinalProjectFilm.mp4"

[ -f "$HERE/exports/$FILM" ] || { echo "no final master at exports/$FILM"; exit 2; }
mkdir -p "$DEST"; find "$DEST" -mindepth 1 -delete   # empty it in place (the folder itself may be open in a shell)
cp "$HERE"/{README.md,PROJECT-BRIEF.md,beat_sheet.json,BUILD-PROMPT.md,SOURCES.md,FRICTIONAL.md,FACTCHECK.md,SHOTLIST.md,PROMPTS.md} "$DEST/"
cp "$HERE/exports/$FILM" "$DEST/"
mkdir -p "$DEST/mp3"   # flat layout: the scripts find beat_sheet.json, fonts/ and mp3/ beside themselves
cp "$HERE"/{make_sheet.py,scene_body.py,assemble_scenes.py,scenes.py,voice.py,pronunciation.json,finish_audio.py,word_clock.py,pronunciation_check.py,make_submission.sh} "$DEST/"
cp -r "$HERE/fonts" "$DEST/"
cp "$HERE"/mp3/beat-*.mp3 "$HERE/mp3/words.json" "$HERE/mp3/timings.json" "$DEST/mp3/"
cp -r "$HERE/evidence" "$HERE/reports" "$DEST/"
printf '__pycache__/\n*.pyc\nmedia/\nmanim/\nclips/\n' > "$DEST/.gitignore"
# Privacy: show my home folder as ~ in the staged logs, reports and receipt (originals stay untouched in this folder).
python - "$DEST" <<'PY'
import re, sys
from pathlib import Path
home = re.compile(r"(?:[A-Za-z]:|/[a-z])(?:\\\\|\\|/)Users(?:\\\\|\\|/)[^\\/\"'\n]+?(?=\\|/)", re.I)
# Manim's log formatter wraps long paths, leaving 'C:\Users\<name> alone at a line end
wrapped = re.compile(r"(?:[A-Za-z]:|/[a-z])(?:\\\\|\\|/)Users(?:\\\\|\\|/)[^\\/\"'\r\n ]+(?=[ \t\r]*$)", re.I | re.M)
n = 0
for f in Path(sys.argv[1]).rglob("*"):
    if f.is_file() and f.suffix.lower() in (".log", ".json", ".md", ".txt", ".patch"):
        with open(f, encoding="utf-8", errors="replace", newline="") as fh:   # keep line endings byte-for-byte
            s = fh.read()
        t = home.sub("~", s)
        t = wrapped.sub("~", t)
        if t != s:
            with open(f, "w", encoding="utf-8", newline="") as fh:
                fh.write(t)
            n += 1
print(f"home path shown as ~ in {n} staged file(s)")
PY
rm -f "$ZIP"
( cd "$DEST/.." && powershell.exe -NoProfile -Command "Compress-Archive -Path 'final-project-film' -DestinationPath '$(cygpath -w "$ZIP")' -Force" )
echo "staged: $DEST"; du -sh "$DEST"; ls -la "$ZIP"

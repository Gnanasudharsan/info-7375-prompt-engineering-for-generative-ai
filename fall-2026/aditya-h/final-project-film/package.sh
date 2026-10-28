#!/bin/sh
# package.sh: builds the submission folder and the Canvas zip from one explicit file list.
# Output: ~/PEAI_Class/submission/final-project-film/ (the GitHub folder contents) and
#         ~/PEAI_Class/Hasija_Aditya_INFO7375_FinalProjectFilm.zip (Canvas; same files).
# It never touches git. Copying into the course repo, committing and pushing happen only on Aditya's go-ahead.
set -e
cd "$(dirname "$0")"
OUT="$HOME/PEAI_Class/submission/final-project-film"
ZIP="$HOME/PEAI_Class/Hasija_Aditya_INFO7375_FinalProjectFilm.zip"
rm -rf "$OUT" && mkdir -p "$OUT"

FILES="README.md productlens-ai-pitch.mp4 PROJECT-BRIEF.md SCRIPT-v2.md beat_sheet.json FRICTIONAL.md SOURCES.md
FACTCHECK.md SHOTLIST.md BUILD-PROMPT.md BUILD-LOG.md PROMPTS.md make_sheet.py scenes_body.py build_scenes.sh
prepare_crops.py package.sh pronunciation/aditya.json
research/baseline-v2-prompt.md research/baseline-v2-dateproof.png research/baseline-v2-shot1.png research/baseline-v2-shot2.png
research/baseline-v2-shot3.png research/baseline-v2-shot4.png research/baseline-v2-shot5.png
research/film-crops/prompt.png research/film-crops/date.png research/film-crops/premise.png research/film-crops/chip.png
research/film-crops/chipzoom.png research/frictional-answers-raw.md research/alternatives.md
research/baseline-prompt.md research/baseline-claude-run1.md research/baseline-claude-run2.md research/baseline-claude-run3.md
research/baseline-claude-metrics.json research/baseline-chatgpt.md research/baseline-chatgpt-screenshot.jpg
reports/gate-T-TYPECHECK.md reports/gate-V-REPORT.md reports/gate-V-contact-sheet.png reports/layout-audit.md
reports/whisper-check.md reports/bookend-check.txt reports/stills-contact-v2.png reports/art-run.log reports/art-final.log"

for f in $FILES; do
  [ -f "$f" ] || { echo "MISSING: $f"; exit 1; }
  mkdir -p "$OUT/$(dirname "$f")" && cp "$f" "$OUT/$f"
done

# privacy scan: no email, keys or passwords in text files
# (patterns match real values, e.g. "api_key=..." or "password: ...", not the words in prose; this script is skipped)
if grep -rIlE --exclude=package.sh -e "hasija\.a@" -e "sk-ant-[A-Za-z0-9]" -e "(api[_-]?key|password|secret)[\"' ]*[:=][\"' ]*[A-Za-z0-9]{6,}" "$OUT"; then echo "PRIVACY HIT, aborting"; exit 1; fi

rm -f "$ZIP" && (cd "$(dirname "$OUT")" && zip -r -X -q "$ZIP" final-project-film -x "*.DS_Store")
echo "files: $(find "$OUT" -type f | wc -l | tr -d ' ')  size: $(du -sh "$OUT" | cut -f1)  zip: $ZIP"

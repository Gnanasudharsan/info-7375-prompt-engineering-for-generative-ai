#!/bin/bash
# record_beat.sh — record my own voice for one beat of the TraceCase pitch.
#
#   ./record_beat.sh BIDEA        (the intro)    ·    ./record_beat.sh B05    (any other beat)
#
# It shows the line to read, records from the MacBook Pro Microphone until you press  q ,
# cleans the take (rumble filter, light noise reduction, trims silence, matches the film's
# loudness of -23.7 LUFS), saves it where the toolkit expects that beat's audio, re-measures
# the beat's length, and re-aligns its word timings. The raw take is kept in takes/.
# First run: macOS will ask to let your terminal use the microphone. Allow it.
set -euo pipefail
cd "$(dirname "$0")"
BID="${1:?usage: ./record_beat.sh BEAT_ID   (e.g. BIDEA)}"
TK="$HOME/Desktop/College/CSYE7375/brutalist-final"
PY="$TK/.venv/bin/python"

LINE=$("$PY" -c "import json,sys;b=[x for x in json.load(open('beat_sheet.json'))['beats'] if x['beat_id']==sys.argv[1]];print(b[0]['narration_text'] if b else '')" "$BID")
[ -n "$LINE" ] || { echo "No beat called $BID in beat_sheet.json"; exit 1; }

# ffmpeg always exits non-zero after listing devices; "|| true" keeps set -e/pipefail from quitting silently.
MIC=$( (ffmpeg -hide_banner -f avfoundation -list_devices true -i "" 2>&1 || true) | sed -n 's/.*\[\([0-9]*\)\] MacBook Pro Microphone.*/\1/p' | head -1)
[ -n "$MIC" ] || { echo "MacBook Pro Microphone not found"; exit 1; }

mkdir -p takes
TAKE="takes/$BID-$(date +%Y%m%d-%H%M%S).wav"
echo
echo "────────── read this, word for word ──────────"
echo "$LINE" | fold -s -w 90
echo "──────────────────────────────────────────────"
read -r -p "Press Enter, wait one second, then read. Press  q  when you finish. "
ffmpeg -hide_banner -loglevel error -f avfoundation -i ":$MIC" -ac 1 -ar 48000 "$TAKE"
echo "Saved raw take: $TAKE"

# A take this quiet means the microphone recorded silence (usually macOS has not given this app mic access).
PEAK=$(ffmpeg -hide_banner -i "$TAKE" -af volumedetect -f null - 2>&1 | sed -n 's/.*max_volume: \(-*[0-9.]*\) dB.*/\1/p')
if awk -v p="${PEAK:--99}" 'BEGIN{exit !(p < -35)}'; then
  echo
  echo "That take is silent (peak ${PEAK} dB), so nothing was changed."
  echo "Give microphone access to the app you're typing in: System Settings > Privacy & Security > Microphone,"
  echo "or run this command in the macOS Terminal app, which asks for access the first time."
  exit 1
fi

# BIDEA and BOUT get padding added later by finish_audio.py, so their clean take is the "-unpad" file.
case "$BID" in BIDEA|BOUT) OUT="mp3/beat-$BID-unpad.mp3" ;; *) OUT="mp3/beat-$BID.mp3" ;; esac
[ -f "$OUT" ] && mkdir -p takes/replaced && cp "$OUT" "takes/replaced/$(basename "$OUT" .mp3)-$(date +%H%M%S).mp3"
ffmpeg -hide_banner -loglevel error -y -i "$TAKE" -af \
"highpass=f=80,afftdn=nf=-25,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.15,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.3,areverse,loudnorm=I=-23.7:TP=-2:LRA=11" \
  -ar 24000 -c:a libmp3lame -b:a 192k "$OUT"

"$PY" finish_audio.py
"$PY" "$TK/runtime/scripts/align.py" . --only "$BID" | tail -1
echo
echo "Done. Listen:   afplay mp3/beat-$BID.mp3"
echo "Not happy? Just run ./record_beat.sh $BID again."

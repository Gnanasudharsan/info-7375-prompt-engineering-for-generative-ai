"""Pad the bookends (0.8 s lead on BIDEA, 1.0 s tail on BOUT) and write the measured clock back.
Run after generate_audio_kokoro.py; idempotent (keeps the unpadded originals as *-unpad.mp3)."""
import json, subprocess
from pathlib import Path
R = Path(__file__).resolve().parent
sheet = json.loads((R / 'beat_sheet.json').read_text())
for b in sheet['beats']:
    path = R / b['audio_file']
    if b['beat_id'] in ('BIDEA', 'BOUT'):
        raw = path.with_name(path.stem + '-unpad.mp3')
        if not raw.exists() or raw.stat().st_mtime < path.stat().st_mtime:
            path.replace(raw)
        effect = 'adelay=800:all=1' if b['beat_id'] == 'BIDEA' else 'apad=pad_dur=1'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', effect,
                        '-c:a', 'libmp3lame', '-b:a', '192k', str(path)], check=True)
    d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                       '-of', 'default=nw=1:nk=1', str(path)]))
    b['actual_duration_s'] = round(d, 3)
    if b['beat_id'] in ('BIDEA', 'BDEFS'):
        b['shot']['remotion']['props']['durationSeconds'] = round(d, 3)
(R / 'beat_sheet.json').write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + '\n')
(R / 'mp3/timings.json').write_text(json.dumps({b['beat_id']: b['actual_duration_s'] for b in sheet['beats']}, indent=2) + '\n')
print('Measured runtime: %.1f s' % sum(b['actual_duration_s'] for b in sheet['beats']))

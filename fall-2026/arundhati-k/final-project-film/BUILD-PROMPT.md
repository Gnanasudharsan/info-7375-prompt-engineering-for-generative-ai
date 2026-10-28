# BUILD-PROMPT — Co-op Sponsor Check

Arundhati Kandelkar · INFO 7375 Final Project pitch · 2026-10-12

Free pipeline only: no API keys, no accounts, no paid calls, no upload.

## 0. Prerequisites

```bash
git clone https://github.com/nikbearbrown/brutalist.art brutalist-final   # built at b21f625
cd brutalist-final
/opt/homebrew/bin/python3.12 -m venv .venv        # NOT macOS's python3 3.9 — onnxruntime has no 3.9 build
export PATH="$PWD/.venv/bin:$PATH"
./setup --install
```

`./setup --install` installs everything, then exits 1 at its own ElevenLabs guard because a toolkit example
(`youtube/brutalist/claude-liam-brutalist-command-setup/SCRIPT.md`) quotes the guarded string. Nothing is
wrong with the install; verify it directly:

```bash
ffmpeg -version | head -1 && node --version && python3 -c "import kokoro_onnx, manim, faster_whisper, PIL; print('ok')"
python3 runtime/scripts/setup_smoke_kokoro.py      # expect "kokoro synth OK"
```

## 1. Local toolkit edit (required — the assignment forbids the instructor's credit line)

`runtime/remotion/src/scenes/ClaudeTitleOutro.tsx` hard-codes `@NikBearBrown`. Add an optional `handle`
prop and render `{handle || HANDLE}`:

```diff
   lectureLayout: z.boolean().optional(),
+  handle: z.string().optional(),
 });
-export const ClaudeTitleOutro: React.FC<ClaudeTitleOutroProps> = ({ title, slug, mascotAnimation, lectureLayout }) => {
+export const ClaudeTitleOutro: React.FC<ClaudeTitleOutroProps> = ({ title, slug, mascotAnimation, lectureLayout, handle }) => {
-        {HANDLE}
+        {handle || HANDLE}
```

Second local edit (GATE T §8.1): in `runtime/remotion/src/scenes/ClaudeDefinitions.tsx` set
`const meanSize = 50;` (was 48 — its lowercase definitions measured 40 px against the 41 px floor at 4K).

## 2. Check the evidence first

From my fork of the Reallocation Engine at `03784b0`:

```bash
python3 scripts/contrib/2026fa/arundhatik26-coop-sponsor-swe-15-1252/coop_sponsor_check.py
python3 -m unittest discover -s scripts/contrib/2026fa/arundhatik26-coop-sponsor-swe-15-1252/tests
```

Must match `evidence/recipe-rerun-2026-10-10.txt` (7 roles, 17 tests OK). If they disagree, the film is wrong.

## 3. Build

Reel folder: `info-7375-prompt-engineering-for-generative-ai/youtube/coop-sponsor-check-pitch/`
(holds `make_sheet.py`, `scenes.py`, FACTCHECK/SHOTLIST/PROMPTS/SOURCES).

```bash
REEL=../info-7375-prompt-engineering-for-generative-ai/youtube/coop-sponsor-check-pitch
python3 $REEL/make_sheet.py
python3 runtime/scripts/generate_audio_kokoro.py $REEL          # voice bf_emma, from metadata.voice_kokoro
# pad the outro with 1.0 s of silence, then write ffprobe durations back into the sheet
ffmpeg -y -i $REEL/mp3/beat-BOUT.mp3 -af apad=pad_dur=1.0 $REEL/mp3/_p.mp3 && mv $REEL/mp3/_p.mp3 $REEL/mp3/beat-BOUT.mp3
python3 - <<'EOF'
import json, subprocess; p='../info-7375-prompt-engineering-for-generative-ai/youtube/coop-sponsor-check-pitch/beat_sheet.json'
d=json.load(open(p)); base=p.rsplit('/',1)[0]
for b in d['beats']:
    t=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',base+'/'+b['audio_file']]))
    b['actual_duration_s']=round(t,3)
    if b['shot'].get('remotion'): b['shot']['remotion']['props']['durationSeconds']=round(t,2)
json.dump(d,open(p,'w'),indent=2,ensure_ascii=False)
EOF
python3 runtime/qc/factcheck_check.py $REEL && python3 runtime/scripts/bookend_check.py $REEL
./art run   $REEL --height 2160
./art final $REEL --height 2160 --out $REEL/exports/landscape
```

Whisper-check the narration after any re-voice (Kokoro misread "U.S." and "a pitch by" + my name).

## 4. Prompt used with Claude Code

> Read `skills/make/show-tell/SKILL.md` completely. Build the pitch film at
> `youtube/coop-sponsor-check-pitch/` from `PROJECT-BRIEF.md` and `SCRIPT-DRAFT.md`. The assignment
> overrides the skill: narrate in my name with Kokoro `bf_emma`, no instructor name, persona, handle or
> portrait. Past tense only for what `evidence/` shows; tag every body beat EXISTS, PLANNED or CONSTRUCTED.
> Audit every frame, bookends included, against the honesty rule. Fix any gate failure; do not ship over it.

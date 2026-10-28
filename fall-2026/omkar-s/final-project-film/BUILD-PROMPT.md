# BUILD-PROMPT — rebuild the BiteCheck pitch film

## 1. The prompts that produced this build
Given to Claude Code (Claude desktop app, Opus 5.5), in order, with the Canvas assignment text pasted above the first:

1. 2026-10-11: `explaiin me the assignment and give me detailed summary`
2. `so this assignment is about building a portfolio?`
3. `if i give you my resume can you move forward?` (then the résumé PDF path; the résumé is not in this folder)
4. 2026-10-12: `go with option A`
5. 2026-10-13: `gather all the requirements i dont want to loose marks`
6. `now as a TA rate my assignment`
7. `i want full marks .. reslve the gaps`
8. 2026-10-21 (after grading): `check why the dedeuctions were made and fix it … make sure the pitch video contains who is doing it, explains what you are doing easily to a 5 year old or a non-technical person clearly and make sure it is concise and explains your project to the fullest technical detail in the short format.`
9. `fix everything`
10. 2026-10-22: `go through the assignment after that read the comments. Fix all the issues`. Omkar then gave his mutant plan in chat, asked Claude to create the private repo and run CI (`fix this`), and asked Claude to write up the results (`write it`), which went in as a Claude-labelled log entry.

## 6. Re-run the CI evidence (B10, B13)
The loan app is in the private repo `O7580/instaloan-los`. Locally: `cd LOS/backend && npm ci && npm run typecheck && npm test && npm run test:mutants`. On GitHub, every push runs `.github/workflows/backend-ci.yml`. The first run (39843450055, 2026-10-22) is saved in `evidence/ci/`.

Every decision after that is recorded in `FRICTIONAL.md`.

## 2. Paste-ready prompt to rebuild it
```text
Rebuild the BiteCheck pitch film in this folder with the free Brutalist pipeline.
Folder: <absolute path to final-project-film>. Toolkit: a sibling brutalist.art checkout at b21f625.
1. python3 make_sheet.py  (writes beat_sheet.json; keeps measured audio if narration is unchanged)
2. Regenerate narration with Kokoro am_michael (audio is the clock).
3. Pre-audit each scene: static_scene_check.py from a folder holding only scenes.py,
   and manim_layout_audit.py --curve-strict in this folder. Fix the scene, never the gate.
4. art run --height 1080 (Gates A, B, V + review cut), look at frames, then art final --height 1080.
5. Run bookend_check.py and record its result (it fails OUTRO by design; see FRICTIONAL).
No paid calls, no API keys, no publishing.
```

## 3. Exact commands
From a parent folder containing `brutalist.art/` and `final-project-film/`:

```bash
# toolkit (macOS). Week-1 setup notes apply: brew install ffmpeg cairo pkg-config pango
git clone https://github.com/nikbearbrown/brutalist.art && (cd brutalist.art && git checkout b21f625)
cd brutalist.art && uv venv --python 3.12 .venv && source .venv/bin/activate \
  && ./setup --install && uv pip install -r requirements.txt && cd ..
# Kokoro model files go in brutalist.art/runtime/models/kokoro/ (see generate_audio_kokoro.py header)

cd final-project-film && python3 make_sheet.py && cd ..
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py "$PWD/final-project-film"

brutalist.art/art run   "$PWD/final-project-film" --height 1080
brutalist.art/art final "$PWD/final-project-film" --height 1080 --out "$PWD/final-project-film/final"
python3 brutalist.art/runtime/scripts/bookend_check.py "$PWD/final-project-film"
```

The evidence run (`evidence/los_smoke_test.txt`) used the local InstaLoan backend (`npm --prefix LOS/backend start`, port 4000) and three `curl` calls: `POST /api/applications` with monthly income 14999, then 15000, then `POST /api/applications/<id>/disburse` on the second application.

## 4. Re-run the Stryker evidence (B06)
From a scratch folder holding a copy of `LOS/backend/src`, `tsconfig.json`, and `evidence/stryker/stryker.config.json`:

```bash
echo '{"name":"los-stryker-scratch","private":true,"type":"module"}' > package.json
npm install --save-dev @stryker-mutator/core@8.7.1 typescript@5.5.4
npx stryker run          # 92 mutants; open reports/mutation/mutation.html
```

No tests exist, so the command runner (`node -e "process.exit(0)"`) makes every mutant "survive". The run only lists what Stryker generates. The HTML report it writes embeds the loan app's source, so it is not in this folder (removed 2026-10-22). `evidence/stryker/stryker_summary.txt` holds the counts and the rule-line mutants.

## 5. Pronunciation check
`evidence/pronunciation_check.txt` is a Whisper-tiny transcript of each `mp3/beat-*.mp3`, diffed against `narration_text`.

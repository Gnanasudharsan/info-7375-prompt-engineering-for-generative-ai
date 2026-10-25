# API Impact — final project pitch film

- **Name:** Chethan Gowda (GitHub: chethangowda-git)
- **Course:** INFO 7375, fall 2026
- **Working title:** API Impact
- **Target role:** AI Software Development Engineer
- **Runtime:** 3:59 (239.6 s), 3840×2160 (re-cut 2026-10-25 per TA feedback)
- **Film:** `api-impact-pitch.mp4`
- **Status:** a pitch. The tool is not built yet. The film labels everything REAL, CONSTRUCTED or PLANNED.

**One sentence:** Before a backend change merges, API Impact will find the frontend lines it breaks and open a draft fix PR in each frontend repo, linked to the backend PR.

## What's in this folder
| File | What it is |
|---|---|
| `api-impact-pitch.mp4` | the rendered film |
| `PROJECT-BRIEF.md` | the seven answers, plus "exists today" and "will exist" |
| `beat_sheet.json` | narration and visual plan (the build's source of truth) |
| `BUILD-PROMPT.md` | the prompts and commands that rebuild it |
| `SOURCES.md` | what I made, what Claude contributed, third-party material and licences |
| `FRICTIONAL.md` | dated log: my own entries first, then a Claude-drafted summary |
| `FACTCHECK.md` | every claim in the film, its source and its status |
| `CHECKS-REPORT.md` | proof-gate report written before the first render |
| `evidence/` | my oasdiff run on a planted rename in my RealWorld fork (2026-10-25) |
| `_qc/REPORT.md`, `_qc/contact_sheet.png` | Gate V visual-QC report |
| `scenes/ApiImpactPitch.tsx` | the film's custom Remotion scenes (13 `Aip*` compositions) |
| `scenes/Root.tsx.patch` | registers those compositions in the toolkit's `Root.tsx` (made against brutalist.art @ `29ba0e8`) |

## How to rebuild
You need the brutalist.art toolkit cloned next to `fall-2026/`, with its `.venv` and Kokoro model set up (`./setup --install`). Then:

```bash
cd brutalist.art && source .venv/bin/activate
# install the film's scenes from this folder into the toolkit
cp ../fall-2026/chethan-t/final-project-film/scenes/ApiImpactPitch.tsx runtime/remotion/src/
git apply ../fall-2026/chethan-t/final-project-film/scenes/Root.tsx.patch
python3 runtime/scripts/generate_audio_kokoro.py ../fall-2026/chethan-t/final-project-film
./art run   ../fall-2026/chethan-t/final-project-film --height 1080
./art final ../fall-2026/chethan-t/final-project-film --out ../fall-2026/chethan-t/final-project-film
```

Full steps are in `BUILD-PROMPT.md`.

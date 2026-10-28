# Final Project Pitch Film: README Checker

- **Name:** Lavanya R
- **Course:** INFO 7375, Final Project Pitch Film
- **Working title:** README Checker: *Does the README actually work?*
- **Target role:** Software Engineer
- **Runtime:** 3 min 29 s (3840×2160, 24 fps)
- **Made with:** [Brutalist](https://github.com/nikbearbrown/brutalist.art) (commit `519fcbb`), show-tell format, free local pipeline (Kokoro voice, Manim, Remotion, ffmpeg)

## What the film pitches
A planned command-line tool (Python, Claude, Docker) that will run a README's setup steps, one at a time, inside a throwaway container. It will report pass, warning or fail for each step, citing the README line it came from and the real error output.

**Nothing in the tool is built yet.** The only real evidence is two manual README runs I did on 2026-10-13, and my existing public repo. See [PROJECT-BRIEF.md](PROJECT-BRIEF.md).

## Files

| File | What it is |
|---|---|
| `readme-checker-film.mp4` | The rendered film |
| `PROJECT-BRIEF.md` | The seven answers, plus "exists today" and "will exist" lists |
| `beat_sheet.json` | Narration and visual plan for all 20 beats |
| `BUILD-PROMPT.md` | Prompts and commands that rebuild the film |
| `SOURCES.md` | What I used, what I made, what Claude contributed, licences |
| `FRICTIONAL.md` | Dated log of what broke and what I did instead |
| `gate-reports/` | Brutalist's quality-gate reports (Gate V, Gate T, layout audit, fact-check, shot list) |
| `build/` | The source files needed to rebuild: `make_sheet.py`, `scene_body.py` |

## How to rebuild the film
Full steps are in [BUILD-PROMPT.md](BUILD-PROMPT.md). In short:

```bash
git clone https://github.com/nikbearbrown/brutalist.art ~/brutalist.art
cd ~/brutalist.art && git checkout 519fcbb && ./setup --install
```

Then, from a working folder (for example `~/INFO7375/readme-checker-film/`) containing the files in `build/`:

```bash
python3 make_sheet.py
python3 ~/brutalist.art/runtime/scripts/generate_audio_kokoro.py .
cat ~/brutalist.art/skills/make/show-tell/templates/iso_kit.py scene_body.py > scenes.py
cd .. && ~/brutalist.art/art run readme-checker-film --height 2160
~/brutalist.art/art final readme-checker-film --height 2160 --out readme-checker-film/exports/landscape
```

Two notes on rebuilding:
- `./setup --install` exits with code 1 at this commit, because of a guard that flags the toolkit's own example files. The install itself completes. See FRICTIONAL.md.
- Re-voicing the last beat (B14) needs a 1 s silent tail added afterwards. See BUILD-PROMPT.md.

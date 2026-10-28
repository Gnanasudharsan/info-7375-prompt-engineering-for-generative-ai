# Final Project Pitch Film: CueGate

| | |
| --- | --- |
| Name | Deepak Kumaran Thoppudu Sudharsanan |
| Working title | CueGate |
| Target role | Applied AI Engineer / AI Engineer |
| Runtime | 3:40.9 (220.92 s, measured with ffprobe on cuegate-pitch.mp4) |
| Film | cuegate-pitch.mp4 (3840x2160, 24 fps, h264 + AAC, 9.8 MB); captions in cuegate-pitch.srt |
| Toolkit | Brutalist (github.com/nikbearbrown/brutalist.art at commit 519fcbb), skill show-tell, Kokoro voice am_onyx, free local pipeline |

The narration text is mine. It is voiced by Kokoro am_onyx because the assignment requires the free local pipeline.

## What is in this folder

- `cuegate-pitch.mp4`: the rendered film. `cuegate-pitch.srt`: its captions (every word of the narration).
- `PROJECT-BRIEF.md`: the seven answers, ending with Exists today and Will exist. It renders to one page (`evidence/PROJECT-BRIEF-one-page.pdf`) at US Letter, 11 pt Times New Roman, 1.2 line spacing, 1-inch margins (`tools/brief_pdf.py`, headless Chrome).
- `beat_sheet.json`: narration and visual plan, 16 beats, with the measured durations.
- `BUILD-PROMPT.md`: the prompt and the commands that built the film, in order, with dates.
- `SOURCES.md`: what I used, what I made, what Claude contributed, and every third-party asset with its licence.
- `gates/`: the toolkit's gate reports. `gates/INDEX.md` lists each gate, its command, its result and its report.
- `FRICTIONAL.md`: my dated working log.
- `rebuild.sh`: rebuilds the film with one command (below).
- `reel/`: code and paperwork written for this film. `scenes_film.py` (the Manim scenes), `build_scenes.py` (assembles scenes.py at build time), `make_captions.py`, `make_sheet.py` and `make_b00.py` (the beat sheet and the B00 still), and the GATE P paperwork (FACTCHECK.md, SHOTLIST.md, PROMPTS.md, PEDAGOGY.md with my signature). `reel/media/B00.png` is my screenshot as placed in the film.
- `patches/`: the two local toolkit patches.
- `evidence/`: the planning document (`CUEGATE-PLAN.md`) and PDF, the Claude exchange shown in the film (`claude-exchange.md`, `claude-exchange.png`), the dated day-one source checks (`day-one/`), `exists_today.json`, and the one-page brief render.
- `tools/brief_pdf.py`: renders the brief to PDF and counts its pages.

Files written in my local working folder are named in some documents by their working paths. In this folder they are: `inputs/claude-exchange.*` → `evidence/claude-exchange.*`; `inputs/CUEGATE-README.md` → `evidence/CUEGATE-PLAN.md`. `inputs/NARRATION.md` (my narration source) is not included; its text is in `beat_sheet.json`. `make_sheet.py` and `make_b00.py` read those working paths and are included to show how the sheet and the still were made; `rebuild.sh` doesn't need them.

## Two local modifications to the toolkit

`rebuild.sh` applies both. Both are in `patches/` and neither is committed to the toolkit.

1. `patches/setup-guard.patch` (filtered setup): the toolkit's `setup` refuses to run because its ElevenLabs guard matches the toolkit's own `youtube/` fixture files. The patch adds `--exclude-dir=youtube` to that guard's two grep calls, so it still scans everything else.
2. `patches/outro-handle.patch` (outro handle): the toolkit's outro card hard-codes the instructor's channel handle. The patch adds optional `handle` and `showMascot` props, with the defaults unchanged. This film sets the handle to my name and turns the mascot off.

Two more build-time details, neither a change to the toolkit: `rebuild.sh` restores one lockfile that `npm install` rewrites (no package versions change), and `reel/build_scenes.py` copies the show-tell kit's drawing code from the pinned checkout at build time, so no toolkit code is included here.

## Rebuild

Prerequisites (versions this film was built with):

- Python 3.13 (3.13.2)
- Node 24 or newer (v24.21.0) and npm (11.19.0)
- ffmpeg and ffprobe (9.0.1): `brew install ffmpeg`
- Homebrew pkgconf (3.0.8): `brew install pkgconf`. manim's pycairo needs it.
- Homebrew cairo (1.18.4): `brew install cairo`
- git and curl. About 1 GB of free disk; setup downloads the 340 MB Kokoro model.

`rebuild.sh` checks these first and stops with a message naming anything missing.

```bash
./rebuild.sh
```

It builds everything in a new `./_rebuild/` folder and writes the film to `_rebuild/out/cuegate-pitch.mp4` and the gate reports to `_rebuild/gates/`. If the folder's path is long, the Python virtual environment goes in a short temporary folder instead (`/tmp/cgv.*`), because the Kokoro voice's espeak-ng library can't read its data from a path longer than about 150 characters; the script says when it does this. No keys, no paid services, nothing published.

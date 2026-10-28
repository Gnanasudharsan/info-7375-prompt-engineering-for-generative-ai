# Electricity Supplier Check: final project pitch film

- **Name:** Hemanth Rayudu
- **Course:** INFO 7375, Prompt Engineering & Agentic AI (Fall 2026)
- **Working title:** Electricity Supplier Check
- **Target role:** AI Engineer (agentic systems), ideally at energy companies
- **Runtime:** 3:38 (217.7 s), 3840×2160, 24 fps
- **Film:** `exports/landscape/electricity-supplier-check-pitch.mp4`

> **Where the film and audio are.** The course repository keeps audio and video out of Git (its `.gitignore` blocks `*.mp3` and `*.mp4` at any depth). So the GitHub copy of this folder has no `.mp4` and no `mp3/*.mp3`; everything else is identical. The film and the narration audio are in the Canvas zip, `Rayudu_Hemanth_INFO7375_FinalProjectFilm.zip`. The audio can also be regenerated (see below).

## What the film is

A pitch for a tool that will read a Massachusetts electric bill and tell you exactly how much more, or less, you paid than your utility's default basic service rate, with the math shown. Claude will read and explain; Python will do all the math.

**Nothing is built yet.** Today the only things that exist are this film, its paperwork and `PROJECT-BRIEF.md`. Every statement about the tool says "will". Every mock-up is tagged CONSTRUCTED (or PROPOSED) on screen. No real bill appears, and no Claude response is shown.

The film answers the assignment's seven questions in 13 beats, in show-tell format: one simple drawn picture per beat, minimal labels, and the narration carries the explanation. The beat-by-beat map is in `PEDAGOGY.md`.

## How to rebuild it

Requirements:
- the Brutalist toolkit (https://github.com/nikbearbrown/brutalist.art, commit `519fcbb`), cloned next to this project and set up with `./setup --install` inside its `.venv`;
- ffmpeg and Node ≥ 20.

```bash
cd <path>/brutalist.art && source .venv/bin/activate
export ART_HOME="$PWD"
R=<path to this folder>
python3 "$R/build_scenes.py"                               # scenes.py = toolkit iso kit + scene_body.py
./art run "$R" --height 2160                               # gates + review cut (uses mp3/ as the clock)
./art final "$R" --height 2160 --out "$R/exports/landscape" # GATE T + verified 4K master
```

The audio in `mp3/` is the master clock. In the GitHub copy (no `.mp3` files), generate it first: run `runtime/scripts/generate_audio_kokoro.py "$R"` and then `runtime/scripts/align.py "$R"`.

The full prompt and every command are in `BUILD-PROMPT.md`. The run costs $0.00: no API keys and no upload.

## Files

| File | What it is |
|---|---|
| `PROJECT-BRIEF.md` | The seven answers, ending with "exists today" and "will exist" |
| `beat_sheet.json` | Narration, visual plan, timings and build stamps |
| `scene_body.py`, `build_scenes.py`, `scenes.py` | The drawings (Manim) and the script that pastes the toolkit's iso kit in |
| `mp3/` | Narration audio (Kokoro `am_onyx`; the `.mp3` files are in the Canvas zip only) and the word clock (`words.json`, in both copies) |
| `BUILD-PROMPT.md` | The prompts and commands that rebuild the film |
| `SOURCES.md` | What I used, what I made, what Claude contributed, third-party licences |
| `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, `PEDAGOGY.md` | Claim checks, shot list, generation prompts (none), beat-by-beat pedagogy |
| `CHECKS-REPORT.md`, `TYPECHECK.md`, `MASTERCHECK.md`, `LOUDNESS.md`, `_qc/` | The toolkit's gate reports and the visual-QC contact sheets |
| `FRICTIONAL.md` | My dated log of what went wrong and what I did about it |

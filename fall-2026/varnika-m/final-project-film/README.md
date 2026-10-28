# Terraform Docs, Quoted — final project pitch film

**Name:** Varnika M · INFO 7375 · Final project pitch film
**Working title:** Terraform Docs, Quoted
**Target role:** AI Software Developer / Software Engineer
**Runtime:** 3:05 (185.3 s, measured from the rendered file)
**Film:** `final/varnika-final-project-pitch.mp4`, 3840×2160, 24 fps, H.264/AAC, 8.7 MB, sha256 `60c1f4edde7c66b722af0336f55727331d13f8b4e2509420588b43e8336c2296`. Rendered 2026-10-14.

**One sentence:** a Python tool that will answer questions about Terraform's AWS provider from the
official docs, and back every answer with the exact docs line it came from, or say "not in the
docs."

## Files

| File | What it is |
|---|---|
| `final/varnika-final-project-pitch.mp4` | The film |
| `PROJECT-BRIEF.md` | The seven answers, ending with "exists today" and "will exist" |
| `beat_sheet.json` | Narration and visual plan, 16 beats, with measured durations (written by `make_sheet.py`) |
| `scenes.py` | Every scene, drawn in Manim |
| `FACTCHECK.md` | Every claim with its source |
| `SHOTLIST.md`, `PROMPTS.md` | Toolkit paperwork (pictures and labels; no generation prompts) |
| `SOURCES.md` | Sources, what I made, what Claude contributed, licences, the synthetic-voice disclosure |
| `FRICTIONAL.md` | Dated log |
| `BUILD-PROMPT.md` | Prompts and commands that rebuild the film |
| `gate-reports/` | The toolkit's quality-gate reports, and what failed on the way |
| `evidence/` | The pinned docs page and licence, the licence check, and my screenshots of the two alternatives |

## How to rebuild

Full steps are in `BUILD-PROMPT.md`. In short, with brutalist.art at `b21f625` and its virtual
environment active:

```bash
python3 make_sheet.py                                   # only before re-voicing
python3 <brutalist.art>/runtime/scripts/generate_audio_kokoro.py <this folder>
./art run   <this folder> --height 2160
./art final <this folder> --height 2160 --out <this folder>/final
```

## Disclosure

The narration is a synthetic Kokoro voice (`am_onyx`), first person, as me. Who did what is in
`SOURCES.md`.

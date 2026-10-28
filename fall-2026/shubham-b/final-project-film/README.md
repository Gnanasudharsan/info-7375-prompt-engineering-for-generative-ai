# Marino Desk Assistant: A Pitch — final project pitch film

| | |
|---|---|
| **Name** | Shubham Bagwe (GitHub `bagwe-shubham1727`) · INFO 7375, Fall 2026 |
| **Project (working title)** | **Marino Desk Assistant** (repo [`marino-rag`](https://github.com/bagwe-shubham1727/marino-rag)): a chat assistant that will answer front-desk questions (fees, hours, guest rules) at the Marino Recreation Center, Northeastern University's campus gym, from the university's public recreation website, quoting the page it used and saying "I don't know" when the site doesn't say |
| **Target role** | New-grad full-stack software engineer |
| **Runtime** | **3:57** (237.4 s master; 237.1 s of measured narration), 16 beats |
| **Film** | `Bagwe_Shubham_INFO7375_FinalProjectFilm.mp4`, 3840×2160, 24 fps. **In the Canvas submission only.** A TA confirmed on 2026-10-13: "Only beat sheet to git. Video to Canvas." sha256 `ea18ed8b5f405bda07ee334e1704ec26729b1ab62d56bf98ce0f46bf389cab99` lets a grader match the Canvas file to this build |
| **Stack (project)** | Python, FastAPI, sentence-transformers (BGE embeddings + cross-encoder rerank), Chroma, Next.js/TypeScript; answers moving from OpenRouter to **Claude** |
| **Made with** | brutalist.art (commit `519fcbb`), show-tell style; free local pipeline only (Kokoro voice, Manim). Cost $0.00 |
| **Narration** | A script Claude drafted from my decisions and I approved, spoken by a local synthetic Kokoro voice (`am_michael`). Both are disclosed in the first beat, aloud and on screen |

## What the film says, in one breath

A desk assistant at Marino (Northeastern University's recreation center) with a member waiting has two options today: scroll a ~780-word page of fee tables, or use the site's search, which returns pages, not answers. Marino Desk Assistant will give one answer, quote the line and link it, and refuse when the site doesn't say. A first version exists (`marino-rag`, 60 tests passing on 2026-10-13). What I will build:
- a public-only index;
- Claude under a prompt contract;
- a 50-question evaluation, with my own answer keys, that lists every miss.

## Read in this order

| # | File | What it is |
|---|---|---|
| 1 | `Bagwe_Shubham_INFO7375_FinalProjectFilm.mp4` (Canvas) | The film |
| 2 | `PROJECT-BRIEF.md` | The seven answers on one page, ending with *exists today* / *will exist* |
| 3 | `beat_sheet.json` | Narration and visual plan, beat by beat. Each beat names the question it answers and its claim status (`exists`, `planned`, `framing`) |
| 4 | `FACTCHECK.md` | Every claim in the film, its verdict, and its source (27 rows) |
| 5 | `gate-reports/` | The toolkit's own quality-gate reports and build logs (start with `gate-reports/GATES.md`) |
| 6 | `FRICTIONAL.md` | Dated log of what happened, including the first pitch I rejected and why |
| 7 | `SOURCES.md` | What I used (with licences), what I made, what Claude contributed |
| 8 | `BUILD-PROMPT.md` | The prompts and commands that rebuild the film |
| 9 | `evidence/` | Checks run on 2026-10-13: marino-rag tests, the site's search, the Alumni page, the narration transcript |

Also included: `SHOTLIST.md` and `PROMPTS.md` (Gate F's work order and its "no generation prompts" note), and the build sources `make_sheet.py`, `scenes.py`, `finish_audio.py`, `whisper_check.py` and `make_shotlist.py`.

## How to rebuild the film

Full detail is in `BUILD-PROMPT.md`. In short, with brutalist.art cloned beside this folder (at commit `519fcbb`) and its venv active:

```bash
python3 make_sheet.py
python3 ../brutalist.art/runtime/scripts/generate_audio_kokoro.py . --speed 1.1
python3 finish_audio.py && python3 make_shotlist.py
cd ../brutalist.art
./art run   ../final-project-film --height 2160
./art final ../final-project-film --height 2160 --out ../final-project-film/final
cp ../final-project-film/final/marino-desk-assistant-pitch.mp4 ../final-project-film/Bagwe_Shubham_INFO7375_FinalProjectFilm.mp4
```

## Status update, 2026-10-21 (resubmission)

The first submission was graded 45/50. The TA's note: this log read as written from Claude's side rather than in my own words, and the repo hadn't yet caught up to what the film promises (SharePoint still described as in scope, no `eval/report.md`). Both are addressed now — see `FRICTIONAL.md`'s final entry for the full account. In short:
- `FRICTIONAL.md` is rewritten in the first person throughout, with every date, time and decision unchanged.
- marino-rag now has a real public-only index (60 pages crawled from `recreation.northeastern.edu`, 2026-10-21) and a real `eval/report.md`: 48/50 (96%) of a 50-question retrieval check finds its expected source page in the top 3. README and `docs/PRD.md` there no longer describe SharePoint ingestion as in scope.
- The film, `PROJECT-BRIEF.md` and `beat_sheet.json` are unchanged, because they describe this milestone as "will exist" and the narration can't be re-recorded for this resubmission — the repo now backs up that promise, a week later than the film claims it will.

## Honesty notes

- Past tense on screen and in the brief means it exists and was re-run on 2026-10-13. Everything else is "will".
- Every beat carries a corner tag saying what the picture is: `real …`, `constructed · planned`, or `illustration`. Every picture is drawn in code; none is a screenshot. `real …` means the content drawn is real and dated (in `evidence/`); `constructed · planned` and `illustration` both mean a constructed sketch, not something that exists.
- The checks in `evidence/` were run by Claude Code and are labelled that way.
- marino-rag's current code was mostly AI-generated under my direction. My existing-skill evidence is EventFlow Engine (`robust-data-processor`), which I wrote myself.
- Only public website data appears anywhere: no SharePoint or other internal Marino documents.
- No accuracy, usage or latency numbers are claimed for marino-rag. No Claude response is shown.

Not included, on purpose: regenerable caches (`media/`, `mp3/`, `mp4/`, `manim/`, `final/`, `_qc/frames`), the toolkit itself, and any transcript of my Claude conversation.

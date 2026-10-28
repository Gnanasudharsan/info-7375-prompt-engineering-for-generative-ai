# BUILD-PROMPT — rebuild the pitch film

Everything runs locally and costs nothing. No API keys, no paid generation, no upload.

## Layout this assumes

```
INFO-7375/
├── brutalist.art/                       # toolkit checkout, commit ba2d0e0
├── youtube/atharva-sponsorsql-pitch/    # the reel: beat_sheet.json, scenes.py, paperwork
└── final-project-film/                  # this submission folder
```

`beat_sheet.json` and `scenes.py` in this folder are copies of the reel's. To rebuild from a fresh copy, put them in `youtube/atharva-sponsorsql-pitch/` together with the reel's `FACTCHECK.md`, `SHOTLIST.md` and `PROMPTS.md` (all three are required by GATE F).

## Commands

```bash
cd INFO-7375/brutalist.art
source .venv/bin/activate              # Python 3.12; the system python3 (3.14) breaks the dependencies
python3 -V                             # must print 3.12.x
export PYTHONDONTWRITEBYTECODE=1       # keeps .pyc files out of the toolkit

# 1. Audio first: measured narration lengths become the clock for every scene
python3 runtime/scripts/generate_audio_kokoro.py ../youtube/atharva-sponsorsql-pitch

# 2. Remotion beats (B00 cold open, B01 hesitant writer, B11 your turn)
python3 runtime/scripts/remotion_scenes.py ../youtube/atharva-sponsorsql-pitch

# 3. Gates L, SHAPE, A, W, B, then Manim renders, then compile, then GATE V
./art run ../youtube/atharva-sponsorsql-pitch
```

```bash
# 4. Clean master (no review label), written into the reel folder, not the toolkit's renders/
./art final ../youtube/atharva-sponsorsql-pitch --height 1080 --out ../youtube/atharva-sponsorsql-pitch
```

Step 2 appends rows for this reel to the shared, git-ignored `runtime/remotion/_bench/consumers.json`. To leave the toolkit exactly as it was, remove those rows afterwards:

```bash
cd runtime/scripts && python3 -c "import remotion_scenes as r; i=r.load(r.CONSUMERS); [i.__setitem__(k,[x for x in v if x.get('video')!='atharva-sponsorsql-pitch']) for k,v in list(i.items())]; r.atomic_json(r.CONSUMERS,i)"
```

## Prompt (Claude Code)

The film was built in Claude Code (Opus 5.5) from these instructions, given over the session of 2026-10-12 to 2026-10-14:

> Build a 2–4 minute Brutalist pitch film for my INFO 7375 final project, SponsorSQL, from PROJECT-BRIEF.md. Use the existing brutalist.art checkout without changing any of its files. Put the reel in a new folder, youtube/atharva-sponsorsql-pitch/. Narrate in first person as me, with the free Kokoro voice, and say that the voice is synthetic. Don't use the instructor's name, persona, handle or credit line. Give each body beat one drawing with minimal labels, and let the voice carry the explanation. Everything in the project is future tense; label mock-ups and invented examples CONSTRUCTED on screen; show no Claude response. Run the toolkit's gates and fix any failure. Don't submit over a failed gate.

## Revision prompt (2026-10-24)

> Switch the film to the latest LCA release (FY2026 Q3): download it, record its checksum, and confirm the column names from its header row. Correct the credits to "written with Claude, reviewed by me" in B00 and B12. Rebuild B04 around my ChatGPT test (saved in evals/), and update B10's "exists today". Re-render only what changed, re-run the gates, look at the frames, and keep the toolkit untouched.

Data file used:

```bash
curl -L -o LCA_Disclosure_Data_FY2026_Q3.xlsx "https://www.dol.gov//media/LCA_Disclosure_Data_FY2026_Q3.xlsx"
shasum -a 256 LCA_Disclosure_Data_FY2026_Q3.xlsx   # f8ca8448a528671f784d3692923775a13741c99caec2816b2fe30c8885bd28b3
```

## After the build: visual QC

The gates check geometry, not content. Sample frames and look at them:

```bash
ffmpeg -i ../youtube/atharva-sponsorsql-pitch/atharva-sponsorsql-pitch.mp4 -vf fps=1 /tmp/qc/%04d.png
```

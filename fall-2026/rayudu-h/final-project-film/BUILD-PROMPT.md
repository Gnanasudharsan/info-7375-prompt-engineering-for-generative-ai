# BUILD-PROMPT: Electricity Supplier Check (pitch film)

Everything here runs locally for $0.00: no API keys, no paid generation, no upload.

The commands assume this layout:

```
<parent>/brutalist.art/                     # the toolkit, https://github.com/nikbearbrown/brutalist.art @ 519fcbb
<parent>/<project>/PROJECT-BRIEF.md
<parent>/<project>/youtube/electricity-supplier-check-pitch/   # this folder
```

## 1. Paste-ready Claude Code prompt (run from `<project>/`)

```text
Rebuild the pitch film in ./youtube/electricity-supplier-check-pitch/ with the Brutalist toolkit in
../brutalist.art (show-tell format). Activate ../brutalist.art/.venv first; run toolkit commands from the
toolkit root. Free pipeline only: no API keys, no publishing, no git push.

Ground truth, read first: PROJECT-BRIEF.md; the reel's beat_sheet.json (narration approved by the
narrator, Hemanth Rayudu, 2026-10-14); FACTCHECK.md; SHOTLIST.md; PEDAGOGY.md; SOURCES.md;
../brutalist.art/skills/make/show-tell/SKILL.md.

Standing rules (they override toolkit defaults):
- Hemanth narrates in first person. No nbb/hai persona, no "in for Bear", no instructor name,
  channel chip, handle or credit line. Never set metadata.channel_title.
- Voice: kokoro am_onyx.
- Only claims in PROJECT-BRIEF.md, plus the tariff rates already in FACTCHECK.md.
- Constructed visuals keep their on-screen CONSTRUCTED / PROPOSED tags. No real bill.
  No Claude response is shown.

Steps:
1. python3 build_scenes.py (in the reel) to regenerate scenes.py from scene_body.py and the
   toolkit's show-tell iso kit.
2. Audio, if mp3/ has no .mp3 files (the GitHub copy keeps media out of Git) or narration changed:
   generate_audio_kokoro.py <reel>, then align.py <reel>.
   Whisper-check each beat.
3. ./art run <reel> --height 2160. Then sample the review cut at 2 fps and look at every frame.
   Fix root causes in scene_body.py.
4. ./art final <reel> --height 2160 --out <reel>/exports/landscape.
5. Run the master checks: master_check.py, loudness_check.py and bookend_check.py (advisory;
   its OUTRO failure is the narrator's rule).
6. Report and STOP. Never publish.
```

## 2. The commands

```bash
cd <parent>/brutalist.art && source .venv/bin/activate
R="<parent>/<project>/youtube/electricity-supplier-check-pitch"

# drawings: scenes.py = toolkit iso kit + this reel's scene_body.py
python3 "$R/build_scenes.py"

# audio (the master clock) and word timing. Only needed if narration_text changes.
python3 runtime/scripts/generate_audio_kokoro.py "$R"
python3 runtime/scripts/align.py "$R"

# pre-flight gates (Gate A must see scenes.py alone, so copy it into an empty folder)
mkdir -p /tmp/gateA && cp "$R/scenes.py" /tmp/gateA/
for c in $(grep -oE '^class (B[0-9]+_[A-Za-z]+)\(Scene\)' "$R/scenes.py" | sed -E 's/class (.*)\(Scene\)/\1/'); do
  PYTHONPATH=runtime/manim python3 runtime/qc/static_scene_check.py /tmp/gateA/scenes.py --class "$c" --quiet
  python3 runtime/qc/wcag_margin_check.py "$R/scenes.py" --class "$c" --quiet
done
python3 runtime/qc/factcheck_check.py "$R"

# review cut: Gates F, L, A, W, B per scene, compile, then Gate V
./art run "$R" --height 2160

# clean 4K master: GATE T, paperwork, beat lint, render integrity, Gate V
./art final "$R" --height 2160 --out "$R/exports/landscape"

# master reports
python3 runtime/scripts/master_check.py "$R" --mp4 "$R/exports/landscape/electricity-supplier-check-pitch.mp4"
python3 runtime/scripts/loudness_check.py "$R" --mp4 "$R/exports/landscape/electricity-supplier-check-pitch.mp4"
python3 runtime/scripts/bookend_check.py "$R"
```

## 3. How this cut was made (session record, 2026-10-14)

Hemanth's instructions, in order:

1. Verify the brief against the AG report and the National Grid tariff. Stop on any mismatch.
2. Check the toolkit and log every command, error and fix in FRICTIONAL-NOTES.md.
3. Draft the reel with Hemanth as first-person narrator, Kokoro `am_onyx`, the fixed beat order, brief-only claims and CONSTRUCTED labels. No Claude exchange, free pipeline only. Stop to show the narration.
4. After review:
   - follow the assignment's show-tell format;
   - update the toolkit to the current GitHub version;
   - show the real `meco_basic_service.pdf` rates with the bill;
   - keep the formula as a placeholder;
   - narration approved; continue.

Claude Code (Opus 5.5) ran every step; see `SOURCES.md` for what it contributed.

## 4. My prompts, verbatim (Hemanth Rayudu, 2026-10-14)

These are my messages to Claude Code in the order I sent them, copied exactly, typos included. Claude's replies aren't included: they're part of the session transcript, which the assignment says to leave out. What each instruction led to is in `FRICTIONAL.md` and `FRICTIONAL-NOTES.md`.

**Prompt 1 (the build instructions):**

```text
Context: this folder is my final project pitch film for INFO 7375. It
contains PROJECT-BRIEF.md (my answers, the source of truth),
Final_Project_Pitch_Film_Assignment.pdf (the assignment, which governs
everything), a National Grid basic service tariff PDF, and the
Massachusetts AG competitive supply report PDF. List the folder first and
tell me which file is which.

The Brutalist toolkit is already installed in the parent folder (../).
Confirm that ../art and ../HOW-TO.md exist. If they don't, stop and tell
me. Do not reinstall or clone anything. Run all toolkit commands from
the toolkit root, for example: (cd .. && ./art run <absolute reel path>).

STEP 1: Verify my brief against the source PDFs.
a. Read the assignment PDF fully and summarize the deliverables and
   rules back to me as a short checklist.
b. Find each statistic in PROJECT-BRIEF.md ($738.7 million; suppliers
   charging 10% to 30% above basic service causing more than half of
   losses) in the AG report. Give me a table: claim, exact page,
   matches or not.
c. Open the tariff PDF and confirm the effective date and the
   residential basic service rows.
d. Check the download dates in the brief against the PDF file dates.
   If they differ, update only those dates in the brief.
Do not change any other text in the brief. If a claim doesn't match its
source, stop and tell me.

STEP 2: Check the toolkit.
Run (cd .. && ./setup) to confirm readiness. Read ../HOW-TO.md,
../CLAUDE.md, ../CLAUDE-CODE-VISUAL-QC-CHECK.md, run
(cd .. && ./art ai-explainer --help), and study
../examples/ai-explainer/claude-debunked/. Log every command, error, and
fix with timestamps in FRICTIONAL-NOTES.md in this folder. Facts only;
I will write FRICTIONAL.md myself.

STEP 3: Draft the reel with the ai-explainer skill.
Reel location: ./youtube/electricity-supplier-check-pitch/ inside THIS
folder, not inside the toolkit's own folders.
These rules override every toolkit default:
1. I am the narrator, Hemanth Rayudu, in first person. No nbb or hai
   persona, no "in for Bear" line, no instructor name, channel chip, or
   credit line. Find where the toolkit injects these and disable them for
   this reel only. Do not edit shared toolkit files if a per reel setting
   exists. List every file you changed.
2. Voice: kokoro, am_onyx.
3. Target 2 to 4 minutes. Duration is an output; never pad.
4. Beat order, one idea per beat: my story (I overpaid on my own bill),
   the AG finding with its source on screen, what it is, who it is for
   and their first sixty seconds, the alternatives and what mine adds,
   how it works (Claude reads and explains, Python does all math), what
   it proves, in/out/first, the main risk and my fix, why I picked it,
   exists today vs will exist.
5. Use only claims in PROJECT-BRIEF.md. If a beat needs anything else,
   ask me.
6. Past tense only for the brief's "exists today" items. Everything else
   uses "will".
7. Every constructed visual (sample bill, mock report, architecture)
   shows an on screen CONSTRUCTED label. Never show my real bill.
8. Never depict a Claude response unless I give you a real one with its
   date. If the skill's cold open needs a Claude exchange, replace it
   with a plain title card.
9. Free pipeline only. No API keys, no publishing.

Write beat_sheet.json and a draft PEDAGOGY.md in the reel folder. Do not
generate audio. Then STOP and show me every beat's narration in a table
so I can rewrite it in my own words.
```

**Prompt 2** (toolkit path, tariff file, download date):

```text
yes use ../brutalist.art, meco_basic_service.pdf, today's date
```

**Prompt 3** (the "over $738.7 million" mismatch):

```text
yes make it 738.7 million
```

**Prompt 4** (answers to Claude's questions on draft v1):

```text
1, its ok for past tense
2. name is fine
3. I did not understand this
4. explain more
5.idk do what ever is correct for our scenaria
6. did you read the @Final_Project_Pitch_Film_Assignment.pdf ?
```

**Prompt 5** (after draft v2):

```text
yes update to current github version, in that bill print the meco_basic or any of the bills from the web, keep option a and the narration looks good. continue with the project
```

**Prompt 6:**

```text
Yes fix the brief's layout, and give me instructions on how to write the Frictional.md
```

**Prompt 7:**

```text
Yes generate a skeleton Frictional.md with these five entries and everything, but I still want to improve things a little bit more
```

**Prompt 8** (picked in a multiple-choice question; I didn't pick "Narration in my words"):

```text
Redraw B08 skills visual, Title card + my name, Tariff rates on the bill
```

**Prompt 9** (I declined Claude's pick-one pronunciation question and typed this instead):

```text
Hey- Month Ra- You- do
```

**Prompt 10:**

```text
Actually you know wha tI did, decide, agreed and not agreed, can you write the frictional.md for me and I'll read and approve it?
```

**Prompt 11:**

```text
but the frinctional.md does not contain my prompts and the files I gave in this project right?
```

**Prompt 12:**

```text
yes, inputs I have provided and exclude the assignment pdf
```

**Prompt 13:**

```text
In will exist section of project-brief.md there should be the product and the tool itself right? For what we are trying to do?
```

**Prompt 14:**

```text
ok, I read the frictional and I saw the video, the video is nice but I feel like the images are not relevant.I see alot of cardboard boxes and I dont know why. Also the video says this is a drawing and not mine, which should not be mentioned at all. We are just explaining a concept so drawing a bill by default is ok. Also instead of cardboard iamges all over, could you replace them with transformer images because it is relevant to eletricity, and also Why would AI Engineer see the eval report from thte tool, Are we giving him access to the code and how would he determine if the data is from cod eor not. and Where are we using claude codee in the project?
```

**Prompt 15** (picked in a four-part multiple-choice question):

```text
Where does Claude Code run: Build + runtime
B05 line: Rewrite B05
Visuals: Electricity cast
Disclaimers: Remove both
```

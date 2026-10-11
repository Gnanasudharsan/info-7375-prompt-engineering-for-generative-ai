# FRICTIONAL.md — Final Project Pitch Film

Dated log of friction while working. Only things that actually happened.

---

## 2026-10-09 — Brutalist setup record

**Where the setup facts come from.** I installed Brutalist before this
assignment. The file timestamps put the Kokoro model download on
2026-09-14 at 12:54 and the `.venv` creation at 12:56 on the same day. The
command list below comes from my zsh history. That history has no
timestamps and no command output, so it shows the commands I ran and their
order, but not the error messages. Everything marked **verified today** I
re-ran on 2026-10-09.

### Install commands, in the order my shell history shows them

```bash
git clone https://github.com/nikbearbrown/brutalist.art
./setup --install                 # run 3x from ~/Downloads/7375 — the wrong directory
chmod +x setup.sh art.sh          # copied from a guide; this repo has no .sh files —
./setup.sh --install              #   the scripts are named `setup` and `art`
./setup.sh
cd brutalist.art                  # repeated the same .sh commands from inside the repo
less setup                        # read the real script before running it
./setup --install
brew install ffmpeg
brew install python@3.12
$(brew --prefix python@3.12)/bin/python3.12 -m venv .venv
source .venv/bin/activate
python -V
./setup --install
brew install pkg-config cairo pango        # system libraries for Manim's text rendering
which -a node npm
brew list --versions node
brew link --overwrite node
brew install node
./setup --install
brew install --cask basictex               # LaTeX, needed only for Manim equation beats
brew list --cask
which latex dvisvgm
ls /Library/TeX/texbin | head -20
ls /usr/local/texlive
brew uninstall --cask mactex --force
brew install --cask basictex
eval "$(/usr/libexec/path_helper)"
which latex dvisvgm
sudo tlmgr update --self
sudo tlmgr install dvisvgm standalone preview
./setup
```

### Errors and fixes

- **Wrong file names and wrong directory.** I ran `setup.sh` and `art.sh`,
  which don't exist; the scripts are `setup` and `art`. I also ran
  `./setup --install` from `~/Downloads/7375` instead of from inside the
  repo. **Fix:** I `cd`'d into `brutalist.art`, read `setup` with `less`, and
  ran `./setup --install`.
- **Missing system dependencies.** After each `./setup --install` I installed
  another dependency and ran it again: ffmpeg, Python 3.12 in a `.venv`,
  cairo/pango/pkg-config, Node, then BasicTeX with `dvisvgm`. History doesn't
  keep the error text, so I can't quote what each failure said. I only know
  the order of the fixes.
- **LaTeX not found after install.** I removed a MacTeX cask, reinstalled
  BasicTeX, and ran `eval "$(/usr/libexec/path_helper)"` to put
  `/Library/TeX/texbin` on my PATH. Then I used `tlmgr` to add `dvisvgm`,
  `standalone` and `preview`.
- **Readiness check gives false failures without the venv** (still true
  today). Running `./setup` without `source .venv/bin/activate` first reports
  Kokoro, Manim and compile as blocked. With the venv active, they all pass.

### Tool versions — verified today (2026-10-09)

| Tool | Version |
|---|---|
| Python (in `.venv`) | 3.12.14 (Homebrew `python@3.12`) |
| System `python3` | 3.14.0 (not used by Brutalist) |
| ffmpeg / ffprobe | 9.0.1 (Homebrew) |
| TTS engine | Kokoro, run locally with `kokoro-onnx` 0.6.1 and `onnxruntime` 1.30.0. Model files: `kokoro-v1.0.onnx` and `voices-v1.0.bin` |
| Manim | 0.18.1 |
| Node / npm | v26.8.2 / 11.19.1 |
| Remotion | 4.0.486 |
| LaTeX | pdfTeX 3.141592653-2.6-1.40.29 (TeX Live 2026), dvisvgm 3.6 |
| Brutalist checkout | commit `ba2d0e0` |

### `./setup` readiness check — verified today

With `.venv` active, every row came back `✅ ready`: Kokoro audio, captions
and word clock, Manim beats, Manim equation beats, Remotion beats and
bookends, slates/previz/compile, and fonts. Cost reported: $0.00.

Did the sample film render? Not with `./art smoke`. It did with a
workaround — see the next entry.

---

## 2026-10-09 — `./art smoke` fails: the toolkit's fixture slug breaks its own slug rule

- **`./art smoke` FAILED.** It stopped at GATE 0 (Kokoro narration) with
  `generate_audio_kokoro.py failed`. The smoke script deletes its temp
  folder when it exits, so the log went with it. I ran the audio step by hand
  on a copy of `examples/_smoke/` and got the real error:
  `[kokoro] REFUSED: metadata.slug must be a filename, not a path`.
- **Cause:** a bug in the toolkit, not in my setup. The smoke fixture's
  slug is `_smoke`. The slug check (`runtime/scripts/build_safety.py`, line
  186) only accepts slugs that start with a letter or digit, so the
  toolkit's own test fixture fails its own safety check.
- **Workaround (toolkit not modified):** I copied the fixture to a scratch
  folder and changed the slug to `smoke`. Then I ran the same steps the smoke
  script runs:
  `python3 runtime/scripts/generate_audio_kokoro.py <copy>`, then
  `ART_FACTS=0 ART_QC=1 ART_STRICT=0 bash runtime/scripts/run.sh <copy>`.
- **Result:** both narration beats were synthesized (B00 8.73 s, B01 5.12 s,
  cost $0.00). It compiled `smoke-slate.mp4`: h264 3840×2160 video plus AAC
  audio, 13.9 s, 579,600 bytes, audio mean volume −24.2 dB. All three of
  the smoke script's checks pass: volume above −40 dB, real video and audio
  streams, and the file is larger than 20,000 bytes. I looked at
  `qc-sheet.png` myself: two readable slate frames, B00 and B01, showing the
  narration text.
- GATE V (visual QC) reported 0 BLOCKER and 4 MAJOR `underfill` (content
  fills about 42% of the safe area; the minimum is 55%). The smoke script
  expects this on its bare slates and runs with `ART_STRICT=0` for that
  reason, so this doesn't show a broken pipeline.
- **Still open:** `./art smoke` itself will keep failing until the fixture
  slug or the regex is fixed upstream. I didn't edit the toolkit.

---

## 2026-10-09 — No show-tell skill in this checkout

The assignment says to use the `show-tell` skill "if your checkout includes"
it. Mine doesn't. I searched the whole toolkit (commit `ba2d0e0`) for
`show-tell`, `show_tell` and `showtell` and got no matches. The skills in
`skills/make/` are: ai-explainer, anthropics, cli-explainer, deep-explainer,
duration-planner, explainer, fashionista, fellows, finance, guests, hai,
logo, logo-motion, nbb, nopunt, screen-clean, sri-explainer and your-turn.

**Plan:** I'll follow the show-tell format by hand in `beat_sheet.json`:

- one simple picture per beat
- one idea per beat
- minimal on-screen text
- the narration (`narration_text`) carries the explanation.

Before writing each beat, I'll check the toolkit's existing scene library
with `./art scenes "<what the beat needs>"`.

---

## 2026-10-09 — Instructor defaults found in the toolkit; I'll replace or avoid them

The assignment says to narrate as myself and not use the instructor's name,
persona or credit line. Reading the toolkit, I found these defaults:

- **Voice:** the default Kokoro voice is `am_onyx` ("Onyx", which the docs
  call "Liam") (`runtime/scripts/generate_audio_kokoro.py:77`). **Plan:** set
  my own voice in `metadata.voice_kokoro`.
- **"…this is Liam, in for Bear.":** this is a narration convention, the
  "IN-FOR-BEAR LAW" in `skills/make/ai-explainer/SKILL.md` and `HOW-TO.md`.
  No script enforces it. **Plan:** write my own opening and closing lines
  under my own name.
- **"Hola, Bear" opener:** this is the default `greeting`, and the default
  `folderLabel` is `@NikBearBrown`, in the `ClaudeComposerAsk` scene
  (`runtime/remotion/src/scenes/ClaudeComposerAsk.tsx:34,38`). **Plan:**
  override both through the scene props, or don't use that scene.
- **`@NikBearBrown` outro:** the handle is hard-coded as a constant in
  `ClaudeTitleOutro.tsx:19` (and its 9:16 version), with no setting to
  change it, and `OUTRO-LOCK.md` locks it. **Plan:** don't use
  `ClaudeTitleOutro`; end the film with a different scene.
- **Channel chip:** `metadata.channel_title` (e.g. `@HumanitariansAI`).
  **Plan:** leave it unset.

**I'll check the result:** before I submit, I'll read every on-screen frame
in `qc-sheet.png` and the full narration for any of these names.

---

## 2026-10-09 — Made a synthetic test pack for alternative tools, with Claude Code

To compare my project against tools that already exist, I needed the same
input for every tool, and it had to contain no real data. **Claude Code
wrote the documents.** I specified their shape: a fictional company
("Northwind Logistics"), six documents of 150–250 words each, and four
questions.

- **Where it lives:** `~/info7375-scratch/alt-test-pack/`, outside any git
  repo. It isn't committed here. Every file is marked `SYNTHETIC`.
- **The documents:**
  - 2026-03-02 meeting notes: choose PostgreSQL for the tracking service
  - 2026-03-10 ticket TRK-112: implement PostgreSQL
  - 2026-05-18 meeting notes: reverse to DynamoDB because of scaling cost;
    refers back to the March decision
  - 2026-05-20 email: the fictional manager Daniel Achebe approves the switch
  - 2026-06-01 ticket TRK-140: the migration
  - 2026-06-15 retro: unrelated noise
- **The questions:**
  - Q1: Which database does the tracking service use now, and why?
  - Q2: Was there ever a different decision, and what changed?
  - Q3: Who approved the switch?
  - Q4: What budget was approved for the migration? **No document says.** A
    correct answer has to say it's unknown. I grep-checked that no document
    contains "budget" or a dollar amount. The May notes do contain a
    projected-cost comparison ("roughly four times"), which is a deliberate
    near-miss a tool could wrongly report as the budget.
- **Notes template:** one blank template per tool in
  `~/info7375-scratch/alt-notes.md` (Q1–Q4 Y/N, what it did well, one thing
  it didn't do).
- **Status:** I haven't tested any tool yet.

---

## 2026-10-10 — Ran the alternatives test (NotebookLM, ChatGPT)

I gave NotebookLM and ChatGPT the six synthetic Northwind documents and the
four questions. Everything is in `evidence/alternatives-test/`: the answer
key, the grades, the test pack and the screenshots.

- **NotebookLM's summary overstated the migration as finished.** Its
  auto-generated summary says the team will "successfully deploy the new
  NoSQL infrastructure." In fact the migration ticket, TRK-140, is still
  In Progress: dual writes are on, the backfill is in progress, and reads
  haven't been switched. Its Q1 answer (run 2) has the same problem: it says
  the service "uses DynamoDB as its primary datastore" and never mentions
  that the migration is unfinished.
- **ChatGPT got the status right but cited an unrelated document's date.**
  It correctly said the service is "transitioning" and the migration isn't
  done. But it dated that status "June 15, 2026 (latest supplied records)."
  June 15 is the date of the unrelated Customer Apps retro. The last real
  migration update is 2026-06-09, in TRK-140. Nothing flagged the mismatch.
- **Both tools passed Q4.** Neither invented a budget. ChatGPT explicitly
  said the ~4× cost projection is not a budget.
- **I didn't capture a screenshot of NotebookLM run 1.** I copied its
  answer text into my notes on 2026-10-09 but never took a screenshot. The
  screenshots I have are from 2026-10-10: the NotebookLM summary, NotebookLM
  run 2 Q1–Q4, and ChatGPT Q1–Q4. For run 1, the only evidence is my copied
  text.

---

## 2026-10-10 — Drafted PROJECT-BRIEF.md with Claude; reviewed and edited by me

Claude (claude.ai chat) drafted the seven answers. I reviewed them and made
two edits before committing:

- **Brutalist line made precise.** "Exists today" no longer says Brutalist
  simply works. It now says the toolkit's own smoke test fails on a
  fixture-name bug, and that a renamed copy rendered locally (see the
  2026-10-09 entries).
- **Verification claim narrowed to what code can check.** Code will only
  check that each cited passage appears word for word in the named
  document. Whether the passage supports the claim will be judged by a
  second model call, which I'll spot-check against the test set. The brief
  doesn't say code verifies support.

Before committing, Claude Code checked the brief against the evidence
folder and this log. It looked at the factual claims, the tense rule and
the word count. Its findings were reported to me and not silently fixed.

---

## 2026-10-10 — Narrowed competitor claims and fixed tense after Claude Code's evidence check

Claude Code checked the brief against `evidence/alternatives-test/` and
this log. It flagged four claims and three tense problems. I fixed them by
replacing specific sentences:

**Competitor claims**

- The test date now says I tested on 2026-10-09 and captured the
  screenshots on 2026-10-10. It used to say "2026-10-09/10".
- **NotebookLM summary.** The brief no longer says the summary called the
  migration "successfully" deployed. The screenshot only says TRK-140 was
  initiated "to … successfully deploy the new NoSQL infrastructure". It now
  says the summary gave no sign the migration was still in progress, and
  quotes it.
- **NotebookLM "which database" answer.** It now says the answer itself
  didn't say the switch was unfinished. The run 2 Q1 suggested follow-up
  does mention "completing the migration".
- I dropped "Neither tool checks its own claims against its sources". Two
  tests can't show how either product works. It now says only what this
  test showed: neither flagged the overstated status or the wrong date, and
  neither showed how often it is right.

**Tense**

- §4 prompt contracts: "must … fail" became "will be required … will fail".
- §5: "a test passes" became "a test will pass".
- §6: the six existing documents "were generated with Claude Code"; the
  larger set "will be too".

**Still open:** the brief is 805 words, over my ~750 target. I'll choose
the cuts myself.

---

## 2026-10-10 — Beat plan approved; scene mapping started

I approved the 13-beat plan (B00–B12) with its narration text. Scene
mapping has started, but nothing is rendered yet.

- **Working folder:** `~/info7375-films/decisiontrace-pitch/`. It's outside
  every git repo and outside the toolkit folder.
- I copied the two real screenshots there unedited:
  `2026-10-10_notebooklm_summary.png` and `2026-10-10_chatgpt_q1.png`.
- **I searched the scene library for every beat.** I ran `./art scenes`
  with `--no-log`, because a plain search writes every miss into the
  toolkit's `TEMPLATE-MISSES.md`, and I don't want to modify the toolkit.
  - Most hits are built for one specific reel: they take only a
    `sparkLine` prop and their content is hard-coded.
  - `FormBCard` needs `public/form-b-icons/`, which is missing from this
    checkout.
  - `Ch1AttnBoundary` renders on my machine, but it's my untracked Week 01
    component, so a clean clone of the toolkit couldn't rebuild it.
  - `LookPlate` (the only image scene) is a Fashionista plate with a
    Higgsfield "generated model" stamp, so it would mislabel a real
    screenshot.
- **There's no tracked, generic scene for showing a screenshot.** The
  pipeline's plain still slot (`media/<beat>.png`) has three problems:
  - by default it crops the image to fill 16:9 and desaturates it
  - it can't carry an on-screen label by itself
  - `./art final` refuses to export if any beat is still a slate.
- **Voice samples:** I rendered three non-instructor Kokoro voices into
  `voice-samples/` (am_eric, am_adam, af_heart) to choose a narrator.

---

## 2026-10-10 — Toolkit gaps while building the film: no picture scenes, no image scene, slates blocked

- **No generic picture scenes, so I wrote my own Manim scenes.** Every
  drawn-picture scene in the toolkit's library is built for one specific
  reel, with its content hard-coded. The only reusable scenes are text
  cards. I wrote four simple line-drawing scenes myself in the film's own
  `scenes.py`, outside the toolkit:
  - B01: a question mark resolving into a status tag
  - B05: a claim and its quote, ✓ found / ✗ missing
  - B07: the answer → verify → retry → "not supported" loop
  - B09: a hand grading its own paper

  Each scene's length comes from that beat's measured narration. The other
  beats use the generic `MedhavyConceptCard`, and B06 uses
  `BrutalistTerminalOpen` with every default line replaced.
- **No image scene, so I composed labelled frames.** No reusable scene
  shows a screenshot. The plain still slot crops and desaturates by
  default, and it can't show a label. For B03 and B04 I built each frame
  with a small script (`tools/compose_frames.py`):
  - the real screenshot, scaled only, never edited
  - on a plain background
  - with the required "REAL · … · captured 2026-10-10" label drawn above it
  - and highlight boxes drawn on the frame around the quoted phrases.

  The build settings keep the image unaltered: `fit: pad`,
  `treatment: none`, `motion: hold`. The original PNGs stay in
  `evidence/alternatives-test/screenshots/` for comparison.
- **Slates are blocked by `./art final`.** It refuses to export while any
  beat is still a slate (placeholder) card. So no beat could be left as a
  placeholder; every one needed a real fill.

---

## 2026-10-10 — GATE V failed with 19 MAJOR findings; what I fixed; the B04 crop; my name spelled phonetically in narration only

**GATE V failed on the first draft.** The first full draft passed GATE L
(beat mix), GATE F (paperwork), GATES A/W/B (Manim checks) and the
render-integrity check. It failed GATE V, the frame-level visual check,
with 0 BLOCKER and 19 MAJOR findings:

- **2 × `empty-frame` on B00 and 13 × `underfill` on the text-card beats
  (B02, B08, B10, B11, B12).** `MedhavyConceptCard` draws a small white
  card with small text on a near-identical cream background. The gate was
  right: those frames looked empty.
- **4 × `underfill` on my own drawings (B01, B09) and on B04.** The
  content was too small for the frame.

I didn't use `ART_STRICT=0` to turn these into warnings and ship. Fixes:

1. **Text beats:** I replaced all six card beats with text-led Manim
   scenes. They use large serif type between two rules, with the same
   on-screen text as before.
2. **Drawings:** I scaled up B01, B07 and B09. I also redrew B07 so the
   whole loop is on screen early, because GATE V samples frames at 50%
   and 85% of each beat.
3. **B06 label:** "CONSTRUCTED · NOT REAL OUTPUT" was the terminal
   scene's small corner label. It's now large text across the top of the
   frame (`tools/label_b06.py`, overlaid after the toolkit renders the
   clip).
4. **Gates A and B along the way:**
   - Gate A rejected the text scenes as "shapes never change", so each
     now animates an underline and an accent mark.
   - Gate B caught an "A+" crossing the paper edge in B09.
   - On the second pass, GATE V caught B07's mid-beat frame at 54.6%
     against a 55% minimum.

**Result:** draft 3 passes every gate in strict mode, with GATE V at
0 BLOCKER / 0 MAJOR, and render integrity passes. Runtime: 186.6 s (3:07).

**Why I cropped B04.** Scaled whole, the ChatGPT screenshot is nearly
square, so it left wide empty bands on both sides and failed GATE V. I
cropped it to one section:

- **From** the heading "What is the current implementation status?"
- **Through** the end of the "Bottom line" sentence.
- **It includes** both phrases the narration relies on: "June 15, 2026
  (latest supplied records)" and "not a completed switch".
- **The crop box** is (22, 406, 656, 698) in source pixels, recorded in
  `tools/compose_frames.py`.
- **Otherwise unaltered:** the pixels are only scaled, and the label and
  highlight box are drawn on the frame. The full original is still in
  `evidence/alternatives-test/screenshots/`.

**My name in the narration.** Kokoro mispronounced "Gnanasudharsan
Ashokumar". I compared five phonetic spellings with af_heart samples,
using Kokoro's own phoneme output plus listening, and chose
"Nya-na-sudharsan Ashok Kumar". It's used **only** in `narration_text`
for B00 and B12. Every on-screen name stays "Gnanasudharsan Ashokumar".
The toolkit generates no captions. If I add captions later, I'll have to
correct those two lines by hand, because captions built from narration
would show the phonetic spelling.

---

## 2026-10-10 — Draft 4: revisions after watching draft 3

What I changed:

- **B08:** I added one narration sentence, "What's in: the tool, the
  verifier, the test set, and the evaluation report", and an "In:" line
  on screen. Only B08's audio was regenerated. No other beat's narration
  changed.
- **B01:** the second half now shows a dashed repository folder labelled
  **PLANNED**, with four items: CLI, synthetic docs, test set, eval
  report. Each item appears as it's named. I found the cue times by
  measuring pauses in the narration audio with ffmpeg silencedetect.
- **B03:** it's now two real screenshots in sequence. First the NotebookLM
  summary, then from 8.61 s ("Asked which database") the run 2 Q1 answer,
  with "uses DynamoDB as its primary datastore" highlighted. I placed the
  box edges by scanning for the blank pixel columns between words. Both
  halves carry "REAL · NotebookLM · captured 2026-10-10".
- **B06:** rebuilt as my own Manim scene. The toolkit's
  `BrutalistTerminalOpen` hard-codes its window title, its background, a
  red underline and the FAIL colour, and none of them can be set. The new
  B06 has:
  - a cream frame, with the large "CONSTRUCTED · NOT REAL OUTPUT" label
    drawn in the scene itself
  - the window title "zsh — decisiontrace"
  - an answer line "→ DynamoDB (decided 2026-05-18) · status: in progress"
  - FAIL in red, and no stray red line.

  The film no longer uses any toolkit Remotion component.
- **B07:** I added a "✓ pass → cited answer" branch and a "✗ fail"
  label, placed "retry once" beside the curved arrow, and timed the dot to
  the narration. There's no stray mark near "not supported".
- **B09:** it now ends with a page labelled "hand-written by me", where a
  "hard case" gets a ✗.
- **B00:** the name is now about 2.6× larger. I measured it: 46 px tall
  for the old overlay, about 120 px now. The old
  `metadata.channel_title` overlay has no size setting, so the name moved
  into the B00 scene and `channel_title` was removed.
- **B11:** "test" is now "alternatives test".

**Problems the low-resolution previews caught before the 4K render:**

- B01's mid-beat frame was underfilled while the folder was still
  drawing. It now crossfades.
- B01's "synthetic docs" label ran past the folder edge.
- B07's "pass" and "fail" labels sat on top of their arrows.
- B00's first name size came out 3.7×, outside the 2–3× I asked for.
- Gate A's stand-in for Manim has no `np`, so I replaced the numpy maths
  with plain coordinates.

**Result:** draft 4 passes every gate in strict mode, with GATE V at
0 BLOCKER / 0 MAJOR, and render integrity passes. Runtime is 191.5 s
(3:11), under the 4:00 limit.

**Open question: recording my own voice for B00 and B12.** I checked
whether I can supply my own mp3. The pipeline reads each beat's
`audio_file`, and `audio_policy` only offers `silence` and `preserve` (a
video's own embedded audio). So it's possible, but I haven't changed
anything yet. B12's line "The narration voice is synthetic" would become
false if B12 were in my own voice.

---

## 2026-10-10 — Kokoro mispronounced my name in all 5 spellings; I recorded B00 and B12 myself

**Kokoro got my name wrong every time.** It read "Gnanasudharsan
Ashokumar" as roughly "NAN-uh-sud-har-sun uh-SHOH-kyoo-mer". I tried five
phonetic spellings with the af_heart voice (`name-samples/`):

| # | Spelling |
|---|---|
| 1 | Nyaana-sudharsan Ashok-kumaar |
| 2 | Gyaana-sudharsan Ashok Kumar |
| 3 | Nyana sudarshan Ashokumar |
| 4 | Nyah-nuh-sudharsan Ashok Kumar |
| 5 | Nya-na-sudharsan Ashok Kumar |

None got the opening sound of my first name right. Kokoro read each one
as "Nai" or "Jai". Draft 4 used #5, but it still wasn't my name.

**What I did instead:**

- **Recorded both name lines myself.** The originals are `audio/B00.m4a`
  and `audio/B012.m4a`. They aren't modified; their SHA-256 hashes still
  match.
- **Prepared the audio** with `tools/prep_own_audio.py`. It trims to the
  speech, keeping 0.2 s of padding, and applies one fixed gain. Nothing
  else is changed.
  - **B00:** 9.20 s, gain +5.1 dB.
  - **B12:** 8.80 s, gain +3.3 dB.
- **Matched the loudness target to the Kokoro beat files**, which measure
  about −22.3 dB each, not to the whole film's −25.4 dB. The film's
  figure includes pauses, so using it would have made my lines about
  3 dB quieter than the rest. Measured inside the finished film, my lines
  are −25.8 and −25.7 dB against −25.3 dB for Kokoro beats.
- **Changed the narration text and labels:**
  - B00 and B12 `narration_text` now use my real name.
  - B12 says "The rest of the narration is a synthetic voice, made with
    Kokoro". The old line, "The narration voice is synthetic", would have
    been false.
  - B12 on screen now reads "Narration: synthetic voice (Kokoro) · name
    lines recorded by me".
- **Protected the recordings from being overwritten.**
  - B00 and B12 have `engine: "own-recording"`, so the Kokoro script skips
    them even without `--only`. I confirmed this with a dry run.
  - From now on, any Kokoro regeneration uses `--only <beat ids>`.

**Also in this round:**

- B11's heading is split over two centred lines, so it now renders larger
  than its second line.
- B00, B11 and B12 were re-rendered to their new lengths.

**Result:** draft 5 passes every gate in strict mode, with GATE V at
0 BLOCKER / 0 MAJOR, and render integrity passes. Runtime is 194.5 s
(3:14).

---

## 2026-10-10 — Back to one Kokoro voice for the whole film; fixed my name with explicit IPA phonemes

**Why I switched back.** I removed my own-voice recordings from B00 and
B12 so the whole film uses one consistent voice, af_heart. Five phonetic
respellings had already failed, as logged above. So instead of respelling
the name, I fixed its pronunciation inside Kokoro with explicit phonemes.

**What I checked first:**

- **Phoneme input works.** kokoro-onnx 0.6.1 accepts a phoneme string
  directly through `Kokoro.create(..., is_phonemes=True)`.
- **Most symbols I needed are available.** Every symbol in my candidate
  IPA (`ɲ ɑ ː ɚ ə ɹ ʃ oʊ ˈ ˌ`) is in Kokoro's 114-symbol vocabulary, and so
  is the aspiration mark `ʰ`.
- **Two marks are missing.** The dental mark ◌̪ and the breathy mark ʱ
  aren't in the vocabulary. So I approximated the soft, slightly breathy
  "dh" as `dʰ`.

**What I built.** `tools/phoneme_name.py` is in the working folder, not in
the toolkit.

- It phonemises each B00/B12 sentence with Kokoro's own tokenizer and
  swaps in hand-set IPA for the name only.
- It reuses the toolkit's own model loading, text normalisation, mp3
  writer and duration measurement.

**What I chose.** I rendered five af_heart samples (A–E) and picked
**E** by ear: `ɲˈɑːnɑːsˌuːdʰɚʃɑːn ɑːʃˈoʊk kuːmˈɑːɹ`. That's "ny" with a
silent G, a breathy "dh", lighter stress on "soo" and full stress on
"mahr".

- **New audio:** B00 is 8.13 s and B12 is 6.83 s.
- **Loudness:** the in-film mean is −25.4 / −25.2 dB, matching the other
  beats at −25.3 dB.
- **Recorded in the sheet:** the exact IPA and the full phoneme string are
  in `beat_sheet.json` under `phoneme_note`.

**What else changed:**

- **Recordings off the build:** both beats are `engine: "kokoro-phoneme"`,
  so `generate_audio_kokoro.py` skips them. I confirmed this with a dry
  run.
- **Own-voice files moved out:** the own-voice mp3s and their prep script
  are in `old-draft-5/`. My original .m4a recordings are kept and
  unmodified. None were ever copied to the course fork.
- **B12 restored:** the narration and the on-screen text are back to "The
  narration voice is synthetic, made with Kokoro" and "Narration:
  synthetic voice (Kokoro)". That's true again now that every beat is
  Kokoro.

**Result:** draft 6 passes every gate in strict mode, with GATE V at
0 BLOCKER / 0 MAJOR. Render integrity passes: the output matches the
timeline exactly at 191.500 s. Runtime is 3:11.5.

**A correction to my own logs.** The duration differences I recorded for
earlier drafts, about 0.125 s, were measured against the summed clip
files. Those files carry a little container padding. The toolkit's real
check compares against the frame-rounded beat lengths, and against that
reference every draft matched.

---

## 2026-10-10 — Draft 7: small visual fixes (no narration changes)

- **B06:** the cursor now sits just after whatever was last typed. Before,
  it jumped to the start of the next line. I restored the line
  "→ report   eval/report.md" as the last line. Typing now starts at 3.6 s,
  as the first sentence ends, so the completed screen holds for about
  5.3 s. That's measured from the preview's last visual change at 7.7 s.
- **B08:** I removed the short orange dashes. They happened to sit under
  single words ("Jira", "test set"). Each line now has one accent
  underline running its full width.
- **B01:** the four repository items now appear as each previous phrase
  ends, instead of when each item is named. The completed folder is on
  screen from 15.3 s, so it holds about 1.8 s before the beat ends.
- **Not changed:** the two conditional items (B02's dates, and phoneme
  overrides for other words). I didn't confirm a 10-10 ChatGPT run or
  list any mispronounced words, so B02's narration and PROJECT-BRIEF.md
  are unchanged.
- **Re-rendered:** only B01, B06 and B08.

**Result:** draft 7 passes every gate in strict mode, with GATE V at
0 BLOCKER / 0 MAJOR. Render integrity passes: 191.500 s output against a
191.500 s timeline. Runtime is 3:11.5.

---

## 2026-10-10 — Wrote README.md, BUILD-PROMPT.md and SOURCES.md

Claude Code drafted these three files from my outline. I asked for every
fact to be checked against the actual files and packages, and anything it
couldn't confirm to be marked UNVERIFIED.

**What was checked:**

- **Versions:** read from the build machine.
- **Toolkit:** commit `ba2d0e0`. Its scripts and gates are unmodified
  against that commit.
- **Licences:** checked from the installed packages, the font files and
  `ffmpeg -L`. For two items I also checked upstream licence metadata,
  read-only: the GitHub licence API, and the Hugging Face API for the
  Kokoro-82M model card.

**Two licence items stay UNVERIFIED:**

- **Kokoro's converted model files.** The ONNX conversion and voices file
  carry no licence text of their own. The model card says Apache-2.0.
- **espeak-ng's bundled copy.** espeakng-loader has no licence metadata or
  file. Upstream espeak-ng is GPL-3.0.

**Found along the way:**

- **The toolkit declares no licence.** There's no LICENSE file, and GitHub
  reports none. This folder doesn't redistribute any toolkit code.
- **The rebuild steps are confirmed.** Starting only from this folder's
  files, `compose_frames.py` regenerates `B03a.png`, `B03b.png`, `B04.png`
  and the B03 clip byte-for-byte identical.
- **Narration history in SOURCES.md.** I first described the narration as
  "approved unchanged". Because B08 and B12 were edited later, SOURCES.md
  now says Claude drafted the *original* narration and points to the logged
  edits.

**Prompts.** BUILD-PROMPT.md §6 quotes my Claude Code prompts verbatim.
Two are summarised: the one that pasted the course's assignment text, and
the documentation prompt. My claude.ai chat prompts aren't in the
repository, so they aren't reproduced.

**Path redaction.** In the copies of `decisiontrace-pitch.verified.json`
and `build-state.json`, my home-directory path was replaced with `~`. All
SHA-256 values are unchanged, and the toolkit re-checks against the
originals in the working folder, so verification isn't affected.
`final-run.log` keeps the full paths.

**Left open on purpose:**

- PROJECT-BRIEF.md's "Exists today" list doesn't include the film, though
  B11's narration says "this brief and this film".
- The brief is 786 words, against the ~750-word one-page target.

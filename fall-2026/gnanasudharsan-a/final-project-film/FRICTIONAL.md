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

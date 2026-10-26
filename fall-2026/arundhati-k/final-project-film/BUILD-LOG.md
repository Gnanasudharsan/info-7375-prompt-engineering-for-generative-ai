# BUILD-LOG — Final Project Pitch Film (Claude's log)

> **Written by Claude Code**, not by me. Until 2026-10-21 this file was FRICTIONAL.md; the grader noted it was
> Claude-drafted, so it was renamed to say so plainly. It is kept because it records commands, errors and fixes
> exactly. **My own dated entries are in [FRICTIONAL.md](FRICTIONAL.md).**

## 2026-10-10 (Sat) — choosing the project; toolkit setup

- **Timeline.** The brief suggests a five-day shape; I started on Saturday with the film due Monday
  2026-10-12 11:59pm, so Days 1–5 are compressed into three days.
- **Project chosen:** Option A of three Claude sketched for me (the others were an English-to-SQL checker
  on a synthetic hospital schema and a job-posting requirement extractor). I picked growing my Reallocation
  recipe (co-op sponsor check, commit `03784b0`), because it is the only one with real work to show in past tense.
- **Toolkit pull failed.** `git pull` in my Week 1 `brutalist.art` checkout aborted: uncommitted edits from
  the Week 1 build (`Root.tsx`, `kit.tsx`, `scenes.json`, `package-lock.json`) would have been overwritten.
  Instead of stashing them, I cloned a fresh copy to `brutalist-final/` at `b21f625` (2026-10-10).
- **Show-tell skill found in the new checkout** at `skills/make/show-tell/SKILL.md` (a first search with
  `find -iname` looked at the wrong level and missed it).
- **Conflict between toolkit and assignment.** Show-tell defaults to "Liam, in for Bear", a spoken
  @NikBearBrown outro, and Professor Bear portraits for any person. The assignment says to narrate as
  myself and not use the instructor's name, persona or credit line, so all three are removed. CLAUDE.md
  also lists show-tell as "ADVANCED — Bear only"; I am using it because the assignment names it as the
  right format.
- **Re-ran the recipe today** to confirm the "exists today" list: same 7 role outcomes as 2026-10-03,
  17/17 tests pass (`evidence/recipe-rerun-2026-10-10.txt`). The run rewrote the date stamp in four tracked
  output files; I reverted them so the fork still matches `03784b0`.
- **Finding for the risk section:** the sponsorship dataset's README says it starts from an SEC list of
  funded companies matched to DOL/USCIS records — a documented reason the big banks are missing.
- **`./setup --install` failed twice in the fresh clone.** (1) It called macOS's system `python3` (3.9.6),
  and `kokoro-onnx` needs `onnxruntime>=1.20.1`, which has no build for 3.9 → pip `ResolutionImpossible`.
  Fix: created `.venv` with Homebrew Python 3.12 and put it first on `PATH` (the same thing Week 1 needed).
  (2) It then exited 1 at its own "ElevenLabs guard": the toolkit's film script
  `youtube/brutalist/claude-liam-brutalist-command-setup/SCRIPT.md` quotes the guarded header name in its
  narration, so the guard catches the toolkit's own example. I did not edit the toolkit; I ran the checks that
  come after the guard myself: ffmpeg 9.0.2, Node 25.8.2, Python imports OK, Kokoro smoke test
  "synth OK — mean_volume -21.8 dB", Remotion node_modules present, EB Garamond installed.

## 2026-10-12 (Mon, due day) — voice

- **Voice decision (mine):** keep Kokoro `am_onyx`, the toolkit's default voice, but with my name in place of
  "This is Liam, in for Bear". Claude rendered four alternatives (`af_heart`, `af_sarah`, `bf_emma`,
  `am_michael`) for comparison; I chose to stay with the default. The opening line says the voice is
  synthetic and reading my script, so nothing presents it as my own voice. No instructor name, persona,
  outro or portrait appears in the film.
- **Voice changed (mine, same day):** after listening to the four samples I picked `bf_emma` instead of
  `am_onyx`. Set as `metadata.voice_kokoro` in the beat sheet; Kokoro uses British-English pronunciation
  for `bf_` voices. The synthetic-voice disclosure line stays.

## 2026-10-12 (Mon, due day) — build

- **Instructor handle hard-coded in the outro.** `ClaudeTitleOutro.tsx` renders `@NikBearBrown` as a constant,
  and `bookend_check.py` requires the film to end on that card. The `ClaudeDefinitions` and `ClaudeComposerAsk`
  cards also default their corner label to `@NikBearBrown`. Fix: a three-line local edit adding an optional
  `handle` prop to the outro (BUILD-PROMPT §1); `folderLabel` set to my name on the other two. Bookend gate passes.
- **Two mispronunciations caught by a whisper transcript, not by ear.** "A pitch by Arundhati Kandelkar"
  transcribed as "a pitch buyer and hearty candle car"; "U.S. work-visa" as "you, S". Reworded to
  "Pitched by …" and "United States work visa" in the narration (the on-screen prompt keeps "U.S.").
  Whisper also cannot spell my name; I still have to listen to BIDEA and BOUT myself.
- **faster-whisper 1.2.1 crashed on mp3 input** with the installed `av` 19 (`metadata_errors` keyword).
  Worked around by decoding with ffmpeg to raw PCM first; no packages changed.
- **First contact sheet looked broken** — my ffmpeg `xstack` layout string was wrong, not the scenes. Rebuilt
  with `tile=2x5`. One real defect found: B02's "ask a person" label overlapped the speech-bubble tail; moved.
- **Honesty tags added to every body beat** (EXISTS with its evidence, PLANNED, or CONSTRUCTED · not built yet),
  so no frame relies on the narration alone to say what is real. B07's results table is drawn empty on purpose.
- **First `art final` blocked by GATE T** (min text size §8.1): B01 and BDEFS each had a text run 40 px tall
  against a 41 px floor — short lowercase words with no ascenders ("live", "dates", "co-op"). Gates A, B, V and
  my own frame review had all passed, so only the type gate caught it. Fix: B01 labels 38 → 46; term
  "co-op" → "Co-op". B03's bank boxes also started 0.3 units lower to clear the date tag. Old clips and the
  Manim cache moved to `_superseded/`, then re-rendered — not submitted over.
- **GATE T failed twice more; I was guessing.** Enlarging B01's labels, capitalising "Co-op", enlarging the
  tags and removing the terms card's 32 px corner label did not change the result (still 40 px). I then ran
  the checker's own functions (`visible_text_mask`, `text_run_bboxes`) on the midpoint frames and printed the
  sub-floor boxes. The real culprits: in B01, the scribble "handwriting" on the record page, read as a text run;
  in BDEFS, short x-height-only words ("as", "no") in the definitions, set by the component at a hard-coded
  `meanSize = 48`. Fixes: ghost ruled lines instead of scribbles in B01; second local toolkit edit
  `meanSize` 48 → 50 in `ClaudeDefinitions.tsx`. Lesson: measure before changing things.
- **Alternatives (B05).** I asked Claude to look up the USCIS H-1B Employer Data Hub instead of doing it by hand.
  It opened the Tableau dashboard and typed into the employer-name filter. Findings: no job-title filter;
  "MELLON" lists three BNY entities and Carnegie Mellon University; JPMorgan Chase *is* in the hub though not in
  my dataset. That made the name-matching risk concrete and pointed at the obvious second data source.
  The first narration draft ran 30 s, so it was split into B05 and B05A. Total runtime now ~3:22 before B11.
- **Removed the spoken "synthetic voice" line from the opening (my decision).** Claude flagged that saying my
  name in a synthetic voice with no disclosure could read as my real voice, so the disclosure stays in writing
  (README.md, SOURCES.md, FACTCHECK row 1). BIDEA re-voiced (17.2 s → 14.5 s) and re-rendered; runtime ~3:39.
- **The film was silently left out of the first commit.** The course repo's `.gitignore` ignores `*.mp4`, so
  `git add` on the folder skipped it with no warning. Caught by reading the staged file list; fixed with
  `git add -f` (as classmates' committed films show is the norm) and an amend before pushing.
- **First 6 evaluation rows ran (2026-10-12, ~18:45).** I asked Claude to run my six companies (PayPal, Visa,
  Goldman Sachs, Mastercard, BlackRock, LSEG) through my recipe's matcher and the USCIS hub. 6/6 in the hub, 0/6 with
  a record in my dataset. It also exposed a defect I had not predicted: `norm_name` strips "CO"/"LLC" but not "AND",
  so "GOLDMAN SACHS AND CO LLC" → "GOLDMAN SACHS AND". "LSEG" finds nothing in the hub; only the legal name does.
  The browser pane had closed between sessions, so the first click failed until it was reopened.
  Film updated: B07 now says the first rows ran (past tense), new B07A shows the bug. Kokoro fused "and Co into" into
  "and cointer"; reworded. Runtime ~3:50.
- **Self-audit against the rubric found two film gaps (2026-10-12, evening).** Q4 "what does it prove" and Q1's
  one-sentence answer + finished form were in PROJECT-BRIEF but not in the film (a word search of the narration found
  no "verify" or "skill"). Added BWHAT (Q1) and B09P (Q4). That pushed the film to 4:02, over the limit, so B04, B08,
  B09 and Your Turn were trimmed (no claim removed) and B09P tightened → 3:58. While checking B09P's wording I found
  source grounding already exists — the run log carries 48 `csv_line` citations — so it is stated in present tense.
- **PROJECT-BRIEF cut to one page** (107 → ~45 lines). Also corrected a stale guess: §6 had used "BNY Mellon NA", a
  name Claude invented on 2026-10-10 as an example; it now uses the Goldman names the hub actually lists.
- **Evidence for existing skills added (B11A).** I gave Claude my résumé to pick one evidence line; it chose my
  Software Developer role at Giesecke+Devrient (Java/Spring Boot) and claimed only what that role shows —
  not Angular, which is on my skills list but not in that job. The résumé is not committed. Kokoro read the name as
  "G-Sec and Deviant", so the narration says "G plus D" (the company's own short name); the label shows the full name.
- **Caught a wrong date before committing.** The first résumé copy gave the G+D role as Aug 2021–Sep 2022, so B11A
  said "for a year". I then shared an updated résumé (Aug 2021–Sep 2024) and stopped Claude after the render but
  before the commit. B11A now says "for three years"; fact-check row 24 records both copies.

# FRICTIONAL — INFO 7375, Final Project Pitch Film

Akshit Verma · *SponsorScout*

**My reflections:**I am Akshit Verma and I have picked the SponsorScout because I wanted to pick some topic which is based on the real life application. The title that is proposed here is an extension of Reallocation Engine. First, I gave the descriptions and then based on that I created the video which can explain the concept of this project that I proposed. Then, I looked into video and realised that it can be made more better so I asked to make changes in the video, like adding captions, visuals, transition effects, and add a few better description in some of the video parts.

Here are the track of events - 

---

## Entry 1 — 2026-10-12: choosing the project and drafting PROJECT-BRIEF.md

**I tried / expected:** I asked Claude what I could make the final project on, then chose
its recommended option: extending my Assignment 1 recipe (network-targets) into the final project.

**What happened:**
- Claude proposed four options; I picked the recommended one.
- Claude re-ran the Assignment 1 tests: `Ran 25 tests … OK` (2026-10-12).
- `gh pr view 44`: state `OPEN`, not merged.
- Alternatives check: MyVisaJobs homepage fetched 2026-10-12. H1BGrader returned
  HTTP 403 and is **not** cited.
- The Brutalist checkout has no `show-tell` skill (`skills/` holds only `make`, `upload`).

**What Claude contributed:** project options; collected facts from Assignment 1
(`SUBMISSION.md`, `WORKED-RUN.md`, `FRICTIONAL.md`, run-2 report, engine-baseline report);
drafted `PROJECT-BRIEF.md`. Section 7's reason is left for me to write.

**Evidence and next step:** `PROJECT-BRIEF.md`. Next: my review of the brief, then the beat sheet (Day 2).

---

## Entry 2 — 2026-10-14: where the files live, and finding the show-tell skill

**I tried / expected:** I asked Claude to proceed with Day 2 (the beat sheet). Partway through, I
asked where the files were being stored, and then asked for everything to be kept in
`PromptEngr/Assignment_Final Project Pitch Film/`.

**What happened:**
- Claude had first written the Day 1 files into the course repo
  (`info-7375-course/fall-2026/akshit-v/final-project-film/`). They were moved here; that
  course folder was removed (nothing was committed). They will be copied into the course
  repo's `fall-2026/akshit-v/final-project-film/` only at submission.
- `git fetch` in `brutalist.art/`: upstream `main` is 54 commits ahead of my checkout
  (`6a8380a` → `4115560`) and **does** contain `skills/make/show-tell/SKILL.md`. My working
  tree was not changed. Read-only copies of the skill files are in `_reference/`.
- The show-tell skill's defaults use the instructor's persona: the "Liam, in for Bear"
  greeting, the `am_onyx` "Liam" voice, the `claude-liam` channel and a spoken
  `@NikBearBrown` outro. The assignment says to narrate as myself, so those are replaced.

**What Claude contributed:** the move; the upstream fetch and reading of the skill.

**Evidence and next step:** `_reference/`. Next: `beat_sheet.json`.

---

## Entry 3 — 2026-10-14: the beat sheet

**I tried / expected:** a beat sheet built from `PROJECT-BRIEF.md`: one picture and one idea per beat, 2–4 minutes.

**What happened:**
- Claude's first draft was 18 beats and 835 words, about 4.5 min at the Week 01 film's
  measured 3.11 words/s (556 words / 178.5 s). That is over the 4-minute limit.
- The second draft drops the terms card and tightens every beat: 17 beats, 646 words,
  **estimated 3.5 min** (the real length comes from the audio on Day 3).
- `bookend_check.py` (upstream) can't exempt the outro and matches its handle to
  `metadata.channel_title` (default `@NikBearBrown`). So `channel_title` is set to my name.
- B14 (question 7, why I picked the project) still holds a placeholder for my own
  words. `make_sheet.py` exits 2 until it is replaced, so it can't be voiced by accident.

**What Claude contributed:** `make_sheet.py`, `beat_sheet.json`, `SHOTLIST.md`, and the
narration draft, built from the brief and from Assignment 1's run outputs.

**Evidence and next step:** `beat_sheet.json`, `SHOTLIST.md`. Next: my review of the narration,
my B14 sentence, the voice choice, then Day 3 (build).

---

## Entry 4 — 2026-10-14: checking the drafts against the assignment, and fixing them

**I tried / expected:** before building, I asked Claude to confirm that every instruction was being
followed exactly.

**What happened:** Claude re-read the full assignment text against the brief and the beat sheet,
and checked my Assignment 1 log for who did what. It found six problems in its own drafts:
1. **Overclaimed skills.** Q7 listed "the Python prototype and tests" as skills I already
   have. My Assignment 1 `SUBMISSION.md` says Claude Code wrote most of the code. Rewritten:
   what I can show is judgment (I made recent funding a NETWORK requirement and recorded why,
   and I signed gates G1 and G3), not code.
2. **"Which I ran on October third"** was wrong. My log records `[AI] ran`. Now: "which I had
   Claude Code run".
3. **Wrong tense / unsupported claim.** B00 described the proposed workflow in present tense.
   B12 claimed "many companies use job systems with no public interface", which my data doesn't
   show (107/123 are only *unmapped*). Both reworded.
4. **Value line missing from the film**, though it was in the brief. Added to B03.
5. **Stack not named** ("Stack is your choice — name it"). Added to the brief (§1) and B01.
6. **Target role only implied.** Now stated in B05 and brief §3.

Also changed: the MyVisaJobs claim. Claude's fetch had shown an "H-1B Jobs" link, so the
old line ("I didn't find whether a company has a job open today") might be false. B04 now
states only the networking-list difference. `make_sheet.py` won't let B04 be voiced until
I have looked at the site myself and dated it.

**What Claude contributed:** the audit and all six fixes.

**Evidence and next step:** `PROJECT-BRIEF.md`, `make_sheet.py`, `beat_sheet.json` (17 beats, about
3.7 min estimated with the B14 placeholder). Still open, mine: the B14 sentence, the MyVisaJobs
check, the voice choice.

---

## Entry 5 — 2026-10-14: choosing the voice

**I tried / expected:** I chose Kokoro `am_michael` (free, local, synthetic, disclosed on screen)
over recording my own voice. It isn't the instructor's `am_onyx` "Liam" voice.

**What happened:**
- A local test with the toolkit's model files (`runtime/models/kokoro/`) confirmed
  `am_michael` is available.
- Measured pace: **2.57–2.73 words/s**, slower than the 3.11 the estimate had borrowed from
  `am_onyx` in Week 01. At that pace the 666-word script came to about 4.2 min, **over the limit**.
- Speed 1.1 only raised the pace to 2.71 w/s on the same sentence, so speed stays at 1.0 and
  the script was cut instead. It now has 572 words with the B14 placeholder, estimated at 3.6 min.
  No beat and no question was dropped.

**What Claude contributed:** the voice test, the measurement, the cut.

**Evidence and next step:** `make_sheet.py` (`WPS = 2.6`). The real length is measured from the
audio on Day 3.

---

## Entry 6 — 2026-10-14: Day 3, building with my existing toolkit checkout

**I tried / expected:** I told Claude not to make a fresh clone and to start Day 3 right away,
using my existing `brutalist.art` checkout (`6a8380a`, with my Week 01 patches).

**What happened:**
- **The toolkit's own README** (read first, as the assignment says) lists no show-tell builder:
  this checkout predates it. The show-tell *style* is followed by hand. Its drawing kit
  (`iso_kit.py`) was copied from the already-fetched upstream history (`git show`, not a clone)
  into `_reference/` and pasted into `scenes.py`, as the skill says to do. The instructor-portrait
  helper (`professor_bear`) was left out.
- **Folder:** the toolkit expects films under `youtube/brutalist/`. A directory junction,
  `brutalist.art/youtube/brutalist/final-project-film` → this folder, lets it build here
  without moving files. ⚠ Remove it with `cmd /c rmdir`, never a recursive delete, which
  would follow the junction into this folder.
- **Outro conflict:** `bookend_check.py` requires `ClaudeTitleOutro`. That component
  hardcodes `@NikBearBrown` ("HARDCODED — no prop, no lookup, no override"). The assignment
  forbids the instructor's credit line, and its rule governs. A new `PitchOutro`
  (`runtime/remotion/src/illustrations/pitch.tsx`) credits me instead, so `bookend_check`'s
  OUTRO rule will fail by design. Week 01's `SubmissionOutro` wasn't reused because it
  hardcodes "Kokoro am_onyx" in its credit line.
- **No `ShowTellCard`** in this checkout, so B06 (the real run-2 counts) became a Manim drawing.
- **EB Garamond** ships in `runtime/fonts/` but isn't installed in Windows. `scenes.py`
  registers the font file with manimpango.
- **Audio:** 15 of 17 beats voiced with Kokoro `am_michael`, $0.00, **194.1 s** total.
  B04 (MyVisaJobs) and B14 (my reason) are not voiced, and `--only` was used so the B14
  placeholder could not be. The toolkit's own sentinel check only catches `[PLACEHOLDER]`.
- **Stills first:** the first contact sheet had 5 broken layouts (objects into the corner
  tag, a crate leaving the frame) and a crate hidden behind a tray's back. Fixed over
  two more rounds.
- **Gates before render:** Gate A (static scene check) 15/15 clean · Gate L (beat-mix lint)
  clean · `factcheck_check.py` 2 blockers. Both are the PENDING rows for B04 and B14, as intended.

**What Claude contributed:** all of the above: `scenes.py`, `pitch.tsx`, the `Root.tsx`
registration, the junction, `FACTCHECK.md`, `PROMPTS.md`, the audio run and the layout fixes.

**Evidence and next step:** `scenes.py`, `FACTCHECK.md`, `mp3/`. Next: the `run.sh` review cut.

---

## Entry 7 — 2026-10-14: my two inputs, and the first Gate B failure

**I tried / expected:** I gave Claude the two missing pieces. (1) I looked at MyVisaJobs on
**2026-10-07**, and I confirmed that B04's line matches what I saw: it lists sponsors and their
past job counts, and doesn't route a sponsor with nothing open to networking. (2) My reason: *"I
believe this is something I am also going through job applications, and I needed to understand
what's the best and efficient strategy to get a job rather than just doing 100-200 applications
every day."* I asked Claude to make it clearer if needed.

**What happened:**
- Claude tightened my reason for B14 to 18 words: "I picked it because I'm job hunting too, and
  I wanted a smarter strategy than a hundred-plus applications a day." The brief keeps "100–200".
- `make_sheet.py` now exits 0. B04 and B14 were voiced: **all 17 beats, 226.4 s of audio (~3:48
  with the lead-in and outro tail)**. `factcheck_check.py` has no blockers left.
- First `run.sh`: BIDEA, BOUT, B00, B01 and B02 rendered and passed Gate B. **Gate B FAILED on B03**:
  "label on a curve/line: `network`" at t≈9.2 s, where the label touched the tray's bottom corner.
  The clip was not slotted. The fix moved the label beside the tray, and the build was re-run.

**What Claude contributed:** the wording, the audio, the B03 fix.

**Evidence and next step:** `layout_audit.md` (the failing report, before the fix). Next: finish the build and read Gate V.

---

## Entry 8 — 2026-10-14: the first full cut fails Gate V, and is fixed rather than submitted

**What happened:**
- Second `run.sh`: B03–B11 rendered and passed Gate B. **Gate B (strict) stopped on B12**: a WARN
  "outside safe area: `check by hand`" (right edge 6.84 > 6.2). The label moved left of the tray.
  B12–B14 were then pre-audited with the same command `run.sh` uses (CLEAN ×3). The first try at
  that pre-audit failed because a relative path through the junction resolved to the wrong folder.
- Third `run.sh`: all 15 scenes slotted, and the toolkit compiled the review cut, **226.8 s (3:47)**.
- **Gate V FAILED: 34 frames sampled, BLOCKER 0, MAJOR 6.**
  - `low-contrast` 0.27–0.28 (< 0.30) on B00, B01 and B11 (twice). The cause: large pale kraft
    surfaces, a pale bar, and in B00 a label caught mid-fade at the midpoint frame, because one
    `play` call missed the midpoint guard.
  - `underfill` 38% (< 55%) on the outro, twice.
- Fixes: dark plinths under B00's crate and B01's box (the show-tell skill's own fix for
  low contrast); darker bar tones in B11; the midpoint guard on B00's label; a larger outro with
  framing rules. **No waiver was used to pass Gate V.** The failing cut, its `REPORT.md` and its
  contact sheet are kept in `_superseded/2026-10-14-gateV-1/` as the record.

**What Claude contributed:** the diagnosis and the fixes.

**Evidence and next step:** `_superseded/2026-10-14-gateV-1/REPORT.md`. Next: the Gate V re-run.

---

## Entry 9 — 2026-10-14: Gate V passes, but a frame read finds a defect no gate caught

**What happened:**
- Re-run: B00, B01 and B11 re-rendered (Gate B CLEAN ×3), outro re-rendered, cut recompiled
  (226.8 s). **Gate V: 34 frames, BLOCKER 0, MAJOR 0.** `run.sh` exited 0.
- Claude then sampled every beat at 90% of its length and read the frames. **BIDEA never showed its
  correction**: the film's opening idea ("apply to" → "network with") was missing, and the writer
  still read "…apply to" when the beat ended. Every gate had passed it.
  - Cause 1: `BrutalistHesitantWriter` matches triggers **one word at a time**
    (`p.text.split(/(\s+)/)`, then `triggers.indexOf(core)`), so the two-word trigger "apply to"
    could never match. The show-tell skill warns about punctuation in triggers, not about this.
  - Cause 2: the correction is timed by typing speed, not by the voice. The spoken correction
    came at 12.5–13.4 s of a 13.5 s beat.
  - Fix: two single-word triggers (`apply, to` → `network, with`), and the question moved to the
    start of the narration so the correction lands as it's spoken. The words are unchanged; only
    the order is. BIDEA was re-voiced.
- Also: the "network" (B03) and "check by hand" (B12) labels were moved further from their trays.
  Gate B passed them, but on the frames they looked crowded.

**What Claude contributed:** the frame read, the diagnosis (from the component source), and the fix.

**Evidence and next step:** `_superseded/2026-10-14-bidea/` (the cut without the correction). Next: re-check the frames.

**Result (same day):** BIDEA re-voiced (13.67 s), B03 and B12 re-rendered (Gate B CLEAN ×2), cut
recompiled: **227.0 s (3:47), 17/17 slots filled, Gate V BLOCKER 0 · MAJOR 0, `run.sh` exit 0.**
Frames read at 1, 2, 3, 3.6, 4.2, 5, 7 and 13 s: the writer types "apply" in terracotta (marked for
deletion), erases it, types "network", then "to" → "with". "Which companies should I network with"
holds from about 7 s to the end of the beat. The B03 and B12 labels now clear their trays.
Day 3 done: the first review cut (replaced by the revision in Entry 11).

---

## Entry 10 — 2026-10-14: Day 4, gates, listening check, honesty pass

**I tried / expected:** I told Claude to go ahead with Day 4: run the remaining gates, check
the narration, and check every claim against the honesty rule.

**What happened:**
- **`bookend_check.py`: first run BLOCKED** ("OUTRO handle is empty — must be 'Akshit Verma'").
  Claude had predicted (Entries 6 and 8, and the shot list) that this check would fail by design
  because the outro isn't `ClaudeTitleOutro`. **That prediction was wrong.** The check reads the
  outro's `handle` and matches it to `channel_title`; it doesn't check the component. The outro
  already shows "Akshit Verma", so `handle` was set to that. **Re-run: PASS.**
- **`align.py`** (faster-whisper word timing): 17/17 aligned, 0 fallbacks. It places *known*
  words, so it can't catch a mispronunciation.
- **Blind transcription** (faster-whisper `small`, each beat's mp3 diffed against its script,
  `_qc/whisper_check.json`): most differences were whisper spelling only ("16", "labeled",
  "Clawed" = how "Claude" is said, "Zooks" = how Zoox is said). Two were real:
  - B06 "two apply" was heard as **"to apply"**: ambiguous by ear. Now "two to apply, one to network…".
  - B07 "I decided the fix" was heard as **"I decided to fix"**, which changes who did what.
    Now "I chose the fix". Checking Kokoro's phonemes showed "résumé" (/ˈrɛzuːmeɪ/) and
    "Form D filings" are voiced correctly, so they were left alone.
- **Honesty pass, every line** (past tense only for what exists, no invented results):
  - B03 "A student **stops** applying…" read as an outcome with real users, and there are none.
    Now "So a student **can** stop…".
  - B09 "Claude Code stops at **each** gate for my sign-off" overclaimed. The recipe's gate
    table: G1 (board map) and G3 (outreach sign-off) are human; G2 (liveness) is automatic.
    Now "the human gates". B14 likewise: "signed its human gates".
  - The brief's "It saves…" became "It will save…".
- B06 and B07 re-voiced and re-rendered: Gate B CLEAN ×2, Gate V 0/0, bookend PASS. Whisper now
  hears "Two to apply, one to network, 107 to check by hand, 13 to skip" and "I chose the fix".

**What Claude contributed:** the checks, the transcription diff, the honesty findings and the
rewording. **Still mine to do:** watch the film and sign `FACTCHECK.md`.

**Evidence and next step:** `_qc/whisper_check.json`, `FACTCHECK.md` rows 7, 19 and 26. Next: B03, B09 and B14 re-render, then the final gate run.

**Result (same day):**
- B03, B09 and B14 re-voiced and re-rendered (Gate B CLEAN ×3). Whisper hears "can stop applying",
  "stops at the human gates" and "signed its human gates".
- **Gate T** (`type_check.py`, inside `./art final`): **PASS**. Eight checks ran on 17 beats with
  0 FAILs (min-size, overflow, contrast, local contrast, kerning, bbox overlap, card clip,
  no-wordy-card). Only §8.10 (redundancy, advisory) was skipped.
- `./art final … --height 1080` wrote the master, **228.8 s (3:49)**, 1920×1080, 24 fps, H.264/AAC,
  byte-identical to the review cut. **Gate V on the master: 34 frames, BLOCKER 0, MAJOR 0.**
  `bookend_check` PASS. `factcheck_check` clean (28 rows).
- Two SKIN LINT advisories (non-blocking) note that the opening and outro aren't the
  instructor-branded defaults. That's expected, and the assignment requires it.
- The master's frames were read: there's no burned-in text and no instructor credit anywhere.
  ("drawtext: yes" in the compile log means the ffmpeg filter is available. Per `compile.py`'s
  header, it is used only for the running timecode in `--review` cuts, which `ART_BURNIN=0`
  turns off, and the master is compiled without `--review`.)
- Unchanged and noted: whisper hears "scorer" in B03 as "score". It's left as is, because the
  sentence still reads correctly.

**Day 4 done.** Mine to do: watch the film and sign `FACTCHECK.md`.

---

## Entry 11 — 2026-10-14: my review of the film, and the revision it led to

**I tried / expected:** I watched the Day 4 film and asked for six changes:
1. A one-word project name, with the video starting on it and going straight into the explanation.
2. In the intro, say the pitch was made by me, without "in a synthetic voice".
3. Correct visuals: boxes were passing over the conveyor gates, and the table had two legs (I sent
   three screenshots). Make it more visually appealing, with smooth transitions and effects.
4. The visuals should explain the content better, together with the audio.
5. Captions for the whole video.
6. At the end, remove "Everything marked proposed is still to be built", the narration line
   and the "built with brutalist" line.

**What happened:**
- **Name.** Claude suggested Warmlist; I didn't like it. From a second list (Sponsight, Triage,
  VisaLens, Beacon, Inroad, Foothold, SponsorScout, H1Bridge, Visa Bridge, Vantage, Waypoint,
  Doorway, each checked for how Kokoro pronounces it), **I chose SponsorScout**. Slug and title
  changed; narration now says "SponsorScout" in the title beat, B00, B03 and the outro.
- **Intro.** It now opens on the name: "SponsorScout. A final project pitch by Akshit Verma.
  I'll show what already ran, and what I will build." Claude kept "**by** Akshit Verma"
  rather than "I'm Akshit", so the synthetic voice never claims to *be* me. The voice is
  still disclosed in README.md and SOURCES.md.
- **Outro.** Now only: SponsorScout · a pitch by Akshit Verma · INFO 7375 · Final Project Pitch.
  The corner tags still mark ran / proposed on every drawing, and the title beat shows that legend.
- **Visuals rebuilt** (`scenes.py` rewritten). Cause of the overlap: every crate was drawn on top
  of everything. Now there's a depth order: a gate's back post, then the crate, then the front
  post, then the lamp, and trays hold crates between their walls. The desk was replaced by a
  clearer three-step diagram in B05. Each scene now has:
  - a staggered entrance and a fade at its end (smooth transitions)
  - a conveyor whose dashes move with the crate, and lamps that pulse
  - reveals timed to the exact spoken word, from `words.json` instead of an estimate
  - more explanatory labels (the four verdicts; the engine-vs-SponsorScout split; the three
    60-second steps; the blocked actions)
  - nothing in the caption band
  The hesitant-writer opening is replaced by two Manim title beats, so the film has one style.
- **Preview rounds before rendering:** three rounds of low-resolution frames at 50% and 88% of
  every beat. They found label collisions (B00, B02, B04, B09, B12, B14), labels past the safe
  edge, and reveals too late to read. All fixed before the full render.
- **Captions:** `tools/make_captions.py` is reused from my Week 01 film. It builds them from
  `mp3/words.json`, so they're the narration verbatim, in sync.
- New audio for BOPEN, BIDEA, B00, B03 and BOUT; all 18 beats re-aligned (fallback 0). **223.7 s of audio.**

**What Claude contributed:** the name options, all redrawing, re-timing and re-voicing.
**Mine:** the six notes, the name, and the review of the result.

**Evidence and next step:** v1 (the film I reviewed) is kept in `_superseded/2026-10-14-v1-before-revision/`.
Next: full render, gates, captions.

**Result of the revision (same day):** four gate failures, each fixed at the source, none waived:
- **Gate B**, BIDEA: "label on a curve/line". The strike-through line across "apply to?" was
  intentional, but it breaks the rule. Now the words grey out with a cross beside them.
- Pre-audit of all 17 scenes in one pass (so the render doesn't stop one scene at a time):
  B08 and B13 had labels past the right SAFE edge (6.43, 6.39 > 6.2). Moved in.
- **Gate V**, 4 BLOCKERs: `edge-bleed` on B00 and B01. The dark plinths poked past the left
  SAFE edge, which Gate B (text only) can't see. Scenes shifted right, then checked by
  measuring rendered pixels.
- **Gate T**, B09: "bbox-overlap 100%". The token stopped exactly on the gate square. It now
  stops just short, and the sign-off check sits clear of the loop line.
- **Claude's frame read of the captioned film** (2 frames per beat) found what no gate did: a
  duplicate "Akshit Verma" burned in under the title-beat caption, a label clash in B00 and B04,
  and B06's "job seeker: fictional" showing only in the beat's last second. The duplicate is
  `compile.py` burning `metadata.channel_title` into beat one. It's turned off with a new
  one-line opt-in switch, `ART_CHANNEL_TITLE=0` (toolkit change, `compile.py:767`). The field
  stays set, because `bookend_check` needs it.
- **Final: 224.0 s (3:44)**, 18/18 slots, 1920×1080 24 fps, captions burned in (110 cues, from
  `mp3/words.json`). Gate B CLEAN ×17 · Gate V 0/0 on the cut and on the captioned film ·
  Gate T PASS · bookend PASS · factcheck clean (29 rows).
- Each failing version and report is in `_superseded/2026-10-14-v2-*`.

---

## Entry 12 — 2026-10-14: Day 5, sign-off, paperwork, folder and zip

**I tried / expected:** "Go ahead", which Claude recorded as my approval of the final film. Then:
finish Day 5, **don't push anything yet**.

**What happened:**
- **Sign-off** recorded in `FACTCHECK.md` (Status line), worded exactly as I gave it.
- **Blind listening check, all 18 beats** (`_qc/whisper_check.json`): spelling-only differences
  ("Sponsor Scout", numerals, "labeled", "Clawed" = "Claude", "Zooks" = "Zoox"). One near-miss:
  BOPEN's "A final project **pitch** by" was heard as "pitched by". The meaning is the same, so
  it was left as is and is noted here.
- **Fresh gate log** of the final files (`_qc/gates-2026-10-14.txt`): F clean · L clean · A 17/17 ·
  B 17/17 CLEAN · T PASS · V 0/0 on the captioned film · bookend PASS.
- **Toolkit changes** exported to `toolkit-changes/`. Claude tested the apply steps by rebuilding
  every touched file from `6a8380a` and applying the patches: all ten files byte-identical to my
  checkout. The first try, a git worktree, failed on Windows' path-length limit; then it worked.
- Written: `README.md`, `SOURCES.md` (tools, versions, licences, who did what). `BUILD-PROMPT.md`
  and `PROMPTS.md` were rewritten for the final pipeline.
- **Packaged** to the course repo folder `fall-2026/akshit-v/final-project-film/` and to
  `Verma_Akshit_INFO7375_FinalProjectFilm.zip`. Left out: `_reference/` (toolkit copies), render
  caches, the uncaptioned and review cuts, the toolkit's own status files (they contain local
  paths), and every superseded video (the failing *reports* are kept).
- **Not done, on purpose:** no commit, no push (my instruction). The Canvas submission needs the
  GitHub folder link and the final commit hash, so that waits for me.

**What Claude contributed:** all of the above. **Mine:** the sign-off and the no-push decision.

---

## Entry 13 — 2026-10-14: one name everywhere, and a check that every file is current

**I tried / expected:** I asked for SponsorScout to be the only name in every file. Then I asked
whether FRICTIONAL.md and the other files were up to date.

**What happened:**
- The earlier working title was removed from the submission. Claude **edited one line of an
  earlier entry** (Entry 9: the Day 3 file name became "the first review cut") and this file's
  header. Nothing else in earlier entries was changed.
- **Three of the first version's passing gate reports** (its TYPECHECK, gate log and listening
  check) were taken **out of the submission**, not edited. They're the toolkit's own output for
  a film that really carried the old title, so editing them would have made them false. They
  stay in my local `_superseded/` archive. The failing-gate reports from both versions don't
  carry the old title and are still included.
- Claude searched every submission file, the zip and the film's metadata: no old title left.
- **Stale details found and fixed:**
  - SHOTLIST and the beat sheet still said "apply to?" is "struck through". It now greys out
    with a cross, because the strike line failed Gate B.
  - The beat sheet's metadata said the synthetic voice is "disclosed in BIDEA and BOUT". It is
    disclosed in README and SOURCES, not on screen, per my request in Entry 11. It also said the
    film opens on the hesitant writer, which was removed.
  - README now states the listening-check result.
  - FACTCHECK gained row 29, tying the on-screen numbers to their spoken, sourced claims.
  - SOURCES now lists what was left out.
- `make_sheet.py` was re-run so `beat_sheet.json` matches. The course folder and zip were re-synced.

**What Claude contributed:** the search, the edits, the re-sync. **Mine:** the request.

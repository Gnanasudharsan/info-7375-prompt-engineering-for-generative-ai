# FRICTIONAL — honest work log

Dated entries, newest at the bottom. What I tried, what broke, what changed.

> **Who wrote what:** the bullet-point log entries were drafted by Claude Code during our working sessions, from what we actually ran and decided. I checked them. The **In my own words** sections are written by me. The *Reflection: points I picked* section uses Claude's wording for points I selected.

## 2026-10-08 (written 2026-10-09, from memory)
- Read the assignment brief.
- Watched the course AI-policy video.
- Thought about possible project ideas; did not pick one yet.
- Looked at the Brutalist repository.

## 2026-10-09
- Read the assignment. Chose project idea: **Seeded Faults** — Claude-generated data-quality tests scored against planted faults. Picked it because it fits Data Engineering / BI roles and can be verified by a stranger.
- Used Claude Code (Opus 5.5) to help choose the project from three options and to draft PROJECT-BRIEF.md, beat_sheet.json and the scaffolding files. I need to review and rewrite every line in my own words before submission.
- I wanted the folder under "Projects"; there is no `~/Desktop/Projects`, so the work lives in `~/Projects/INFO7375/fall-2026/atharva-c/final-project-film/`.
- Brutalist: my local checkout (`~/Applications/brutalist.art`, commit 29ba0e8) is behind GitHub (22264a3). The `show-tell` skill is not in my checkout. Next: pull and check whether `show-tell` appears.
- Open item: the alternatives (Great Expectations, dbt-expectations) are named from general knowledge, not yet checked hands-on. I must try them before the film states what they do or don't do.
- Open item: confirm which of my GitHub repos are public before citing them as evidence.
- Set up a practice sandbox (`~/Projects/seeded-faults-sandbox`, not part of this submission). Installed great_expectations 1.24.0, dbt-core 1.12.5, dbt-duckdb 1.11.0, pandas 3.0.6. No install errors.
- Downloaded NYC TLC yellow taxi trips, January 2024 (public; 2,964,624 rows, 19 columns). Kept the first 2,000 rows as `trips_sample.csv`.
- Great Expectations: ran one hand-written check (`passenger_count` not null) on the 2,000-row sample → passed, 0 unexpected. I had to write the rule myself.
- First planted-fault test (script drafted by Claude, run by me): blanked `passenger_count` in 50 random rows. Same check → clean file passed (0 unexpected); faulted file failed with exactly 50 unexpected. This is the project's core idea done once by hand, for one fault type.
- Checked whether GX Core 1.x (free library) suggests expectations automatically:
  - Searching the docs for "profiler" returned only tutorial pages (dbt tutorial, SQL connection, uniqueness use case) — none answered the question.
  - The "Create an Expectation" page (https://docs.greatexpectations.io/docs/core/define_expectations/create_an_expectation/, read 2026-10-09) describes choosing an Expectation from the Gallery and setting its parameters by hand. No automatic-suggestion step.
  - Searched the installed great_expectations 1.24.0 package for "data_assistant", "DataAssistant" and "onboarding": no matches.
  - **Finding:** in GX Core 1.24.0 I wrote each check by hand; I found no automatic suggestion feature in the docs page or the installed library. GX Cloud not checked — the docs site no longer has Cloud pages, so the film will not make any claim about Cloud.
  - This changes the brief: section 2 said GX "can propose expectations from your data". That was from general knowledge (older versions) and is not supported by what I checked. Brief and beat B03 must be corrected.
- dbt: set up a minimal dbt-duckdb project in the sandbox (`dbt_try/`, files drafted by Claude) with one model reading the taxi CSV and two hand-written tests (`not_null` on passenger_count, `accepted_values` 0–6 on payment_type).
  - Clean sample: `dbt build` → PASS=3 (view + both tests passed).
  - Faulted sample (50 blanked passenger_count values): not_null → FAIL 50; accepted_values → PASS (column untouched). Same result as the GX run.
  - Observation: as with GX, dbt ran exactly the tests I wrote. It did not suggest any, and it says nothing about faults I didn't write a test for.
  - Still open: read the dbt-expectations README (who maintains it, whether it generates or scores tests).
- dbt-expectations: Claude read the README on the dbt package hub (https://hub.getdbt.com/metaplane/dbt_expectations/latest/, v0.10.10, 2026-10-09) and summarised it; I checked the summary against the page. It's a maintained fork of the original calogica package, now under metaplane. It adds ~60 GE-style test types that you still choose and write in `schema.yml`. Nothing in the README about generating tests, coverage, or planted faults.
- Step B: rewrote beat B03 and brief section 2 to use only what I checked today. Removed the earlier "GX can propose expectations" claim.
- Step C: checked which of my GitHub repos are public (GitHub API, 2026-10-09): 8 public, 1 of them a fork. I cite only public repos. Citing DMDD_FinalProject (CRMS, solo, has `testing.sql`) in beat B08 and both CRMS and Chinook_ADF in the brief. Chinook_ADF's README is only a title; worth improving before anyone opens it.
- Added `evidence/2026-10-09-first-planted-fault/`: the GX and dbt scripts plus logs, so the past-tense claim in B03 can be checked. Logs come from a re-run at 17:32 EDT (same numbers as the first runs). Data files not committed; SHA-256 fingerprints and download steps are included.
- Honesty pass on narration: fixed 4 lines that were out of date after today's test or overclaimed. B01 and B09 no longer say nothing exists; B02 now calls "AI-written tests make this worse" a guess to be measured, not a fact; B06 says the first build is the full fault-injection script.


## 2026-10-10
- Updated Brutalist with `git pull`: 29ba0e8 → b21f625. My local change to `runtime/remotion/package-lock.json` didn't block the pull.
- `show-tell` skill now exists (`skills/make/show-tell/`). Read its SKILL.md. **Conflict with the assignment:** show-tell's fixed bookends use the instructor's persona — the "Liam, in for Bear" greeting, the Kokoro `am_onyx` voice, and a spoken "@NikBearBrown" outro. The assignment says to narrate as myself with no instructor name, persona or credit line. Plan: keep show-tell's drawing style (one isometric picture per beat, minimal labels) but replace the greeting and outro with my own, and use a different Kokoro voice. If the toolkit's bookend check fails because of this, I'll record it here, not hide it.
- Ran `./setup --install`. Two problems:
  1. **Wrong environment.** My sandbox venv from yesterday was still active in that terminal, so pip installed Brutalist's Python deps (manim, kokoro-onnx, faster-whisper…) into `seeded-faults-sandbox/.venv` instead of Brutalist's own `.venv`. Fix: activate `~/Applications/brutalist.art/.venv` before any Brutalist command.
  2. **Setup exits 1 at its "ElevenLabs guard".** The guard scans the repo and stops if any file references ElevenLabs. It found hits in the toolkit's own example folders (`youtube/brutalist/claude-liam-brutalist-command-setup/…` and others, which came with the update), so it stopped before running its readiness checks. Not caused by my files. I didn't edit the toolkit to get around it.
- Workaround: ran the readiness checks by hand in Brutalist's own venv. All dependencies import (manim 0.18.1), ffmpeg 9.0.2 is present, the Kokoro model files were already downloaded, and `runtime/scripts/setup_smoke_kokoro.py` passed: "kokoro synth OK — mean_volume -21.8 dB". `./art --list` works and lists `show-tell`.
- Asked Claude to rewrite the narration so the beats connect and sound less stiff. It rewrote all ten beats with the same facts and tenses (recorded in SOURCES.md). Next: read it aloud and change lines into my own words.
- Voice: listened to Kokoro samples of B00 (am_adam, am_michael, am_eric, bm_george) and chose **am_michael**. Avoided am_onyx and af_bella (instructor persona voices) and am_liam (the persona's name).
- Generated narration audio with Brutalist's `generate_audio_kokoro.py` (am_michael, local, $0.00) in a build folder outside this submission (`~/Projects/seeded-faults-film-build/`), so mp3s and render caches stay out of the repo. Narration runs **3:33** (212.7 s); B03 is the longest at 33.7 s. Brutalist's approval gates didn't apply, since this isn't a fellows or professor-notes reel.
- Pronunciation check: transcribed every beat with faster-whisper (base.en) and compared it to the script. Kokoro had trouble with "Claude" in the middle of a phrase ("contract Claude has to follow" came out as "clause"; "tests Claude generates" as "claw"; "tests that Claude writes" as "clawed rights") and with "caught-or-missed" ("quad or mistable"). Reworded B01 and B06 without changing their meaning ("the prompt contract that Claude follows", "the tests written by Claude", "a table of what was caught and what was missed") and regenerated those beats; the re-transcription now matches. To check by ear: "Seeded" (Whisper heard "seated"/"ceded"), "GitHub" in B01 ("get hub"), "plants" in B06 ("plans").
- Film structure decided: open straight on B00 ("Hi, I'm Atharva"), end with my own short title outro ("Seeded Faults. Atharva C."). Dropping show-tell's persona bookends (hesitant writer with the "Liam, in for Bear" greeting, the terms card, Your Turn). The toolkit's bookend check allows this through its `bookend_exempt` list plus `channel_title` set to my name. Narration is not locked yet; I'm editing lines before the pictures are built.
- Narration locked. Claude built the film in show-tell style (scenes.py: 10 drawn Manim scenes plus a drawn title outro; make_sheet.py; FACTCHECK.md, SHOTLIST.md, PROMPTS.md), working in the build folder.
- **Outro problem:** the toolkit's standard outro card (`ClaudeTitleOutro`) hard-codes the instructor's handle "@NikBearBrown" with no way to change it. Using it would put the instructor's credit line in my film, which the assignment forbids. So the outro is a drawn Manim title scene ("Seeded Faults / Atharva C"). Consequences: compile.py prints an advisory OUTRO LAW warning, and the standalone `bookend_check.py` will report the missing ClaudeTitleOutro. Neither blocks the render. I'm recording them instead of hiding them.
- Gate results while iterating (1080p review renders): Gate A first warned that the "CONSTRUCTED" labels in B01/B04 sat outside the safe area, and Gate B (strict) refused to slot B04 → moved the labels inward. GATE T then failed twice: B05's handwriting squiggles read as text below the size floor, and in B07 the balance beam, post and pans fused into one giant "text" blob → recoloured those in kraft. After the fixes, Gates A, B, W, V, F and T all passed on the 1080p test cut (3:37). Also moved B06's "1" badge off the "faults" label. 4K render started.
- 4K render: `./art run --height 2160` passed Gates A, W, B and V (0 BLOCKER/MAJOR); `./art final --height 2160` passed GATE T and wrote the verified master (3840×2160, 216.8 s = 3:37, sha256 3142aa40…0137). `bookend_check.py` fails as expected (no ClaudeTitleOutro, for the persona reason above); explained in gate-reports/README.md. Copied the film, gate reports and film-source/ into this folder; updated README, BUILD-PROMPT and SOURCES.
- Still to do: watch the whole film and check every line against the honesty rule; check by ear the words Whisper flagged ("Seeded", "GitHub" in B01); sign off FACTCHECK.md; fill in my own narration edits in SOURCES.md, or say there were none.


## 2026-10-12
- Got feedback on my previous assignment: random variation was described rather than shown, my Frictional log was drafted by Claude with no reflection of my own, and on-screen text was too small. Applied all three lessons here:
  - **Shown, not described:** B03 now puts the real program output from 2026-10-09 on screen (GX `unexpected_count=0` on the clean sample, `=50` on the faulted one; dbt `PASS` vs `FAIL 50`), labelled "real output · 2026-10-09", copied verbatim from `evidence/…/output/`.
  - **Text size:** every label now has a 44-point minimum (it was 32–42), the CONSTRUCTED stamps are 48, and I removed the toolkit's tiny corner name on B00 (`channel_title`). My name is spoken in B00 and large on the outro.
  - **My own reflection:** added the "Who wrote what" note at the top and "In my own words" sections for me to write.
- Re-render: the 1080p test first failed Gate B (strict) because the larger CONSTRUCTED stamp in B01 crossed the safe area → moved it inward. After that, all gates passed at 1080p. 4K re-render started.
- 4K re-render done: Gates A, W, B, V passed (0 BLOCKER/MAJOR), GATE T PASS, master "ready" (3840×2160, 216.8 s, sha256 fd90da0c…c84b). Replaced the film and gate reports in this folder; the old master is kept outside the repo.

### Reflection (2026-10-12): points I picked
Claude offered a list of moments from this project. These are the ones **I picked** as true for me. The wording is Claude's; the choices are mine.

**What surprised me**
- The not-null check caught exactly 50 of 50 planted blanks, in both Great Expectations and dbt.
- Both tools passed the clean data perfectly, which proves nothing about whether they'd catch problems.

**What I believed that turned out wrong**
- The brief originally said Great Expectations "can propose expectations from your data". Checking the docs and the installed library didn't support that, so the claim was removed.
- My first narration said things like "nothing exists yet", but by the end of Day 1 one real test did exist.

**What was frustrating**
- Brutalist got installed into the wrong Python environment, because the sandbox one was still active.
- The setup error, and having to check readiness by hand.
- Text checks failed twice (B05, B07), and Gate B refused B01 once.
- The feedback from my last assignment, and having to redo the text sizes.
- Re-rendering takes about 20 minutes each time.

**What I'd find hardest to explain to a TA**
- How `ge_fault.py` plants the 50 blanks (`random_state=7`, blanking `passenger_count`).
- What `unexpected_count` means in Great Expectations output.

### In my own words (2026-10-12)
The most surprising part of the test run was seeing the numbers match exactly: the script blanked 50 rows in passenger_count, and both Great Expectations and dbt flagged exactly 50 unexpected rows. What bothered me was the clean run right before it. Both tools passed the clean sample with zero errors, which felt good for a second until I realized that a green test run tells you nothing about whether your assertions would actually catch a bad row.

I also had to roll back an assumption I had made in the brief. I thought Great Expectations still suggested tests automatically from data, but when I searched the docs page and searched the installed package for those features, nothing came up. In GX Core 1.24.0, I had to write the rule by hand. dbt worked the same way—it only evaluated the assertions I explicitly wrote in schema.yml. In the two tools I tested, test generation wasn't automatic at all.

Most of the time lost went to small setup and formatting issues. I accidentally ran ./setup while my sandbox virtual environment was still active, so packages installed into the wrong place. Later, Gate T's text-size check failed because Manim squiggles and drawn scale parts were being measured as undersized text, and Gate B rejected B01 because a label sat outside the safe margin.

If a TA asks me to explain the core test in person: ge_fault.py uses random_state=7 to deterministically set 50 random values of passenger_count to null. Running the check against that file outputs an unexpected_count of 50, which simply means 50 rows violated the not-null rule. The clean data proved the rule doesn't produce false positives; the faulted data proved it actually detects the failure.

## 2026-10-13 – 2026-10-14
- Read the 11 claims in `film-source/FACTCHECK.md` and signed it off. Confirmed I made no narration edits of my own after Claude's rewrite. Checked the folder against the assignment with Claude: updated the brief's exists/will-exist lists, removed a stray `.Rhistory`, replaced the SOURCES.md placeholders.
- Watched the final 4K film all the way through (2026-10-14). It looks right; no changes needed.

- Submitting to the class repo (github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai). Its `fall-2026/README.md` says no full names are stored there, and my Week 01 used "Atharva C". So I replaced my full surname everywhere in this folder and the film to "Atharva C" (including earlier log lines here). Re-voiced and re-rendered only the outro ("Seeded Faults. By Atharva C."); Gates V and T passed again; new master is 3840×2160, 216.5 s, sha256 96f04f51…a68e. Commits go to the class repo as "Atharva C" with GitHub's noreply email, same as Week 01.
- Personal-data check before final submission, because my previous assignment lost points for committing personal details (immigration data and my own job-search background). Searched this folder for résumé, immigration, employer, application and contact details, local file paths and my full name in any form. Found and fixed: a `channel` config field that spelled out my surname (now `atharva-c`) and a mention of a private team project from my background (removed). What remains is what the assignment asks for: my target role, and links to my own public course repos as evidence. The data in `evidence/` is public NYC taxi data; there is no résumé, transcript, contact or immigration information in the folder or the film.

# FRICTIONAL — Final Project Pitch Film

Two kinds of entry, kept apart on purpose (course AI policy: AI may organise notes; the experience must be mine):

- **Part A: build log.** Drafted by Claude Code from what happened in the 2026-10-14 session: commands run, what broke, what was changed. These are factual and traceable to files in this folder.
- **Part B: my entries.** Written by me, in my own words. Claude did not write them.

---

## Part A: build log (Claude Code session, 2026-10-14)

**2026-10-14 · choosing the project**
- Tried / expected: Claude surveyed my local repos: the Reallocation Engine recipe `data-role-sponsor-match` (DRAFT, 2026-10-03), my NBA RAG app (Dec 2025), Jobsekr (team repo; I have 5 commits), and my Week 01 film. It proposed two projects; I chose "grow the sponsor-match recipe into an agent".
- What happened: reading `assignments/assignment-final-project.md` showed that the December final must be **agentic** (a loop, tools with an enforced permission policy, a stop condition, a human gate). So the pitch describes those parts as "will".
- Honesty check: the recipe's own SOURCES.md says Claude wrote all its code and tests, and that I accepted them unchanged. So the film does not use the recipe as evidence of my coding skill. Beat B11 says this aloud.

**2026-10-14 · toolkit**
- `brutalist.art` was at `cd4bf20`; upstream was at `519fcbb` (approved original props, ShowTellCards, Gate W fixes, and a Manim 0.20 pin).
- Saved my local Windows patch to `.shim/local-win-2026-09-27.patch`, kept a branch `win-setup-2026-09-27`, stashed, ran `git pull --ff-only`, and reapplied the one-line `npx` fix in `runtime/scripts/remotion_scenes.py`.
- Upgraded the venv: Manim 0.19.1 → 0.20.1, Pillow 10.4 → 12.3 (`requirements.txt` says 0.18 renders one frame short and `compile.py` then refuses the film).

**2026-10-14 · the skill's defaults conflict with the assignment**
- show-tell defaults to Liam's voice ("Liam, in for Bear") and a spoken `@NikBearBrown` outro. `runtime/remotion/src/scenes/ClaudeTitleOutro.tsx` hard-codes `const HANDLE = '@NikBearBrown'` and the mascot. ClaudeDefinitions defaults its folder label to `@NikBearBrown`.
- The assignment says to narrate as yourself and not use the instructor's name, persona or credit line. Response:
  - my own recorded voice;
  - no BDEFS or BHTF;
  - my own Manim outro `BOUT_Title`, declared in `bookend_exempt` with a reason.
- `compile.py` only warns about a non-ClaudeTitleOutro outro (line ~529); `bookend_check.py` is not wired into `art run` or `art final`.
- EB Garamond was not installed on Windows (Pango would silently fall back), so `fonts/` carries the OFL TTFs and `scene_body.py` registers them.

**2026-10-14 · fact check caught a false claim in the draft**
- The draft B09 said "the CSV keeps only five titles per company". `evidence/csv_title_coverage.py` showed otherwise. Of the 1,552 companies with approvals, 862 list one title, 1,510 list five or fewer, and 42 list 6–14.
- Rewritten to "more than half the sponsoring companies … list just one title" before I recorded (FACTCHECK #17). The project brief was corrected too.
- Also checked: the DOL LCA record layout does have `JOB_TITLE`. An LCA is not an approval, so the brief says so.

**2026-10-14 · gates before rendering**
- Gate A (`static_scene_check.py`, run on a scratch folder holding only `scenes.py`): B08 failed with "shapes never change", because its only shapes were added in the first play. Fixed by adding a check mark after the crates are sorted.
- Layout audit (`manim_layout_audit.py --curve-strict`):
  - B04 errors: "label on a curve/line" (`tool`, `log`), where the moving crate crossed the labels. Fixed by moving the labels 0.35 lower.
  - B05 warning: "outside safe area" (`Greenhouse API` at x 6.46). Fixed by moving it left.
- Gate W (`wcag_margin_check.py`): all 13 clean.
- Stills review (contact sheet): fixed overlaps in B00, B01, B10, B11 and BOUT. Removed a made-up command name (`$ triage`) from B03, because no such CLI exists yet.

**2026-10-14 · audio and word clock**
- `align.py` crashed: `TypeError: open() got an unexpected keyword argument 'metadata_errors'`. faster-whisper 1.2.1 passes it, PyAV 19 removed it, and `pip install "av<15"` has no wheel for Python 3.13.
- Fixed with `word_clock.py`, which decodes with ffmpeg and passes faster-whisper a numpy array. `align.py` itself is unchanged.
- **Rehearsal:** to test the gates before my recordings existed, the whole film was built once in a throwaway temp folder with a stand-in Kokoro voice (`af_heart`). That audio is not in this folder or the film.

**2026-10-14 · rehearsal results (stand-in audio, 1080p, temp folder)**
- `art run` failed before Gate V. ffmpeg could not parse the `drawtext=fontfile=` path to EB Garamond. It was a Windows path with an unescaped drive colon (`C:`) and a space in my user-folder name.
  - Local patch to `compile.py`: escape the path as `'C\:/Users/...'`.
- After that, Gate V failed **28 of 28** frames with `edge-bleed`, top-right edge. The cause was the review cut's burned-in timecode box, which is drawn only when ffmpeg has `drawtext`. My Windows ffmpeg build has it; the toolkit's Mac/Homebrew ffmpeg does not.
  - I did **not** change the gate. Instead, another local patch makes `ART_NO_TIMECODE=1` skip the timecode, so the review cut matches the Mac's. Gate V then gave 28 frames, 0 BLOCKER, 0 MAJOR.
  - Both patches are in `evidence/brutalist-local-windows-patches-2026-10-14.patch`.
- Gate T at 1080p failed six beats on §8.4 "kerning". The checker measures the darkest pixel band, which here was dark props (servers, tool blocks), not text. `type_check.py` skips that pixel check at 4K by design ("counter-spaces … false positives"), so it does not apply to the 4K master. To confirm on the real render.
- Gate T §8.1 min-size failed B09: an 8–14 px "text run". `type_check.py`'s own blob functions placed it on the `server-tower` prop's right face, at its slot stripes. Making the prop bigger did not help (14 px). Replacing it in B09 with the kit's plain `Iso.server` stack (dot lights only) passes at 0.5 and 0.85 of the beat. The "?" glyphs in B07/B09 were also swapped for drawn rings, since a "?" dot is a tiny blob.

**2026-10-14 · voice: from my recording to Kokoro**
- My first choice was to record my own voice, so Claude wrote a per-beat recording script and `finish_audio.py`.
- Later the same day I told Claude that a TA said a Brutalist voice is fine. Claude made four samples (af_heart, am_michael, bf_emma, bm_george). It left out `am_onyx` and `am_liam`, which are the instructor's Liam persona. I chose `af_heart`, and chose to disclose the synthetic voice in the README only.
- `RECORDING-SCRIPT.md` and the empty `recordings/` folder were removed. `finish_audio.py` now takes the Kokoro mp3s (`--src mp3 --prefix beat-`). Measured runtime: 3:29.7.
- Whisper check (`reports/PRONUNCIATION-CHECK.md`, faster-whisper `small`): F-1, H-1B, CSV, API, 404 and 1,640 all came out right.
  - "NBA RAG app" was spelled out letter by letter, as "N-B-A-R-A-G". Kokoro's phonemizer showed that "RAG" in that sentence becomes `ɑːɹɹeɪdʒiː`.
  - "Kommuri" came out as KAHM-yur-ee.
  - Fixed both with reel-local respellings in `pronunciation.json`, applied by `voice.py`; the toolkit is unchanged. "OPT" looked wrong when tested alone, but in its sentence it is said O-P-T, so no fix was needed.
  - Whisper still writes my name as "City Comery". It does not know the name, so only my ear can judge it.

**2026-10-14 · the real 4K build**
- Moved a stale `media/` cache from the layout audits aside before rendering, because the skill warns old caches push clips past their audio. Then ran `ART_NO_TIMECODE=1 art run . --height 2160`.
- Gates L, SHAPE, A and W passed for all 13 scenes. B00–B10 rendered and passed Gate B. The run was then **interrupted** while rendering B11, when the earlier Claude session ended (`reports/art-run-4k.log` stops there).
- Moved the half-written B11 cache aside and re-ran. `art run` renders only empty slots, so B11 and BOUT rendered and passed Gate B (`reports/art-run-4k-resume.log`). Gate V: 28 frames, 0 BLOCKER, 0 MAJOR.
- Every clip ended 0.06–0.10 s *before* its audio, so `compile.py` retimes them rather than centre-cutting.

**2026-10-14 · opener out of sync (found by looking, not by a gate)**
- In Gate V's contact sheet the opener already showed "data roles" at 50% of the beat, while the voice was still saying "H-1B visas". With `charMs: 30` the whole typing performance was over in about 4 s.
- First try, `charMs: 240`: the stills seemed far too slow. I had read frame numbers at 24 fps, but the `BrutalistHesitantWriter` composition runs at **30 fps** (`Root.tsx`).
- Bundled the component's own `buildTimeline()` with esbuild and printed the step times. At 240 ms per character: "H-1B visas" typed at 9.5 s (spoken "visas" 10.0 s), backspace from 11.0 s, "data roles" done 14.4 s (spoken 14.2–14.5 s), total 15.0 s inside the 15.4 s beat. Kept 240.
- Re-rendered only BIDEA. Checked frames of the master at 10, 12 and 14.7 s.

**2026-10-14 · final**
- `art final . --height 2160 --out exports`: Gate T PASS on all 14 beats. At 4K the §8.4 pixel kerning check is skipped by design, as the rehearsal predicted.
- Master `exports/sponsor-triage-pitch.mp4`: 209.875 s, 3840×2160, 24 fps. SHA-256 `8b02d2fb…7efb66` matched the receipt (this first master was later superseded; see below).
- Ran by hand: `master_check.py` PASS; `loudness_check.py` PASS (−20.34 LUFS, true peak −4.96 dBTP); `sharpness_check.py` PASS.
- Wrote `reports/RENDER-INTEGRITY.md`. My first draft compared the file with the *raw* sum of audio lengths (209.656 s, apparently 0.22 s off). The compiler's timeline rounds each beat up to whole frames (209.875 s), which matches exactly. Corrected the report.
- **Honesty-tag fix after the first master.** Looking at the end frames of B07–BOUT (Gate V's contact sheet showed only the first half), B09's tag read "RECORD · CSV and run of 2026-10-03". But the same picture shows the DOL data source being connected, which is a plan. No gate checks this. Changed the tag to "RECORD · CSV, run of 2026-10-03; DOL link: SKETCH", re-ran Gate A/W/layout on B09, re-rendered only B09, and rebuilt the master (`reports/art-run-4k-b09.log`, `reports/art-final.log`). The first master (`8b02d2fb…`) was superseded. The new master `8a516552…67ae45` (209.875 s) passed Gate B on B09, Gate V (0/0), Gate T, `verify_output`, and the master, loudness (−20.34 LUFS) and sharpness checks.
- Siddi confirmed on 2026-10-14:
  - the TA said a Brutalist voice is fine, with no condition attached;
  - Siddi built the NBA RAG app;
  - the name sounds right.
  No changes to the film were needed.

---

## Part B: my entries (Siddi, in my own words)

**2026-10-14 · the TA, my checks, and my decisions**

- **The TA:** On 2026-10-14 a TA confirmed that I did not need to use my own voice and that a Brutalist voice was enough.
- **My checks:** I listened to the opener and confirmed my name sounds right. I watched the whole film and thought it was good. Beyond that, I only asked for technical details to be checked, such as frame rate, audio modulation and resolution.
- **My decisions:** I chose the sponsor-match project, chose to say in the film that I'm on F-1, and chose the af_heart voice with the disclosure in the README only. I made these choices because I wanted the film to present my profile as it actually is.
- **What I understand now:** The December final must be agentic. I also learned that the topic can be changed over the course of the term if something comes up, as long as the change is logged here.
- **Still unclear / next step:** Nothing is unclear right now. Over the coming weeks I'll take time to decide whether to stay on this topic or change direction for Update 1.

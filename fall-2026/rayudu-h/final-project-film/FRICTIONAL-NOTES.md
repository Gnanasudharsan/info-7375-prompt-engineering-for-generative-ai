# FRICTIONAL-NOTES.md

Raw log for the pitch film build. Facts only, in order. Times are local (EDT) on 2026-10-14, taken from `date` in the same shell call unless marked "not captured" (then the bracketing captured times are given) Toolkit root: `../brutalist.art/`.

## Setup and source checks (Step 0 to Step 1)

| Time | Command / action | Result | Fix / follow-up |
|---|---|---|---|
| before 15:15:25 (not captured) | `ls -la ../art ../HOW-TO.md` | `No such file or directory` for both. The toolkit is at `../brutalist.art/`, not `../`. | Stopped and asked. User confirmed `../brutalist.art` as the toolkit root. |
| before 15:15:25 (not captured) | `cmp` on the two tariff PDFs | `meco_basic_service.pdf` (M.D.P.U. No. 1-26-H, effective Aug 1, 2026) and `5.1.26_…basic_service-(2).pdf` (No. 1-26-F, created Apr 28, 2026) are different files. Both also have identical copies in the parent folder. | User chose `meco_basic_service.pdf` as the tariff source. |
| 15:15:25 | `pdftotext -layout Final_Project_Pitch_Film_Assignment.pdf` | 4 pages, read in full. | none |
| 15:15:25–15:23:45 (not captured) | `pdftotext -layout "03.30.2026_CES Report.pdf"` | 46-page PDF. Page 1 (cover) is an image with no text layer. Pages 26–46 have under 100 characters of text each (image pages). The $738.7 million figure is on p. 2 (Executive Summary, Table ES-1, "Ten-Year Total Net Loss", July 2015–June 2025). The 10–30% figure is on p. 4: "account for 51.45 percent of customer losses". | none |
| 15:15:25–15:23:45 (not captured) | Compared brief to AG p. 2 | Brief said "paid **over** $738.7 million more". The report says "paid $738.7 million more". The AG press-release URL in the brief says "lost over 738 million". | Stopped and asked. User approved removing "over". |
| 15:15:25–15:23:45 (not captured) | `pdftotext -layout meco_basic_service.pdf` | "Effective: August 1, 2026", "Issued: July 16, 2026". Residential (R-1, R-2) Total Billed Basic Service Rate: Fixed $0.17185; Aug $0.16074; Sep $0.15616; Oct $0.15615; Nov $0.16204; Dec $0.18477; Jan $0.20086. Only the industrial rows are split by load zone (SEMA/NEMA/WCMA). | none |
| 15:15:25–15:23:45 (not captured) | Compared download dates to file dates | The brief had `[downloaded on: add date]` on the tariff line and no date on the AG line. Every PDF's filesystem modification time is 2026-10-14 15:02–15:04, so the real download date can't be recovered from the files. | User chose today's date. Both PDF source lines now end `[downloaded on: 2026-10-14]`. |
| 15:23:45 | Edit `PROJECT-BRIEF.md` line 16 | "paid over $738.7 million more" became "paid $738.7 million more". | none |

## Toolkit check (Step 2)

| Time | Command / action | Result | Fix / follow-up |
|---|---|---|---|
| 15:23:50–15:24:38 | `(cd ../brutalist.art && ./setup)` | Exit 0, but the table printed "Something is blocked". Blocked: audio (Kokoro: "pip install kokoro-onnx", test phrase failed), captions (faster-whisper), Manim beats, Manim equation beats. Ready: Remotion, slates/previz/compile, fonts. | See 15:29:57. |
| 15:24:46 | `(cd ../brutalist.art && ./art ai-explainer --help)` | Exit 0. Prints `skills/make/ai-explainer/SKILL.md` (48,450 bytes). | none |
| 15:24:38–15:24:46 | Read `HOW-TO.md`, `CLAUDE.md`, `CLAUDE-CODE-VISUAL-QC-CHECK.md` | HOW-TO.md §2 says `cd books/brutalist` before `./setup --install`; that path doesn't exist in this checkout. HOW-TO.md says "Three skills", CLAUDE.md says "15 skills", `./art --list` prints 16 skill rows, and `find skills -name SKILL.md` finds 18. | none (recorded only) |
| 15:25:07 | `find skills -name SKILL.md` and a search for "show-tell" | No show-tell skill in this checkout. The assignment PDF says to use show-tell "if your checkout includes" it. | Used ai-explainer as instructed. |
| 15:25:07 | `ls examples/ai-explainer/claude-debunked/` | Files: beat_sheet.json, BUILD-PROMPT.md, FACTCHECK-THE-FACTCHECK.md, PEDAGOGY.md, qc-sheet.png. HOW-TO.md §5 also lists `NARRATION-GATE-P.md` for this example; it isn't in the folder. | none |
| 15:25:07–15:25:19 (not captured) | Read the example's beat_sheet.json, BUILD-PROMPT.md, PEDAGOGY.md, FACTCHECK, qc-sheet.png | The example's BUILD-PROMPT.md calls `runtime/scripts/generate_audio.py` with an ElevenLabs voice. That script isn't in this checkout (checked 15:32:24: `No such file or directory`). qc-sheet.png shows slate cards (beat text plus beat-ID chip), not rendered scenes. | none |
| 15:25:19 | `grep -rn … --include=*.py` (my command) | zsh error: `no matches found: --include=*.py` (unquoted glob). | Re-ran with quoted `--include='*.py'` at 15:25:24. |
| 15:25:24–15:27:44 | grep of runtime/scripts, runtime/qc and runtime/remotion/src for persona, handle, logo and credit injection | Injection points found (listed in the next section). | Disabled per reel (next section). |
| 15:25:53–15:26:58 (not captured) | `echo ======` (my command) | zsh error: `==== not found` (zsh `=` expansion). | Used `echo '-----'` instead. |
| 15:27:17 | `./art scenes "<need>"` for 8 beat needs | Most hits are reel-specific compositions whose only prop is `sparkLine` (content is hardcoded). Usable parameterized components with no handle or logo: `FormACard` (lines, meta, dark) and `MedhavyTwoColumnCard` (sparkLine, left/right header and items). | none |
| 15:27:36 | `./art scenes --check <Name>` ×16 | `Threshold`: NOT RENDERABLE (no `<Composition>` in Root.tsx). `Illu-LayerStack`, `Illu-SourceFlow`, `Illu-ChipGrid`, `Illu-PredictCard` are renderable, but `illustrations/previews.tsx` bakes in their sample props, so beat-sheet props don't reach them. | Beats that need new visuals are marked `component_status: "to-build"` in beat_sheet.json. |
| 15:25:39–15:25:53 (not captured) | Read `runtime/scripts/remotion_scenes.py` | Renders from the fixed entry `runtime/remotion/src/index.ts`. There is no reel-local Remotion entry, so any new composition has to be registered in the shared `runtime/remotion/src/Root.tsx`. `run.sh` does accept a reel-local Manim `scenes.py`. | Open decision for the build step; not acted on. |
| 15:25:39–15:25:53 (not captured) | Read `runtime/scripts/run.sh` and `build_safety.py` | GATE F: `run.sh` refuses to render without FACTCHECK.md, SHOTLIST.md and PROMPTS.md in the reel folder. `compile.py` (final) writes to `<toolkit>/renders/` unless `--out DIR` or `$ART_OUT` is set. | Recorded for the build step. |
| 15:29:57 | `python3 runtime/scripts/build_safety.py examples/ai-explainer/claude-debunked` | `[safety] REFUSED: metadata.voice and voice_kokoro disagree; choose one persistent voice` (exit 1). The shipped example fails the toolkit's own validator. | Our beat sheet sets only `voice_kokoro`. |
| 15:29:57 | `which python3`; `import kokoro_onnx` | The PATH `python3` is `~/.rye/shims/python3`, which lacks `kokoro_onnx`. `../brutalist.art/.venv/bin/python` imports it fine. `./setup` calls bare `python3`. | Activate the toolkit venv first. |
| 15:30:07–15:30:59 | `(cd ../brutalist.art && source .venv/bin/activate && ./setup)` | All 7 features ready, exit 0. Python 3.12.9 from `.venv`. Nothing installed. | Fix: always `source .venv/bin/activate` before toolkit commands. |
| 15:30:59 | `git status --short` in `../brutalist.art` | Same as before this session: ` M .gitignore`, ` M runtime/remotion/package-lock.json`, `?? INSTRUCTIONS.md`, `?? ROADMAP.md`. No toolkit file changed this session. | none |

## Where the toolkit injects persona, handle, logo and credit

| Injection point | What it adds | How this reel disables it (per reel) |
|---|---|---|
| `skills/make/ai-explainer/SKILL.md`: DEFAULT CHANNEL claude-liam, IN-FOR-BEAR LAW, greeting `[hello], Liam` | "this is Liam, in for Bear" in B00 and the outro | Beat sheet authored directly. No persona and no greeting in any beat. |
| `runtime/scripts/brand_variant.py` | Scaffolds claude/claude-liam/nbb variants with the IN-FOR-BEAR note and NikBearBrown outro | Not run. |
| `runtime/scripts/build_cli_d3_reels.py` lines 142, 182 | Hardcoded "This is Liam, in for Bear." | Not used (cli builder). |
| `scenes/ClaudeComposerAsk.tsx` line 38: `folderLabel` default `@NikBearBrown` | Footer channel chip | No ClaudeComposerAsk beat in this reel. |
| `scenes/ClaudeTitleOutro.tsx` and `ClaudeTitleOutro916.tsx` (OUTRO-LOCK.md) | Hardcoded `@NikBearBrown` handle plus mascot | No outro beat in this reel. |
| `NikBearBrownOutro`, `CodexTitleOutro`, `CurriculumStages`, `SycophancyGradient`, `CoworkHourClock` | `handle` default `@NikBearBrown` | Not used. |
| About 30 scene components (e.g. `CadencesFig*`, `K12Fig*`, `CodingAgentsFig*`, `Values*`, `SleeperAgents*`) | Hardcoded `@NikBearBrown` watermark (LOGO LAW) | Not used. The only library scenes used are `FormACard` and `MedhavyTwoColumnCard`; grep shows neither has a handle or logo. |
| `runtime/scripts/compile.py`: `metadata.channel_title` | Centered handle over the first beat | Not set. |
| `runtime/scripts/compile.py`: `metadata.keep_review_labels` | Beat-ID chips in the final | Not set. |
| `runtime/scripts/compile.py` `lint_skin` | Warns if palette=`claude` and B00 isn't ClaudeComposerAsk or the last beat isn't ClaudeTitleOutro | `metadata.palette` isn't set to `claude`; the reel doesn't claim the Claude-brand bookend contract. |
| `runtime/qc/beat_lint.py` RULE 7 and `runtime/qc/brand_labels.json` | Enforces the channel kicker and folder chip | `metadata.brand` is a value not in the table, so the rule skips. |
| `runtime/scripts/shorts.py` `--handle` default `@nikbearbrown` | End-card handle on Shorts | No Short planned. |

## Step 3 (draft)

| Time | Command / action | Result | Fix / follow-up |
|---|---|---|---|
| 15:32:24 | `mkdir -p youtube/electricity-supplier-check-pitch` | Created the reel folder in this project, not in the toolkit. | none |
| 15:35:30 (first run not captured; between 15:32:24 and 15:35:30) | Generated `beat_sheet.json` with a script kept outside the project (scratchpad `make_beat_sheet.py`) | First draft: 680 words, estimate 3:52 (≈3.0 words/s, the example reel's measured Kokoro pace). Trimmed wording without changing any claim: 659 words, estimate 3:44. | Estimate only; the real length comes from audio. |
| 15:35:30 | `python3 runtime/scripts/build_safety.py <reel>` (venv active) | Exit 0. | none |
| 15:35:30 | `python3 runtime/qc/beat_lint.py <reel>` | `[beat-lint] clean — beat mix OK`, exit 0. | none |
| 15:35:30 | `git status --short` in `../brutalist.art` | Unchanged from the start of the session. | none |
| 15:35:48 | `python3 runtime/scripts/generate_audio_kokoro.py <reel> --dry-run` | 12 beats would generate, all `voice=am_onyx`, "cost: $0.00", exit 0. Dry run returns before any synthesis or write; the reel folder still holds only beat_sheet.json. | No audio generated (per instructions). |
| after 15:35:48 | Wrote `PEDAGOGY.md` (draft) in the reel folder | Draft; VERDICT: DRAFT. | Awaiting narrator rewrite. |

## Re-check against the assignment (after narrator review)

| Time | Command / action | Result | Fix / follow-up |
|---|---|---|---|
| before 15:52:53 (not captured) | Narrator asked whether the assignment PDF had been read | It had been read in full as text at 15:15:25. On re-check, draft v1 broke it: v1 put lists on screen and trimmed the voice, but the assignment's pitch format is "one simple drawn picture per beat, minimal on-screen text, narration carrying the explanation". v1 also left out of the narration Q2's "saves a [person] [thing]" sentence, Q4's course skills, the full target role and the stack, and B02 didn't say when the source was obtained. | Redrafted as v2 (below). |
| 15:52:53 | `cat ../brutalist.art/README.md` | The assignment says "Work from the toolkit's own README". It hadn't been read before this point. It mentions no "render-integrity check" and no show-tell skill. | none |
| 15:53:02 | `git ls-remote origin HEAD` | Upstream HEAD is `519fcbb`; local HEAD is `ba2d0e0` (2026-09-07). | none |
| 15:53:02 | `gh api repos/…/commits?per_page=3` (my command) | zsh error: `no matches found` (unquoted `?`). | Quoted the URL at 15:53:16. |
| 15:53:02 | `gh api …/contents/skills/make` (read-only) | Upstream has `skills/make/show-tell/`. The local checkout doesn't. | Asked the narrator whether to update. |
| 15:53:16 | `gh api …/show-tell/SKILL.md` saved to scratchpad and read | show-tell: one isometric Manim drawing per beat; labels 1–3 words, at most 2–3 per beat; the voice explains; reel-local `scenes.py`; its default bookends use the Liam persona and a spoken @NikBearBrown outro. Upstream's latest commit is 2026-10-12, "Pin Manim to the 0.20 series". | Format adopted in v2; persona and outro bookends overridden by rule 1. |
| 15:55:14 | `grep sparse runtime/qc/final_frame_check.py` (local) | The local Gate V has no `sparse_by_design` waiver (fill minimum 0.55 of SAFE, MAJOR). Upstream's copy mentions it 5 times. Local `.venv` has manim 0.18.1; upstream `requirements.txt` pins `manim>=0.20,<0.21`. | Recorded for the toolkit-version decision. |
| 15:55:14 | `git fetch --dry-run` in `../brutalist.art` (my command) | It reported `ba2d0e0..519fcbb main -> origin/main` and downloaded upstream objects into `.git/objects`. Checked at 15:56:21: HEAD, `origin/main` (both still `ba2d0e0`) and the working tree are unchanged. | Disclosed. No refs moved, no files changed. |
| 15:56:15 | `git rev-parse --short HEAD origin/main` (my command) | `fatal: Needed a single revision` (`--short` takes one revision). | Re-ran as separate calls at 15:56:21. |
| 15:59:13 | Regenerated `beat_sheet.json` (v2) from scratchpad `make_beat_sheet_v2.py`; v1 kept in scratchpad as `beat_sheet.v1.json` | 13 beats, 669 words, estimate 3:48. `build_safety.py` exit 0; `beat_lint.py` clean; `fill_plan` routes B00 to remotion and B01–B12 to manim (pipeline); `--dry-run` reports 13 beats, all am_onyx, $0.00. Toolkit `git status` unchanged. | No audio generated. |
| after 15:59:13 | Rewrote `PEDAGOGY.md` as DRAFT v2 | | Awaiting narrator rewrite. |

## Build (narrator approved narration, toolkit update, tariff on bill, formula option a)

| Time | Command / action | Result | Fix / follow-up |
|---|---|---|---|
| 16:06:50 | `git fetch origin` in `../brutalist.art` | origin/main `ba2d0e0..519fcbb`. Upstream changes `.gitignore` (+44 lines), which also has a local edit (`.venv/`). It doesn't touch the local `package-lock.json` edit or the untracked `INSTRUCTIONS.md` and `ROADMAP.md`. | Backed up the local edits to the scratchpad (`toolkit-local-backup/`). |
| 16:07:05 | `git stash push -- .gitignore runtime/remotion/package-lock.json`; `git merge --ff-only origin/main`; `git stash pop` | Fast-forward to `519fcbb`; the stash popped with no conflict; the `.venv/` line is kept. | none |
| 16:07:24–16:09:54 | `./setup --install` (venv active) | pip installed Pillow 12.3.0, manim 0.20.1, manimpango 0.6.1, beautifulsoup4, soupsieve; npm "up to date". **Exit 1** from setup's ElevenLabs guard, which hit upstream's own example files under `youtube/brutalist/…` (e.g. `claude-liam-brutalist-command-setup/beat_sheet.json`). The readiness table never printed. | Didn't edit shared toolkit files. Ran the readiness checks by hand (next row). |
| 16:10:18 | Manual readiness: imports, `ffmpeg -version`, `node -v`, model files, `setup_smoke_kokoro.py` | PIL 12.3.0, manim 0.20.1, faster_whisper 1.2.1, kokoro_onnx, numpy 2.5.3 all OK; ffmpeg 9.0.1; node v23.11.0; Kokoro smoke OK (-21.8 dB). `dvisvgm` not found (only needed for Manim equation beats; none here). | none |
| 16:11–16:14 (not captured) | Read show-tell `SKILL.md`, `iso_kit.py`, `example-make_sheet.py`; `bookend_check.py`, `factcheck_check.py`, `type_check.py`, `final_frame_check.py`, gate headers | `bookend_check.py`: the OUTRO (ClaudeTitleOutro with @NikBearBrown) can never be exempted. It isn't wired into `art run` or `art final`. GATE T §8.5 allows ≤1 display line + 1 label on a Remotion card. | B00 cut to title + name. Bookend OUTRO failure accepted as narrator rule 1. |
| 16:14:02 | `factcheck_check.py <reel>` | Clean: 14 rows, 13 beats covered, 0 uncovered. | none |
| 16:14:02 | `pronunciation.py --say …` | "Hemanth Rayudu" → `hˈɛmænθ ɹˈeɪuːdˌuː`; "pytest" → `pˈaɪɾɪst` (wrong). "py-test" → `pˈaɪtˈɛst`. | Wrote "py-test" in narration_text for B07 and B09 (voice only). |
| 16:14:39–16:15:32 | `generate_audio_kokoro.py <reel>` | 13 beats, 211.37 s total, $0.00. | none |
| 16:15:57 | `align.py <reel>`; faster-whisper transcript of each mp3 (scratchpad `transcribe.py`) | words.json aligned 13/13. Transcript matches except B00 "Hemant Ray Udu" and B06 "isn't instant" heard as "is an instant". | B06 reworded "it is not instant". B00 left for the narrator to listen to. |
| 16:16:48 | `generate_audio_kokoro.py <reel> --only B06`; `align.py --only B06`; re-transcribe | B06 20.07 s; transcript "and it is not instant". Total 211.54 s. | none |
| 16:24:54–16:25:13 | `manim -ql` all 12 scenes into the scratchpad | All exit 0; every clip ≤ its audio. Frame review found: label/tag crowding (B01); coin on caption (B01); a dashed line implying a connection (B01); bill parked over the house (B04); number blocks overlapping bars (B05); no text at the midpoint (B08); crowded trays (B09, B11). Measured text widths: two captions were wider than the safe area (12.95 and 14.15 units vs 12.4). | Fixed in `scene_body.py`; re-rendered and re-checked. |
| 16:28:06 | Gate A/W loop (my command) | zsh didn't split `$CL`, so all class names went in as one `--class`. | Re-ran under `bash -c`: Gate A 0 and Gate W 0 on all 12. |
| 16:28:27–16:28:41 | `manim_layout_audit.py scenes.py --class <C> --curve-strict` ×12 | B03 exit 2: "label on a curve/line: `$`" (the slip faded in over the bill's scribbles). Others 0. | The slip now rises straight to its rest point; B03 re-audit 0. |
| 16:29:19–16:59:47 | `./art run <reel> --height 2160` (run 1) | 13/13 slots filled; review cut 211.8 s; Gate B passed per scene. **GATE V FAILED**: B00 `underfill` MAJOR ×2 (8% of SAFE vs 55%). | Declared `qc.sparse_by_design` with a written reason on B00 (title card). |
| 17:00:29 | `final_frame_check.py <reel> --mp4 <slate>` | Gate V clean: 26 frames, 0 BLOCKER, 0 MAJOR. | none |
| after 17:00:29 | 2 fps frame sample of the review cut (424 frames, 11 contact sheets in `_qc/`), every sheet read | Found: about 8 s with no motion in B05 and about 7 s in B03 (fails show-tell's still-frame test); about 1.5–2 s of empty stage at the start of B06, B11 and B12; B12's dashed outlines were plain rectangles. | Fixed in `scene_body.py`; old B03/B05/B06/B11/B12 clips and the Manim cache moved to `_superseded/run1/`; started `./art run` (run 2). |
| 17:03:54–17:06:57 | `./art run <reel> --height 2160` (run 2) | Rendered only the 5 superseded scenes. Gates L, A, W and B pass; B00 skipped (already filled). Review cut 211.8 s. Gate V clean (0 BLOCKER, 0 MAJOR). Exit 0. | Re-read the 5 changed beats at 2 fps (`_qc/recheck_*.png`): OK. |
| 17:07:40–17:10:28 | `./art final <reel> --height 2160 --out <reel>/exports/landscape` | GATE T PASS, 13/13 beats, 0 FAILs (§8.10 SKIP on every beat). Master written: `exports/landscape/electricity-supplier-check-pitch.mp4`, 211.8 s, 14.6 MB, plus `.verified.json`. Exit 0. | none |
| 17:10:44 | `master_check.py`, `loudness_check.py`, `bookend_check.py` | MASTER PASS (3840×2160, 24 fps, yuv420p, h264, 211.8 s). LOUDNESS PASS (−24.70 LUFS, −2.76 dBTP). BOOKEND exit 2: "OUTRO (BOUT): no ClaudeTitleOutro beat". sha256 `0ea17b67155f38d93c36d6f0cf1d1c112c71ff7b8ffc9eceaca9d3651cb27af9`. | BOOKEND failure is by design (rule 1: no channel handle or credit line). Recorded in CHECKS-REPORT.md. |
| after 17:10:44 | 2 fps sheets of the final master (`_qc/master-2fps/`, 11 sheets) | 2 sheets spot-checked against the review cut: same frames. | none |
| after 17:10:44 | Staged `submission/final-project-film/` (19 MB) | Contents: README, PROJECT-BRIEF, beat_sheet, BUILD-PROMPT, SOURCES, FACTCHECK, SHOTLIST, PROMPTS, PEDAGOGY, CHECKS-REPORT, TYPECHECK, MASTERCHECK, LOUDNESS, `_qc/`, scene source, `mp3/`, master mp4 and verified.json. Left out: caches (`media/`, `clips/`, `manim/`, `__pycache__/`, `_superseded/`). FRICTIONAL.md not included (the narrator writes it). | No zip made and nothing pushed. |

## Brief layout fix (narrator approved: "Yes fix the brief's layout")

| Time | Command / action | Result | Fix / follow-up |
|---|---|---|---|
| before 19:29:13 (not captured) | Backed up the brief (scratchpad `PROJECT-BRIEF.before-layout.md`, 989 words); moved the Sources section out; switched to bold run-in section labels; condensed the wording over several passes | Measured each pass with `pandoc` (LaTeX, 11 pt, 1 in margins) and with Chrome headless print (Helvetica/Arial class, 11 pt, 1 in margins). 899 → 849 → 832 → 778 → 747 → 725 → 673 → 668 → 655 → 628 → 608 → 620 words. Still 2 pages in both layouts: 4 lines over in the Arial-class layout. Calibri (Word default) isn't installed, so it couldn't be measured. Some squeezed phrasings changed meaning slightly ("traceable to a tariff", "dated rates") and were restored. | Left at 620 words with every claim kept; final check found 0 missing claims. |
| 19:29:13 | Added the AG announcement URL to SOURCES.md; changed FACTCHECK.md row 7 to "(brief §2)"; copied the brief, SOURCES.md and FACTCHECK.md to `submission/final-project-film/`; ran `factcheck_check.py` | Fact check clean (14 rows, 0 uncovered). Submission brief identical to the project brief. | none |

## Revisions after the first master (narrator: title card, name, tariff on the bill, B08)

| Time | Command / action | Result | Fix / follow-up |
|---|---|---|---|
| before 19:39 (not captured) | `pronunciation.py --say` on four respellings; four sample MP3s generated | Narrator declined the pick-one question and typed "Hey- Month Ra- You- do". "Hey-month Rah-you-doo" → `hˈeɪmˈʌnθ ɹˈɑːjuːdˈuː`. | Used that spelling in B00 narration_text (voice only). |
| 19:41:52 | `generate_audio_kokoro.py <reel> --only B00`; `align.py --only B00`; whisper transcript | B00 6.29 s; heard as "I'm hey month raw you do and this is my pitch…". | none |
| before 19:44:29 (not captured) | Rewrote B00 (Manim `B00_Title`, title 80 pt), B01 (printed bill rows with the tariff rates), B08 (five skill objects); moved old `media/B00.mp4` (FormACard), `manim/B01.mp4`, `manim/B08.mp4` to `_superseded/run2/`; low-q render and stills | Fixed from the stills: B00 content sat high; B08's final check overlapped the rail. Gates A, W, B = 0 on all three. | none |
| 19:44:29–19:48:48 | `./art run <reel> --height 2160` (run 3) | 13/13 Manim; Gate V 0 BLOCKER / 0 MAJOR; review cut 211.9 s; exit 0. 2 fps re-check sheets for B00, B01, B08 read. | none |
| 19:49:26–19:53:06 | `./art final …` (first master moved to `_superseded/master-1/`) | GATE T PASS 13/13 (B01 min text-run 49 px ≥ 41 px). Master 211.9 s, sha256 `c66583e099dd35ec7c34ab223d722378260f9e1334ab031df41e2bd92248211f`. | none |
| 19:53:20 | `master_check.py`, `loudness_check.py`, `bookend_check.py`, `factcheck_check.py` | MASTER PASS; LOUDNESS PASS (−24.70 LUFS, −2.66 dBTP); BOOKEND OUTRO fail (by design); factcheck clean. | Docs, skeleton and submission folder updated; submission re-staged (55 files, 19 MB). |
| after 19:53:20 | Checked for the brief backup `PROJECT-BRIEF.before-layout.md` | Still present in the old scratchpad. | Copied to `_archive/PROJECT-BRIEF.before-layout.md` (989 words, the full pre-layout brief). |
| (not captured) | Narrator asked Claude to draft FRICTIONAL.md from the session record for his review; drafted with 17 "Confirm:" lines and a blank approval line | Draft in project root, not in the submission folder. | Awaiting narrator approval. |
| (not captured) | Added an "Inputs I provided" table to FRICTIONAL.md (assignment PDF excluded, at the narrator's request); added the narrator's 12 prompts verbatim to BUILD-PROMPT.md section 4; synced BUILD-PROMPT.md to `submission/final-project-film/` | Copies identical (`diff -q`). | none |
| (not captured) | Narrator pointed out that the brief's Will exist list named only the parts, not the tool. Added "Electricity Supplier Check itself: a Python repository with the agent that reads a bill and shows what you paid versus basic service, with the formula and next steps" as the first item (wording from brief §1 and §3, no new claim); copied to the submission folder | Brief 649 words. | Film B12 unchanged: its line "Everything I've described… will exist" already covers the tool. |

## Second round of revisions (narrator: visuals, disclaimers, eval-report reader, Claude Code role)

| Time | Command / action | Result | Fix / follow-up |
|---|---|---|---|
| before 22:14:35 (not captured) | Brief: Stack header now says what Claude Code does; §3 portfolio reader opens the GitHub repository, whose evaluation report matches numbers to the calculator and can be rerun; §5 adds "For now it is a portfolio demo: whoever runs it needs Claude Code access." Previous version in `_archive/PROJECT-BRIEF.before-claude-code-edit.md` | Brief 697 words. | none |
| 22:14:35 | Edited B01, B04, B05, B07 narration_text; `generate_audio_kokoro.py --only B01 B04 B05 B07`; `align.py --only …`; whisper check | B01 7.96 s, B04 15.02 s, B05 21.10 s, B07 21.63 s; total 217.36 s. Whisper base hears "Claude" as "Cloud" in B07 (phonemes `klˈɔːd`). | none |
| before 22:19:20 (not captured) | Redrew B02, B03, B05, B06, B09, B11, B12 (transformer, coin stack, offers board, GitHub folder, contract, plain panels); house recolored; low-q review | B03 labels "test bills"/"eval report" touched; spaced out. Gates A, W, B: first loop exited 2 because `$Q` (path with a space) was unquoted (my command); re-run quoted, all 0. | none |
| 22:19:20–22:25:31 | `./art run` (run 4) | **Gate V FAILED**: B03_85 low-contrast 0.27, B05_50 low-contrast 0.22 (min 0.30), from the folder body's BAR3 fill. | Folder body set to CARD with a BAR1 tab. |
| 22:26:47–22:29:54 | `./art run` (run 5), B03 and B05 only | Gate V clean. | 2 fps sheets of the whole cut (`recheck_cast_A`–`E`) read; found holds in B03 (~6 s) and B05 (cursor arrived early). |
| before 22:34:40 (not captured) | B03: formula blocks at "math shown"; B05: cursor drift 5.0 s → 7.0 s; Gates A/W/B 0; `./art run` (run 6) | Gate V clean. | Checked B05 clip frames at 2/4/6/8 s: cursor reaches the folder at about 6–8 s. |
| 22:37–22:40 | `./art final` (master-2 moved to `_superseded/master-2/`); master, loudness, bookend checks | GATE T PASS 13/13; MASTER PASS 217.7 s; LOUDNESS −24.68 LUFS / −2.82 dBTP; BOOKEND OUTRO fail (by design). sha256 `c1dffb5c60fc91ffcdf0ee584b1c2b2d1d936ef6cc4681799e885beb4c3de72c`. | Docs updated; submission re-staged. |

## Submission

| Time | Command / action | Result | Fix / follow-up |
|---|---|---|---|
| (not captured) | Narrator filled FRICTIONAL.md's approval line ("Oct 14 2026") and said "go" to push and zip | — | — |
| (not captured) | `git pull --ff-only origin main` in `../chapter1-course`; copied the folder to `fall-2026/rayudu-h/final-project-film/`; `git check-ignore` | The repo's `.gitignore` ignores `*.[mM][pP]3` and `*.[mM][pP]4` at any depth ("Keep generated audio/video out of Git", since 2026-09-09). My earlier search for "mp4" had missed the bracket pattern, so I had wrongly told the narrator only `youtube/` media was blocked. | Narrator chose to follow the rule: the GitHub copy has no `.mp4`/`.mp3`; the Canvas zip has everything; README and BUILD-PROMPT say so. |

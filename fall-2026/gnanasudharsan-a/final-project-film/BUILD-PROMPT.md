# BUILD-PROMPT — how to rebuild `decisiontrace-pitch.mp4`

The film was built on 2026-10-10. The master is 191.5 s long and its SHA-256 is
`07526250c8e4e0dcc5a7ad520bc8d4d69e3d18f01d262fbdfaf384aaa58e08b7` (see
`gate-reports/decisiontrace-pitch.verified.json`).

---

## 1. Environment

I read these versions from the machine that built the film.

| Component | Version |
|---|---|
| OS | macOS 27.0.1 (build 26A434), arm64 |
| Python | 3.12.14 (Homebrew `python@3.12`), in the toolkit's `.venv` |
| ffmpeg / ffprobe | 9.0.1 (Homebrew) |
| kokoro-onnx | 0.6.1, with onnxruntime 1.30.0, phonemizer 3.4.0, espeakng-loader 0.2.4 |
| Kokoro model files | `kokoro-v1.0.onnx` (325,532,387 bytes) and `voices-v1.0.bin` (28,214,398 bytes), in `runtime/models/kokoro/` |
| Voice | `af_heart`, for every beat |
| Manim | Community 0.18.1, with ManimPango 0.5.0 |
| Node / Remotion | v26.8.2 / 4.0.486. The toolkit installs these, but the final film uses no Remotion scene. |
| Fonts on screen | EB Garamond (`runtime/fonts/EB_Garamond/static/`, also installed in `~/Library/Fonts`), and PT Mono in B06 (macOS system font) |

---

## 2. Toolkit

```bash
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art
git checkout ba2d0e0f043f5b3b35a50d336e0fc66fbfecfc0c
./setup --install    # Python deps, Remotion node modules, Kokoro model download
source .venv/bin/activate
./setup              # readiness table; run it with the venv active, or it falsely reports blocked
```

- **Commit used:** `ba2d0e0f043f5b3b35a50d336e0fc66fbfecfc0c`, dated 2026-09-07, "Preserve report
  audio and enforce safe fellows exports".
- **Unmodified:** every toolkit file this build ran (`runtime/scripts/`, `runtime/qc/`, `art`,
  `setup`) matches that commit.
- **Local edits:** my checkout has edits under `runtime/remotion/`. They predate this film and are
  unused, because no beat is a Remotion scene.
- **Known issue:** `./art smoke` fails on the toolkit's own fixture. Its slug `_smoke` breaks the
  toolkit's slug rule in `build_safety.py`. The pipeline itself works; see FRICTIONAL.md, 2026-10-09.

---

## 3. Working-folder layout

Build the film in a folder **outside** the toolkit. I used
`~/info7375-films/decisiontrace-pitch/`. Copy files into it like this. Paths on the left are
relative to this submission folder.

| Copy from | To (inside the working folder) |
|---|---|
| `beat_sheet.json` | `beat_sheet.json` |
| `build/scenes.py` | `scenes.py` |
| `build/tools/compose_frames.py`, `build/tools/phoneme_name.py` | `tools/` |
| `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` | same names. GATE F refuses to render without them. |
| `evidence/alternatives-test/screenshots/2026-10-10_notebooklm_summary.png` | folder root, same name |
| `evidence/alternatives-test/screenshots/2026-10-10_notebooklm_run2_q1.png` | folder root, same name |
| `evidence/alternatives-test/screenshots/2026-10-10_chatgpt_q1.png` | folder root, same name |

`beat_sheet.json` has 30 path strings:

- **2 resolve already.** `tools/phoneme_name.py` and `tools/compose_frames.py` are the copies above.
- **28 are created by the build steps in §4:**
  - 13 × `mp3/beat-B00.mp3` … `mp3/beat-B12.mp3`, the narration audio
  - 11 × `manim/B00.mp4` … `manim/B12.mp4` (every beat except B03 and B04), rendered by `./art run`
    from `scenes.py`
  - `media/B03.mp4` (listed twice) and `media/B04.png`, written by `compose_frames.py`.
    `build/frames/` holds the frames used in this build. Run from this folder's files, the script regenerates
    `B03a.png`, `B03b.png`, `B04.png` and `media/B03.mp4` byte-for-byte identical (checked 2026-10-10).

---

## 4. Commands, in order

These run from the toolkit folder with the venv active. `R` is the working folder.

```bash
cd ~/Downloads/7375/brutalist.art && source .venv/bin/activate
R=~/info7375-films/decisiontrace-pitch
```

**Narration audio.** The audio's measured lengths set every beat's duration.

```bash
python3 runtime/scripts/generate_audio_kokoro.py $R --only B01 B02 B03 B04 B05 B06 B07 B08 B09 B10 B11
python3 $R/tools/phoneme_name.py beats $R --variant E --only B00 B12
```

- **B00 and B12** have `engine: "kokoro-phoneme"`, so `generate_audio_kokoro.py` always skips them.
- **History:** during the build, audio was generated in stages: all beats at first, then
  `--only B08` after its narration changed, then B00 and B12 with `phoneme_name.py`.
  The commands above reproduce the final state.
- **`phoneme_name.py`** finds the toolkit through `ART_HOME`, default `~/Downloads/7375/brutalist.art`.

**Screenshot frames for B03 and B04.** Run these after the audio, because the B03 clip length
comes from B03's measured audio.

```bash
python3 $R/tools/compose_frames.py $R runtime/fonts/EB_Garamond/static/EBGaramond-Medium.ttf
```

**Review build.** This renders every Manim scene and runs every gate in strict mode.

```bash
./art run $R
```

It renders each scene with `manim -qk --fps 24 -r 3840,2160 scenes.py <Scene>`, then compiles and
runs these gates:

- GATE L (beat-mix lint)
- GATE F (paperwork)
- GATE A (static scene check)
- GATE W (contrast and margins)
- GATE B (layout audit, after each render)
- GATE V (frame QC on the compiled review cut)
- `verify_output` (render integrity), which runs inside every compile

**Final master.**

```bash
./art final $R --out $R/final
```

`./art final` re-runs the preflight and refuses if any beat is still a placeholder card. It then
runs `verify_output` and GATE V on the candidate, and writes `final/decisiontrace-pitch.mp4` and
`final/decisiontrace-pitch.verified.json`.

**Gate and check commands I also ran on their own:**

```bash
./art scenes "<what the beat needs>" --top 6 --no-log      # library search; --no-log keeps the toolkit unmodified
./art scenes --check MedhavyConceptCard BrutalistTerminalOpen FormBCard Ch1AttnBoundary LookPlate
T=$(mktemp -d); cp $R/scenes.py $T/                         # GATE A checks an isolated copy, as run.sh does
PYTHONPATH=runtime/manim python3 runtime/qc/static_scene_check.py $T/scenes.py --class <Scene>
python3 runtime/qc/wcag_margin_check.py $R/scenes.py --class <Scene>
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height -show_entries format=duration $R/final/decisiontrace-pitch.mp4
ffmpeg -v error -xerror -i $R/final/decisiontrace-pitch.mp4 -f null -
ffmpeg -hide_banner -i $R/final/decisiontrace-pitch.mp4 -af volumedetect -f null -
```

**Notes:**

- I never used `ART_STRICT=0` or any other `ART_*` override.
- The cue times inside `scenes.py`, such as `clock.until(8.84)`, were measured from this build's
  mp3s with `ffmpeg -af silencedetect=noise=-35dB:d=0.18`. If regenerated audio comes out a
  different length, re-measure the cues. Each scene's total length always comes from
  `beat_sheet.json`.

---

## 5. Name pronunciation (B00 and B12)

Kokoro's normal text-to-speech mispronounced "Gnanasudharsan Ashokumar", and five respellings
didn't fix it (FRICTIONAL.md). B00 and B12 therefore use explicit phonemes for the name only.

- **IPA, variant E:** `ɲˈɑːnɑːsˌuːdʰɚʃɑːn ɑːʃˈoʊk kuːmˈɑːɹ`
- **How it's made:** voice `af_heart`, through `Kokoro.create(phonemes, voice="af_heart", lang="en-us",
  is_phonemes=True)` in kokoro-onnx 0.6.1.
- **Everything else is normal:** `phoneme_name.py` phonemises the rest of each sentence with
  Kokoro's own tokenizer and puts the IPA in place of the name.
- **Recorded in the sheet:** `beat_sheet.json` → B00/B12 → `phoneme_note` holds the variant, the IPA
  and the full phoneme string.
- **Approximation:** Kokoro's phoneme set has no dental mark (◌̪) or breathy mark (ʱ), so the soft,
  breathy "dh" is written `dʰ`.
- **On screen:** the spelling is unchanged: "Gnanasudharsan Ashokumar".

---

## 6. Prompts

**Where the narration comes from:** `beat_sheet.json`, each beat's `narration_text`. B00 and B12
use phonemes for the name only (§5).

**Prompts I wrote elsewhere.** I drafted my plans and the narration in a separate claude.ai chat
(see SOURCES.md). Those chat prompts aren't in this folder, and Claude Code never saw them, so they
are **not reproduced here**.

**Below are the prompts I gave Claude Code in this build, in order, quoted verbatim.** Two
exceptions are marked:

- **P1** is summarised where it pasted the course's assignment text, which is course material.
- **P19** is summarised because its templates are the files themselves.

Short replies I gave to Claude Code's questions are included where they changed the build.

**P1 (2026-10-09)** — *summarised.* I pasted the assignment description and asked Claude Code to
follow these steps first (quoted):

```
1. Add a FRICTIONAL.md entry dated 2026-10-09 recording the Brutalist setup:
   exact install commands run, tool versions (python, ffmpeg, TTS engine),
   whether the sample film rendered, and any errors plus how they were fixed.
   State only what actually happened.
2. Save your README findings to ../brutalist-notes.md (my reference, not a submission file):
   show-tell beat format, beat_sheet.json schema, gate commands, where gate reports are written,
   what the render-integrity check tests, and any default narrator name, persona or credit line I must replace.
3. Create fall-2026/gnanasudharsan-a/final-project-film/ containing empty README.md,
   PROJECT-BRIEF.md, beat_sheet.json, BUILD-PROMPT.md, SOURCES.md, and move FRICTIONAL.md into it.
4. Add a .gitignore that excludes caches, .env files, and temp audio and render folders.
5. Commit with the message "final-project-film: scaffold + Brutalist setup log".
```

**P2 (2026-10-09)**

```
Work in fall-2026/gnanasudharsan-a/final-project-film/ in my course fork.

A. FRICTIONAL.md: confirm these are logged as separate dated (2026-10-09) entries, adding any that are missing:
   - ./art smoke fails because the toolkit's fixture slug "_smoke" violates its own slug rule; worked around on a scratch copy renamed "smoke"; toolkit not modified.
   - No show-tell skill in this checkout; plan is to follow the format by hand (one picture per beat, minimal on-screen text, narration carries it).
   - Instructor defaults found (voice, "Liam, in for Bear", Hola Bear opener, hard-coded @NikBearBrown outro); will replace or avoid them.

B. Create ~/info7375-scratch/alt-test-pack/ (OUTSIDE any git repo) with 6 short fictional .txt docs
   for "Northwind Logistics", 150–250 words each:
   2026-03-02_meeting_notes.txt (decide PostgreSQL for the tracking service, with reasons),
   2026-03-10_ticket_TRK-112.txt (implements it),
   2026-05-18_meeting_notes.txt (REVERSES to DynamoDB over scaling cost; references the March decision),
   2026-05-20_email.txt (manager confirms the switch, named fictional approver),
   2026-06-01_ticket_TRK-140.txt (migration),
   2026-06-15_retro.txt (unrelated noise).
   Plus questions.txt with:
   1. Which database does the tracking service use, and why?
   2. Was there ever a different decision about this? What changed?
   3. Who approved the switch?
   4. What budget was approved for the migration? (NOT in any doc)
   Also create ~/info7375-scratch/alt-notes.md containing an empty notes template per tool:
   Tool / date tried / Q1–Q4 result (Y/N + notes) / did well / one specific thing it didn't do.
   Log a FRICTIONAL entry: synthetic alternative-test pack generated with Claude Code.

C. Commit only the film folder ("alternatives test pack + friction log") and push.
   Run git status first and confirm nothing outside the film folder is staged.

D. Find my "Reconstructing Enterprise Decision Memory" repo on this machine
   (search the home directory for folders with "decision" in the name that contain a .git folder).
   Show me the matches and wait for me to confirm the right one.
   Then do a READ-ONLY inventory: modify nothing, no installs into its environment without asking me.
   Report: modules and what each does; what actually runs today (run its tests or entry point, show results verbatim);
   any eval, test set, or metrics; first and last commit dates; public or private; any real or private data present.
   End with two lists: "Verified runs today" and "Exists but unverified/incomplete".
```

My answers to the follow-up questions: merge rather than force-push ("Don't force-push. Merge
origin/main into my local main (git pull --no-rebase), so 19678f7 stays in history. If there are
conflicts, show me the conflicting files … and stop."). Then "Remove the 11, then push", and "Skip
Part D for now".

**P3 (2026-10-10)**

```
In my course fork, inside fall-2026/gnanasudharsan-a/final-project-film/, create evidence/alternatives-test/ and:

1. COPY (don't move) these into evidence/alternatives-test/screenshots/ (find them wherever they are; check ~/Desktop, ~/Downloads, ~/info7375-scratch/screenshots/):
   2026-10-10_notebooklm_summary.png
   2026-10-10_notebooklm_run2_q1.png ... _q4.png
   2026-10-10_chatgpt_q1.png ... _q4.png
   Show me the source paths found before copying. If any file is missing, list it and stop.

2. COPY ~/info7375-scratch/alt-test-pack/ (6 docs + questions.txt) into evidence/alternatives-test/test-pack/.

3. COPY ~/info7375-scratch/alt-notes.md into evidence/alternatives-test/alt-notes.md, then fix these lines in the copy:
   - Replace "Run 2 Q1: [CHECK SCREENSHOT — same or different?]" with:
     "Run 2 (one question at a time) checked: all four matched run 1; run 2 Q1 said 'uses DynamoDB as its primary datastore', no mention the migration is unfinished."
   - Tool 1 screenshots line ->
     "Screenshots (captured 2026-10-10): 2026-10-10_notebooklm_summary.png, 2026-10-10_notebooklm_run2_q1–q4.png. Run 1: no screenshot; answer text copied 2026-10-09."
   - Tool 2 screenshots line ->
     "Screenshots (captured 2026-10-10): 2026-10-10_chatgpt_q1–q4.png"
   Show me the diff of every change.

4. Create evidence/alternatives-test/README.md (short) stating: what was tested; that the test pack is synthetic and was generated by Claude Code on 2026-10-09; that the answer key was written before grading; which tools were used and when; and that screenshots are unedited captures from 2026-10-10.

5. Add a FRICTIONAL.md entry dated 2026-10-10: ran alternatives test (NotebookLM, ChatGPT); NotebookLM summary overstated the migration as completed; ChatGPT got the status right but tied it to an unrelated doc's date; run 1 screenshot not captured.

6. Run git status, confirm only files inside final-project-film/ are staged, commit "evidence: alternatives test (NotebookLM, ChatGPT)", and push to myfork main.
```

**P4 (2026-10-10)**

```
In final-project-film/evidence/alternatives-test/:
1. README.md: replace the answer-key sentence with:
   "The answer key was drafted by Claude (claude.ai chat, 2026-10-09) from the six docs before any tool was asked Q1–Q4, and checked by me against the docs. The NotebookLM auto-summary appeared on upload, before the key existed."
2. alt-notes.md line 12: trim to one sentence: "Run 2 (one question at a time) checked: all four matched run 1; run 2 Q1 said 'uses DynamoDB as its primary datastore', no mention the migration is unfinished."
3. Delete the blank template ~/info7375-scratch/alt-notes.md (outside the repo) so there's only one notes file.
Show diffs, commit "evidence: fix attribution", push.
```

**P5 (2026-10-10)** — The instructions are quoted below. I also pasted the full text of the
first PROJECT-BRIEF.md draft, which is preserved in commit `4991dec`.

```
Replace the contents of final-project-film/PROJECT-BRIEF.md with the brief below. Then:
- Check every factual claim in section 2 and "Exists today" against evidence/alternatives-test/ (notes + screenshots) and FRICTIONAL.md. List any claim not supported; do not fix silently.
- Check tense: past tense only for things that exist in the repo; flag any violation.
- Report the word count; flag if over ~750 words (assignment says one page).
- Add a FRICTIONAL entry dated 2026-10-10: brief drafted with Claude (claude.ai), reviewed and edited by me (Brutalist line made precise; verification claim narrowed to what code can check).
Show findings, then commit "brief: seven answers" and push.
```

**P6 (2026-10-10)**

```
Edit final-project-film/PROJECT-BRIEF.md with exactly these replacements, show the diff, report the new word count:

§2 — replace "On 2026-10-09/10 I tested two real alternatives" with:
"On 2026-10-09 I tested two real alternatives (screenshots captured 2026-10-10)"

§2 NotebookLM bullet — replace with:
"- NotebookLM answered the facts correctly and refused to invent a budget, but its auto-summary described the migration with no sign it was still in progress ("…successfully deploy the new NoSQL infrastructure") when the ticket shows it In Progress, and its answer to "which database" said "uses DynamoDB" without saying the switch was unfinished."

§2 — replace "Neither tool checks its own claims against its sources or tells you how often it is right." with:
"In this test, neither tool flagged the overstated status or the wrong date, and neither showed any measure of how often it is right."

§4 Prompt contracts bullet — replace with:
"- Prompt contracts: the model will be required to return JSON matching a schema, with a citation for every claim; responses that break the schema will fail."

§5 — replace "because a test passes" with "because a test will pass".

§6 — replace "The synthetic documents are generated with Claude." with:
"The six existing synthetic documents were generated with Claude Code, and the larger set will be too."

If still over 750 words, tell me which sentences you'd cut — don't cut on your own.
Add a FRICTIONAL entry 2026-10-10: narrowed competitor claims and fixed tense after Claude Code's evidence check. Commit "brief: narrow claims, fix tense" and push.
```

**P7 (2026-10-10)**

```
In final-project-film/PROJECT-BRIEF.md apply only these, show diff + word count:
- Cut 3: §2 opener → "The hard question is not only what was decided, but whether it still holds and is finished."
- Cut 4: §3 → "A hiring manager or engineer."
- Cut 5: §6 remove ", keep them separate from document generation,"
- §2: replace "DecisionTrace will do both:" with "DecisionTrace will do what neither did:"
Do NOT apply cuts 1 or 2.
Commit "brief: tighten" and push.

Then print the beat_sheet.json schema section from ../brutalist-notes.md, plus the toolkit's own example beat sheet if one exists (path + contents), so I can plan the film.
```

**P8 (2026-10-10)** — the beat plan and the original narration

```
Goal: plan the pitch film's beat_sheet.json. Do NOT render yet.

Working folder: ~/info7375-films/decisiontrace-pitch/ (outside every git repo, and NOT inside brutalist.art/).
Run toolkit commands from brutalist.art/ with .venv active.

Rules:
- Build from the schema in ../brutalist-notes.md. Do not copy or edit any example beat sheet.
- No instructor persona anywhere: no NikBearBrown/Bear greeting, no "Liam", no folderLabel @NikBearBrown,
  no persona/channel_title of the instructor, no ClaudeTitleOutro, no voice_env/ELEVENLABS keys.
- Use narration_text only (no "narration" field). Narration must be EXACTLY the text below. Don't reword.
- metadata: title "DecisionTrace — Final Project Pitch", slug "decisiontrace-pitch", engine "kokoro", aspect "16:9",
  channel_title "Gnanasudharsan Ashokumar".
- Show-tell style: one simple picture per beat, minimal on-screen text, narration carries the idea.
- Required on-screen labels: B02 "SYNTHETIC TEST DATA"; B03 "REAL · NotebookLM · captured 2026-10-10";
  B04 "REAL · ChatGPT · captured 2026-10-10"; B06 "CONSTRUCTED · not real output".
- B03 uses final-project-film/evidence/alternatives-test/screenshots/2026-10-10_notebooklm_summary.png
  B04 uses .../2026-10-10_chatgpt_q1.png. Copy them into the working folder, unedited.

Stage 1, then STOP and wait for me:
1. For each beat, run ./art scenes "<what the beat needs>" and propose one scene/pattern + props.
   Show a table: beat | picture needed | proposed pattern | why | on-screen text.
2. Tell me how a real screenshot can be shown (which pattern supports an image). If none does, say so plainly
   and suggest the simplest honest fallback.
3. If a beat has no suitable scene, propose a plain SLATE rather than forcing a mismatched scene.
4. List 3 Kokoro voices that are NOT am_onyx (instructor's) and render one short sample sentence each
   in the working folder so I can listen and pick.

Beats (beat_id | act | narration_text):
B00 | title | I'm Gnanasudharsan Ashokumar. This is a pitch for a project that doesn't exist yet. Its working title is DecisionTrace.
B01 | what | DecisionTrace will answer one question about a team's history: why did we decide this, and where does that decision stand now? It will be a public GitHub repository: a Python command-line tool, a synthetic document set, a hand-checked test set, and an evaluation report.
B02 | test setup | Before pitching it, I tested two tools that already do something close. On October ninth, I gave NotebookLM and ChatGPT the same six synthetic documents about a fictional company switching databases. The switch was approved, but not finished.
B03 | notebooklm | NotebookLM got the facts right and refused to invent a budget. But its summary gave no sign the migration was still in progress. Asked which database the service uses, it said DynamoDB, without saying the switch wasn't done.
B04 | chatgpt | ChatGPT got the status right. But it dated that status to June fifteenth, which is an unrelated team retrospective. Nothing flagged it.
B05 | difference | In this test, neither tool flagged those mistakes, and neither showed how often it was right. DecisionTrace will do what neither did: report a decision's status, mark any claim whose cited passage is missing or doesn't support it, and publish its score on a hand-checked test set.
B06 | who | The person opening it will be a hiring manager or an engineer. In the first sixty seconds, they'll run one command, see an answer with a pass or fail line for every claim, and open the evaluation report.
B07 | proves | It will show I can build and measure a grounded tool. A prompt contract will force JSON with a citation for every claim. Code will check each quote appears word for word. A second model call will judge whether it supports the claim, and I'll spot-check those judgments. If a claim fails, the loop retries once, or says the sources don't support it. It won't prove it works on real company data, because it won't be tested on any.
B08 | scope | It will not connect to Slack, Jira, or email, and it will use no real data. The first piece to run will answer one question over those six documents, and a test will pass confirming every quote appears in its source.
B09 | risk | The risk that could sink it: the documents are written with Claude. If Claude also writes the questions, the evaluation grades its own homework. So I'll write the hard cases myself, including reversed decisions, unfinished work, and questions with no answer, and report that limit.
B10 | why | Why this project? Mostly to learn. Evaluation harnesses, citation checking, prompt contracts, and agent loops are new to me. What I already have is building RAG pipelines and LLM backends in Python, from a co-op. That code belongs to the company, so this repository will be the first public evidence.
B11 | exists vs will | What exists today is the test I just showed you, with its documents, notes, and screenshots, plus this brief and this film. Everything else is will.
B12 | outro | I'm Gnanasudharsan Ashokumar. The narration voice is synthetic, made with Kokoro. Thanks for watching.

Also add a FRICTIONAL entry dated 2026-10-10: beat plan approved; scene mapping started.
```

**P9 (2026-10-10)** — My voice choice, sent as a reply when Claude Code asked: `af_heart`.

```
Decisions:
- Voice: <am_eric | am_adam | af_heart> for every beat (metadata.voice_kokoro + per-beat voice).
- Manim (scenes.py in the working folder, simple line drawings, no text beyond 1–3 words per element):
  B01 question mark → status tag "decided · in progress · superseded"
  B05 a claim + its cited quote, check ✓ found / ✗ missing
  B07 loop: answer → verify → retry once → "not supported"
  B09 a hand grading its own paper
- All other beats: MedhavyConceptCard with the on-screen text from your table; B06 BrutalistTerminalOpen
  with EVERY default checklist line overridden (no "voice NikBearBrown" can survive).
- B03/B04: composed frame. Screenshot unaltered except scaling, fit pad, treatment none, motion hold,
  required label above, plus a highlight box drawn on the frame (not in the image) around:
  B03 "successfully deploy the new NoSQL infrastructure"; B04 "June 15, 2026 (latest supplied records)".

Then:
1. Write beat_sheet.json in the working folder. Narration exactly as given.
2. Generate audio. Report each beat's actual_duration_s and the total runtime (must be 2–4 min).
   Tell me if Kokoro mispronounces "Gnanasudharsan Ashokumar" or "DecisionTrace".
3. Render a draft and run every quality gate, including render-integrity. Save the gate reports.
4. Make a contact sheet (one frame per beat) and grep every rendered text/prop and the final
   beat_sheet.json for: Bear, NikBearBrown, Liam, Talofa, Hola, ELEVENLABS. Report any hit.
5. STOP. Don't copy anything into the course fork yet. Show me the contact sheet, runtime, gate results.
Add a FRICTIONAL entry 2026-10-10 for: no generic picture scenes in the toolkit (wrote own Manim scenes),
no image scene (composed labelled frames), slates blocked by ./art final.
```

**P10 (2026-10-10)**

```
Apply:
1. Replace every MedhavyConceptCard beat with text-led scenes in scenes.py: large frame-filling type, same palette, same on-screen text as now.
2. Scale up the B01, B07, B09 drawings to fill the frame.
3. B06: put "CONSTRUCTED · NOT REAL OUTPUT" in large text at the top of the frame.
4. B04: crop the ChatGPT screenshot from the heading "What is the current implementation status?" through the
   "Bottom line" sentence (must include "June 15, 2026 (latest supplied records)" and "not a completed switch").
   Pixels otherwise unaltered; keep label + highlight box. Original stays in evidence/.

Name pronunciation, BEFORE re-rendering:
Render af_heart samples of the sentence "I'm ___." for each of these spellings, named by number:
  1. Nyaana-sudharsan Ashok-kumaar
  2. Gyaana-sudharsan Ashok Kumar
  3. Nyana sudarshan Ashokumar
Wait for my pick. Then use it ONLY in narration_text for B00 and B12. On-screen text keeps "Gnanasudharsan Ashokumar".
Check: if any subtitles or captions are generated from narration_text, tell me, since they'd show the phonetic spelling.

Then re-render, re-run every gate (strict, no ART_STRICT=0), new contact sheet, persona grep again. Stop and report.
Log in FRICTIONAL (2026-10-10): GATE V failure (19 MAJOR) and fixes; B04 crop and why; phonetic name spelling in narration only.
```

**P11 (2026-10-10)**

```
Render two more af_heart samples, "I'm ___.", and show their phonemes:
  4. Nyah-nuh-sudharsan Ashok Kumar
  5. Nya-na-sudharsan Ashok Kumar
```

**P12 (2026-10-10)**

```
Use #5 in narration_text for B00 and B12 only. Then re-render strict, run every gate, new contact sheet, persona grep, FRICTIONAL entry. Stop and report.
```

**P13 (2026-10-10)**

```
Revise the draft (don't touch other beats' narration):
1. B08: narration add after the Slack/Jira sentence: "What's in: the tool, the verifier, the test set, and the evaluation report."
   On screen add an "In:" line. Regenerate B08 audio only.
2. B01: second half shows a repo folder with 4 items (CLI · synthetic docs · test set · eval report), labelled PLANNED.
3. B03: split visual: summary screenshot first half, then evidence/.../2026-10-10_notebooklm_run2_q1.png
   (same REAL label, highlight "uses DynamoDB as its primary datastore"), timed to "Asked which database".
4. B07: add a "✓ pass → cited answer" branch from verify; place "retry once" beside the curved arrow; check the stray mark near "not supported".
5. B09: end with a page labelled "hand-written by me" showing a ✗ on a hard case.
6. B06: add answer line "→ DynamoDB (decided 2026-05-18) · status: in progress" above the checks; FAIL in red;
   cream background; remove stray red line; window title "zsh — decisiontrace" if settable.
7. B00: name text 2–3× larger. B11: "test" → "alternatives test".
8. Tell me whether audio_policy (or anything else) lets me supply my own recorded mp3 for B00 and B12. Don't change audio yet.
Then re-render strict, all gates, contact sheet, persona grep, runtime (must stay under 4:00). Log FRICTIONAL 2026-10-10. Stop and report.
```

**P14 (2026-10-10)** — own-voice recordings. **Reversed by P15**, so the final film uses none.

```
I recorded B00 and B12 myself:
  ~/info7375-films/decisiontrace-pitch/audio/B00.m4a
  ~/info7375-films/decisiontrace-pitch/audio/B012.m4a   (this is B12)

1. Convert both to mp3 (audio/B00-own.mp3, audio/B12-own.mp3). Trim leading/trailing silence, keeping ~0.2 s padding,
   and normalise loudness to match the Kokoro beats (target mean ≈ −25.4 dB). Report each file's length and mean dB.
   Keep the original .m4a files untouched.
2. Set for B00 and B12: audio_file → the new mp3, actual_duration_s → measured length, narration_text → exactly:
   B00: "I'm Gnanasudharsan Ashokumar. This is a pitch for a project that doesn't exist yet. Its working title is DecisionTrace."
   B12: "I'm Gnanasudharsan Ashokumar. The rest of the narration is a synthetic voice, made with Kokoro. Thanks for watching."
3. B12 on-screen text: "Narration: synthetic voice (Kokoro) · name lines recorded by me".
4. B11: split the heading over two lines so it renders larger than its second line.
5. From now on use --only for any audio regeneration so my recordings are never overwritten.
6. Re-render B00, B11, B12 to the new lengths, recompile strict (no ART_STRICT=0), run every gate,
   persona grep, report runtime (must stay under 4:00). Update FACTCHECK.md and SHOTLIST.md for the own-voice beats.
7. Log FRICTIONAL 2026-10-10: Kokoro mispronounced my name across 5 spellings; recorded B00 and B12 in my own voice.
Stop and report. Don't copy to the course fork yet.
```

**P15 (2026-10-10)** — one voice for every beat; name from IPA

```
Change of plan: remove my own-voice recordings and use af_heart (Kokoro) for EVERY beat, so the whole film
has one consistent voice, with my name pronounced correctly via explicit phonemes.

1. Revert B00 and B12 to Kokoro: engine "kokoro", voice af_heart; remove the own-recording audio_file entries.
   Delete audio/B00-own.mp3 and audio/B12-own.mp3 from the build. Keep my original .m4a files untouched.
   Check the course fork: if any own-voice audio was copied there, remove it and commit.
2. Restore narration_text (real spelling):
   B00: "I'm Gnanasudharsan Ashokumar. This is a pitch for a project that doesn't exist yet. Its working title is DecisionTrace."
   B12: "I'm Gnanasudharsan Ashokumar. The narration voice is synthetic, made with Kokoro. Thanks for watching."
   B12 on-screen text back to: "Narration: synthetic voice (Kokoro)".
3. Pronunciation via phonemes. Check whether kokoro-onnx 0.6.1 can synthesise from a phoneme string (e.g. is_phonemes=True).
   If yes, write tools/phoneme_name.py in the working folder (NOT in brutalist.art/) that phonemises each B00/B12
   sentence normally but replaces ONLY the name with a hand-set IPA string.

   My pronunciation guide:
   - Full: "Nyahn-ah-soo-dhar-shahn Ah-shohk-koo-mahr"
   - Gna-: G is silent; sounds like "ny" in "canyon" / Spanish "ñ", then a soft "ah" → "Nyahn"
   - -na-: short soft "ah"
   - -su-: "soo"
   - -dhar-: soft dental "d" (tongue behind teeth), slightly breathy, then a short "ur" → "dhar"
   - -san: "shahn", soft "sh"
   - Ashok-: "Ah-shohk" ("oh" in the middle)
   - -kumar: "koo-mahr"

   Render af_heart samples of "I'm <name>." for these IPA variants, and add one or two of your own if you think they fit the guide better:
     A. ɲˈɑːnɑːsuːdɚʃˌɑːn ɑːʃˈoʊk kuːmˌɑːɹ
     B. njˈɑːnɑːsuːdɚʃˌɑːn ɑːʃˈoʊk kuːmˌɑːɹ   (fallback if ɲ is unsupported)
     C. ɲˈɑːnɑːsˌuːdəɹʃɑːn ɑːʃˈoʊkkuːmˌɑːɹ
   Report which symbols are in Kokoro's phoneme vocabulary; substitute unsupported ones and say what you changed.
   Name files samples/name-A.mp3 etc. STOP and let me pick by ear.
   If phoneme input is NOT supported, stop and tell me; don't fall back silently.

4. After I pick: generate B00 and B12 with that IPA, af_heart, normal loudness matching other beats.
   Mark both beats so the standard Kokoro script won't overwrite them. Record the exact IPA in a note field
   in beat_sheet.json (it goes into BUILD-PROMPT.md later).
5. Re-render B00 and B12, recompile strict (no ART_STRICT=0), run every gate, persona grep, report runtime (< 4:00).
   Update FACTCHECK.md and SHOTLIST.md.
6. Log FRICTIONAL 2026-10-10: removed own-voice lines to keep one consistent voice; fixed name pronunciation
   with explicit IPA phonemes in Kokoro after five respellings failed.
Stop and report.
```

**P16 (2026-10-10)**

```
Go with e
```

(Variants D and E were added by Claude Code. E is the breathy `dʰ` version with lighter stress on
"soo" and full stress on "mahr".)

**P17 (2026-10-10)**

```
Small fixes to draft 6 (don't change any narration unless stated):
1. B06: cursor must sit after the typed text, not before; restore the line "→ report   eval/report.md" after the claim lines;
   start typing earlier so the completed screen holds for at least 4 s.
2. B08: remove the short orange accent dashes under "Jira" and "test set" (keep any accent that doesn't sit under a single word, or move it under the full line).
3. B01: hold the completed folder (all 4 items) at least 1.5 s before the beat ends.
4. [ONLY IF I say ChatGPT ran on 10-10] B02 narration: "On October ninth and tenth, I gave NotebookLM and ChatGPT…";
   regenerate B02 audio with --only; also update PROJECT-BRIEF.md §2 date accordingly.
5. [ONLY IF I list mispronounced words] use phoneme overrides for just those words, like the name.
Re-render only affected beats, recompile strict, all gates, persona grep, runtime. Log FRICTIONAL 2026-10-10. Stop and report.
```

(I didn't trigger items 4 or 5, so neither was applied.)

**P18 (2026-10-10)**

```
I confirm the ChatGPT date is correct as narrated and I've listened to draft 7. Approved.

1. Run ./art final for decisiontrace-pitch (strict, no ART_STRICT=0). Confirm the review-cut corner tags
   (e.g. "B00 GRAPHIC MANIM") are absent in the final master. Save the final gate reports.
2. Report final .mp4 size (GitHub limit 100 MB).
3. Copy into fall-2026/gnanasudharsan-a/final-project-film/:
   - final master as decisiontrace-pitch.mp4
   - beat_sheet.json
   - gate-reports/ (final run only; no draft subfolders)
   - FACTCHECK.md, SHOTLIST.md, PROMPTS.md
   - build/: scenes.py, tools/ (phoneme_name.py, compose_frames.py, any other script used in draft 7),
     and the composed B03/B04 frames
   Do NOT copy: own-voice audio or old-draft-5/, my .m4a files, name samples, Kokoro audio cache, venvs, old drafts.
4. Check that every path in beat_sheet.json resolves against the copied build/ layout, or list which paths are
   relative to the working folder (I'll explain that in BUILD-PROMPT.md).
5. Commit the pending FRICTIONAL entries with these files. git status first: only final-project-film/ staged.
   Commit "film: final render + gate reports" and push.
6. Report: file list with sizes, final runtime, commit hash.
```

**P19 (2026-10-10)** — *summarised.* I asked for this README.md, this BUILD-PROMPT.md and
SOURCES.md, with every fact checked against the actual files or packages. The prompt also asked
for:

- an optional redaction of my home path in the gate reports
- a checklist against the assignment and a consistency check
- a FRICTIONAL entry
- a commit with the message "docs: README, BUILD-PROMPT, SOURCES".

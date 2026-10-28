# BUILD-PROMPT — Record Beats AI

How this film was built: the instructions I gave Claude Code (Opus 5.5, Claude desktop app), in order, then the exact commands. The instructions are reproduced as given, lightly trimmed only where they repeated themselves or named local paths. They are my instructions only; no Claude replies or chat transcripts are included.

## Generation prompts

There were none. This is the content of the film's `PROMPTS.md`, which the toolkit's Gate F requires:

> No generation prompts. Every picture is drawn natively: Manim vector scenes from the show-tell kit (`scenes.py`) and the toolkit's Remotion bookend and card templates (`BrutalistHesitantWriter`, `ClaudeDefinitions`, `ShowTellCard`). No AI image, video, or upscaling service was used. Narration is free, local Kokoro TTS (`am_michael`), a synthetic voice, disclosed on screen and in the outro.

## Instructions to Claude Code, in order

**1. Fresh toolkit checkout**
```text
Set up a fresh, separate Brutalist checkout for a new film. Do not touch my old Brut folder in any way.
1) git clone https://github.com/nikbearbrown/brutalist.art BrutFilm
2) Follow the new checkout's own README to create its .venv and run its setup. Do not copy the old .venv.
3) Run the doctor check and report the result.
4) Run ./art smoke and report whether a test video actually rendered, with its path and runtime.
5) Confirm skills/make/show-tell/SKILL.md exists and report the example folder it references.
6) Report the exact commit hash you cloned.
Change no files in the toolkit. Report everything, including any errors verbatim.
```

**2. Voices**
```text
Read-only, change no toolkit files:
1) List every Kokoro voice actually available on this machine.
2) Name any American or British male voice other than am_onyx that is available AND allowed without editing toolkit files.
3) If using another voice would require editing ALLOWED_VOICES, tell me the exact file and line, but do not edit it.
4) Make voice-tests/ and generate a 10-second test clip with each allowed male voice saying:
   "I'm Sreevarshan Sathiyamurthy, and this is a pitch for something I will build."
```

**3. Verify, then write the beat sheet and claims table**
```text
Write the beat sheet for my pitch film. Do not render anything yet.
Inputs: my brief (PROJECT-BRIEF.md); the toolkit (follow skills/make/show-tell/SKILL.md and its templates);
my project repo the-reallocation-engine, read-only.
Step 1, verify before writing. For every line under "Exists today" in the brief, check it against the repo
(commit hashes, current test count, the AMGEN 404, the funnel numbers, PR #32 status, DRAFT status).
Report each as CONFIRMED, CHANGED (with the real value) or NOT FOUND. Anything not CONFIRMED must not
appear in past tense in the film.
Step 2, write beat_sheet.json in the show-tell format.
- Runtime 2 to 4 minutes. Every one of the brief's seven sections gets at least one beat.
- Narrator is me, in first person. Kokoro voice am_michael for the whole film.
- Nothing anywhere may say the toolkit's default narrator or its owner's channel: narration, labels,
  captions, outro, or folder labels. Replace show-tell's outro with my own sign-off using my name.
  Drop the "Your Turn" Claude.ai composer beat.
- The "why now" beat may use only a real number from the repo's worked run, attributed on screen.
- The persona meera-krishnan is fictional: label her CONSTRUCTED on screen. Use no real personal data of mine.
- Say that the prototype was built for my INFO 7375 Assignment 2 in early October 2026.
- Past tense only for CONFIRMED items. Everything else uses "will."
Step 3, write CLAIMS.md: one row per narration sentence, tagged SHOWN (with the repo file or output
that proves it), WILL, or CONSTRUCTED. List any Claude reply or Terminal output on screen, with the
file I need to put in evidence/.
```

**4. Hand-check command**
```text
Read-only. From WORKED-RUN.md, give me the exact one-line Terminal command I used to check the
AMGEN INC 1882.0 and HUMAN INC 1382.0 values. Do not run it yourself.
```
The answer: the command isn't recorded in WORKED-RUN.md. I then supplied it myself and re-ran it on 2026-10-11 (see `SOURCES.md`, "Hand check").

**5. Record both hand checks**
```text
In the film's CLAIMS.md and SOURCES.md, record both: the original check in early October (Assignment 2)
and the re-run screenshot dated 2026-10-11. Do not edit the Reallocation repo.
```

**6. Transcript and screenshot decisions**
```text
1) Do not add any chat transcript export. The assignment forbids private conversation transcripts.
   State that HC-1 is backed by my statement and WORKED-RUN.md:191,199, and that the transcript is
   intentionally excluded per the assignment's rule.
2) Do not show hand-check-terminal.png on screen. In B15, draw the two values as a simple show-tell
   illustration with a small caption "re-run 2026-10-11". The screenshot stays in evidence/ only.
```

**7. Title**
```text
Change the film's working title to "Record Beats AI: A Sponsorship Job Finder That Checks Its Own Answers".
```

**8. Build**
```text
1) BIDEA: add a small on-screen label "Narrated with a synthetic voice (Kokoro am_michael)".
   BOUT: add a spoken line disclosing the synthetic voice.
2) B18: "Why build the evaluation log first? In my worked run, the liveness tool contradicted both postings
   an AI had called open. Two is a sample, not a rate. The log will measure it properly." Keep "2 of 2"
   with its source caption.
3) Keep total narration under 4 minutes; if over, cut framing lines first, never SHOWN facts.
4) Copy the repo-sourced evidence files into evidence/, each with its original date.
5) Write SOURCES.md, FACTCHECK.md, SHOTLIST.md, PROMPTS.md. SOURCES.md must state that Claude (chat) and
   Claude Code drafted the brief, script and build, that I reviewed them, that the voice is synthetic,
   that the two sponsor sites were checked by me on 2026-10-11, and that the hand check was first run in
   early October (Assignment 2) and re-run on 2026-10-11.
6) Write scenes.py following show-tell: one simple drawn picture per beat, labels of 1 to 3 words,
   no person icons, anything constructed visibly stamped CONSTRUCTED.
7) Generate the Kokoro audio, render the full film, and run every quality gate the toolkit has.
   If any gate fails, fix and re-render until all pass, up to 3 attempts per failure.
```

**9. Fix pass**
```text
1) Restore graded content that was cut for length: B14 in full; B15's opening "New to me: …";
   B11's done-criterion.
2) BOUT: "This narration uses a synthetic voice. I drafted the script with Claude and checked every claim."
3) Fix my name's pronunciation by changing narration text only. Respell it phonetically for Kokoro and
   re-check with whisper. On-screen labels and the byline keep the real spelling. Record the respelling
   in CLAIMS.md as a pronunciation aid.
4) If the restored lines push narration over 4:00, raise Kokoro's speed just enough, up to 1.1, to land
   between 3:45 and 3:58, if that can be done without editing toolkit files; otherwise cut FRAMING lines only.
5) If the 4K master is under 90 MB, make it the deliverable.
```

**10. One label**
```text
B10: change the "CONSTRUCTED" label on the third excluded item to "personal data". Keep CONSTRUCTED only on
the meera-krishnan persona file in B03. Re-render B10 only, recompile, and rerun every film-level gate on
the new 4K master.
```

**11. SOURCES line, then assemble this submission folder.**

**12. Final fixes**
```text
1) B02: name the alternatives: "Sponsor sites like Ellis and F1Jobs count past visa filings; mine will also check
   that a posting is live, and match occupation and level." Add small on-screen labels "Ellis" and "F1Jobs" on the
   past-filings side of B02's drawing.
2) B03: add the target role: "In the first minute, a hiring manager for an ML or AI engineer role will open the
   README, run one command on a made-up persona, Meera Krishnan, and open the report."
3) Keep total runtime under 3:59. Keep Kokoro at --speed 1.09. If needed, cut FRAMING lines only (never SHOWN
   facts, never the B11/B14/B15 restored lines). Re-voice and re-render only the changed beats.
4) SOURCES.md licences: read the actual licence files and add each third-party component with its licence.
```
Result: the two new lines ran the film to 240.9 s, so B18's opening question "Why build the evaluation log first?" (FRAMING) was cut. B03's labels went to 44 for Gate T, and its persona column moved right for Gate B.

## Commands, in order

The commands assume a `Downloads/` layout with `BrutFilm/` (toolkit) and `final-project-film/youtube/show-tell-reallocation-recipe-pitch/` (film folder, `$R`) side by side.

```bash
# toolkit
git clone https://github.com/nikbearbrown/brutalist.art BrutFilm      # HEAD b21f6253a336098f3f55847a9525ae6868ccbdb7
cd BrutFilm && /opt/homebrew/bin/python3.11 -m venv .venv && source .venv/bin/activate
./setup --install                                   # deps OK; exits 1 at the ElevenLabs guard (toolkit bug)
git checkout -- runtime/remotion/package-lock.json  # undo setup's lockfile change

# sheet + audio (in $R)
python3 make_sheet.py
python3 ../../../BrutFilm/runtime/scripts/generate_audio_kokoro.py . --speed 1.09
python3 finish_audio.py                             # pads BIDEA (0.8 s lead) and BOUT (1.0 s tail); runtime 238.2 s (master 238.6 s)

# render + gates
../../../BrutFilm/art run "$R" --height 1080        # Gates F, L, SHAPE, A, W, B, V; review cut
../../../BrutFilm/art final "$R" --height 2160 --out "$R/exports/landscape-4k"   # Gate T, then the 4K master

# remaining gates (from BrutFilm/runtime), M = the 4K master
python3 scripts/bookend_check.py "$R"
python3 qc/factcheck_check.py "$R"
python3 qc/beat_lint.py "$R/beat_sheet.json"
python3 qc/gate_shape.py "$R/beat_sheet.json"
python3 qc/content_check.py "$R"
python3 qc/placeholder_check.py "$R"
python3 qc/lane_check.py "$R"
python3 qc/banned_card_check.py "$R"
python3 scripts/math_layout_check.py "$R/beat_sheet.json"
python3 qc/frame_check.py "$R" --height 2160
python3 qc/final_frame_check.py "$R" --mp4 "$M"
python3 scripts/master_check.py "$R" --mp4 "$M"
python3 scripts/loudness_check.py "$R" --mp4 "$M"
python3 scripts/sharpness_check.py "$R"
python3 scripts/srt_check.py "$R"                   # SKIP: no captions
python3 scripts/audit_review_queue.py --list audit-list.txt --root final-project-film --out audit-queue
```

Fixes that came out of the gates during the build:
- **Gate B:** B18's source caption was outside the safe area; shrunk and moved.
- **Gate T, B04:** the focus card's lens enclosing a row's text read as overlapping text; B04 was redrawn as a Manim funnel.
- **Gate T, B17 and B14:** text was under the 41 px floor. B17's labels were enlarged; B14's small scribbles were replaced with ghost lines.
- **Gate T, then Gate B, B03:** after the B03 narration change, its 40 px labels were sampled at the midpoint; they were raised to 44, and the persona column was moved right to keep "CONSTRUCTED" inside the safe area.
- **Stills review:** label overlaps in B00, B05, B10, B13 and B16 were fixed before any 4K render.

# BUILD-PROMPT — how this film was made, and how to make it again

Built on 2026-10-14 with Claude Code (Claude Opus 5.5) running locally, using the Brutalist toolkit
(https://github.com/nikbearbrown/brutalist.art, commit `519fcbb`) and its `show-tell` skill.
No paid generation, no API keys, no uploads.

## 1. The rebuild prompt

To rebuild the film with an agent, give it this folder plus a clone of the toolkit, and this prompt:

> Use the Brutalist `show-tell` skill to rebuild the film in `build/`. Read the skill's SKILL.md and
> `build/make_sheet.py` first. Do not change the narration, the voice (`af_bella`, speed 1.05), or the
> honesty labels: only Money Map exists; everything about Remnix is "will"; B05 stays labelled
> CONSTRUCTED; the film shows no Claude interface or response; there is no instructor greeting, handle,
> portrait or credit line, and the outro is the student's own card. Follow the commands in README.md in
> order. Run every gate. If the render-integrity check or Gate V fails, fix the scene source and
> re-render; never weaken a checker. Do not publish anything.

## 2. The prompts I gave, in order (my words, summarised)

These are my instructions to Claude in the build session, summarised, not a transcript.

1. Make a 2–4 minute pitch film for my INFO 7375 final project with the Brutalist toolkit, following the
   assignment text. I gave the project (Remnix Agent), the stack, the build order, the alternatives, the
   target role, my existing and new skills, and nine rules (honesty, no invented facts, label
   mock-ups "constructed", no Claude responses without a real date, no MIT DCI repo code or data, no
   private data, first person as me with no instructor persona, an honest FRICTIONAL log, free pipeline only).
   Work in 8 steps and pause after each one.
2. Step 1: clone the toolkit, explain the pipeline, use show-tell if it exists.
3. Voice: use a free Kokoro voice reading my first-person script, and say on screen that it is synthetic.
4. Step 2 answers: my last name (used only for the Canvas file name); Wise's comparison page and Monito do not include stablecoin routes;
   research the World Bank site; data access unknown at that point; I built Money Map alone.
5. Steps 3 and 4 approved, including `./setup --install`, Manim and the Kokoro model download.
6. After watching the review cut: remove "ask MIT DCI first", because I can use Money Map's data; check the
   film against the seven questions.
7. Add researchers and policymakers who study remittance costs as a second audience.
8. Confirmed the B14 line "I picked it because it builds on Money Map and points at the fintech work I want".
9. Step 6: apply all the honesty fixes, keep the film under 4:00, re-render and re-run the gates.
10. Push to the course repo; use "Revan C" instead of my full name, because the course repo stores no full names.

**Resubmission, 2026-10-25** (after grades and the TA's class note asking films to say who is doing it, explain
simply for a non-technical viewer, stay concise and give full technical detail):

11. Make improvements from the grading comments; ask me the FRICTIONAL questions here and I'll answer in my own words.
12. No dated snapshot for now.
13. Introduce me as a graduate student at Northeastern who built Money Map at MIT DCI.
14. Plan approved as proposed, including the technical design (tables `quotes`, `fx_rates`, `snapshots`;
    `POST /ask`; tools `get_quotes`, `compute_cost`; pytest writing `wrong_answers.md`).

## 3. Commands

Environment (the toolkit's venv plus the espeak-ng fix; see `build/env.sh`):

```bash
cd brutalist.art && python3.14 -m venv .venv && PATH="$PWD/.venv/bin:$PATH" ./setup --install
brew install espeak-ng
export TOOLKIT="/path/to/brutalist.art" && source build/env.sh
```

Screenshot of the public Money Map page (taken once, 2026-10-14 16:20 EDT; already in `build/pantry/`):

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
  --window-size=1600,1000 --virtual-time-budget=15000 \
  --screenshot="build/pantry/money-map-2026-10-14.png" https://mit-dci.github.io/payments-dashboard/
ffmpeg -i build/pantry/money-map-2026-10-14.png -vf "crop=1600:460:0:0" build/pantry/money-map-2026-10-14-top.png
```

Build (the same as README.md):

```bash
REEL="$PWD/build"
python3 "$REEL/make_sheet.py"
python3 "$TOOLKIT/runtime/scripts/generate_audio_kokoro.py" "$REEL" --speed 1.05
python3 "$REEL/finish_audio.py"
python3 "$REEL/build_scenes.py"
(cd "$TOOLKIT" && ./art run "$REEL" --height 2160)
(cd "$TOOLKIT" && ./art final "$REEL" --height 2160 --out "$REEL/exports/landscape")
```

Checks that were run before rendering, per scene (Gate A in an isolated folder holding only `scenes.py`, as the skill asks):

```bash
PYTHONPATH="$TOOLKIT/runtime/manim" python3 "$TOOLKIT/runtime/qc/static_scene_check.py" scenes.py --class B00_MoneyMap --quiet
python3 "$TOOLKIT/runtime/qc/manim_layout_audit.py" scenes.py --class B00_MoneyMap --curve-strict
python3 "$TOOLKIT/runtime/qc/wcag_margin_check.py" scenes.py --class B00_MoneyMap --quiet
manim -ql -s scenes.py B00_MoneyMap        # low-res last-frame still, looked at before any 4K render
```

Gates run after the master:

```bash
M="$REEL/exports/landscape/remnix-agent-pitch.mp4"
python3 "$TOOLKIT/runtime/scripts/master_check.py"   "$REEL" --mp4 "$M"
python3 "$TOOLKIT/runtime/scripts/loudness_check.py" "$REEL" --mp4 "$M"
python3 "$TOOLKIT/runtime/scripts/sharpness_check.py" "$REEL"
python3 "$TOOLKIT/runtime/qc/factcheck_check.py"     "$REEL"
python3 "$TOOLKIT/runtime/scripts/bookend_check.py"  "$REEL"   # fails 2 outro items by design; see gate-reports/GATE-SUMMARY.md
ffmpeg -hide_banner -sseof -0.9 -i "$M" -af volumedetect -vn -f null -   # silent outro tail
```

To change one beat: edit `make_sheet.py` and/or `scene_body.py`, then rerun `make_sheet.py`, the audio
step and `finish_audio.py` (Kokoro returned identical audio for unchanged lines). Move that beat's
`manim/<BID>.mp4` (or `media/<BID>.mp4` for BIDEA/BDEFS) and `media/videos/` into `_superseded/`, then
rerun `art run` and `art final`. `art run` only renders slots that are missing.

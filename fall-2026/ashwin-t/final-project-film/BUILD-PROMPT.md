# BUILD-PROMPT.md: how to rebuild the TraceCase pitch film

## The prompts I gave Claude Code (2026-10-13)

> I want you to understand my resumes, my skills and what are the roles I've been applying to lately using the
> tool and whatever the current job market requires … and build something like that for my AI prompt engineering
> course project … It should be an AI-based project and also include, I don't know if it is possible to include
> Redis, caching and stuff like that. If it is not, it's fine, but not forcefully.

Then, after choosing TraceCase:

> Yes, please start building it and please add the fictional log … write the fictional log [like] me, don't write
> it like Claude … build me the film properly and make the film look intuitive and make the voice very nice and
> calming.

The working rules Claude followed, in my words:

1. Use the Brutalist toolkit's `show-tell` skill: one drawn picture per beat, minimal text, the voice explains.
   Keep one cast across the film (service, logs, trace, magnifier for the agent, fix card, barrier gate).
2. Answer the assignment's seven questions in order, one idea per beat, from `PROJECT-BRIEF.md`. Stay under four
   minutes.
3. Narrate as me, in first person. Don't use the instructor's name, the "Liam, in for Bear" persona, or the
   instructor's credit line. The final cut uses the synthetic voice throughout, by my choice.
4. Honesty rule: every product sentence in the future tense, every picture of the product tagged "constructed",
   no invented numbers (B09 shows "? / 10"). Name alternatives only with facts checked against their own pages.
5. Run the toolkit's gates and fix anything that fails. Never submit over a failed render check.

## One-time setup (macOS, Apple silicon)

```bash
git clone https://github.com/nikbearbrown/brutalist.art brutalist-final   # used at b21f625
brew install python@3.12 pango ffmpeg        # manim 0.18 needs Python < 3.13; manimpango needs pango
cd brutalist-final
/opt/homebrew/bin/python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install "av<16"                          # av 19 breaks faster-whisper 1.2.1
(cd runtime/remotion && npm install)
# Kokoro model: ./setup --install downloads it, or copy runtime/models/kokoro/ from an existing checkout
```

Apply my local changes to the toolkit (copies are in `build/` here):

```bash
TK=/path/to/brutalist-final
cp build/ashwin.json $TK/runtime/pronunciation/ashwin.json             # voice-only: "Redis" -> "Reddiss"
git -C $TK apply "$PWD/build/patches/ClaudeTitleOutro-handle.patch"    # outro takes my name, not the instructor's handle
```

`build/build_scenes.py` and `build/record_beat.sh` expect the toolkit at `~/Desktop/College/CSYE7375/brutalist-final/`;
change the path at the top of each if yours is elsewhere.

## Rebuild

Work on a copy outside the course repo, so audio and clips stay out of it:

```bash
cp -R build /tmp/tracecase-pitch
cp gate-reports/{FACTCHECK,SHOTLIST,PROMPTS}.md /tmp/tracecase-pitch/      # Gate F needs them
cd /tmp/tracecase-pitch && source $TK/.venv/bin/activate
python make_sheet.py                                                     # writes beat_sheet.json
python $TK/runtime/scripts/generate_audio_kokoro.py . --speed 0.95       # synthetic narration for every beat
python finish_audio.py                                                   # pads BIDEA/BOUT, writes measured durations
# ./record_beat.sh BIDEA                                                 # optional: replace a beat with your own voice (not used in the final cut)
python $TK/runtime/scripts/align.py .                                    # word timestamps -> mp3/words.json (scenes cue on these)
python whisper_check.py                                                  # transcript vs script, by beat
python build_scenes.py                                                   # scenes.py = iso_kit.py + scene_body.py
(cd $TK && ./art run /tmp/tracecase-pitch --height 2160)                 # renders; gates L, A, W, B, V
(cd $TK && ./art final /tmp/tracecase-pitch --height 2160 --out /tmp/tracecase-pitch/final)   # Gate T + master
python $TK/runtime/qc/factcheck_check.py /tmp/tracecase-pitch            # fact-check gate
python $TK/runtime/scripts/bookend_check.py /tmp/tracecase-pitch         # bookend gate
```

# BUILD-PROMPT

Part A is enough to rebuild the film. Part B is the prompt history that produced it: the instructions given to Claude Code in VS Code, in order, quoted as given.

## Part A: Commands that rebuild the film

Run these from the Brutalist toolkit root, with this folder placed at `youtube/brutalist/agent-proving-ground/`:

```bash
./setup --install            # Python deps, Kokoro model files, dependency check

# 1. Narration first; the measured durations and sentence start times are the clock.
#    Use sentence_audio.py, NOT runtime/scripts/generate_audio_kokoro.py:
#    the usual script voices each beat in one pass and would drop the
#    0.35 s sentence pauses, B12's 1.5 s tail, and the sentence times
#    scenes.py uses for cue timing.
python3 youtube/brutalist/agent-proving-ground/sentence_audio.py

# 2. Review cut, then 4K master. ./art run needs the FULL path:
#    the bare slug "agent-proving-ground" fails (run.sh resolves it
#    from the current folder).
./art run youtube/brutalist/agent-proving-ground
./art final youtube/brutalist/agent-proving-ground   # -> renders/agent-proving-ground.mp4
```

- `beat_sheet.json` holds the final narration. `scenes.py` holds every visual.
- `./art run` skips any beat whose `manim/<BEAT>.mp4` already exists. To force a beat to re-render, delete its file first.
- To re-voice selected beats: `python3 youtube/brutalist/agent-proving-ground/sentence_audio.py --only B06 B07`.

## Part B: Prompt log

### Prompt 1: Read the format, check for show-tell, build the beat sheet

Sent with BEAT-PLAN.md attached.

> Context: I'm starting a new pitch film in this toolkit. First read CLAUDE.md, runtime/schema/beat_sheet.schema.json, and my Week 1 reel at youtube/brutalist/token-not-word/beat_sheet.json as a format example. Also check whether a show-tell skill exists in this checkout and, if it does, read it.
>
> Then create youtube/brutalist/agent-proving-ground/beat_sheet.json from the attached BEAT-PLAN.md:
>
> Use beat IDs B00–B11 exactly as in the plan.
> Copy the narration word for word. Do not rewrite it.
> Put each visual description in the schema's visual field.
> Validate the file against the schema and report any errors.
>
> Don't generate audio or render anything yet. Report back: whether show-tell exists, which render path it implies, and the validation result.

*Outcome:* show-tell does not exist. The schema has no `visual` field, so each visual went into `graphic.production_viz.mechanic`. The sheet validated with 0 errors.

### Prompt 2: Check ai-explainer; search the library; set Manim; first audio

> Next steps for agent-proving-ground:
>
> Read the ai-explainer SKILL.md and tell me in 3–4 lines what it requires for a Manim build. If it doesn't fit a pitch film, say so and stop.
> Run ./art scenes and report any existing scenes I could reuse.
> Set graphic.engine to Manim for every beat.
> Remove markdown marks (\*\*, \*, backticks) from the visual text. Keep the words the same.
> Re-validate against the schema.
> Generate the narration audio with Kokoro am_onyx, as in Week 1, and report each beat's measured duration and the total runtime.
>
> Don't write scenes or render yet.

*Outcome:* ai-explainer does not fit (see FRICTIONAL.md, ai-explainer), so the build stopped there.

### Prompt 3: Build like Week 1

> Agreed. Build it the same way as Week 1: plain Manim scenes, my narration as written, no Claude interface, no channel branding. Go ahead with the rest of the list (./art scenes, engine, strip markdown, re-validate, generate am_onyx audio, report durations and total). Don't write scenes or render yet.

### Prompt 4: Write the scenes, render the review cut

> Write youtube/brutalist/agent-proving-ground/scenes.py: plain Manim scenes, the same style as my Week 1 reel token-not-word/scenes.py. Rules:
>
> One scene per beat, B00–B11. Each scene's length comes from mp3/timings.json.
> Draw each beat's visual from graphic.production_viz.mechanic. You may use the layouts of AlgArtPipeline, CodingAgentsFig1Loop, and K12Fig05DiffVsTrack as references only. No Claude or brand styling, no logos, no channel name.
> Keep on-screen text minimal. The narration carries the explanation.
> B00, B02, B05, and B08 must show "Constructed — not built yet." on screen for the whole beat. Add B08 to the sheet's mock-up list too.
> Animate as the narration lands. No static slides.
>
> Then render the review cut with ./art run agent-proving-ground, pull one frame from the middle of every beat, look at each one, and report anything wrong. Don't run ./art final.

*Outcome:* `./art run agent-proving-ground` fails, because it resolves the name from the current folder, so the full path `youtube/brutalist/agent-proving-ground` was used. Rendering also required `FACTCHECK.md`, `SHOTLIST.md` and `PROMPTS.md`. Frame review caught a broken B04 merge and misaligned B11 headers, both fixed.

### Prompt 5: Narration changes after the review watch

> Narration changes for agent-proving-ground:
>
> Replace the narration of B04 and B10 with the text below, word for word.
> Add a new beat B12 with the narration below. Visual: the Sandbox → Trace → Check row from B01 draws back in, then "Thank you." fades in under it. No Constructed label is needed.
> In B10, change the on-screen label "what the roles ask for" to "what I want to build".
> Re-validate the sheet.
> Regenerate audio for B04, B10, and B12 only (--only), then report the new durations and total.
> Update the cue phrases in scenes.py for B04 and B10 to match the new wording, and write the B12 scene.
> Re-render the review cut. Check the middle and last frames of B04, B10, B11, and B12, and report. In B11, make sure "failure analysis" isn't too close to the bottom edge.
>
> Don't run ./art final.
>
> B04: Before planning this, I looked at two existing tools. E2B is a service that runs AI-generated code in sandboxes. Langfuse is a tool that records LLM traces and scores them. Each covers one piece. Mine will join sandbox, trace, and check into one small loop you run on your own machine, where pass or fail comes from tests run inside the sandbox, not from another model’s opinion.
>
> B10: I picked this project because it mixes skills I have with skills I want. In earlier projects I built agent workflows, an LLM evaluation harness, and cloud infrastructure with Docker and Terraform. Kubernetes, sandbox isolation, and trace design are new to me. I want to work on the infrastructure that AI agents run on, and building this is how I’ll learn it.
>
> B12: So that’s the pitch. An agent can say it’s done. Agent Proving Ground will show whether it really is. Thank you.

### Prompt 6: Sentence pauses

> Add a short pause after every sentence in the narration:
>
> For each beat, split the narration into sentences at . ? ! and generate each sentence separately with Kokoro am_onyx.
> Join the sentences with 0.35 s of silence between them (ffmpeg) into that beat's mp3. Don't add silence at the start or end of a beat, except for B12: pad its end with 1.5 s of silence so "Thank you." holds on screen.
> Keep the narration text in beat_sheet.json exactly as it is. Re-validate the sheet.
> Update timings.json and the sheet with the new durations, and record each sentence's start time per beat.
> In scenes.py, time the reveals from the real sentence start times where a cue begins a sentence, instead of estimating.
> Re-render the review cut and check the middle and last frames of every beat.
> Report: new duration per beat, total runtime, and anything that drifted.
>
> Don't run ./art final.

*Outcome:* `sentence_audio.py` was written for this step (see FRICTIONAL.md, sentence pauses).

### Prompt 7: B06 and B07 last sentences

> Two narration changes for agent-proving-ground:
>
> B06: replace the last sentence "It won't prove production scale, and I won't claim it." with "It’s built for one laptop, not for production traffic." Change the on-screen label "production scale" to "one laptop, not production".
> B07: replace the last sentence "Go and cloud deployment come later, as a side project." with "Go and cloud deployment can be added in the future."
> Re-validate the sheet.
> Re-voice only those two beats with python3 sentence_audio.py --only B06 B07.
> Update the cues in scenes.py for the changed sentences, re-render the review cut, and check the middle and last frames of B06 and B07.
> Report the new durations and total.

### Prompt 8: Fix both labels

> Fix both labels:
>
> B06: remove the red ✗ in front of "one laptop, not production". Use no mark at all.
> B07: change the bottom line "later — a side project" to "can be added later".
>
> Re-render only what's needed, check the last frames of B06 and B07, and report. Don't run ./art final.

### Prompt 9: Final master and every quality gate

> All checks are done. Run ./art final youtube/brutalist/agent-proving-ground, then run every quality gate the toolkit has, including render integrity. Report each gate's result and where its report file is saved. If any gate fails, stop and tell me. Don't work around it.

*Outcome:* the final succeeded. Gates 1–10 passed, and gate 11 stopped the run (see FRICTIONAL.md, gate 11).

### Prompt 10: Install matplotlib, re-run gates 11 and 12

> Yes, install matplotlib into the project's .venv (use ./setup --install if it covers it, otherwise pip install matplotlib inside the venv). Then re-run gate 11 and gate 12 and save their reports under \_qc/gates/. Report the results. If either still fails, stop and tell me. Don't change the film.

### Prompt 11: Smoke test against a scratch copy

> Don't edit anything in the toolkit or examples/. Instead, copy examples/\_smoke/ to a scratch folder outside the repo, change only the copy's slug to "smoke", and try running the smoke test against that copy. If the smoke script can't be pointed at another folder without editing it, stop and say so. Save the result as \_qc/gates/12_smoke_scratch.txt, and update SUMMARY.txt to show both runs.

*Outcome:* the smoke script can't be pointed elsewhere without editing it (see FRICTIONAL.md, gate 12).

### Prompt 12: Assemble this folder

> Assemble the submission folder at fall-2026/tushar-p/final-project-film/ in my course repo clone, the same way as Week 1. Draft every file from what's actually in the reel folder. Don't invent anything.

The rest of this prompt listed the contents of each file in this folder.

### Prompt 13: Future tense for B06 and B07; re-render, final master, gates 1–12

> Narration: change B06’s last sentence to “It will be built for one laptop, not for production traffic.” Change B07’s first sentence to “It will run locally, on kind, which is Kubernetes inside Docker, with one agent and tasks I write myself.” Re-validate the sheet.
> Audio and scenes: re-voice with python3 sentence_audio.py --only B06 B07. Update the cues in scenes.py, re-render, check the middle and last frames of B06 and B07, and confirm no late reveals.
> Final and gates: run ./art final youtube/brutalist/agent-proving-ground, then gates 1–12 again. Gate 12 is expected to fail for the same toolkit reason. If anything else fails, stop.
> Submission folder updates:
> Copy the new mp4 and the new gate reports, with paths shortened the same way.
> Update the SHA-256 and runtime in README.md.
> Copy the updated beat_sheet.json and scenes.py.
> BUILD-PROMPT.md: add this as a new prompt entry. Don’t edit the earlier entries, because they record what was actually asked.
> SOURCES.md: change “the printed > PASS line” to “an illustrative > PASS line”. Make the B05 table line say clearly that the rows are made up.
>
> Then report results and show the diff. Don’t commit.

*Outcome:* the final was re-exported (190.917 s). Gates 1–11 passed, and gate 12 failed for the same toolkit reason (see FRICTIONAL.md, gate 12).

### Prompt 14: Resubmission (Go harness, OmniSQL-Postgres in B10); re-render, final master, gates 1–12

> Resubmission changes for agent-proving-ground. The pitch is being resubmitted. Replace these narrations word for word:
>
> B02: When it’s done, it will be a public GitHub repository: a Go harness, ten to twenty synthetic coding tasks with automatic checks, saved traces of every run, an evaluation log, and a failure analysis.
> B06: It will show four skills from this course: a prompt contract for every task, an agent loop I write myself in Go with the Claude API, verification from deterministic checks, and evaluation I can repeat and compare across runs. It will be built for one laptop, not for production traffic.
> B07: It will run locally, on kind, which is Kubernetes inside Docker, with one agent and tasks I write myself. It will not be a hosted or multi-user service. Cloud deployment can be added in the future.
> B09: The real risk is learning Go and Kubernetes at the same time, so the evaluation never gets built. So I’ll build the harness and checks on plain Docker first, then move them onto kind by a fixed date. If I miss it, I’ll ship the Docker version and log why.
> B10: I picked this project because it mixes skills I have with skills I want. In OmniSQL-Postgres, a public project of mine, I fine-tuned a text-to-SQL model and built the evaluation that measured it. Execution accuracy went from 23 to 69 percent on a held-out test set of 200 questions. Its infrastructure uses Docker, Terraform, and AWS. Go, Kubernetes, sandbox isolation, and trace design are new to me. I want to work on the infrastructure that AI agents run on, and building this is how I’ll learn it.
>
> Visual changes:
>
> B02: the repo tree stays the same.
> B09: add a small “Go” label next to the Kubernetes wheel.
> B10:
> Have column: “LLM evaluation · Docker · Terraform · AWS”.
> Under it, show the real URL github.com/tushar-patel28/omnisql-postgres and “23% → 69% execution accuracy (200 held-out)”, with a small label “public repo, checked 2026-10-22”.
> New column: “Go · Kubernetes · sandbox isolation · trace design”.
> Make sure the URL is large enough to read on a laptop.
>
> Then:
>
> Re-validate the sheet. Re-voice only B02, B06, B07, B09, and B10 with python3 sentence_audio.py --only …, update the cues, re-render, check the middle and last frames of those five beats, and confirm no late reveals.
> Run ./art final youtube/brutalist/agent-proving-ground and gates 1–12. Gate 12 is expected to fail for the same toolkit reason. Stop on anything else.
> Update fall-2026/tushar-p/final-project-film/:
> Copy in the new mp4, beat_sheet.json, scenes.py, SHOTLIST.md, and the gate reports, with paths shortened as before.
> README.md: update the SHA-256 and runtime, change “my earlier projects” to “my public OmniSQL-Postgres project” in the tense line, and change “Python” to “Go” in any project description.
> SOURCES.md: add the OmniSQL repo and demo links, and the Anthropic Go SDK (github.com/anthropics/anthropic-sdk-go) as the planned SDK.
> FACTCHECK.md: add two claims, each marked for me to verify. First, the 23% → 69% figure, against the OmniSQL README. Second, that the official Go SDK exists.
> BUILD-PROMPT.md: add this as a new prompt entry.
> Show me the diff. Don’t commit.

*Outcome:* the final was re-exported (202.625 s). Kokoro read "AWS" as one word, so `sentence_audio.py` now voices it as "A-W-S"; the narration text and the screen keep "AWS". At a laptop-readable size the URL is about 10 units wide, too wide for one column, so B10's evidence sits in a full-width card under both columns, left-aligned under Have. Gates 1–11 passed, and gate 12 failed for the same toolkit reason (see FRICTIONAL.md, gate 12).

Follow-up the same day: B10's stat was changed to "23% base → 69% fine-tuned execution accuracy (200 held-out)", FACTCHECK.md C4 and its OmniSQL-Postgres wording were updated, and only B10 was re-rendered; the final was re-exported (202.625 s), gates 1–11 passed again, and gate 12 failed for the same toolkit reason.

### Prompt 15: B00 greeting, B01 opening line, B10 without the figure; re-render, final master, gates 1–12

> More resubmission changes for agent-proving-ground. Narration word for word:
>
> 1. B00 narration: "Hi, I'm Tushar. Have you ever wondered, when an AI coding agent tells you it's done, whether it really is? Today, the honest answer is often: check it yourself. My final project will do that check for you." Visual: show "Tushar Patel" briefly at the top during the first sentence, then continue as before.
>
> 2. B01: replace "I'm Tushar, and this is Agent Proving Ground." with "This is Agent Proving Ground." Keep the rest of B01 unchanged.
>
> 3. B10 narration: "I picked this project because it mixes skills I have with skills I want. I've already built LLM evaluation and cloud infrastructure with Docker, Terraform, and AWS, in a public project you can check on GitHub. Go, Kubernetes, sandbox isolation, and trace design are new to me. I want to work on the infrastructure that AI agents run on, and building this is how I'll learn it."
> B10 visual: keep the two columns (Have: LLM evaluation · Docker · Terraform · AWS / New: Go · Kubernetes · sandbox isolation · trace design). Remove the 23% → 69% stat. Under the Have column, in small but laptop-readable text: "Shown in my public project: OmniSQL-Postgres", the URL github.com/tushar-patel28/omnisql-postgres, and the label "public repo, checked 2026-10-22".
>
> 4. Re-validate the sheet. Re-voice B00, B01 and B10 with python3 sentence_audio.py --only (keep the AWS respelling). Update cues, re-render those three beats, check their middle and last frames, and confirm no late reveals.
>
> 5. Run ./art final youtube/brutalist/agent-proving-ground and gates 1–12. Gate 12 is expected to fail; stop on anything else.
>
> 6. Submission folder:
> - Copy in the new mp4, beat_sheet.json, scenes.py, SHOTLIST.md and gate reports, with paths shortened.
> - README.md: update the SHA-256, runtime and gate 10 figures.
> - FACTCHECK.md: the film no longer shows 23% → 69%, so mark C7 as "brief only, not in film" and change the intro line back to "No numbers from outside sources appear on screen." Copy it to the reel folder too.
> - SOURCES.md: in the OmniSQL row, remove the stat from the film description and note that the stat is in PROJECT-BRIEF.md only.
> - BUILD-PROMPT.md: add this as a new entry, Prompt 15.
>
> Show me the diff. Don't commit.

*Outcome:* the final was re-exported (194.542 s). At a laptop-readable size the URL (Menlo, about 7 units wide) is wider than the Have column, so the B10 block is left-aligned under Have and runs a little past the centre line; the divider stops above it. Gates 1–11 passed, and gate 12 failed for the same toolkit reason (see FRICTIONAL.md, gate 12).

Follow-up the same day: B00 now opens on "Tushar Patel" alone, centred, during "Hi, I'm Tushar."; the top rail, Constructed label, bubble and "agent" label arrive as "Have you ever wondered" starts, and the label stays to the end of B00. Only B00 was re-rendered; the final was re-exported (194.542 s), gates 1–11 passed again, and gate 12 failed for the same toolkit reason.

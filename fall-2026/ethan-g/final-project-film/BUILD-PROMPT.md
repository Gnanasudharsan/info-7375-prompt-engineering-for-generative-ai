# BUILD-PROMPT — how to rebuild this film

Everything is free and local: no API keys, no paid generation, no upload. The submitted film is version 3, built from
`film-v3/`.

## 1. Toolkit (one time)

```bash
git clone https://github.com/nikbearbrown/brutalist.art Brutalist     # built against commit 519fcbb
cd Brutalist
python3.11 -m venv .venv && source .venv/bin/activate              # macOS system python3 (3.9) lacks the deps
pip install -r requirements.txt                                     # Manim 0.20.x pinned
./setup --install                                                   # see FRICTIONAL.md: its ElevenLabs guard trips on
                                                                    # the toolkit's own youtube/ examples at 519fcbb
./art smoke                                                         # end-to-end proof that a video renders
```

Put this folder beside the toolkit (`Final_Project_Pitch/` next to `Brutalist/`), or set `ART_HOME` to the toolkit.

## 2. DataSentry's first pieces (from `Final_Project_Pitch/first-run/`), run before the film

```bash
./run_all.sh        # makes its own .venv, downloads NYC TLC Jan 2025, plants 2 defects, runs pandera + dbt + GX Core
                    # recorded output -> results/<date>/
```

Then the two Claude rounds (Claude desktop app, a new chat, no files):

1. Paste `claude-checks/PROMPT-round1.md` unchanged. Save the reply verbatim as `claude-checks/round1-reply-<date>.md`
   and its code block, unedited, as `claude-checks/round1_checks.py`.
2. `./score_round.sh 1` — plants the five defect types (seeds 25 and 99) on first use, scores the hand-written baseline
   and round 1, and prints which rules flag the clean copy (the only feedback allowed into round 2).
3. In the same chat, paste `claude-checks/PROMPT-round2.md` (written from step 2's clean-copy output). Save the reply
   as `round2-reply-<date>.md` and `round2_checks.py`.
4. `./score_round.sh 2`.

The film typesets `results/2026-10-25/`, chosen in `film-v3/embed_recorded.py` (`$RESULTS` overrides the newest dated folder).

## 3. Film (from `Final_Project_Pitch/film-v3/`)

```bash
source ../../Brutalist/.venv/bin/activate
T=../../Brutalist

python make_sheet.py                                         # beat_sheet.json from the narration + visual plan
python $T/runtime/scripts/generate_audio_kokoro.py .         # narration first: the measured mp3s are the clock
python finish_audio.py                                       # 0.8 s lead on BIDEA, 1.0 s tail on BEND; re-measure
./build_scenes.sh                                            # scenes.py = iso_kit + props + recorded output (embed_recorded.py) + scenes_body.py
cd $T && ./art run   ../Final_Project_Pitch/film-v3          # Gates F, L, A, W, B; 4K renders; review cut; Gate V
         ./art final ../Final_Project_Pitch/film-v3 --out ../Final_Project_Pitch/film-v3/exports   # Gate T + verified master
```

Subtitles (after `art final`, from `film-v3/`):

```bash
python $T/runtime/scripts/align.py .                 # word clock from the known narration
python make_captions.py                              # ../DataSentry_Pitch_EthanGomes.srt + .vtt, all words kept
python $T/runtime/scripts/srt_check.py . --srt datasentry-pitch-v3.srt
ffmpeg -i exports/datasentry-pitch-v3.mp4 -i ../DataSentry_Pitch_EthanGomes.srt -map 0:v -map 0:a -map 1:0 \
  -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=eng -disposition:s:0 default \
  -movflags +faststart ../DataSentry_Pitch_EthanGomes.mp4  # soft track; picture and sound are stream-copied
```

Re-voicing one beat: `generate_audio_kokoro.py . --only B07` then `python finish_audio.py`.
Re-rendering one scene: edit `scenes_body.py`, run `./build_scenes.sh` (the renderer reads `scenes.py`), move
`manim/<BID>.mp4` (and `media/videos/`) into `_superseded/`, then `./art run` again.

## 4. The prompts (Claude Code, model Opus 5.5)

The film was planned and built with Claude Code. My prompts, in order (lightly trimmed):

1. *"New Assignment using Brutalist. Read through all the assignment requirements and instructions first. Then tell me
   what needs to be done:"* followed by the full assignment text.
2. *"ignore the 5 day plan — all the steps need to be done in 1 day"*
3. *"suggest a few topics for me … I am looking for Data related full time roles like Data Engineer, Data Analyst and
   Business Intelligence roles. Provide a topic that is related to my full time job search. Also check if the topics
   suggested can answer all these questions for the 2–4 min film"* followed by the seven questions and the
   "Choosing a project" criteria.
4. *"I want to follow topic 2 [Data-Quality Test Generator, Scored on Planted Defects] — will it satisfy the 7
   questions? will you be able to make a 3:30 to 4 min video? does this topic satisfy all the criteria?"*
5. *"what is great expectations?"* · *"is the scope and size of this project satisfy the requirements?"*
6. *"for question 7 — this is something you already know how to do and want to show off. I think this will help me
   create relevant things to the job posting and data processing required by a particular company."*
7. *"go ahead and start generating a 3:30 to 4 min video on this topic in a new folder under the Prompt Engineering
   folder … name the new folder Final_Project_Pitch. Make sure to include visuals along with text … follow all the
   steps: brief, beat sheet, build, gates + honesty check + re-render, Frictional + assemble."*
8. *"Start the video by saying 'This is a Final Project Pitch Film Created by Ethan Gomes' and then say the project
   name and then continue with the rest"* (after the first master; the opener and B00 were re-voiced and re-rendered).
9. *"are there subtitles for the video? if not add subtitles for the video"*
10. *"[Q4 — What it proves — only partly answered: it doesn't say what a reviewer could fairly conclude.] Provide
    additional content and make changes to answer this question clearly in the video"*
11. *"Change the name to DataSentry. Also in 'Why this project' do not include 'Mostly to show off'; say that 'This
    project will help me land a Data job like a Data Engineer or a Data Analyst role.' Also change the visuals
    accordingly. Say that this project will highlight the skills I am working on like python, pandas and the rest …
    I do not want to give proof of the work done right now, so say that I am working on these skills."*
12. *"Instead of this [the typed 'Can Claude write checks I can measure' opener] write 'DataSentry' and below that
    write a short 1 line about the project which is being pitched"*
13. *"Put the Tick mark next to the 'tested, not trusted' not above it"*
14. *"Can you level the right lower side of the frame with the other side?"* then *"is it possible to make the right
    lower side shorter and under the top bar? Generate it and I'll let you know if I want to revert back to the original"*
15. *"revert back to the original"*
16. *"Can you change the lower left leg to go under top bar?"*
17. *"[Q2] Add this: 'it tells a data engineer which bad rows their checks would let through.'"*
18. *"Can you make sure the block is behind the bar and doesn't overlap it when the transition starts"*
19. *"so say for example before the nyc taxi trips data part"*

**Resubmission (2026-10-25), after the TA's feedback:**

20. *"for this assignment, i got this grade and feedback from the TA, i can resubmit … Read through this first and tell me
    what went wrong in this submission. Do not do anything on github, everything will be done locally"*
21. *"leave the frictional part out for now, i will look into it. make all the necessary changes for the rest"* — then my
    answers: Q7 reason = my DAMG 7370 project; I run the recorded command myself.
22. I ran `first-run/run_all.sh` in my own terminal (2026-10-25 06:16).
23. *"can you make a separate version for this film along with the current version"* — version 2 adds the TA's later
    guidance: who is doing it, a plain-language beat, and an "under the hood" technical walk-through.
24. *"so can i include ai written data checks to satisfy the 'Scoring AI-written data check' line?"*
25. *"in both the videos on the 1st intro page write 'Final Project Pitch Film created by Ethan Gomes' my name should
    be clearly visible in the video"*
26. *"instead of saying DAMG 7370 is it okay to say in a previous projects i have worked on? if so you can title it as
    'Food Inspections Dataset Project' and make the changes in both the videos"*
27. *"how do i resolve the 'i did not do the great expectations' thing? I do not want to show that i will do, i want to
    do the things so that i can say that i have done"*
28. *"[the evidence uses no AI yet] How can i resolve this issue while keeping the same topic?"* — Claude Code wrote the
    five-defect planter, the scorer and the round-1 prompt; I pasted the prompt into the Claude desktop app (Opus 5.5,
    effort High) and pasted the reply back.
29. I ran `./score_round.sh 1` in my own terminal, pasted the output, then pasted Claude's round-2 reply (to
    `PROMPT-round2.md`) and ran `./score_round.sh 2`. After the scorer was corrected, I re-ran
    `./score_round.sh 1 && ./score_round.sh 2` (2026-10-25 17:25).
30. *"How much time will it take to create a new version of the v2 with all the updates you need to make?"* then
    *"start making it but don't change anything in the original or v2"* — version 3 (`film-v3/`): the Claude rounds and
    the real scorecard.
31. *"remove the 'I'm Ethan Gomes and INFO 7375 student looking for data engineer ….'"*
32. *"for part 1 and part 2 write it as a title in the video in v3"*
33. *"just scan the captions if everything is correct in v3"* (all 78 cues matched the script)
34. *"i want to use v3 for the submission"*
35. *"i have watched the v3 film, it is correct"*
36. *"for P4, i found in that project that checks weren't efficient and fast enough to catch bad rows"* — then, choosing
    the "missed bad rows" reading: *"In my Food Inspections Dataset Project, my checks let bad rows through and I didn't
    know which ones until later. DataSentry measures exactly that: which bad rows a set of checks misses." Yes include
    this.* (B13 re-voiced and re-rendered.)
37. *"before that, you verify against the below if everything is satisfied"* followed by the full assignment text — then
    *"Make the changes to fulfil these gaps"*: B01 names the artifact (a public GitHub repo, when done), B11 says how you
    know it ran, B13 separates new skills from ones I already had, and PROJECT-BRIEF.md was cut to one page.

Claude Code's working rules for prompt 7 came from the toolkit's `CLAUDE.md` and `skills/make/show-tell/SKILL.md`,
overridden where the assignment says otherwise (narrate as yourself; no instructor name, persona, or credit line).

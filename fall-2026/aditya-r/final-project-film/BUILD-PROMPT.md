# BUILD-PROMPT — how this film was made

**Tool:** Claude Code (model Opus 5.5), in VS Code. **Date:** 2026-10-14 (one session). **Toolkit:**
brutalist.art, local clone at `main` `519fcbb96e9e1898d374c8794117cab494ffc5cb` (no toolkit source
changes for this film; see `TOOLKIT-CHANGES.md`). **Skill:** `show-tell`. Aditya chose it explicitly;
the toolkit lists it as "ADVANCED — Bear only", and this is not a claim of Bear's sign-off.

## The prompts Aditya gave (verbatim, in order)

Claude's replies are not reproduced. What came of each prompt is logged in `FRICTIONAL.md`.
The prompts are verbatim, except for one phrase removed from Prompt 4 at Aditya's request
(2026-10-14); the removal is marked `[…]`.

### Prompt 1 — brief
> I'm Aditya Raj. Help me make a 2–4 minute final project pitch film for my Prompt Engineering and Agentic AI class.
>
> The project is called DayThread: an AI check-in assistant that connects details across daily conversations and brings concerning changes to a home care coordinator for review. This is a proposed project, not a working application yet.
>
> I've opened my Brutalist workspace in VS Code. The toolkit is already cloned in brutalist.art. Use that copy; don't clone it again. Put this film's work in my-videos/youtube/daythread and leave my other videos alone.
>
> Read the toolkit's instructions and inspect its setup. You can use the show-tell skill to create the videos. Keep the film's content and assets outside the toolkit folder, and record any toolkit changes needed to rebuild it.
>
> Start FRICTIONAL.md immediately. It's worth 5 marks. Keep dated notes about actual attempts, decisions, changes, checks, and unresolved issues. Record what you contributed and what I accepted, changed, or rejected. Don't invent struggles or claim I checked something I haven't checked.
>
> The film must answer seven questions:
> 1. What is it, and what will I deliver?
> 2. Why would anyone care, and how does it differ from real alternatives I reviewed?
> 3. Who opens it, and what do they do in the first minute?
> 4. What course skills will it demonstrate, and what evidence will support them?
> 5. What's included, excluded, and the first thing I'll make run?
> 6. What specific failure could sink it, and how will I handle it?
> 7. Why did I choose it, and which skills are new versus already demonstrated?
>
> The grading is: what and who—7 points; unique value—5; skills and planned evidence—5; personal motivation and new versus existing skills—4; scope and honest risk—5; explanatory visuals and quality checks—4. Frictional is worth 5, matching GitHub and Canvas submissions are worth 5, and relative quality is worth 10. That totals 50.
>
> Use the free local pipeline.
>
> Start by asking the seven questions. I'll give you the content before we write or render the film.

### Prompt 2 — film decisions and the seven answers
> here is the answer to the film decisions that the toolkit forces :
> 1. yes, it should say "Liam, in for Aditya". The outro should have my name : Aditya Raj and my Github : https://github.com/aditya-raj-sde
>
> 2. i agree with showing no people at all and telling the story with objects: a phone, a thread of check-ins, the coordinator's review queue.
>
> 3. ok
>
> Here are my answers to the 7 questions. Help me tighten them without making the project sound more developed than it is.
>
> 1. What is it?
>
> DayThread is a proposed AI check-in assistant that remembers conversations across days and turns concerning changes into evidence a home care coordinator can review.
>
> I'll deliver a runnable repository with a text-based prototype, persistent memory, a review screen, tests, and an evaluation report. I'm proposing Python and SQLite initially, using fictional people and synthetic records.
>
> 2. Why would anyone care?
>
> I want to investigate whether a coordinator can understand changes across several check-ins without manually reconstructing the conversation history.
>
> Help me review Lifeline's fall-detection service and DailyCall's AI check-ins using their official descriptions:
> https://www.lifeline.com/medical-alert-systems/fall-detection/
> https://dailycall.care/ai-companion-for-elderly
>
> Automatic fall detection and AI calling already exist. My focus is connecting reports across days, tracing concerns to the original words, and giving a coordinator control over the proposed action.
>
> Don't claim competitors lack undocumented features, that I tested their products, or that DayThread has already saved time or improved care. Give me the relevant sources to read before saying I reviewed them.
>
> 3. Who opens it?
>
> My target role is AI Engineer.
>
> An engineering hiring reviewer should be able to open the README, run a clearly labeled replay, and inspect a two-day memory example and an approval decision within the first minute.
>
> The intended end user is a care coordinator. They see the concern, supporting conversation excerpts, and options to approve, refuse, or defer.
>
> 4. What does it prove?
>
> I want to demonstrate prompt contracts, an agent loop with a budget and clear stopping conditions, permissions enforced in code, source-linked memory, and evaluation.
>
> Tests and logs will show whether it retrieves earlier information, rejects unauthorized changes, and stops at its limits.
>
> I'll compare the workflow with and without memory, using development cases and separate held-out cases reserved before tuning. I'll include at least five deliberate failure cases and report failures and limitations.
>
> That can demonstrate a tested prototype, not readiness for real care.
>
> 5. What's in, out, and first?
>
> The core is simulated text check-ins, memory, evidence-linked concerns, and human review. Clinical advice, real patient data, and autonomous outreach are excluded. Voice calls and cloud deployment are extensions.
>
> First, one fictional client will complete two simulated days. On day two, the assistant should retrieve something from day one without the user repeating it. I'll save the transcript and source reference, and test that an unauthorized record change is rejected.
>
> 6. What could sink it?
>
> Someone could mention "just a little tumble," and the AI might omit it from the summary. Later steps relying on that summary would miss it.
>
> I'll predict and deliberately test this failure. A separate check of the original conversation will create an internal review item. A coordinator must approve any outbound action, based on the exact evidence and action they reviewed.
>
> The checker could miss unfamiliar language or raise false alarms, so I'll test those too. In the film, show this as a constructed example of the planned workflow, not an observed model failure.
>
> 7. Why this project?
>
> I chose DayThread because I want to explore what makes an AI system useful beyond a single conversation. Remembering something from yesterday is one part of the problem. Knowing when that information needs a person's attention, and showing them the evidence, is the part I find interesting.
>
> This is mainly a learning project. I want to understand how to build an agent that remembers information, uses tools within clear limits, and produces results I can actually check.
>
> One skill I'm already practicing is refining prompts and reviewing AI-generated work. During this project's planning, I asked for clearer instructions, rejected wording that didn't sound like me, and made sure we started tracking our decisions from the beginning. AI helped draft the material; my contribution has been setting requirements, requesting revisions, and deciding what represents my project.
>
> The new skills I want to develop are persistent memory across conversations, permissions enforced in code, human approval tied to the evidence shown, and evaluation using cases kept separate from development.
>
> By the end, I want to be able to explain why the system made a decision, what stopped it from taking an unauthorized action, and where it still fails.
>
> Ask if anything is missing. Don't invent personal experience.
>
> Now write a natural first-person script, initially around 400–450 words, aiming for about three and a half minutes. Cover all seven answers without sounding like a questionnaire.
>
> Use the two-day memory example and the missed "little tumble" as the main story. Give each beat one simple visual. Label imagined screens and conversations "Constructed — proposed workflow."
>
> End with a clear distinction between what exists today and what I intend to build. Show me the script and visual plan before rendering.

### Prompt 3 — revisions, design decisions, and the 15-second preview
> Let's revise this draft and make a small preview first. Don't render the full film yet.
>
> I accept the more cautious competitor comparison. Describe those three features as DayThread's proposed focus, not features we've proved competitors lack. Keep the practical benefit clear: helping a coordinator understand changes without reconstructing several conversations manually. That's an intended benefit, not a measured result.
>
> Don't mark the four product pages as read by me until I confirm. Keep their links available for me.
>
> Cut the script to roughly 450–500 words while preserving all seven answers. There's no need to reach exactly 3.5 minutes. Aim for a comfortable film within the assignment's 2–4 minutes, and measure the actual audio before deciding the final timing.
>
> Replace "Hallo. This is Liam, in for Aditya" with "Hi, I'm Aditya Raj. This is DayThread, my proposed final project." If we use Kokoro, clearly disclose that it's a synthesized voice reading my script. Don't adopt the toolkit's narrator persona.
>
> Change "It's built to show" to "I'm designing it to demonstrate." Replace "At best" with "These tests could demonstrate a controlled prototype, but wouldn't establish readiness for real care." Say "no DayThread prototype or evaluation results yet" rather than "no code," since we'll have code for the film itself.
>
> Here are my design decisions:
>
> The assistant can read check-in history, add source-linked observations, and create internal review items.
>
> It cannot silently overwrite past records, change agency-owned information, or contact anyone.
>
> A separate executor would carry out an approved action after checking that the approval still matches the evidence and proposed action. For the course, delivery would be simulated locally.
>
> The proposed review screen will be a simple local web page showing excerpts and approve/refuse/defer options. We're only illustrating it for this film, not building the application now.
>
> Keep the raw transcript available independently of the summary. Show the separate check running when the check-in ends; don't suggest it waits until day two. Day two demonstrates memory.
>
> For my existing skills, use only decisions and revisions supported by this fresh session's actual log. Don't reconstruct deleted history or mention Week 1 unless you have evidence for the particular claim. Credit the drafting and review assistance honestly.
>
> Ask me to confirm the "new skills" list before finalizing that sentence. Don't assume my technical background. You can work on the preview while that's pending.
>
> Keep the key-terms card and "Your Turn" section out. Remove the GitHub address from the outro until I confirm it. My name and DayThread are enough.
>
> I approve a small optional name/handle setting for the outro if necessary. Preserve existing defaults for other projects, record the change and rebuild instructions, and don't alter my other videos.
>
> Use show-tell for this film. Read its full instructions and use its drawing kit where appropriate. Shared ai-explainer machinery underneath is fine. This is my explicit local workflow choice, not a claim of personal approval from Professor Bear. Apply the assignment's identity requirements over conflicting template defaults and document those exceptions.
>
> Now make ONLY a 15-second preview using the toolkit's normal 4K settings: 3840×2160. Keep its default frame rate and rendering workflow. Don't change the resolution settings or build a separate low-resolution pipeline.
>
> Render only these three short beats, not the full film:
>
> The original check-in includes "a little tumble."
>
> The summary misses it, but the separate check highlights the original words.
>
> The evidence reaches the coordinator's review gate. Nothing is sent.
>
> Use this narration, shortening it if needed to fit naturally:
> "A check-in mentions a tumble. The summary misses it. DayThread's proposed check reads the original words and brings them to a coordinator before anything is sent."
>
> Keep "Constructed — proposed workflow" readable throughout. No opening, outro, mascot, or name-pronunciation test in this preview. Reuse suitable existing assets and cached renders.
>
> Check the preview's actual duration, resolution, sound, and layout. Save the real check results, and record in FRICTIONAL.md that I chose a shorter preview while retaining the toolkit's native 4K configuration.
>
> Give me the 15-second preview and stop for my review. Don't render the full film, package it as final, or upload anything yet.

### Prompt 4 — full film and submission package
> I've reviewed the 15-second preview and approve it. The visual style and pacing work for me. I also approve changing the final line to "It brings them to a coordinator before anything is sent."
>
> Go ahead and finish the full DayThread pitch film using that style and the toolkit's normal 4K settings. Keep the existing 24 fps workflow. Don't change the rendering configuration.
>
> My GitHub is:
> https://github.com/aditya-raj-sde
>
> You can include that in the outro with DayThread and Aditya Raj. This is my profile link, not the final assignment-folder link.
>
> I've now read all four source pages: Lifeline fall detection, DailyCall AI companion, DailyCall daily check-in calls, and DailyCall safety policy. Update SOURCES.md and the Frictional log with my confirmation and today's actual date. Describe this as reading their documentation, not testing their products.
>
> Keep the revised script around its current length. Measure the actual narration and keep the finished film within 2–4 minutes. Don't pad every scene to five seconds—the preview's timing was just for that sample. Let the narration and visual explanation determine the pacing.
>
> Keep the constructed-workflow labels and the synthesized-voice disclosure readable. Separate captions from scene headings, and make the review gate visibly closed until approval. No instructor identity, channel credits, or unrelated mascot.
>
> Apply the previously approved optional name/handle change only if needed for the outro, and document it for rebuilding. Preserve my other videos and their settings.
>
> Render the entire film, then run the toolkit's applicable quality gates on that final render. Fix failures and repeat affected checks. Inspect frames throughout the film and transitions. Verify duration, resolution, audio continuity, captions, and that every assignment question is answered.
>
> Report automated checks separately from human viewing or listening. My preview approval is not approval of the finished film.
>
> Complete the submission materials:
> - README.md with my name, project title, target role, measured runtime, and exact rebuild instructions.
> - The final MP4.
> - A one-page PROJECT-BRIEF.md answering all seven questions and ending with "exists today" and "will exist."
> - beat_sheet.json.
> - BUILD-PROMPT.md with the actual prompts, commands, and toolkit revision.
> - SOURCES.md with source links, licenses, and accurate attribution to me, Claude[…].
> - Actual final-render gate reports.
> - FRICTIONAL.md with the real decisions, attempts, fixes, and unresolved issues.
> - Source assets and any documented toolkit changes needed to rebuild.
>
> Prepare Raj_Aditya_INFO7375_FinalProjectFilm.zip and the matching folder structure fall-2026/aditya-r/final-project-film/. Extract the archive into a separate location and verify that the correct final film and required materials are present.
>
> Exclude caches, credentials, private conversations, and unrelated projects. Flag any MP4 repository-size issue instead of silently omitting it.
>
> Don't upload or submit anything yet. When finished, give me:
> 1. The full film to watch.
> 2. The completed ZIP.
> 3. A concise rubric and submission check, with any unresolved items.
> 4. The remaining steps for posting the matching GitHub version and submitting its actual folder link and final commit hash on Canvas.
>
> Continue through rendering, checks, fixes, and packaging rather than stopping after a plan. Leave the final film approval and submission to me.

### Prompt 5 — GitHub posting
> Let's finish and push my DayThread pitch submission to:
> https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai
>
> Use fall-2026/aditya-r/final-project-film/, alongside my Week 1 folder. Don't change other assignments.
>
> Push the required documents, beat sheet, rebuild source, evidence, and gate reports. Respect the repo's media exclusions: don't force-add MP4 or MP3 files or change its ignore rules.
>
> Keep the finished film and required audio in Raj_Aditya_INFO7375_FinalProjectFilm.zip for Canvas. In the README, state that the film is in the Canvas ZIP and include its filename and SHA-256 checksum. Verify that the shared files match between GitHub and the ZIP, with the media difference clearly documented.
>
> You're authorized to commit and push once those items are resolved. Follow the course repo's workflow, using a pull request if required. Don't force-push, include unrelated files, or upload the ZIP to GitHub.
>
> After verifying the remote submission, give me the final ZIP location and ready-to-paste Canvas text with the assignment-folder link, full commit hash, and PR link and status if applicable. I'll submit the ZIP to Canvas myself.

During this prompt, Claude asked how to handle the repo's no-full-names rule. Aditya chose
"Keep 'Aditya Raj'" (see `FRICTIONAL.md`, 17:35 entry).

### Prompts 6–8 — attribution correction and log answers (summarized)
Aditya asked about one attribution line in `SOURCES.md` and had it removed. Aditya confirmed that
no AI tool other than Claude was used, and asked for the change to be pushed with a new ZIP. Aditya
then answered Claude's questions for the log. Those answers are quoted in `FRICTIONAL.md`.

## Commands actually used for the film (in order)

Environment, every command:
`eval "$(/usr/libexec/path_helper)" && export PATH="/opt/anaconda3/envs/brutalist-daythread/bin:/opt/homebrew/bin:$PATH"`

```bash
cd ~/Desktop/Brutalist/brutalist.art && ./setup                                   # all 7 features ready, $0.00
cd ~/Desktop/Brutalist/my-videos/youtube/daythread/film
python make_sheet.py                                                              # narration from ../SCRIPT.md
python ../../../../brutalist.art/runtime/scripts/generate_audio_kokoro.py .       # Kokoro am_onyx, all beats
python ../../../../brutalist.art/runtime/scripts/generate_audio_kokoro.py . --only B09 BOUT   # after the 2 rewordings
python audio_post.py                                                              # BOUT +1.0 s, measure, word cues
python assemble_scenes.py                                                         # kit + 11 props + scenes_body.py → scenes.py
# pre-audits (scratch copy holding only scenes.py, as Gate A sees it)
python ../../../../brutalist.art/runtime/qc/static_scene_check.py scenes.py --class <Scene>
python ../../../../brutalist.art/runtime/qc/manim_layout_audit.py scenes.py --class <Scene> --curve-strict
cd ~/Desktop/Brutalist
./brutalist.art/art run   my-videos/youtube/daythread/film --height 2160          # Gates F, L, A, W, B, V + review cut
./brutalist.art/art final my-videos/youtube/daythread/film --height 2160 --out my-videos/youtube/daythread/film/exports   # GATE T + verified master
python brutalist.art/runtime/scripts/bookend_check.py my-videos/youtube/daythread/film   # outro rule fails by design (see SCRIPT.md)
```
Each render-fix-rerun cycle is recorded in `FRICTIONAL.md`. The exact final-run logs are in `gate-reports/`.

## Commands used to package and post
```bash
cd ~/Desktop/Brutalist/my-videos/youtube/daythread && python3 package.py   # folder + Canvas ZIP + MANIFEST.json
git clone --filter=blob:none --sparse https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai.git <clone>
cd <clone> && git sparse-checkout set fall-2026/aditya-r prerequisites scripts .github
rsync -a <package>/fall-2026/aditya-r/final-project-film/ fall-2026/aditya-r/final-project-film/
git add fall-2026/aditya-r/final-project-film      # no -f: the repo's .gitignore keeps *.mp3/*.mp4 out
git commit && git push origin main                 # fast-forward, never forced
```

## Resubmission (2026-10-25)

**Tool:** Claude Code (model Opus 5.5), in VS Code, one session.

### Aditya's prompts (summarized; key instructions quoted)

1. **Check the submission and address the TA's feedback.** Aditya shared the assignment PDF, then
   the TA's comment, and asked Claude to inspect the project and explain what the requested replay
   means. Quoted instructions:
   - "Do not simply generate a polished retrospective or invent experiences in my voice."
   - "STOP after recording the prediction … Wait for my response before executing the replay."
2. **Setup.** Use Claude through the existing authenticated CLI ("Do not use Ollama, Llama, Gemma,
   or any other local model"; no separate billing; don't bypass nested-session restrictions).
   Claude was to draft a fictional fixture, show an AI-assisted hypothesis for Aditya to replace in
   Aditya's own words, and fix the criteria before running.
3. **Prediction and run.** Aditya gave a prediction (verbatim in `replay/PRE-RUN.md` §1), adopted
   the fixture with corrections to the evaluation notes, refined the criteria, and asked for 30
   isolated calls with every output, error and retry kept: "Do not change prompts or inputs
   mid-experiment to obtain the predicted result."
4. **Review and finish.** Aditya gave a review (quoted in the 14:59 entry of `FRICTIONAL.md`;
   stored in `replay/runs/20261025T135900/aditya_review.json`). Aditya asked for the documents to be
   finalized, the minimum film corrections with a rebuild and gates, and the ZIP: "Do not add
   experiments … Do not commit, push, or submit."

### Commands (in order)

```bash
# CLI check (non-experimental)
claude --version; claude auth status
claude -p --safe-mode --tools "" --no-session-persistence --output-format json \
  --model claude-opus-5 --effort medium --system-prompt "Reply with exactly the word OK and nothing else." "ping"
# replay
cd replay
python3 -B replay.py --trials 5                       # runs/20261025T135900, 30/30 calls
python3 -B flags.py runs/20261025T135900
python3 -B make_review_sheet.py runs/20261025T135900  # rerun after aditya_review.json was added
# Haiku diagnosis: one call on neutral text with --debug-file (see replay/preflight/HAIKU-TITLE-CALL.md)

# film v4 (reel folder; env as above)
python make_sheet.py
rm -f mp3/raw/beat-B04.mp3 mp3/raw/beat-B15.mp3
python ../../../../brutalist.art/runtime/scripts/generate_audio_kokoro.py . --only B04 B15
python audio_post.py
python assemble_scenes.py
mv manim/B04.mp4 manim/B15.mp4 _superseded/2026-10-25-rerender/
cd ~/Desktop/Brutalist
./brutalist.art/art run   my-videos/youtube/daythread/film --height 2160
./brutalist.art/art final my-videos/youtube/daythread/film --height 2160 --out my-videos/youtube/daythread/film/exports
#   GATE T failed on B04 twice; scenes_body.py fixed; B04 removed from manim/ and both commands rerun
cd my-videos/youtube/daythread/film && python final_checks.py
```

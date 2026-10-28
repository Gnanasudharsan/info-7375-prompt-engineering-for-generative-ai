# BUILD-PROMPT — rebuild this film

Everything is free and local, with no keys. The prompts used are listed first, then the commands.

## Prompts given to Claude Code (2026-10-13, from the brutalist.art folder)
1. "i need to generate a demo pitch video using ai-explainer skill in this repo. this is the project details, dont start video generation until i confirm." [project plan pasted]
2. The full assignment text was pasted, followed by the deliverables list.
3. "today i have only plan for the project, nothing is build yet… use kokoro voice not my own voice, my main goal is ai sde"
4. "create a folder as suggested in the deliverable inside brutalist folder next to brutalist.art folder. leave the github repo part. no citation yet, the draft is good start generating…"

## Revision prompts (2026-10-14)
5. "dont make the video sound like what i am explaining claude, i need video as a pitch of project for a recruiter to see about the project idea"
6. "Have you considerd the facts about honestly rule, I think the pitch flow is not natural…" [honesty rule pasted]
7. "…AI should be able to fix or rename all the lines in frontend automatically and raise PR's with backend as reference" (scope change, logged in FRICTIONAL.md)
8. "drop namaskara and regenerate the video" · "say as api impact" (outro)
9. "the in and out slide explanation is not understandable, make it smooth and check if video explains all of these questions" [seven questions pasted], then "approve"

## Resubmission prompts (2026-10-25)
10. TA comment pasted: "make sure the pitch video contains who is doing it, explains what you are doing easily to a 5 year old or a non-technical person clearly and make sure it is concise…", then "it's from the TA, make both changes" (a plain-language street-renaming comparison in B01; repeated "human merges" lines trimmed from B08 and B11). B03, B06 and B09 were tightened to stay under 4:00, and B12 now says some of the Angular work is on GitHub. Audio regenerated with `--only` for those beats.
11. "in second beat it AI software voice, its not AI, it A I": the voice read "A I" as "uh eye" and "O-A-S diff" as "oh-uh-ess diff". Narration now writes "AI" (B00, B12) and "OAS diff" (B03, B06, B12), which Kokoro reads as letters.

## Paste-ready rebuild prompt
> In `brutalist.art`, using the `ai-explainer` skill, rebuild the reel at `../fall-2026/chethan-t/final-project-film`.
> - Keep `beat_sheet.json` as the source of truth: Kokoro `am_michael`, no Liam persona, no `@NikBearBrown`.
> - Check out brutalist.art @ `29ba0e8` first (the version this film was built with).
> - Copy the film's custom scenes from the reel's `scenes/ApiImpactPitch.tsx` into `runtime/remotion/src/`, and apply `scenes/Root.tsx.patch` to register their compositions in `Root.tsx`.
> - Regenerate audio, run `./art run` at 1080, then read the `_qc/` contact sheet and frames. Fix any BLOCKER or MAJOR defect in scene source and re-run.
> - Then run `./art final <reel> --out <reel>`. Never publish.

## Commands
```bash
cd brutalist.art
git checkout 29ba0e8                           # pin the toolkit; Root.tsx.patch doesn't apply to later versions
source .venv/bin/activate                      # Python 3.12 venv (not Anaconda)
REEL=../fall-2026/chethan-t/final-project-film

# 0. scenes: the film's custom Remotion compositions
#    ship in this folder; install them into the toolkit (patch made against brutalist.art @ 29ba0e8)
cp $REEL/scenes/ApiImpactPitch.tsx runtime/remotion/src/
git apply $REEL/scenes/Root.tsx.patch     # registers the 13 Aip* compositions (folder "ApiImpactPitch")

# 1. audio first: the durations become the clock
python3 runtime/scripts/generate_audio_kokoro.py $REEL

# 2. each beat's durationSeconds prop must equal its actual_duration_s (one-liner)
python3 -c "import json,sys;p=sys.argv[1]+'/beat_sheet.json';s=json.load(open(p));[b['shot']['remotion']['props'].__setitem__('durationSeconds',b['actual_duration_s']) for b in s['beats']];json.dump(s,open(p,'w'),indent=2,ensure_ascii=False)" $REEL

# 3. review cut + gates (L, F, V); force a re-render of scenes with: rm -rf $REEL/media
./art run $REEL --height 1080

# 4. clean master (4K)
./art final $REEL --out $REEL      # without --out it lands in brutalist.art/renders/
```

## Evidence re-run (B04 numbers)
```bash
git clone --depth 1 https://github.com/gothinkster/angular-realworld-example-app ng
cd ng && git checkout dd99ed2   # if available; the film used the 2026-10-13 HEAD = dd99ed2
grep -rnw --include=*.ts --include=*.html username src | wc -l          # 171
grep -rlw --include=*.ts --include=*.html username src | wc -l          # 23
grep -rnw --include=*.spec.ts username src | wc -l                      # 124
```

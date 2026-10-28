# Frictional — DryRun pitch film

Pavithra Prasad · INFO 7375 · Final Project Pitch Film (resubmission)

Prompts: `BUILD-PROMPT.md`, section 3 · Evidence: `evidence/` · Gate reports: `reports/`

Commits in the course repo (`fall-2026/pavithra-p/final-project-film/`): `9f0c632` first posting (2026-10-13) · `33a9278` README credits (2026-10-13, the hash for the first grade) · `f3d68d5` resubmission (2026-10-24, the v5 files) · final commit: the hash given in the Canvas submission (it only adds this line)

My key prompts, quoted short: "go with 3" (the voice) · "score it properly" (v4) · "can you try to remove that [small orange circle]" · "need 49+, no best-of-two … ask before any commit or push" (resubmission) · "add a picture to B14 and B15 the same safe way"

## 2026-10-10 — Choosing the project

- Compared project ideas against the rubric and existing tools, and chose DryRun: test an AI's terminal command on a throwaway copy before it touches real files.

## 2026-10-11 — A real example and the first cuts

- Closest tools: `try` previews a command's file changes (Linux only); InterCode and NL2SH score AI shell commands offline. DryRun will also compare the changes with the request and the AI's own prediction.
- I asked Claude (claude.ai) for a command to delete `.log` files older than 7 days. It gave `find logs -type f -name "*.log" -mtime +7 -delete` and said to preview it without `-delete`. I used this real reply instead of a made-up example (`evidence/claude-reply-2026-10-11.png`).
- v1–v3 built with the free local pipeline (toolkit, Kokoro voice, Manim). A ChatGPT review of the script was checked point by point: real fixes kept, three factual errors rejected. All gates passed (v3, 3:33).

## 2026-10-13 — Testing the preview myself

- **Tried:** ran the preview in my own Terminal on files 6.5, 7.5 and 8.5 days old.
- **Expected:** the 7.5-day and 8.5-day files, since both are older than 7 days.
- **What happened:** only `logs/eight-and-a-half-days.log` came back (`evidence/mtime-test.md`).
- **What I learned:** I understood why checking whether a command runs successfully is not enough. The important part is verifying whether its actual changes match the user's request.

## 2026-10-13 — Final cut (v4)

- After a rubric check ("score it properly"), one narration line was added for each gap. Expected to stay under 4:00; it came to 3:53.
- A ChatGPT review was checked: the audio went up to −19 LUFS, but its −16 target was rejected because it fails the toolkit's −18 ceiling.
- Orange accents removed at my request. All gates passed. Posted as `9f0c632` and `33a9278`.
- **What I would do differently:** I would define the expected results and test cases before creating the storyboard, so the film is built around something I can verify.

## 2026-10-21 — Feedback: 47/50

- The TA's main deductions were "P6 Shown, not asserted 3/4 (-1); Frictional 4/5 (-1)", with a next step for Update 1 (see the end of this log).
- **Friction:** the evidence was in the repository, but on screen most beats were short phrases on a plain background, so the film said things instead of showing them. ChatGPT had flagged the text-heavy beats before the deadline, but that point was set aside as polish on Claude Code's advice. I decided to fix it in a resubmission.
- For Frictional, this log had no commit hashes and no human and AI contributions section.

## 2026-10-23 — Resubmission (v5)

- **Tried:** show the real evidence on screen instead of describing it, without changing a word of the narration. **Expected:** every quality gate passes and the film stays 3:53.
- B02 now shows the real Claude screenshot, B03 my own Terminal lines from 13 Oct (v4's label wrongly said 11 Oct, the day Claude Code ran it), and B19 the real test output from my PR #33, re-run at commit `c0a7693` ("Ran 32 tests in 0.775s … OK", `evidence/pr33-tests-2026-10-23.md`). Six text-only beats got a simple picture each, with every label kept.
- **Unexpected:** the toolkit's contrast check failed on the Claude screenshot. It read the dark chat bubble as dark text on a dark background. **Response:** the original screenshot was not edited. The way it is shown was changed, and the toolkit's documented check for real images was used, which tests each piece of text on its own. It passed.

## 2026-10-24 — Final check

- I asked for pictures in B14 and B15 as well, so B11, B14 and B15 each got one. Only the title cards are still text.
- All gates pass, the runtime is still 232.9 s and the narration is byte-identical to v4. Every v4 label is still on screen, except three lines that were replaced by the real evidence they described (in B02 and B03). Film SHA-256 `1b69f5f1…` (full value in the README).
- A ChatGPT review of the draft (48/50) was checked against the files. Accepted: separate 23 and 24 Oct entries, clearer wording in `SOURCES.md`, and filling the placeholders. Partly accepted: the sharpness gate was also run on the delivered film (22/22 pass).

## Human and AI contributions

- **I did:** chose the project, got the real Claude reply, ran the preview test myself, picked the voice, gave the visual references for B04 and B13, decided to resubmit and set its rules (narration unchanged, nothing posted without my OK), and brought the ChatGPT reviews and approved what was kept.
- **Claude Code contributed:** drafted the narration and the brief from my reasons, wrote the animations and paperwork, ran every quality gate, ran the first preview test, re-ran the PR #33 tests, checked each outside review against the files, and organised these entries from my decisions. My reflection lines are my own words.
- **Accepted:** DryRun, the narration, the louder audio, and the v5 evidence and pictures.
- **Changed:** the B04 picture (redrawn from my reference) and the props (orange removed).
- **Rejected:** ChatGPT's −16 LUFS target, three factual errors in the script review, and changing the narration for the resubmission.

## Still unresolved

- My `-mtime +7` test ran on macOS, but DryRun will first target Linux. The DryRun tool itself has not been built yet.
- **Next step** (the TA's, for Update 1, due 2026-11-05; it matches what I said I would do differently): build the `dryrun run` self-test first, with the planted file changes and their expected diff written before the runner.

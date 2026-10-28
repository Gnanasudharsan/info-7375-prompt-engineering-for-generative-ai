# FRICTIONAL — dated log

## My entries (in my own words)

<!-- Chethan: add your own dated entries here, newest first. -->

### 2026-10-25
i knew the results would come back but i had no solid evidence for it so i run the oasdiff myself got the evidence and then uploaded eviecne for video making flow

### 2026-10-14
because just reporting  break was not enough, i wanted somthing which fixed the issue, because its mostly reduntant work and small changes which had to be done in many places

### 2026-10-13
The idea for this project came because of my probelm i faced in as a frontend developer when i was working, when backed people changed a API but forgot to inform and the frontend broke.

---

## Claude-drafted summary (2026-10-13 to 2026-10-14)

Claude wrote the entries below from my session. The decisions are mine, but the wording is Claude's. My own entries are above.

### 2026-10-13
- **Picked the project and the tool.** Project: API Impact. I chose the toolkit's `ai-explainer` skill. The assignment suggests `show-tell`, but this checkout of brutalist.art doesn't include it.
- **The skill's defaults clash with the assignment.**
  - `ai-explainer` narrates as "Liam, in for Bear," puts `@NikBearBrown` on the footer chip and corner logo, and its outro card (`ClaudeTitleOutro`) hardcodes `@NikBearBrown` with no override.
  - The assignment says to narrate as yourself, without the instructor's name, persona or credit line.
  - What I did instead: no persona, the folder chip and corner wordmark read "Chethan Gowda," and the outro is a small custom card (`AipTitleOutro`).
  - I also chose the Kokoro voice `am_michael` instead of the default `am_onyx`, so the film doesn't sound like the instructor's channel.
- **The opening can't show a made-up Claude answer.** The cold open normally shows Claude "answering." The honesty rule says any Claude response shown must be real and dated, so the opening shows the real first lines of my 2026-10-13 message and three verbatim lines from Claude's actual reply.
- **Dropped Specmatic from the comparison.** My plan listed oasdiff, Optic and Specmatic. Claude flagged that it hadn't checked Specmatic, and the assignment asks for alternatives "you actually looked at," so the film names only oasdiff and Optic.
- **Added one real measurement.** Instead of a made-up "grep is noisy" claim, Claude Code cloned the public angular-realworld-example-app (commit dd99ed2) and ran a whole-word grep for `username`: 171 matches, 23 files, 124 in test files. The film's real call chain (service → component → template) comes from the same commit, with line numbers checked.
- **The first narration was too long: 4:08,** against a cap of 2–4 minutes. I cut seven beats to bring it to 3:52.
- **The hesitant-writer opening beat typed too slowly.** At 90% of its 9.9 s window the sentence wasn't finished. I shortened the on-screen text to "…which specs break." → "…which frontend lines break." and sped up the typing.
- **First preview frames failed my own review.** The B04 samples faded in too late, the B05 connector rail overran its cards, the B07 strike-through hit the filename instead of the code, and the B08 file paths were cut off before their line numbers. I fixed all four in the scene source and re-rendered the stills before the full build.
- **Remotion prints a version-mismatch warning** (`@remotion/paths` vs 4.0.490) on every render. Renders still complete, so I left it alone and noted it here.
- **First review cut: Gate V passed (0 BLOCKER, 0 MAJOR), but my own frame check found three late reveals.**
  - Sampling every beat at 85% showed the last reveal hadn't appeared yet in B06 (stage 5), B09 (the "agent loops — not claimed" chip) and B12 (the frontend → backend line). The gate can't catch this, because a frame with a missing element still fills the canvas.
  - I moved those reveals earlier, re-rendered only those three beats, and re-checked. Gate V was clean again.
- **The skin lint warns that the outro isn't `ClaudeTitleOutro`.** That's expected and deliberate (see the persona override above), so I left it as is.
- **`./art final` wrote the master to the toolkit's `renders/` folder, not the reel folder.** I moved `api-impact-pitch.mp4` and its `verified.json` here, then ran Gate V on the 4K master itself: 0 BLOCKER, 0 MAJOR.

### 2026-10-14
- **I asked for the opening to start straight into the idea, without calling the film a pitch.**
  - The B00 line "This is a pitch, not a build: nothing here runs yet" became "I'm Chethan, and this is API Impact." The B01 banner "PITCH · NOTHING BUILT YET" was removed, and the composer title "API Impact — The Pitch" became "API Impact."
  - Honesty still holds: every tool behavior is "will," B01 still shows Exists today / Will exist, and B06–B11 keep their PLANNED and CONSTRUCTED labels.
  - I re-rendered B00 and B01, and Gate V was clean on both the review cut and the new 4K master. Runtime is now 3:51.
- **Later the same day, I asked that the film not sound like I'm explaining things to Claude.** It's a pitch for a recruiter.
  - The Claude-composer cold open (with the real 2026-10-13 exchange) was replaced by a title card: API Impact, the one-line idea, my name, target role (AI Software Development Engineer) and status (Planned).
  - The "Your turn, paste this into Claude" handoff was cut.
  - Claude now appears only as a planned part of the tool (pipeline stage 3, the verifier).
  - The toolkit's skin lint flags the non-standard cold open and outro. That's intended.
  - I re-rendered B00, and Gate V was clean on the review cut and on the 4K master. Runtime is now 3:33.
- **I said the flow sounded mechanical, as if built to match the requirements.** Claude agreed and found three honesty slips:
  - Planned tool behavior was narrated in present tense ("oasdiff finds…", "a test proves it").
  - "I looked at oasdiff and Optic": I know they exist but haven't used them.
  - "I ran a search": Claude Code ran it in my session.

  The script was rewritten problem-first. It opens on the rename that blanks a page, every tool behavior is "will," the alternatives are "tools like," and the search is "a plain search… returns."
- **Scope change.** I decided the tool should not only report but also fix: open draft fix PRs in each frontend repo, with the backend PR as the reference. Guardrails I accepted:
  - only confirmed lines get edited
  - fixes must pass the frontend's tsc and tests
  - PRs are drafts that a person merges
  - removed fields are reported, not fixed

  The new risk is a fix that compiles but is wrong. It also means a GitHub App with PR access to the frontend repos, where the plan had a read-only token. PROJECT-BRIEF, B01, B03 and B06–B12 were updated. The assignment allows a change like this when it's logged here.
- **Dropped the "Namaskara" greeting.** The problem now comes first, so the greeting no longer had a place.
- **After watching the video, I found the in/out slide hard to follow.** I asked for it to be smoother, and for a check that every one of the seven questions gets answered.

  Claude's audit:
  - Q4 ("what it proves") had gone missing in the rewrite. The skills line was dropped.
  - The artifact form (Q1) and the reader's first minute (Q3) appeared only on screen, not in the narration.
  - "Mostly learning" (Q7) and the "saves a backend developer…" line (Q2) weren't said out loud.

  I approved the fixes:
  - B10 was rewritten as "What v1 will and won't do".
  - The skill chips came back in B09, including "agent loops — not claimed".
  - BVDT now names the public repo, the GitHub Action and the CLI, and says what a hiring manager sees first.
  - B03 and B12 each got one extra line.
- **The approved script came out at 4:06, over the cap.** Four small wording trims, with no facts dropped, brought it to 3:58: B03, B05 (dropped its intro sentence), B07 ("type check and tests" became "tests") and B09.

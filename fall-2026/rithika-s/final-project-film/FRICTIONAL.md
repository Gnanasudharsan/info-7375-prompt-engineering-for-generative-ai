# FRICTIONAL — Final Project Pitch Film
Rithika Sankar Rajeswari · INFO 7375


## 2026-10-10 (Sat, evening): choosing the project
- Read the assignment; the film is required and graded here, though the syllabus calls videos optional.
- Considered switching projects; kept Agentic Retrieval Lab because Milestone 1 was already done and verifiable.
- Ran a read-only inventory in Terminal: 4 commits (Oct 5–9), 103 tests passing, lint clean, 4 dated results folders.
- A Claude Code session opened in the brutalist repo couldn't fill my brief, because it had no access to the retrieval repo.
- Claude (chat) drafted PROJECT-BRIEF.md from my inventory. Checking it against the Q2D-Web paper led to two corrections: Q2D-Web has a public leaderboard (so "cannot rerun" became "cannot inspect the data"), and my low support-query score is likely a labelling artifact, not a real search failure.
- Chose to postpone Experiment 3 and start with the length-only baseline.
- Dropped the $0.68 cost figure from the film because I hadn't verified it.

Reflection: My first thought was to maybe start a new project, but once I saw that Milestone 1 already had real commits, tests and dated results, staying with Agentic Retrieval Lab made more sense. I could show real evidence instead of only promises. Checking the brief against the paper showed me that a sentence can sound right and still be slightly wrong, so I now check wording against the source before I trust it.

## 2026-10-10 (Sat, late night): toolkit setup
- My old brutalist checkout was 47 commits behind, with all tracked files showing as deleted. Cloned fresh to ~/brutalist-v2 instead of pulling.
- Setup's final check failed on upstream example files that mention ElevenLabs; I ran each readiness check individually and all passed.
- `./art smoke` failed because the shipped example's slug "_smoke" breaks the toolkit's own naming rule. Approved a temporary fix on a scratch copy; the test passed and the file was reverted.

Reflection: I expected setup to be the easy part, but the toolkit itself had problems. A fresh clone felt safer than trying to repair a broken folder close to the deadline. I learned that a tool failing doesn't always mean I did something wrong, but I still need to understand why it failed before I approve a fix.

## 2026-10-10 / 11 (overnight): script and first render
- The narration was estimated at ~3:41 but measured 4:02. Chose 3 small cuts plus speed 1.04 so I could keep my beat 11 success check. Final: 3:52.7.
- Whisper caught "agent-tritten"; removed the hyphen. I listened to how my name sounds in beat 4.
- The built-in outro hard-codes the instructor's handle, so I made beat 14 my own outro with my name.
- Fact-check before rendering: "one correct book per question" became "usually just one", and "lowest overall" became "on its main measure".
- The first review cut failed Gate V with 12 blockers. Chose a disclosed local patch for the name stamp instead of submitting over a failing check.

Reflection: I assumed the word-count estimate would be close enough, but measuring showed it ran over. I chose small cuts because I didn't want to lose the line that explains how someone would know my first step ran. Fixing small wordings before rendering felt important, because the honesty rule applies even to a phrase like "one correct book".

## 2026-10-11 (Sun, early morning): rejecting the first visuals
- Watched the first cut: squiggle placeholder text, key terms never shown on screen, unlabelled icons.
- Asked for a redesign: real words, labelled key terms that pop in when spoken, bigger drawings.
- Beat 1 now uses a real query from my data ("when is ski season over" plus its 4 Claude Haiku rewrites). Saved evidence/beat1_example_951820.json so reviewers can verify it.
- On the contact sheet I flagged: the B07 "public" chip was ambiguous (it could read as Q2D-Web being public), B06B needed "not on the key", and labels were clipped in B11, B12 and B13.

Reflection: I was happy with the narration and tone, but the visuals let it down. In a video, what people see sticks better than what they hear, so the screen has to carry the idea. Using a real query from my own data in beat 1 made the film more honest as well as clearer.

## 2026-10-11 (Sun, morning): cast and wording
- While watching, beat 3 still showed squiggles. It turned out my player was showing the old file; I confirmed by pulling a frame with ffmpeg.
- Added cartoon characters: me saying "hi!", two different librarians, a lazy librarian, a searcher and a reviewer. The toolkit's "no people unless instructor portrait" rule is only a written convention, not a gate.
- Rewrote beat 13: dropped "starting January 2027" and said I'm aiming for AI/ML engineering or data science roles, with a special interest in RAG retrieval, generation and evaluation.
- Considered recording my own voice; dropped it because I'm away Monday and needed to submit today.

Reflection: Boxes and carts felt flat, so I asked for people. I think viewers follow characters more easily than objects. Mentioning a job start date felt awkward in a class submission, so I described what actually interests me instead. I would have liked to use my own voice, but a finished, checked film today was more important than a rushed one.

## 2026-10-11 (Sun, late morning): making it flow
- Watching the cast cut, I noticed that my character stayed on screen after her introduction, and that the opening frame was crowded (the robot overlapped the searcher and the bubbles touched).
- Asked for the whole film to be choreographed: each element appears when it is spoken about, leaves or dims when the narration moves on, one focus at a time.
- Before any change, had Claude Code make a backup final master of the passing version. GATE T flagged 4 issues; they were fixed by moving or recolouring outlines, not by exempting the gate.
- A new overlap check every 0.5 s caught 4 collisions that only happened during motion (B03, B06B, B09, B13); all were fixed.
- Watched a 480p preview of the full film to check the flow before the 4K render.

Reflection: Single frames looked fine, but watching the video showed things that didn't match the narration. I wanted it to feel like a proper explainer where everything flows with what is being said. Making a backup first meant I could keep improving without risking having nothing to submit.

## Few headsups
- That my low support-query score is a labelling artifact: this is my hypothesis, not yet tested.
- That the length bias affects rankings: the length-only baseline hasn't been run yet.
- The narration is a synthetic voice (Kokoro af_bella), not a recording of me.
- The film was built with a small local toolkit patch (toolkit-local-patch.diff), not the unmodified toolkit.

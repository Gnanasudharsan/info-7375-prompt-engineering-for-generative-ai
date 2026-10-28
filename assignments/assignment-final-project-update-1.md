<!--
Paste-ready Canvas assignment description. Student-facing, self-contained, all links
absolute, since students reading it in Canvas cannot resolve repo-relative paths. Posted to
Canvas by the instructor after review (2026-10-11). Keep the Canvas text and this file in sync.
-->

# Final Project Update 1 — The First Working Slice

**Points: 50 · Due: Thursday, November 5, 11:59 pm ET · Submit: one .zip through Canvas, plus a matching GitHub folder**

Read the [course AI policy](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/ai-policy.md) and watch [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) before beginning graded work.

## What this assignment is

You pitched a final project. This is a short check on it: **the smallest piece of it that runs.** Nothing here is the whole project. The point is to find out, early and honestly, whether the idea survives contact with a keyboard, and to change it now if it does not.

**Your final project must be agentic and related to agentic AI.** It can be about anything, built in any programming language. By *agentic* we mean it has all of these, and your slice must show where each one lives:

- a **loop**: it observes, decides, acts, records, and stops;
- **tools** it uses to act or to look something up, with limits on what it may touch;
- a **stop condition** that is not "the model said it was done"; and
- a **human gate**: a point where it hands a decision back to a person.

If your pitch was not agentic, this is where you change it. Log the change in `FRICTIONAL.md` and say so in your update. That is a good use of this assignment, not a penalty.

## What to do

1. **Update your project brief.** Revise `PROJECT-BRIEF.md` from your pitch. End it with two lists, **exists today** and **will exist**, and say what changed since the pitch and why. Past tense only for what you can show.
2. **Make the first working slice run.** One small, real piece that runs from a fresh clone: for example, one tool call inside one loop, with a test. Give the language, the toolchain, and the exact commands. A TA must be able to run it.
3. **Show where the four agentic parts live.** One paragraph or table: the loop, the tools and their limits, the stop condition, the human gate. If one is not built yet, say so plainly. A part you have not built is an honest answer; a part you claim and cannot show is not.
4. **Predict, then run.** Before you run the slice for the first time, write down what you expect to happen and what you think will go wrong. After, record what actually happened. Keep your original prediction; do not rewrite it to look right.
5. **Show it.** A recording of the slice running, **90 seconds or less**, with any screen-capture tool. Narrate as yourself. A polished film is not required and earns nothing extra.
6. **Name the next step and the biggest risk.** One of each, specific to your project.

Your own data stays private: no real résumé, contacts, or personal records in the repository or on screen. Use synthetic or public data.

## What to submit

Canvas file name: `LastName_FirstName_INFO7375_FinalUpdate1.zip`
GitHub folder: `fall-2026/first-name-last-initial/final-project/update-1/`

`README.md` (language, toolchain, exact commands) · the updated `PROJECT-BRIEF.md` · the code and test for your slice · the prediction and the result · the recording · `SOURCES.md` (what you used, what you wrote, what Claude contributed) · `FRICTIONAL.md`. Include the GitHub folder link and final commit hash in Canvas. Leave out caches and credentials.

## Grading — 50 points

| Component | Points |
|---|---:|
| The update | 30 |
| [Frictional](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/frictional.md) (honest log) | 5 |
| [GitHub version posting](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/github-submission.md) matching Canvas | 5 |
| [Relative Quartile](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/relative-quartile.md) | 10 |
| **Total** | **50** |

**The update (30)** — a slice that runs from a fresh clone, with a test and exact commands (12) · the four agentic parts shown honestly, built or not (8) · the prediction and the real result, and an honest account of what changed from the pitch (6) · a specific next step and risk (4).

**Frictional (5)** — specific, honest accounts of what you tried and what happened (2) · what you checked, changed, or learned (2) · traceability to commits and prompts (1). An unsuccessful attempt can earn full credit.

**GitHub posting (5)** — source and documentation posted in your folder (2) · Canvas names the exact commit and run instructions (2) · what you submit matches what is posted (1).

**Relative Quartile (10)** — an overall quality score compared with the whole class: specificity, real improvement, demonstrated understanding, evidence, honesty about verification, and usability. Top 25%: 8–10 · Second 25%: 5–7 · Third 25%: 2–4 · Bottom 25%: 0–1. Meeting the criteria earns the other 40 points; it does not guarantee these 10.

## The honesty rule

Past tense only for what you ran and can show. Label every mock-up and simulation. Any Claude response you show is one you actually got, with the date. No invented users, metrics, or results.

## AI use and responsibility

Use Claude as much as you like and name what it contributed in `SOURCES.md`. You remain responsible for what you submit. The instructor or a TA may ask you to explain any part of it. Not being able to explain your own submission reduces points, and misrepresenting what you verified is an academic integrity matter.

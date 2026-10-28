<!--
Paste-ready Canvas assignment description. Student-facing, self-contained, all links
absolute, since students reading it in Canvas cannot resolve repo-relative paths. Posted to
Canvas by the instructor after review (2026-10-11). Keep the Canvas text and this file in sync.
-->

# Final Project — An Agentic System You Choose

**Points: 250 · Due: Sunday, December 20, 11:59 pm ET · Submit: one .zip through Canvas, plus a matching GitHub folder**

Read the [course AI policy](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/ai-policy.md) and watch [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) before beginning graded work.

## What this assignment is

Build **an agentic system of your own choosing** and defend it. It can be about anything, built in any programming language, as long as it is **agentic and related to agentic AI**. It may be the job-search agent you built across the course, or something completely different. It should be a **portfolio piece**: something a reviewer can open and judge in a few minutes.

This is your pitch from October, grown up. You may have changed the project since then. Say so in your README.

## What "agentic" means here

Your system must have, and you must show where each one lives:

- a **loop** that observes, decides, acts, records, and stops, with exits you designed and a budget;
- **tools** it uses to act or look things up, with a **permission policy enforced in code**;
- **memory or state**, or a written reason it needs none;
- a **stop condition** that is not "the model said it was done"; and
- a **human gate** where a person approves, refuses, or defers, bound to what they actually saw.

## The packet

You submit the ten documents of Chapter 15, in an evidence chain, plus the working system:

1. `brief`: the need, who owns it, who is affected, what success looks like, what it is *not* for, and what would make it inappropriate.
2. `data-boundary`: every source and file, labeled public, synthetic, internal, personal, or unknown by the real policy; retention and deletion.
3. `action-surface map`: what the system can read, write, and send, and what authority each needs.
4. `plan`: steps, dependencies, evidence on each edge, stop and refusal paths.
5. `gates`: the human approvals, each tied to what the approver saw.
6. `premortem`: a failure you predict, written before you build it.
7. `evidence`: exact commands and observed results, separating code inspection, fixture output, model output, and human observation.
8. `artifact`: the working system, or a precise way to run it.
9. `audit-note`: predictions before critique, a reviewer's findings (judged genuine or false positive by you), failed cases, and a **Gap Account**: what a reviewer of that kind could never reach.
10. `transfer-reflection`: what you will hand to an agent more readily, what you will keep practicing, and your **ship, narrow, defer, or stop** decision with reasons.

A link between documents is a claim. Open every target and confirm it says what the link says.

## What your system must demonstrate

- **It runs from a fresh clone**, with exact commands and a toolchain list, in the language you chose.
- **An evaluation that can say no:** cases you set aside before you tuned anything (development versus held-out), at least five **deliberate failure cases**, and an honest statement of what your sample can and cannot show.
- **A controlled failure.** Write down a failure you expect, **trigger it on purpose**, show the independent check that catches it, and show your reviewed recovery. A failure you only describe earns nothing.
- **The three devices from the chapters.** *The gate*: the contract and tests you wrote before Claude implemented. *The sign-off*: what you checked, how, what you did **not** check, what you are not claiming, and whether you signed or withheld. *The driver's seat*: what Claude did, what you did, and why that part stays yours.

## The stranger run

Someone who did not help build it (a classmate, a friend, or a TA) runs your project from your README on a clean machine, and you write `STRANGER-RUN.md`: who it was, what they did, where they got stuck, and what you changed. If you cannot find anyone, say so and describe how you tested from a clean clone yourself. The README that survives a stranger is the README that works.

## The demo

A **recording of five minutes or less** showing the system running, and where its loop, tools, and human gate are. Any recording tool is fine; Brutalist is optional. Narrate as yourself. Polish earns nothing by itself.

## Privacy and boundaries

Your real data, résumé, contacts, and conversation transcripts stay on your machine. Use synthetic or public data and a fictional persona wherever a person appears. If your project touches other people's data, say whose, how they consented, and how someone affected could contest a result. Respect every site's terms of use. Do not build anything that sends messages or takes irreversible actions without a person's approval at a gate you can show.

## What to submit

Canvas file name: `LastName_FirstName_INFO7375_FinalProject.zip`
GitHub folder: `fall-2026/first-name-last-initial/final-project/`

`README.md` (what it is, language, toolchain, exact commands, what ran, what did not) · the ten-document packet · the code and tests · saved evidence and raw outputs · `STRANGER-RUN.md` · the recording and a link to it, with its filename and SHA-256 (keep MP4s out of GitHub) · `SOURCES.md` (what you used, what you wrote, what Claude contributed, third-party licenses) · `FRICTIONAL.md`. Include the GitHub folder link and final commit hash in Canvas. Leave out caches, credentials, and private data.

## Grading — 250 points

| Component | Points |
|---|---:|
| Implementation and explanation | 150 |
| [Frictional](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/frictional.md) (honest log) | 25 |
| [GitHub version posting](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/github-submission.md) matching Canvas | 25 |
| [Relative Quartile](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/relative-quartile.md) | 50 |
| **Total** | **250** |

**Implementation and explanation (150)**

| Criterion | Points |
|---|---:|
| **A working agentic system:** loop with exits and a budget, tools with an enforced permission policy, state, a stop condition, runs from a fresh clone, tests | 40 |
| **Evaluation:** a held-out set, at least five deliberate failure cases, honest limits, claims no stronger than the evidence | 30 |
| **Control:** the human gate bound to what the approver saw, the data boundary, the action-surface map, ownership and the things it must never do | 30 |
| **The controlled failure and the audit:** predicted first, triggered, caught by an independent check, recovered with review; the audit note and the Gap Account | 20 |
| **Packet integrity and the decision:** ten linked documents whose links hold, the sign-off with real "Not checked" entries, the driver's seat, and an evidence-based ship / narrow / defer / stop decision | 15 |
| **The demo and the stranger run:** the recording shows what it claims; a README that survives a stranger | 15 |
| **Subtotal** | **150** |

Award partial credit for demonstrated work. Claims must be defensible. A beautiful presentation does not repair an incorrect explanation, and a modest project honestly evidenced outscores an ambitious one that cannot be verified.

**Frictional (25)** — specific, honest accounts of what you tried and what happened (8) · what you checked, changed, or learned, including what is unresolved (8) · what you accepted, modified, or rejected from Claude (5) · traceability to commits, prompts, and tests (4). An unsuccessful attempt can earn full credit. Invented struggle earns nothing.

**GitHub posting (25)** — source and documentation actually posted in your folder (10) · Canvas names the exact commit and the run instructions (8) · the recording's link, filename, and checksum, and what you submit matches what is posted (7).

**Relative Quartile (50)** — an overall quality score compared with the whole class: specificity, real improvement over where you started, demonstrated understanding, evidence, honesty about verification, usability, and professional communication. Top 25%: 40–50 · Second 25%: 25–39 · Third 25%: 12–24 · Bottom 25%: 0–11. Meeting the criteria earns the other 200 points; it does not guarantee these 50. The instructor and TAs review everyone's work before assigning it.

## The honesty rule

Past tense only for what you ran and can show. Label every mock-up, simulation, and seeded run. Any Claude response you show is one you actually got, with the date. No invented users, metrics, testimonials, or results.

## AI use and responsibility

Use Claude as much as you like and name what it contributed in `SOURCES.md`. You remain responsible for what you submit. The instructor or a TA may ask you to explain any part of it, including any line of the code and any claim in the packet. Not being able to explain your own submission reduces points, and misrepresenting what you verified or what the agent did is an academic integrity matter.

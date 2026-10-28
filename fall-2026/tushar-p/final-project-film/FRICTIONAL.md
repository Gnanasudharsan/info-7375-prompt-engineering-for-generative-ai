# FRICTIONAL — Agent Proving Ground pitch film

## 2026-10-12 — Choosing the project
I didn't want to extend the Reallocation Engine, because a lot of the class will probably do that. I wanted something I could actually put on my resume. I went through my job search notes and saw the same gaps coming up: Kubernetes, sandboxing agents safely and tracing. So I picked a sandboxed agent runner with tracing and evals. My worry was that it was too big for the course, so I cut it down to a local version on kind. I plan to add Go and EKS later (not a part of this project for now).

## 2026-10-13 — ai-explainer didn't fit
The closest skill was ai-explainer, but it needs the instructor's channel branding and persona, a rewritten narration style, and Claude's interface on screen. The assignment says to narrate as myself, and I didn't want Claude's output on screen, so I didn't use it.

## 2026-10-13 — Watching the review cut
All the checks passed, but when I watched the film myself I found four problems. B04 talked about E2B and Langfuse as if everyone already knew them. B10 started with "Why this project? It's a mix," which isn't a full sentence. B10 also said I picked the project because of the roles I'm applying for, which isn't really my reason. And the film just stopped on the last list, with no closing. I rewrote B04 and B10 and added B12 as a closing beat. The checks can't catch things like this. I had to watch it.

## 2026-10-13 — No pauses between sentences
The narration sounded like one long sentence. I had each sentence voiced separately, with a 0.35 s gap between them. It sounds a lot more natural now. The runtime went from 2:50 to 3:10, which is still inside the limit.

## 2026-10-13 — Changing B06 and B07
"It won't prove production scale, and I won't claim it" sounded defensive, so I changed it. I also changed "Go and cloud deployment come later, as a side project," because I'm not sure it will be a side project. After that, two on-screen labels no longer matched the narration (a red ✗ and "a side project"), so I fixed those too.

## 2026-10-14 — Gate 11 failed
The toolkit's unit tests failed because matplotlib wasn't installed in the project's .venv. It had nothing to do with my film. I installed it, re-ran the tests, and all 122 passed.

## 2026-10-14 — Gate 12 fails because of a toolkit bug
The smoke test fails on this checkout. The toolkit's own sample reel uses the slug "_smoke", and the toolkit's own safety check rejects slugs that start with an underscore. I tried running it on a copy with the slug fixed, but the script is hardcoded to the original folder. I didn't edit the toolkit, because that's not my code to change. I left the failure in and included the report.

## 2026-10-14 — Present-tense lines
I lost points in Week 1 for one sentence that claimed more than the evidence showed, so I did one last check for tense. Two lines described the project as if it already exists: "It's built for one laptop" (B06) and "It runs locally" (B07). Nothing is built yet, so I changed them to "will be built" and "will run." Then I re-voiced those two beats, re-rendered, and ran all the gates again.

## 2026-10-14 — Making the docs match the film
The README and FACTCHECK said every feature sentence uses "will," but that isn't strictly true. B04 and B08 have present-tense words inside "will" and "you'll" sentences. Instead of re-rendering again, I rewrote the claim so it says exactly what the film does.

## 2026-10-22 — TA feedback on P4, and making OmniSQL public
I got 48.5/50 on the first submission. The one deduction was on "Why this project": all my evidence for existing skills was in private repos, so a reviewer couldn't check the 23% → 69% number. I had forgotten that my OmniSQL-Postgres project already has a public demo site, so I made the repo public too. Before doing that, I checked that it had no API keys or private data. Now the brief links the repo, and the README there shows the number.

## 2026-10-22 — Switching to Go
In my first entry I said Go would come later. I asked the TA, and I can use any language for the final project. My main goal is to learn Go, and agent infrastructure jobs keep asking for it, so I switched the whole project to Go. Anthropic has an official Go SDK, so the agent loop can still use the Claude API. The coding tasks the agent solves will still be small Python repos. This makes the risk bigger, because I'm learning Go and Kubernetes at the same time, so I changed B09 to say that.

## 2026-10-22 — Checking the latest Brutalist
Brutalist had been updated since my checkout, and show-tell was there now. Before changing anything, I cloned the latest version into a separate folder. My film built there fine, but show-tell turned out to be a Bear-only skill with the Liam persona and channel branding, the same problem as ai-explainer. The new version also had new rules (company logos, a Bear portrait for people) and a Manim upgrade that could change my renders. The update did fix the gate 12 bug, but that tests the toolkit, not my film. So I stayed on the version that works, and noted the upstream fix in the README. I also found out my reel folder had no backup at all, so I zipped it first.

## 2026-10-22 — "AWS" was read as "oz"
After re-voicing B10, the voice read "AWS" as one word, like "oz". The audio script now gives the voice "A-W-S" instead. The narration text and the screen still say "AWS".

## 2026-10-22 — Adding a proper intro
The film started straight with "An AI coding agent tells you it's done." It needed a real intro. My first suggested version was too long, so I kept it short: "Hi, I'm Tushar. Have you ever wondered, when an AI coding agent tells you it's done, whether it really is?" B01 no longer repeats my name.

## 2026-10-22 — Name overlapping the B00 drawing
When I watched the new start, my name showed on top of the speech bubble, with the "Constructed" label next to it. That looked messy, and the label made it seem like my name was part of the mock-up. Now my name shows alone, centered, for the first second, and then B00 starts as before. The README and FACTCHECK said the label shows "for the whole beat", which was no longer true, so they now say "for the whole mock-up."

## 2026-10-22 — Simplifying B10
The first B10 rewrite talked about OmniSQL in a lot of detail, and the numbers. That wasn't what the TA asked for. The problem was the missing link, not missing detail. Now B10 just names the skills, with the project name and GitHub link in small text underneath. The 23% → 69% number stays in the brief, where a reviewer can check it through the link.
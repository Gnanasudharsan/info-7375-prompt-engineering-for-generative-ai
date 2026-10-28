# FRICTIONAL.md

Ashwin Thankachan · INFO 7375 · Final Project Pitch Film

My log of choosing the project and making the film. Claude Code helped me turn my chat history and the
command output into these notes. The decisions and the reasons are mine.

---

## 2026-10-09 to 10-10: too many ideas

I thought I'd pick a project in one evening. It took most of a week.

- **Oct 9.** I asked Claude for ideas that would help my resume. It suggested an API contract drift
  detector, an incident postmortem agent and a resume claim checker. None of them excited me. The resume
  checker was out anyway, because the assignment bans real resume, contact and tracker data.
- **Oct 10.** Over many rounds I went through about twenty more ideas: MBTA reliability, an apartment
  records checker, an OPT day tracker, an SEC filing extractor, a ticket-drop engine, an accessibility
  fixer, and others. I kept saying no.
  - The searches kept showing me that "original" ideas already existed. accessiBe launched an
    accessibility code agent in September 2026, Splitwise Pro already itemizes receipts, and Slido
    already groups similar questions.
  - I also thought I had to pick one of the Canvas examples. They're only examples. My auto-apply job
    pipeline is already my Reallocation Engine work, so I wanted something separate.

By the end of it I knew two things. I'm applying for SDE roles, not "AI engineer" roles, and I want the
project to teach me skills my resume doesn't show yet.

## 2026-10-11: ProvenDocs and the first film

I picked ProvenDocs. It would turn every sentence of a code explanation into a JUnit test and mark it
proven, false or untestable, scaled with Kafka, Redis and Kubernetes so I'd learn those too.

I built a full film for it with the Brutalist toolkit. Setup problems:
- manim 0.18 doesn't install on Python 3.13, so I moved to Python 3.12. That needed Homebrew `pango`, and
  pinning `av<16` for faster-whisper.
- The show-tell skill opens with the instructor's persona and ends on his handle. The assignment says to
  narrate as myself, so I replaced both. The outro card had the handle hardcoded, and no gate caught it; I
  only saw it by watching the frames. That led to `build/patches/ClaudeTitleOutro-handle.patch`.
- Gate T blocked twice on text size, once over a single lowercase "w" 1 px under the minimum.

It ran 3:55 and passed every gate. What I learned: passing the gates doesn't mean the film says what you
meant. You still have to watch it.

## 2026-10-11 (evening): a brutal second opinion

I pasted the ProvenDocs pitch into Codex (ChatGPT) and asked for brutal feedback. It gave it 6/10 and asked:
if the generated tests just get committed, what does the tool add beyond ordinary JUnit tests? It also said
I was adding Kafka, Redis and Kubernetes before showing the tool was useful. That was fair. I'd added them
to learn them, not because the project needed them. Its top alternative was an incident investigation
assistant.

## 2026-10-13 (morning): the final rubric changed how I looked at it

The final project (250 points, due Dec 20) asks for:
- a loop with a budget
- tools with permissions enforced in code
- saved state
- a stop condition that isn't "the model said it was done"
- a human approval gate
- a held-out evaluation
- a failure I trigger on purpose

ProvenDocs had no natural human gate, because nobody needs to approve a test result. So I went back to
brainstorming with Codex and other chatbots, pasting their pitches into each other for second opinions:

- **Dependency patching and schema migration agents.** The rubric fit was oversold, and Atlas, Bytebase
  and pgroll already cover much of migrations.
- **"Referee", a patch checker built on the EvilGenie paper.** The pitch claimed hidden tests fix reward
  hacking, but the paper found they help only a little.
- **"FaultLine", an incident agent.** I worried it looked like CloudPulse again.
- **Subscription reconciliation, FraudLens (streaming fraud), model routing, catalog matching.**
- **An outfit picker based on weather and trends.** Weather styling already exists, and my Northeastern
  Claude access doesn't include API credits.

By then I had too many ideas and didn't feel strongly about any of them. Each chatbot changed its
recommendation every time I pasted something new.

## 2026-10-13 (afternoon): deciding with real data

I asked Claude to stop pitching and look at evidence: my resume, and the jobs I've been applying to. My job
pipeline had 3,254 entry-level postings stored from Oct 8–12. Claude counted skill keywords across them
(a simple word count, so it's noisy):

| Skill | SWE postings | AI/ML postings |
|---|---|---|
| Agents / agentic | 12% | 52% |
| Kubernetes | 16% | 19% |
| Observability (Prometheus, OpenTelemetry, Datadog) | 13% | 18% |
| Evaluation, RAG, MCP | — | ~11–22% |
| Redis / Kafka | ~2% / ~4% | ~2% / ~4% |

My resume covers Python, Java, AWS, CI/CD and Spring Boot, and shows nothing for agents, evaluation or
observability. So I went back to the incident agent and named it **TraceCase**.

What made it feel right to me is that it builds on CloudPulse instead of copying it. CloudPulse answers "is
the service healthy?" TraceCase answers "why did it break, and what is safe to do?" I can explain both in an
interview.

Two changes from my earlier plans:
- **Redis stays only where it has a job:** the cache and queue inside the demo service. That gives the agent
  real failures to find, like a stale cache or a backed-up queue.
- **Kafka is out.** Kubernetes is a stretch goal.

## 2026-10-13: checking the alternatives

My draft brief said TraceCase is different because a person approves fixes. Claude checked the primary
sources, and I skimmed both GitHub pages myself.
- **HolmesGPT** (CNCF sandbox, Apache-2.0) is read-only by default. Its optional Kubernetes remediation
  toolset already puts "every mutating action gated behind human approval". So approval isn't my
  difference, and I took that claim out.
- **AIOpsLab** (Microsoft, MIT) is a research framework for evaluating these agents, and it runs on a
  Kubernetes cluster.

The film now says only what TraceCase will do:
- run on a laptop without Kubernetes
- ship its own service to break
- make every claim cite a real log line or trace
- void an approval if the fix or its evidence changes

It doesn't claim the others can't do these things. I haven't run HolmesGPT yet.

## 2026-10-13: first TraceCase draft

- **Script:** the first draft ran ~5:20 against a 4:00 limit. I cut it to 3:53.
- **Drawings:** 16 new scenes with one cast throughout: service, logs, trace, a magnifier for the agent, a
  fix card and a barrier gate. The first contact sheet showed four overlaps, which were fixed before
  rendering.
- **Gates:**
  - Gate B stopped the render twice: a label outside the safe area (B05), and a cross drawn over text (B11).
  - Gate T blocked the master once: it read wavy lines in B08 as overlapping text, so I swapped them for
    bars.
- **Something no gate caught:** the intro card never changed "is it down?" into "why is it down?". The
  trigger phrase included the "?", which the component strips before matching. Watching the frames caught
  it.
- **My voice:** the toolkit has no voice cloning, so I recorded the intro and outro with a script that
  replaces a beat. It took three tries:
  1. The script quit silently, because ffmpeg exits with an error after listing microphones.
  2. The next take was 17 s of silence, because the terminal inside the Claude app had no microphone
     access. The script now stops if a take is silent.
  3. The take recorded in the macOS Terminal app worked.

## 2026-10-13 (evening): drafts 2 and 3

I watched draft 1 and wasn't happy with two things:
- **My voice.** I didn't like how my recording sounded next to the rest of the film, so the whole film now
  uses one synthetic voice (Kokoro `am_michael`, 0.95 speed) reading my first-person script. My takes are
  kept, unused.
- **Some icons and the flow.** The mouse cursor was a stubby triangle that floated in mid-air (B03) or sat
  on a button's edge (B05), and nothing connected one picture to the next. Draft 2 added:
  - a proper pointer, placed on what's being clicked
  - flow arrows (service → evidence → fix → gate, API → Redis → worker → Postgres, and others)
  - direction arrows on the loop
  - one straight trace line in B10
  - a heading on every beat naming which of the seven questions it answers

Then Claude and I checked the film against the grading rubric and fixed what it was missing (draft 3):
- **Prompt contract:** the course term is now said out loud. Each agent step must match a fixed format that
  code checks.
- **Limitation:** an honest one is now stated. It will only be tested on failures I design, so it proves
  nothing about real production systems.
- **Skill labels:** the "why this project" shelves now name the skills (new: agents, tracing, evals; built
  before: Spring Boot, LLMs, Docker).
- **Empty openings:** a few beats opened on a nearly empty frame for a few seconds. Now each beat's main
  picture is there from its first frame.

Adding lines pushed the film to 4:01, so I tightened four sentences. It now runs 3:53.

Two more problems along the way:
- Watching the frames showed the "contract check" in B07 appearing 5 seconds after it was said. The code
  steps were in the wrong order.
- Gate T then blocked B07 twice: the new label was 1 px under the minimum, and the wavy lines in its claim
  cards read as text (the same false alarm as B08). I enlarged the label and swapped the lines for bars.

## What I took from Claude and Codex, and what I didn't

- **Accepted:**
  - Codex's critique of ProvenDocs.
  - Claude's keyword count, which settled the choice.
  - The fact check that removed my "human approval" claim.
  - Claude's drawings and scripts, after I reviewed every contact sheet and draft.
- **Changed:**
  - Claude's first script ran 5:20 and had to be cut.
  - Its first drawings had icon and flow problems I pointed out.
  - It drafted this log, and I corrected it and gave my own reasons.
- **Rejected:**
  - About thirty project ideas.
  - Adding Kafka and Kubernetes just to have them on my resume.
  - Claiming human approval as my difference.
  - My own recorded voice.

## Still open

- Run HolmesGPT myself before the final project, so the comparison isn't based only on its README.
- Nothing of TraceCase is built yet. First piece: the demo service with one failure I can trigger, and a
  saved trace that shows it.

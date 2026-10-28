# DayThread — pitch film script v1 (DRAFT for Aditya's review — not approved, nothing rendered)

Skill: show-tell (Aditya's choice). Voice: Kokoro `am_onyx` ("Liam, in for Aditya"). Every body
beat is one isometric drawing. **There are no people on screen** (Aditya, 2026-10-14). The cast,
reused through the whole film: a **phone**, **check-in cards** on a **thread**, the **memory
drawers**, a **summary page**, a **scanner**, the coordinator's **review queue**, and a **gate
with a stamp**.

Caption rule: every imagined conversation or screen carries the caption
**"Constructed — proposed workflow"** while it is on screen (marked ⓒ below).

Lines starting `VO:` are the narration. Everything else is the visual plan.

---

### BIDEA — the question (hesitant writer)
VO: Hallo. This is Liam, in for Aditya. Can an AI check-in remember yesterday? Better: can it notice what changed since yesterday, and show a person why?
- Visual: the writer types "Can an AI check-in remember yesterday". It strikes "remember" and
  writes "notice what changed since".

### B00 — what it is
VO: DayThread is a project I'm proposing. Nothing is built yet. It's an AI check-in assistant that remembers conversations across days, and turns concerning changes into evidence a home care coordinator can review.
- Visual: a phone arrives. One check-in card, then a second, drops onto a thread that runs
  left to right. Labels: `DayThread` · `proposed`.

### B01 — day one ⓒ
VO: Here's the first story I'll build, with a fictional client and synthetic records. Day one is a short text check-in. In passing, the client says it was just a little tumble.
- Visual: the Day 1 card fills with scribble lines (never real text). One line gets a terracotta
  dot, and the words "just a little tumble" sit beside it. The card files into the memory
  drawers. Labels: `Day 1`.

### B02 — day two: memory, and the first thing that runs ⓒ
VO: On day two, the assistant asks how they've been since the tumble. The client never had to repeat it. That retrieval, saved with a link back to the day-one words, is the first thing I'll make run.
- Visual: the Day 2 card arrives. A drawer slides open and the Day 1 card rises. An ink link
  draws from the Day 1 dot to the Day 2 card. Labels: `Day 2` · `source link`.

### B03 — the failure that could sink it ⓒ
VO: Now the failure that could sink it. Suppose the day-one summary drops the tumble. Every later step reads the summary, so every later step misses it. I'll predict that failure in writing, then trigger it on purpose.
- Visual: the Day 1 card folds into a shorter summary page, with a visible gap where the dot's
  line was. The summary rides a conveyor through two later steps, and the gap rides with it.
  Labels: `summary` · `missed`.

### B04 — the independent check ⓒ
VO: A separate check reads the original conversation, not the summary. If it finds the tumble, it creates an internal review item. That checker could miss unfamiliar wording, or raise false alarms, so I'll test both.
- Visual: a scanner sweeps the original Day 1 card, skipping the summary. It lights on the
  dot, and a review item drops into the review queue. Labels: `original` · `review item`.

### B05 — the human gate ⓒ
VO: The coordinator sees the concern, the excerpts behind it, and the proposed action, then approves, refuses, or defers. Nothing goes out without that decision, and the decision is recorded against exactly what they saw.
- Visual: the review desk shows the concern card, two excerpt slips, and an outbound parcel at a
  closed gate. The stamp cycles through three slots, then lands on one. The record clips to the
  exact slips shown. Labels: `approve` · `refuse` · `defer`.

### B06 — the real alternatives
VO: Fall detection and AI calls already exist. Lifeline's page describes sensors that detect a fall and specialists who respond, and says it doesn't detect every fall. DailyCall's pages describe daily AI calls with summaries for families, and say it isn't emergency monitoring.
- Visual: two trays. The first holds a pendant with a signal arc to a response tower. The second
  holds a phone and a summary page. Labels: `Lifeline` · `DailyCall`. Small caption: "per their
  official pages". No logos.

### B07 — how DayThread differs
VO: I'm not claiming either lacks anything. My focus is narrower: tracing a change across check-ins back to the original words, so a coordinator doesn't rebuild the history by hand, and stays in control of the next step.
- Visual: a third tray slides in, holding the film's own thread, a source link, and the gate.
  Labels: `DayThread` · `proposed`.

### B08 — who opens it, first minute ⓒ
VO: I'm aiming for AI engineer roles, so the first person to open it is probably a hiring reviewer. In the first minute, they open the README, run a clearly labelled replay, and inspect the two-day memory example and one approval decision.
- Visual: a parcel opens and a README page lifts out. A terminal plays a replay, then the
  Day 1 → Day 2 cards appear and the stamp lands. Labels: `README` · `replay`.

### B09 — course skills
VO: It's built to show prompt contracts, a loop with a budget and clear stops, permissions enforced in code, source-linked memory, and evaluation. Tests and logs will show whether it retrieves earlier details, rejects an unauthorized record change, and stops at its limits.
- Visual: a loop ring drains budget slots one by one. A `record change` parcel hits the gate and
  bounces back. The ring stops when the slots run out. Labels: `budget` · `blocked`.

### B10 — evidence and its limit
VO: I'll compare the workflow with and without memory, on development cases and on held-out cases reserved before tuning, plus at least five deliberate failure cases. At best, that shows a tested prototype, not readiness for real care.
- Visual: two benches, `with memory` and `without`. A sealed vault holds the held-out cases, and
  five failure samples line up. Labels: `held-out` · `5 failures`.

### B11 — scope
VO: The core is simulated text check-ins, memory, evidence-linked concerns, and human review, in Python and SQLite. Clinical advice, real patient data, and autonomous outreach are out. Voice calls and cloud deployment are extensions.
- Visual: a crate fills with the film's cast (card, drawers, review desk). Three objects are
  pushed outside a dashed line: a medical cross, a locked file, an envelope. Two wait on a
  side shelf: a phone with a sound wave, and a cloud. Labels: `in` · `out` · `later`.

### B12 — why this project
VO: Why this project? I want to learn what makes an AI system useful beyond one conversation. Remembering yesterday is one part. Knowing when it needs a person, and showing them the evidence, is the part I find interesting.
- Visual: a single card becomes a thread of cards. One card lifts out and travels to the review
  desk. Label: `beyond one chat`.

### B13 — existing versus new skills
VO: I already practise refining prompts and reviewing AI work. Planning this film, AI drafted, while I set requirements, asked for revisions, and decided what represents my project. New for me: persistent memory, permissions in code, approval tied to evidence, and held-out evaluation.
- Visual: two shelves. The `practised` shelf holds a prompt page and a check mark. The `new` shelf
  has four empty slots that fill with a drawer, a gate, a stamp, and a vault.

### B14 — what exists today vs. what I intend to build
VO: What exists today: this plan, this film, and a log of the decisions behind it. No code, no prototype, no results. What I intend to build: a runnable repository with the two-day replay, memory, a review screen, tests, and an evaluation report that shows where it still fails.
- Visual: two trays. `today` holds three solid pages: plan, film, log. `to build` holds only ghost
  outlines with dashed edges: repo, replay, review screen, tests, report. Nothing in it is
  shown as real.

### BOUT — outro
VO: DayThread. Aditya Raj.
- Visual: title `DayThread`, `Aditya Raj`, `github.com/aditya-raj-sde`, then a 1.0 s silent hold.
  (Needs a small toolkit change; see the notes.)

---

## Production notes (for Aditya)
- **Dropped bookends:** the key-terms card (each term is explained in the same breath instead)
  and the Your Turn composer, so the film ends on today versus to-build. Both can come back.
- **Outro:** the toolkit's outro card hardcodes `@NikBearBrown`, and the build check requires
  that card. The fix is a small, backward-compatible toolkit change: an optional name/handle
  prop. It would be recorded in `TOOLKIT-CHANGES.md` with a patch file.
- **Pronunciation to check by ear after audio:** "Aditya", "README", "SQLite", "DayThread",
  "Hallo".

# DayThread — pitch film script v2 (DRAFT for Aditya's review — the full film is not rendered)

v1 is archived at `drafts/SCRIPT-v1.md`. v2 applies Aditya's revision notes from 2026-10-14.

**Workflow and identity.** Skill: show-tell. This is Aditya's explicit local workflow choice, not
a claim of approval from Professor Bear. Where the assignment's identity rules conflict with
template defaults, the assignment wins; the exceptions are listed at the end.

**Voice.** Kokoro `am_onyx` reads Aditya's script. The film does not use the toolkit's "Liam"
persona. The opening says aloud that the voice is synthesized, and a caption repeats it on
screen.

**Cast.** No people on screen. The same objects run through the whole film: the **check-in
page** (raw transcript), the **summary page**, the **memory drawers**, the **separate check**
(a scan line), the coordinator's **review desk**, and the **gate** with its stamp.

**Captions.**
- ⓒ = the caption "Constructed — proposed workflow" stays on screen for the whole beat.
- Every beat also carries "Synthesized voice reading Aditya's script".

Lines starting `VO:` are the narration. Everything else is the visual plan.

---

### BIDEA — opening
VO: Hi, I'm Aditya Raj. This is DayThread, my proposed final project. You're hearing a synthesized voice reading my script.
- Visual: the hesitant writer types "DayThread", then "a proposed final project". No "Liam"
  greeting and no question card.

### B00 — what it is
VO: Nothing is built yet. DayThread would be a check-in assistant that remembers conversations across days, and turns concerning changes into evidence a home care coordinator can review.
- Visual: two check-in pages drop onto a thread, then a review desk appears at the thread's end.
  Labels: `DayThread` · `proposed`.

### B01 — day one ⓒ
VO: Here's the main story, with a fictional client. On day one, they mention just a little tumble. The raw transcript is kept apart from any summary.
- Visual: the check-in page draws its scribble lines. One line gets a terracotta dot and the
  label "a little tumble". The page files into a drawer of its own. Labels: `check-in` ·
  `raw transcript`.

### B02 — the failure that could sink it ⓒ
VO: Here's the failure that could sink it: the summary drops the tumble, so every later step relying on it misses it. I'll predict that, then trigger it on purpose.
- Visual: a shorter summary page appears with a visible gap where the tumble line was. It rides
  a conveyor through two later steps, and the gap rides with it. Labels: `summary` · `missed`.

### B03 — the separate check, when the check-in ends ⓒ
VO: When the check-in ends, a separate check reads the original words and creates an internal review item. It could miss unfamiliar wording or raise false alarms, so I'll test both.
- Visual: a scan line sweeps the raw transcript page (not the summary) and stops on the dot. A
  review item drops into the queue. Labels: `separate check` · `review item`.

### B04 — day two: memory, and the first thing that runs ⓒ
VO: On day two, the assistant asks about the tumble without the client repeating it, linked to the day-one words. That two-day replay is the first thing I'll make run.
- Visual: the Day 2 page arrives. A drawer opens, and an ink link draws from the Day 1 dot to
  Day 2. Labels: `Day 2` · `source link`.

### B05 — the coordinator's gate and the executor ⓒ
VO: A coordinator opens a simple local review page showing the concern, its excerpts, and the proposed action, then approves, refuses, or defers. A separate executor acts only if that approval still matches; for the course, delivery is simulated.
- Visual: a local web page, drawn as an illustration, sits on the review desk. It shows the
  concern, two excerpts, and three buttons. The stamp lands. A small executor block checks
  that the stamp matches the slips, and only then lets a parcel through to a "simulated" tray.
  Labels: `approve · refuse · defer` · `simulated`.

### B06 — permissions
VO: The assistant can read check-in history, add source-linked observations, and create review items. It can't silently overwrite past records, change agency-owned information, or contact anyone.
- Visual: the permission gate. Three parcels pass (read, add, review item). Three bounce back
  (overwrite, agency record, outbound message). Labels: `allowed` · `blocked`.

### B07 — real alternatives
VO: Fall detection and AI calls already exist. Lifeline's page says its fall detection doesn't catch every fall; DailyCall's pages describe daily AI calls with summaries for families.
- Visual: two trays, labelled `Lifeline` and `DailyCall`, with the caption "per their official
  pages". No logos.

### B08 — DayThread's proposed focus
VO: I'm not claiming they lack anything. DayThread's proposed focus is source-linked concerns, an independent transcript check, and a coordinator's decision, meant to help a coordinator understand changes without manually rebuilding several conversations.
- Visual: a third tray slides in, holding the thread, the scan line and the stamp. Labels:
  `proposed focus`.

### B09 — who opens it, first minute ⓒ
VO: I'm aiming for AI engineer roles, so a hiring reviewer should be able to run a labelled replay from the README within a minute, and inspect the two-day memory and one approval decision.
- Visual: a README page, then a terminal replay, then the Day 1 → Day 2 link, then the stamp.
  Labels: `README` · `replay`.

### B10 — course skills and planned evidence
VO: I'm designing it to demonstrate prompt contracts, a budgeted loop with clear stops, permissions in code, source-linked memory, and evaluation: with and without memory, on held-out cases set aside before tuning, plus at least five deliberate failures. These tests could demonstrate a controlled prototype, but wouldn't establish readiness for real care.
- Visual: a loop ring drains its budget slots, then stops. Two benches, `with memory` and
  `without`. A sealed vault holds the held-out cases, and five failure samples line up.

### B11 — scope
VO: The core is simulated text check-ins, in Python and SQLite. Clinical advice, real patient data, and autonomous outreach are out; voice calls and cloud deployment are extensions.
- Visual: a crate labelled `in`, three objects pushed `out`, and two on a `later` shelf.

### B12 — why this project
VO: I chose this because remembering yesterday is only part of the problem; knowing when a person needs to see it, with the evidence, is the part I find interesting.
- Visual: a single page becomes a thread. One page lifts out and travels to the review desk.

### B13 — existing versus new skills  ⚠ new-skills list PENDING Aditya's confirmation
VO: For this pitch, an AI assistant drafted and checked sources; I set requirements, required sources before any comparison, and cut overstated wording. New for me: persistent memory, permissions enforced in code, approval tied to evidence, and held-out evaluation.
- Visual: two shelves. `practised` holds the requirements page and a struck-out line. `new` has
  four empty slots that fill with a drawer, a gate, a stamp and a vault.
- Evidence for the first sentence: `FRICTIONAL.md`, entries for 2026-10-14. That covers the
  revision notes Aditya gave this session. It does not reconstruct earlier history or mention
  Week 1.

### B14 — what exists today vs. what I intend to build
VO: Today there's this plan, this film, and a decision log, but no DayThread prototype or evaluation results yet. I intend to build the repository, the two-day replay, the review page, tests, and an evaluation report that shows where it fails.
- Visual: two trays. `today` holds solid pages: plan, film, log. `to build` holds only dashed
  ghost outlines.

### BOUT — outro
VO: DayThread. Aditya Raj.
- Visual: `DayThread` and `Aditya Raj`, then a 1.0 s silent hold. No GitHub address until
  Aditya confirms it. No mascot.

---

## Template exceptions (assignment identity over toolkit defaults)
| Toolkit default | This film | Why |
|---|---|---|
| "Hallo. This is Liam, in for Bear." | "Hi, I'm Aditya Raj. This is DayThread, my proposed final project." | Aditya's own film; Aditya rejected the narrator persona |
| Persona "Liam (in for Bear)" | Synthesized voice (Kokoro `am_onyx`) reading Aditya's script, disclosed aloud and on screen | Honesty about the voice |
| Key terms card (BDEFS) | dropped | Aditya's decision; terms are explained inline |
| Your Turn composer (BHTF) | dropped | Aditya's decision; the film ends on today vs. to build |
| Outro reads "At Nik Bear Brown" + @NikBearBrown + mascot | "DayThread. Aditya Raj." | Aditya's name; needs an optional outro name setting (approved by Aditya; to be recorded in `TOOLKIT-CHANGES.md` when made) |
| PROFESSOR BEAR LAW portraits for people | no people on screen | Aditya's decision; course brief requires fictional personas |
| show-tell is "ADVANCED — Bear only" | used | Aditya's explicit local workflow choice, not Bear's sign-off |

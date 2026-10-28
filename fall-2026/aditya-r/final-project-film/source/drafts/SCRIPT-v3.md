# DayThread — pitch film script v3 (narration source for the film)

`film/make_sheet.py` reads the `VO:` lines straight from this file, so this file is the one
source of the narration. Earlier drafts: `drafts/SCRIPT-v1.md`, `drafts/SCRIPT-v2.md`.

**Changes from v2 (2026-10-14):**
- **B10 split in two.** v2's 51-word line became B10 (skills) and B11 (evaluation), so no beat runs
  far past ~15 s. Aditya's two required phrasings are kept word for word.
- **B12 scope.** Restored "memory, evidence-linked concerns, and human review" so the beat says
  what's *included* (question 5).
- **B07.** Now says Aditya *read their documentation* (Aditya confirmed reading S1–S4 on
  2026-10-14). It does not say anyone tested the products.
- **B14.** The new-skills list now uses Aditya's own answer-7 wording almost verbatim. Aditya
  didn't explicitly confirm the condensed v2 sentence. Aditya later confirmed this one
  (2026-10-14): "All of those skills are new to me."  "AI helped draft the material" also follows Aditya's answer 7.
- **Outro.** Shows DayThread, Aditya Raj, and github.com/aditya-raj-sde (Aditya's profile link,
  confirmed 2026-10-14). Spoken: "This was DayThread, by Aditya Raj."
- **Two rewordings for pronunciation, from measured audio.** Kokoro voiced "AI engineer roles" as
  "eye-engineer" (heard by faster-whisper base.en and confirmed in a short test), so B09 now says
  "roles as an AI engineer". It voiced the bare "DayThread. Aditya Raj." so badly that the
  transcriber heard "Day thread out of the garage", while "This was DayThread, by Aditya Raj." came
  out clean. The meaning is unchanged.

**Fixed rules for every beat:**
- **Voice.** Kokoro `am_onyx`, a synthesized voice reading Aditya's script. The film does not use
  the toolkit's "Liam" persona.
- **Captions** are italic and live in their own bands, apart from the scene headings:
  - Top band, every beat: *Synthesized voice reading Aditya's script*.
  - Bottom band, beats marked `[C]`: *Constructed — proposed workflow*.
  - Bottom band, B07: *From each company's own documentation, read 2026-10-14*.
  - Headings and labels stay inside y ∈ [−2.45, 2.30].
- **People.** None on screen.
- **Branding.** No instructor identity, channel credit, or mascot.
- **The gate** shows a terracotta stop light and stays visibly closed until a coordinator approves.

Lines starting `VO:` are the narration. Everything else is the visual plan.

---

### BIDEA — opening
VO: Hi, I'm Aditya Raj. This is DayThread, my proposed final project. You're hearing a synthesized voice reading my script.
- Visual: the title `DayThread`, then "a proposed final project" and "Aditya Raj". A thread draws
  under the title and three small pages hang from it.

### B00 — what it is [C]
VO: Nothing is built yet. DayThread would be a check-in assistant that remembers conversations across days, and turns concerning changes into evidence a home care coordinator can review.
- Visual: Day 1 and Day 2 check-in pages drop onto a thread. The thread runs on to a review desk.
  Labels: `Day 1` · `Day 2` · `coordinator`.

### B01 — day one [C]
VO: Here's the main story, with a fictional client. On day one, they mention just a little tumble. The raw transcript is kept apart from any summary.
- Visual: the check-in page draws its handwriting lines. A terracotta dot and "a little tumble"
  land on one line. Memory drawers open, and a copy of the page slides into its own drawer.
  Labels: `check-in` · `"a little tumble"` · `raw transcript`.

### B02 — the failure that could sink it [C]
VO: Here's the failure that could sink it: the summary drops the tumble, so every later step relying on it misses it. I'll predict that, then trigger it on purpose.
- Visual: a summary page arrives with a dashed empty row. Two later-step cards copy it, gap and
  all. Labels: `summary` · `missed` · `later steps`.

### B03 — the separate check, when the check-in ends [C]
VO: When the check-in ends, a separate check reads the original words and creates an internal review item. It could miss unfamiliar wording or raise false alarms, so I'll test both.
- Visual: a terracotta scan line sweeps the ORIGINAL page and stops on the tumble line. A review
  item drops into the review queue. Labels: `separate check` · `review item`.

### B04 — day two: memory, and the first thing that runs [C]
VO: On day two, the assistant asks about the tumble without the client repeating it, linked to the day-one words. That two-day replay is the first thing I'll make run.
- Visual: the Day 2 page writes a question line, and an ink link draws back to Day 1's dot. A replay
  button appears. Labels: `Day 1` · `Day 2` · `first to run`.

### B05 — the coordinator's gate and the executor [C]
VO: A coordinator opens a simple local review page showing the concern, its excerpts, and the proposed action, then approves, refuses, or defers. A separate executor acts only if that approval still matches; for the course, delivery is simulated.
- Visual: a local web page, drawn as an illustration, shows excerpts. Beside it are three
  options: approve, refuse, defer. The gate is closed (barrier down, stop light lit). The approve
  box gets a check, the executor's match check turns on, the barrier lifts, and the parcel passes
  to "simulated". Labels: `approve` · `refuse` · `defer` · `simulated`.

### B06 — permissions [C]
VO: The assistant can read check-in history, add source-linked observations, and create review items. It can't silently overwrite past records, change agency-owned information, or contact anyone.
- Visual: the record binder takes new pages on top, each with a check. An overwrite attempt
  bounces off the binder. An envelope bounces off the closed gate. Labels: `append only` ·
  `no outreach`.

### B07 — real alternatives
VO: Fall detection and AI calls already exist. I read their documentation: Lifeline says its fall detection doesn't catch every fall, and DailyCall describes daily AI calls with summaries for families.
- Visual: two plinths. One holds a pendant whose signal reaches a response tower. The other holds
  a phone and a summary page. Labels: `Lifeline` · `DailyCall`. No logos.

### B08 — DayThread's proposed focus [C]
VO: I'm not claiming they lack anything. DayThread's proposed focus is source-linked concerns, an independent transcript check, and a coordinator's decision, meant to help a coordinator understand changes without manually rebuilding several conversations.
- Visual: a third plinth, `DayThread · proposed`, slides in. Three check-in pages link to one
  concern by a thread, and the concern goes to the gate. Labels: `Lifeline` · `DailyCall` ·
  `DayThread · proposed`.

### B09 — who opens it, first minute [C]
VO: I'm aiming for roles as an AI engineer, so a hiring reviewer should be able to run a labelled replay from the README within a minute, and inspect the two-day memory and one approval decision.
- Visual: a README page, then a terminal replay, then the Day 1 → Day 2 link, then a stamp, with a
  one-minute dial sweeping. Labels: `README` · `replay` · `one minute`.

### B10 — course skills [C]
VO: I'm designing it to demonstrate prompt contracts, a budgeted loop with clear stops, permissions in code, source-linked memory, and evaluation.
- Visual: a contract page, then a loop ring that drains its budget slots and stops. Labels:
  `contract` · `budget` · `stop`.

### B11 — planned evidence [C]
VO: Evaluation compares the workflow with and without memory, on held-out cases set aside before tuning, plus at least five deliberate failures. These tests could demonstrate a controlled prototype, but wouldn't establish readiness for real care.
- Visual: two trays (with and without memory), a sealed vault of held-out cases, and five failure
  cards in a row. Labels: `with / without memory` · `held-out` · `5 failures`.

### B12 — scope [C]
VO: The core is simulated text check-ins, memory, evidence-linked concerns, and human review, in Python and SQLite. Clinical advice, real patient data, and autonomous outreach are out; voice calls and cloud deployment are extensions.
- Visual: an open crate takes a page, a drawer and a check. Three items sit beyond a dashed line:
  a medical cross, a locked file, an envelope. A shelf holds a cloud and a phone. Labels: `in` ·
  `out` · `later`.

### B13 — why this project
VO: I chose this because remembering yesterday is only part of the problem; knowing when a person needs to see it, with the evidence, is the part I find interesting.
- Visual: one page becomes a thread of pages. One page lifts out and travels to the review desk.
  Label: `beyond one conversation`.

### B14 — existing versus new skills
VO: For this pitch, AI helped draft the material and check sources; I set requirements, required sources before any comparison, and cut overstated wording. New for me: persistent memory across conversations, permissions enforced in code, human approval tied to the evidence shown, and evaluation on cases kept separate from development.
- Visual: two shelves. `practised` holds a requirements page, a source page, and a struck line.
  `new` has four empty slots that fill with a drawer, a gate, a check, and a vault.

### B15 — what exists today vs. what I intend to build
VO: Today there's this plan, this film, and a decision log, but no DayThread prototype or evaluation results yet. I intend to build the repository, the two-day replay, the review page, tests, and an evaluation report that shows where it fails.
- Visual: two plinths. `today` holds three solid pages. `to build` holds only dashed ghost
  outlines.

### BOUT — outro
VO: This was DayThread, by Aditya Raj.
- Visual: `DayThread`, `Aditya Raj`, `github.com/aditya-raj-sde`, and the thread, then a 1.0 s
  silent hold. No mascot, no channel handle.

---

## Template exceptions (assignment identity over toolkit defaults)
| Toolkit default | This film | Why |
|---|---|---|
| "Hallo. This is Liam, in for Bear." / persona "Liam (in for Bear)" | "Hi, I'm Aditya Raj…", disclosed synthesized voice | Aditya's own film; Aditya rejected the narrator persona |
| BIDEA = `BrutalistHesitantWriter` (Remotion) | a drawn Manim title beat | v2 dropped the naive question the writer corrects. A drawn beat also carries the disclosure caption |
| Key terms card (BDEFS), Your Turn (BHTF) | dropped | Aditya's decision |
| Outro `ClaudeTitleOutro` (@NikBearBrown + mascot, "At Nik Bear Brown") | a drawn Manim outro: DayThread · Aditya Raj · github.com/aditya-raj-sde | Aditya: no instructor identity, channel credits, or unrelated mascot. A drawn outro needs **no toolkit change**, so the approved optional handle setting was not needed. `bookend_check.py`'s outro rule therefore fails by design (recorded in the gate reports) |
| PROFESSOR BEAR LAW portraits for people | no people on screen | Aditya's decision; the course brief requires fictional personas |
| show-tell is "ADVANCED — Bear only" | used | Aditya's explicit local workflow choice, not Bear's sign-off |

# PEDAGOGY: Electricity Supplier Check (pitch film)

**Status:** BUILT 2026-10-14. The narration (v2 draft by Claude from the brief) was approved by Hemanth Rayudu without edits. Two voice-only respellings followed a whisper check; see SOURCES.md. Master: `exports/landscape/electricity-supplier-check-pitch.mp4`, 3:38.
**Narrator:** Hemanth Rayudu, first person. Voice: Kokoro `am_onyx`.
**Source of truth:** `../../PROJECT-BRIEF.md`, checked against the AG report and the National Grid tariff on 2026-10-14.
**Governing rules:** the assignment PDF, then the narrator's rules 1–9, then toolkit defaults.

## What changed from v1, and why

v1 followed the local ai-explainer skill: lists and columns on screen, with the voice trimmed to fit. That breaks the assignment, which says the pitch format is *"one simple drawn picture per beat, minimal on-screen text, narration carrying the explanation"* (the show-tell format). v2 reverses it:

- **The voice carries every idea.** The assignment's required content is now spoken, not left on screen:
  - Q2's "saves a household the work of…" sentence (B06).
  - Q4's course skills and the reviewer's conclusion (B08).
  - The target role (B05).
  - The stack (B07).
- **The screen shows one simple drawing per beat**, with at most three labels of one to three words each. Exceptions: the one hero number (`$738.7 million`), the CONSTRUCTED/PROPOSED tags, and source captions.
- **The same small cast of objects runs through the whole film:** the drawn bill, the "$" slip, the tool box, the rate table, the verifier gate and the eval report.
- **The AG source caption now says when it was obtained** ("downloaded 2026-10-14"), as the honesty rule requires for data shown.
- **"Who it is for" is two beats** in the same position: the end user (B04) and the portfolio reader (B05). Brief §3 names both readers.

## Beat map

| Beat | Assignment question | Brief | One picture | Tag |
|---|---|---|---|---|
| B00 | (frame) | title | Manim title card: title, name, the drawn bill | — |
| B01 | Q7 / Q2 setup | §7, §2 | a constructed bill printing the real basic service rates; a coin slips out | CONSTRUCTED |
| B02 | Q2 why care | §2 | coin stack; "$738.7 million"; bracket over the lower 51.45% | source caption |
| B03 | Q1 | §1 | bill into a pole transformer (the tool); a GitHub folder fills with the parts | PROPOSED |
| B04 | Q3 end user, first 60 s | §3 | house plus pile of bills; bill into a laptop; "$X more" | CONSTRUCTED MOCK-UP (on screen) |
| B05 | Q3 target role, portfolio reader | header, §3 | cursor opens the GitHub folder; report rows matched to calculator numbers; rerun loop | — |
| B06 | Q2 alternatives and difference | §2 | offers board · queue at a clock · transformer gives "$" at once | site captions |
| B07 | Q1/Q4 mechanism, stack | §4, Will exist | conveyor: scan → schema → calculator → page → verifier gate | CONSTRUCTED |
| B08 | Q4 skills, evidence, conclusion | §4 | five skill objects on a rail; three evidence objects on a shelf | — |
| B09 | Q5 | §5 | three panels: in / out (crossed-out contract) / first; two empty check boxes | not run yet |
| B10 | Q6 | §6 | period bar across Aug 1, 2026; wrong block; "can't verify" stamp | CONSTRUCTED |
| B11 | Q7 | §7 | "have" and "new" panels with skill objects | — |
| B12 | exists vs will exist | lists | empty panel vs dashed outlines of the transformer and parts | — |

All seven questions are answered in the voice.

## Structure checks

| Rule | This reel |
|---|---|
| Assignment: one picture per beat, minimal text, the voice explains | Met in the draft: one Manim drawing per body beat, at most 3 labels |
| Assignment: constructed material labelled on screen | B01, B04, B07, B10 CONSTRUCTED; B03 PROPOSED |
| Assignment: any Claude response is real and dated | None is shown |
| Assignment: data shown says when it was obtained | B02 caption: "downloaded 2026-10-14" |
| Assignment: narrate as yourself | First person throughout; no persona, chip, handle or credit line |
| Toolkit bookends (hesitant writer, key terms, Your Turn, channel outro) | Not used, by narrator rules 1, 4 and 8 |
| Show-tell guidance: beats usually 5–12 s, past ~15 s often two ideas | Body beats run ~11–24 s. Kept as one beat each to follow the narrator's beat order; can be split at his request. |
| Duration is an output | Measured: 211.54 s of narration; the master is 3:32 (211.8 s), inside the 2–4 min window and not padded. |

## Honesty checks

- **Tense (approved by the narrator):**
  - Past tense only for real events: my overpayment, the AG finding, the alternatives I looked at, my prior work.
  - Present tense for the alternatives that exist today.
  - "Will" for everything about the tool.
- **No real bill** is shown. The drawn bill has no numbers, no line items and no logo.
- **No invented numbers:**
  - "$X" stays a placeholder.
  - The formula row on B04 is grey blocks, because the brief doesn't state the formula.
  - B09's check boxes stay empty, because nothing has run.
  - B10 shows no tariff rates.
- **Only brief claims.** Each beat's `brief_ref` names its section.

## Evidence discipline

| Claim | Source | Verdict |
|---|---|---|
| $738.7 million more than basic service, last decade | AG report p. 2, Table ES-1 (July 2015–June 2025) | OK. Brief corrected from "over $738.7 million" on 2026-10-14. |
| 10–30% suppliers account for more than half of losses | AG report p. 4 (51.45%) | OK. The film says "more than half". |
| Energy Switch Massachusetts helps you shop; doesn't read your bill | Brief §2; energyswitchma.gov | Brief claim, **not re-verified against the live site** |
| Town energy coaches check whether you're on competitive supply | Brief §2; City of Newton page | Brief claim, **not re-verified against the live page** |
| Test bill crossing Aug 1, 2026 | Brief §5; tariff M.D.P.U. No. 1-26-H effective Aug 1, 2026 | OK |

## Decisions (narrator, 2026-10-14)

1. **B04 formula:** option (a), grey placeholder blocks with no readable formula.
2. **Toolkit:** updated to upstream `519fcbb`, which includes the show-tell skill.
3. **B01 bill:** a constructed drawing with no supplier amounts. It prints the real residential basic service rates from `meco_basic_service.pdf`, with the tariff caption. Claude first put them beside the bill; the narrator chose to have them on it. The bill is tagged CONSTRUCTED, so it makes no claim about real bill layout.
4. **Past tense for real events, and the narrator's name on the title card:** approved. The title card was rebuilt larger, and B00's voice spells the name "Hey-month Rah-you-doo" so Kokoro says it as the narrator does.
5. **Worked example and Your Turn:** not in the narrator's beat order, so left out.
6. **Visual cast:** the show-tell kit's cardboard boxes were replaced with an electricity cast at the narrator's request: a pole-mounted transformer as the tool, a coin stack, an offers board, a GitHub folder and plain panels.
7. **Spoken disclaimers removed:** "This bill is a drawing, not mine" (B01) and "That screen is a constructed mock-up" (B04). The on-screen CONSTRUCTED tags stay, as the assignment requires.
8. **B05 and B07 reworded:** B05 now says what the hiring manager opens (the GitHub repository and its evaluation report) and how the check works. B07 says Claude Code builds the project and is how the agent calls Claude. The brief was updated first.

VERDICT: PASS. All toolkit gates pass (see CHECKS-REPORT.md). The bookend check fails on the channel outro by design (narrator rule 1).

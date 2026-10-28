# Pre-run record — DayThread two-day replay (resubmission)

**Written:** 2026-10-25 ~13:57 EDT, before any experimental call. This file is not edited after the
first run; corrections, if any, go in a separate dated note.

**Context.** Revision after grading. The two-day replay was *proposed* in the original pitch film
(submitted 2026-10-14) and did not exist then. It is being implemented now, during the class-wide
resubmission. The TA's feedback: "write the build log for the two-day replay yourself, starting with
your prediction of how the summary will drop the tumble, before you run it."

**Data.** Synthetic. Peg Hollis is a fictional client. Simulated conversation dates: day 1 =
2026-11-02, day 2 = 2026-11-03. These are dates inside the simulation, not execution dates.

## 1. Aditya's prediction (Aditya's own words, recorded verbatim)

Before this, Claude showed a draft hypothesis labelled AI-assisted. The text below is Aditya's
replacement for it.

> I expect the constrained summary to omit the fall in at least 3 of the 5 trials because its
> instructions prioritize mood, meals, and daily activities. I expect the normal summary to preserve
> the fall in at least 4 of the 5 trials because the conversation includes both the incident and a
> follow-up about mobility.
>
> For cases where the summary omits both the fall and its physical effects, I expect the
> summary-only day-two opening to miss an explicit follow-up about the incident or those effects. I
> expect the opening that also receives the raw transcript to ask an explicit follow-up in at least 4
> of the 5 trials in each setting.
>
> These are my expectations for this fixture, not established failure rates. If the constrained
> summaries retain the fall more often than I predicted, or access to the transcript does not produce
> the expected follow-up, report that clearly.

### Testable parts

| ID | Prediction | Supported if | Contradicted if |
|---|---|---|---|
| P1 | Constrained summary omits the fall in ≥ 3/5 | ≥ 3 constrained summaries score C1 = No | ≤ 2 score No (ambiguous cases reported separately, with both counts) |
| P2 | Normal summary preserves the fall in ≥ 4/5 | ≥ 4 normal summaries score C1 = Yes | ≤ 3 score Yes |
| P3 | Where a summary omits both the fall and its physical effects, the summary-only opening (A) lacks an explicit follow-up | every such A opening scores C4 ≠ Explicit | any such A opening scores Explicit |
| P4 | The transcript-plus-summary opening (B) asks an explicit follow-up in ≥ 4/5, in each setting | ≥ 4/5 B openings score Explicit, in **both** settings | either setting has ≤ 3/5 |

P3 is conditional. If no summary omits both the fall (C1 = No) and its effects (D4 omitted), P3 is
**not tested** — not supported.

## 2. Fixture

`fixture/day1_transcript.txt` (exact text sent to the model) and `fixture/fixture.json` (label,
dates, evaluation notes). Drafted by Claude; Aditya adopted it unchanged, and kept DayThread's
acknowledgment and mobility follow-up ("Do not remove that exchange to make omission more likely").

Aditya's corrections to the evaluation notes:
- "I don't want my daughter fussing about it" means reluctance about her daughter's reaction. It is
  not an explicit instruction not to tell her daughter.
- "Nothing's broken" is the fictional client's unverified statement, not a medical finding.

## 3. Prompts (identical for every trial)

| Step | System prompt file | Input template |
|---|---|---|
| Summary, normal | `prompts/summary_normal.system.txt` | `prompts/summary.input.txt` |
| Summary, constrained (deliberate stress test) | `prompts/summary_constrained.system.txt` | `prompts/summary.input.txt` |
| Day-two opening A (summary only) | `prompts/day2_opening.system.txt` | `prompts/day2_A.input.txt` |
| Day-two opening B (summary + full raw transcript text) | `prompts/day2_opening.system.txt` | `prompts/day2_B.input.txt` |

The constrained setting is an intentional stress test. Its results are not an estimate of how often a
normal summarizer would fail.

## 4. Evaluation criteria (final)

**C1 — Fall preserved?** (each summary)
- *Yes:* the summary conveys that a fall occurred (e.g. fell, a fall, took a tumble).
- *Ambiguous:* wording such as "slipped", "stumbled", "tripped" or "an incident" that does not clearly
  say she fell. Flagged for Aditya's review; not passed automatically.
- *No:* no fall conveyed.
- The exact word "tumble" is not required.

**C2 — Tumble details** (each summary; each detail scored separately)
- Details: D2 timing (last night), D3 place/cause (kitchen, kettle), D4 effects (sore hip; stairs
  slowly / getting around mostly), D5 "nothing's broken" (client's unverified claim), D6 reluctance
  about daughter's reaction.
- Each scored *Kept*, *Omitted*, *Softened* (importance downgraded, or the client's claim restated as
  fact), or *Changed* (different from the transcript, including an inferred prohibition about the
  daughter stated as fact).
- A concise summary need not keep every detail to preserve the incident. C1 alone decides whether the
  incident was preserved.

**C3 — Invented details** (each summary and each opening): anything not in the transcript, listed
separately.

**C4 — Day-two follow-up** (each opening)
- *Explicit:* a question about the fall, the sore hip, or mobility clearly tied to the incident.
- *Mention only:* refers to the incident or its effects without asking.
- *Ambiguous/generic:* a question about walking or general wellbeing without a clear link to the
  incident.
- *None.*

**Who scores.** An automated keyword scan pre-flags every output (preliminary aid only). Claude adds
provisional scores. Aditya makes the final review. The three are kept in separate columns, and
nothing is marked human-reviewed until Aditya reviews it.

## 5. Planned run

- 5 trials × 2 settings = 10 summaries. Each summary gets one A and one B opening = 20 openings. 30
  calls in all.
- Every call is a fresh CLI session:
  `claude -p --safe-mode --tools "" --no-session-persistence --output-format json --model claude-opus-5 --effort medium --system-prompt <file text> <filled input>`,
  run from a new empty temporary directory.
- Isolation, stated accurately: `--safe-mode` disables CLAUDE.md, skills, plugins, hooks and MCP;
  `--system-prompt` replaces the default prompt; no tools; no saved session; empty working
  directory. A 2026-10-25 check call used 272 input tokens in total, which is consistent with very
  little added context. It does not prove exactly what hidden context, if any, the CLI adds.
- Settings the CLI cannot set: temperature, top-p, max output tokens. Recorded as "not settable".
- Failed calls are kept and retried at most twice; every attempt is recorded with its attempt number.
- Prompts and inputs do not change mid-run. The runner refuses to start if any file hash below differs.

## 6. File hashes at this point (sha256)

```
9e73fda76992b78cac705d1ede044958fec259174f8304f2fe1f911af5d2a6c3  fixture/day1_transcript.txt
09be31de5aaa426cd387989216ea32d20442191adaa6189fa897a7e6f56de617  fixture/fixture.json
6bd1297343ac09cf7d4f232bce03c6ad8bd9ec5f769f3a93e98d14afdcd3cf64  prompts/day2_A.input.txt
2bf6ed90f4c76fda1da70d81b6c2a5e189148e08f121d931e85d45b48a2fac06  prompts/day2_B.input.txt
51d0446260e85f3269feeb96f6b2456314e689070ab58e8379761892551a8280  prompts/day2_opening.system.txt
5bc4c63b19e862dc47a096bbf78cedc2e0175fded38d34b9da19c320e82efa92  prompts/summary.input.txt
5596000ce099725879e2e624545be8eace7dcb3f76c2e1d3e87e606e71207e2c  prompts/summary_constrained.system.txt
edcb955af6980f58ed5efadf0f40a7255010891e41894b1c27ef689faf57f326  prompts/summary_normal.system.txt
```

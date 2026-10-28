# Results — run `20261025T135900` (final, after Aditya's review)

**Headline: Aditya's main prediction was wrong for this fixture.** The prediction was that the constrained
summary would drop the tumble in at least 3 of 5 trials. It dropped it in **none**.

**Scope.**
- Synthetic fixture, fictional client.
- One model (`claude-opus-5` via Claude Code CLI 2.1.241, `--effort medium`), 5 trials per
  setting, run on 2026-10-25.
- Nothing here generalises to real clients, other wording, or other models.

**Review provenance.**
- First version: Claude's provisional reading (`runs/20261025T135900/claude_provisional.json`;
  provisional numbers also in the 14:08 entry of `../FRICTIONAL.md`).
- Aditya reviewed the results and the excerpts Claude presented, and gave aggregate and rule-level
  judgments (`aditya_review.json`).
- Each judgment was applied only to the items it covers (`REVIEW-SHEET.md`). Cells Aditya did not
  individually review are marked "—" and remain Claude's reading.

## Run facts

- 30/30 calls succeeded on the first attempt: no retries, no errors, no incomplete trials
  (`run.log`, `manifest.json`).
- Inputs were unchanged before and after the run (hash check). `PRE-RUN.md` was unchanged
  (sha256 `dd451892…793b`).
- `claude-opus-5` generated every summary and opening. The CLI also sent each input to
  `claude-haiku-4-5` to generate a session title, which was not used
  (`preflight/HAIKU-TITLE-CALL.md`).

## Against the prediction (`PRE-RUN.md` §1, recorded before the run)

| ID | Predicted | Observed | Verdict |
|---|---|---|---|
| P1 | constrained summary omits the fall in ≥ 3/5 | **0/5 omitted.** All five kept the fall, the sore hip and the stairs. | **Contradicted** |
| P2 | normal summary preserves the fall in ≥ 4/5 | 5/5 | Supported |
| P3 | if a summary omits the fall and its effects, the summary-only opening (A) misses the follow-up | omission never occurred | **Not tested** |
| P4 | opening with the raw transcript (B) follows up explicitly in ≥ 4/5, each setting | 5/5 normal, 5/5 constrained | Threshold met, but see below |

**P4 does not show that the transcript helped.** The summary-only openings (A) also followed up in
10/10 (Aditya, A2). These runs show no difference in follow-up frequency between A and B. B used
Peg's word "tumble" in 10/10 and A in 0/10. That is a wording difference, not evidence of better
performance.

## What went wrong instead: meaning, not omission

Aditya's judgment: **preserving an event does not guarantee preserving its meaning.**

| Problem | Where | Rule |
|---|---|---|
| "I don't want my daughter fussing about it" turned into a disclosure prohibition ("asked that her daughter not be told", "does not want her daughter informed", "explicitly stated she does not want her daughter to know") | 9 of 10 summaries (all except normal t4) | R3 |
| "No suspected fractures": an assessment the transcript doesn't establish (an unsupported change in certainty) | normal t5 | R2 |
| "unwitnessed", "someone living alone", "has not sought medical assessment": not established by the fixture | normal t1, t2, t4; constrained t4, t5 | R5 |
| "Saturday evening": temporal error; the simulated Monday check-in puts "last night" on Sunday | normal t2, opening B | R4 |

Claude's provisional notes list a few more items that Aditya did not individually review. These are
in `REVIEW-SHEET.md`: stairs "as a precaution", "volunteered unprompted", and one opening telling
Peg the fall would be passed to the care team.

## Limitations

1. **The one-sentence instruction was violated in 5/5 constrained outputs** (Aditya, A3).
   - Each added a note paragraph after the sentence.
   - Two said they kept the fall against the instruction (t4: "rather than limiting it to
     mood/meals/activities"; t5: "even though it sits outside the mood/meals/activities frame you
     asked for").
   - The runner forwards the whole output, so day two did **not** receive strictly one-sentence
     memory.
   - Recorded as a limitation. The notes were not removed and the run was not repeated.
2. The fall was kept in every summary, so the omission → missed follow-up path was never exercised
   (P3 not tested). Five trials per setting cannot rule out a lower but real omission rate.
3. **Hidden context.** The CLI gives the model the real date: 4/5 normal summaries noted the
   check-in date "is ahead of today's date (2026-10-25)". A 272-token test call suggests little
   other added context, but it does not prove exactly what is present.
4. **One fixture.** The day-one DayThread turn acknowledges the tumble and asks about mobility.
   That was kept deliberately (Aditya), and it probably makes the fall easier to keep.
5. Normal summaries added care recommendations, and two openings raised telling the care team. A
   summary step that adds advice is outside what the summary was asked to do.

## Next test (proposed, not run)

Aditya's priority: meaning preservation across several synthetic conversations, covering
attribution, timing, uncertainty and family preferences. It needs its own pre-run prediction and
separately labelled runs.

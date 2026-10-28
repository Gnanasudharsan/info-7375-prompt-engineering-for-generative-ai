# FACTCHECK — DayThread pitch film

DayThread is a **proposed** project. No prototype exists. **v4 (2026-10-25):** B04 and B15 now report
one real result, from the minimal replay run during the resubmission (`../replay/RESULTS.md`). Every
other claim reports no observed result. Beats that illustrate the proposed workflow carry the on-screen caption "Constructed — proposed
workflow". Every frame carries "Synthesized voice reading Aditya's script".

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | BIDEA | Aditya Raj; DayThread is a proposed final project; the voice is synthesized | PASS | Aditya's brief, 2026-10-14; voice = Kokoro `am_onyx` | Disclosed aloud and on screen |
| 2 | B00 | "Nothing is built yet." DayThread *would* remember conversations and turn concerning changes into evidence for a coordinator | PASS (stated as a proposal) | Aditya's answer 1 | Conditional "would"; [C] caption |
| 3 | B01 | Fictional client mentions "a little tumble"; the raw transcript is kept apart from any summary | EXEMPT (constructed) | Aditya's answer 6 + design decision, 2026-10-14 | [C] caption; fictional client |
| 4 | B02 | The summary dropping the tumble is the failure that could sink it; it will be predicted and triggered on purpose | EXEMPT (planned) | Aditya's answer 6 | Future tense; not shown as an observed failure |
| 5 | B03 | The separate check runs when the check-in ends; it could miss unfamiliar wording or raise false alarms | EXEMPT (planned) | Aditya's design decision, 2026-10-14; answer 6 | [C] caption |
| 6 | B04 | Day two asks about the tumble without the client repeating it (proposed workflow, drawn); "a first, minimal version of that two-day replay ran during my revision" | PASS (v4) | Drawing: Aditya's answer 5. Replay: `replay/runs/20261025T135900/` (30/30 calls, 2026-10-25) | [C] caption kept on the drawing; "minimal" because the replay lacks source-linked memory, the separate check and the record-change test |
| 7 | B05 | A local review page (approve / refuse / defer); a separate executor acts only if the approval still matches; delivery simulated for the course | EXEMPT (planned) | Aditya's design decisions, 2026-10-14 | Gate drawn closed until approval; "simulated delivery" label |
| 8 | B06 | Can: read check-in history, add source-linked observations, create review items. Cannot: silently overwrite past records, change agency-owned information, contact anyone | EXEMPT (planned policy) | Aditya's design decisions, 2026-10-14 | [C] caption |
| 9 | B07 | Lifeline says its fall detection doesn't catch every fall | PASS | S1, verbatim: "Fall detection technology does not detect 100% of all falls." Read by Aditya 2026-10-14 | Attributed to their documentation |
| 10 | B07 | DailyCall describes daily AI calls with summaries for families | PASS | S2/S3: "AI-generated phone calls for daily check-ins"; "Helpful summaries after calls"; "Conversation summaries and highlights". Read by Aditya 2026-10-14 | Attributed; caption "From each company's own documentation, read 2026-10-14" |
| 11 | B07 | "I read their documentation" | PASS | Aditya's confirmation, 2026-10-14 (documentation only; no product tested) | — |
| 12 | B08 | "I'm not claiming they lack anything"; DayThread's *proposed* focus; benefit is *meant* to help | PASS (scoped) | SOURCES.md analysis, accepted by Aditya 2026-10-14 | No comparative or measured claim |
| 13 | B09 | Target role AI engineer; a reviewer *should be able to* run a labelled replay within a minute | EXEMPT (goal) | Aditya's answer 3 | Stated as a goal |
| 14 | B10 | Skills it is designed to demonstrate | EXEMPT (plan) | Aditya's answer 4 | "I'm designing it to demonstrate" (Aditya's wording) |
| 15 | B11 | Evaluation plan; "could demonstrate a controlled prototype, but wouldn't establish readiness for real care" | EXEMPT (plan) | Aditya's answer 4 and wording | — |
| 16 | B12 | Core / excluded / extensions; Python and SQLite | EXEMPT (plan) | Aditya's answers 1 and 5 | — |
| 17 | B13 | Motivation | PASS | Aditya's answer 7 | — |
| 18 | B14 | AI helped draft and check sources; Aditya set requirements, required sources before any comparison, cut overstated wording | PASS | FRICTIONAL.md, 2026-10-14 entries | Uses only this session's logged revisions |
| 19 | B14 | New skills list | PASS (Aditya's own answer-7 wording) | Aditya's answer 7; Aditya confirmed 2026-10-14: "All of those skills are new to me." | — |
| 20 | B15 | Exists today: plan, film, decision log, and a minimal replay run with a fictional client | PASS (v4) | This folder; `replay/` | Caption "Replay run 2026-10-25 · synthetic data · fictional client" |
| 20a | B15 | "I predicted a summary told to focus on mood, meals and activities would drop the tumble; in five trials it never did"; label "prediction: wrong" | PASS (v4) | `replay/PRE-RUN.md` §1 (P1: ≥ 3/5); `replay/RESULTS.md` (0/5 omitted; Aditya's review A1) | Says the prediction was wrong; does not claim omission was shown |
| 20b | B15 | "most summaries changed what she meant about her daughter" | PASS (v4) | `replay/RESULTS.md`: 9 of 10 summaries, judged Changed under Aditya's rule R3 | "most" = 9/10 across both settings |
| 20c | B15 | Still to build: repository, review page, separate check, tests, evaluation report | PASS (plan) | `PROJECT-BRIEF.md` "Will exist" | — |
| 21 | BOUT | DayThread, Aditya Raj, github.com/aditya-raj-sde | PASS | Aditya's confirmation, 2026-10-14 (profile link, not the assignment folder) | — |

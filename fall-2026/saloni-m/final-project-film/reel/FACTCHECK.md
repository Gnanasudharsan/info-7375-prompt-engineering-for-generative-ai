# FACTCHECK.md — OPT Countdown: Final Project Pitch

Every factual claim spoken or shown, with its verdict and source. Sources of record:

- **The prototype:** `the-reallocation-engine`, branch `contrib/2026fa-salonimathure20-opt-countdown`, commit `81d0161` (PR nikbearbrown/the-reallocation-engine#48, open, checked through the GitHub API on 2026-10-13).
- **The re-run on 2026-10-13** (Node 20.20.2): `node --test scripts/contrib/2026fa/salonimathure20-opt-countdown/` printed `# pass 12 # fail 0`. `node scripts/contrib/2026fa/salonimathure20-opt-countdown/opt-countdown.mjs` printed `runway 53 days … 8 roles → scored 6 (Apply 1 · Consider 2 · Skip 3) · blocked for a human 2`. The regenerated report differed from the committed one only in timestamps. Both outputs are saved in `../evidence/rerun-2026-10-13.txt`.
- **The worked run (2026-10-03):** `course/2026fa/submissions/salonimathure20/WORKED-RUN.md`, `CHANGE-BRIEF.md`, `DOMAIN-JUSTIFICATION.md`.

Verdicts: PASS (checked against the source), EXEMPT (a plan or an opinion, said in "will" form, or a labelled sketch).

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | BIDEA | Part of it exists as a prototype; most of it doesn't yet | PASS | the prototype exists (commit 81d0161); the "Will exist" list in PROJECT-BRIEF.md | — |
| 2 | B00 | OPT Countdown *will be* a command-line tool in a public repo | EXEMPT | a plan, said in "will" form | the picture carries the on-screen tag "constructed sketch" |
| 3 | B01 | 12 of 12 tests passed, re-run 2026-10-13 | PASS | rerun-2026-10-13.txt | on-screen tag "real run · 2026-10-13" |
| 4 | B01 | 8 postings, fictional student, 53 days left | PASS | rerun output `runway 53 days`, `8 roles`; persona `ananya-rao-example` is fictional (WORKED-RUN.md) | — |
| 5 | B01 | 1 apply, 2 network first, 3 skip, 2 blocked | PASS | `Apply 1 · Consider 2 · Skip 3 · blocked 2` | "Consider" is shown as "network", matching the report's next action (informational chat before applying) |
| 6 | B02 | About 20 minutes per posting by hand | PASS (as an estimate) | DOMAIN-JUSTIFICATION.md: "I estimate about 20 minutes per posting" | spoken as "an estimate, I haven't timed it"; on screen as "20 min · estimate" |
| 7 | B03 | The liveness checker called a fake job link active | PASS | WORKED-RUN.md line 56: `✅ active https://boards.greenhouse.io/klaviyo/jobs/1000000003` | — |
| 8 | B03 | The dead link redirects to a live careers page | PASS | CHANGE-BRIEF.md Revisions: "The URL redirects to Klaviyo's careers search page" | — |
| 9 | B03 | Greenhouse's job API returned 404 | PASS | WORKED-RUN.md line 72: `404 klaviyo/1000000003` | — |
| 10 | B03 | In my tool the API answer wins | PASS | recipe gate G3; the card: "the Greenhouse API status wins when present" | — |
| 11 | B04 | HubSpot has no row; DraftKings has blank H-1B fields | PASS | report reason codes `no-company-row`, `no-h1b-record-joined` | — |
| 12 | B04 | The prototype marks them blocked | PASS | report: both rows **Blocked** | — |
| 13 | B05 | OPT allows 90 days of unemployment | PASS | persona `unemployment_ceiling` 90; the recipe card | immigration rules otherwise out of scope (said in B08) |
| 14 | B05 | 60-day hiring time vs 53 days left; Klaviyo and Toast skipped for that | PASS | report: "gated: timeline ≈ 0.000", lag 60 d, slack −7 d | the 60 days is an assumed lag (said in B09) |
| 15 | B06 | Who opens it and what they do | EXEMPT | plan | tag "constructed sketch" |
| 16 | B07 | What it would prove; "would not prove it gets anyone hired" | EXEMPT | plan and an honest limit | tag "constructed sketch" |
| 17 | B08 | Out: immigration advice; first: its own repo | EXEMPT | plan | — |
| 18 | B09 | The only apply cleared the bar by 0.017 | PASS | report: Formlabs `composite 0.317 ≥ 0.3` | — |
| 19 | B09 | Hiring times are my own guesses | PASS | the card: "How fast any company really hires. That number is yours." | — |
| 20 | B10 | Existing skill: JavaScript and Node, evidence CodeBuddies | PASS | public repo github.com/salonimathure20/codebuddies-ai (HTTP 200, 2026-10-13); INFO 6150 team project, Node/Express | the student confirmed the skill (2026-10-13) |
| 21 | B10 | Claude Code did most of the typing on the prototype | PASS | the prototype's FRICTIONAL.md: "Most of the hands-on work was done by an AI coding agent (Claude Code) that I directed" | — |
| 22 | B10 | Start the evaluation with 30 postings | EXEMPT | plan | — |

No Claude response appears in the film. No user, employer endorsement, metric or testimonial is invented. Company names are public employers from the worked run's public data.

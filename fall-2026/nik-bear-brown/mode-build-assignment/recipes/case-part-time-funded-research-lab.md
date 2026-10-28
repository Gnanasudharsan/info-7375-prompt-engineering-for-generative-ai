---
status: DRAFT
todos_open: 6
last_gate: null    # a sample run completed on 2026-10-19 (mode-build-assignment/03-run-log-entry.md) but it is not a gate clearance: six human-owned TODOs below are still open
attestation: null
recipe_version: 0.1.0
---

# case-part-time-funded-research-lab: find where the research money is before writing to a lab

## Executive summary

A teaching professor with a full-time job wants a part-time, paid research role alongside it, in computational biology or data-heavy research. Most labs never advertise such a role, so the usual route is to read lab websites and write to the lab. A lab's website never says whether the lab can pay anyone, and writing to forty labs that cannot pay costs weeks. This recipe starts from the other end: federal research money is public, so it asks two award databases which Boston-area institutions hold active research awards on the topic, then keeps only the awards that could plausibly pay a collaborator. What comes out is a list of funded projects, not of labs that want help. A person still has to find whose project each one is, look at the lab's own page, and decide whether to write. Nothing in this recipe sends anything, and where it cannot tell, it says so instead of guessing.

**Who uses it, exactly:** one person on a US-citizen path (no sponsorship needed), based in Boston, able to work about 20 hours a week in term and full-time in summer, willing to work mostly remotely and be on site about once a week within a few miles of Northeastern. It is not built for anyone who needs a visa.

## Required reads

`SNICKERDOODLE.md`, `DOMAIN.md`, `docs/tutorials/01-first-scan.md`, `recipes/local-wage-adjustment.md` (the closest recipe in shape), and this file.

## Purpose

Decide, for a start date and a topic, **which funded projects at which institutions are worth a person's look**, using only public records. Use it when the question is "who could pay me" rather than "who is hiring": research collaborations, consulting, and part-time postdoc-style roles that do not appear on a job board. Do not use it to score a posted job (that is `ats:scan` and `score`), and do not use it for roles that need sponsorship.

## Source inventory

**Existing in the repository, and run for this recipe on 2026-10-19:**

| What | Exact command or path | Used for |
|---|---|---|
| Conformance | `npm run verify` | the machine half: 158 files conform, manifest check passes |
| Doctor | `npm run doctor` | recipe status dashboard, declared vs body TODO counts, private paths untracked |
| ATS scan | `npm run ats:scan -- --dry-run` (needs a private `data/ats/portals.yml`) | the job-board side of the same person's search; shown here to mark where this recipe starts instead |
| Liveness | `npm run ats:liveness -- <url> [<url> ...]` | gate G2 for any page that claims an opening |
| Role quality, national | `data/bls/compact/soc_occupation_compact.csv` (columns `onet_soc_code`, `title`, `annual_median_wage`, `hourly_median_wage`, `oews_year`) | a national wage floor for the occupation the work resembles |

**Existing but not runnable on a clean checkout:** `npm run bls:local-wage -- --metro <metro> --soc <soc>` (a Boston wage floor). It needs `.venv` and the files under `data/bls/local-wage/`, which are not in the repository on `main` (checked 2026-10-19: no such directory, and no commit that ever contained it). See the TODO below.

**New, added by this recipe:** `scripts/funding/check-awards.py` with `scripts/funding/test_check_awards.py` (17 tests, no network). It is an ingest script: it queries the NIH RePORTER API and the NSF Award Search API, applies gates G1 to G3 below, and writes a JSON log and a Markdown report. Stdlib only. Award numbers can be replaced by stable stand-ins in the written files (`--redact-ids`), and the real numbers and investigators' names go only to a file under a `private/` directory (`--with-pi --private-file`).

## Proposed additions

- **[TODO DATA SOURCE]** NSF organisation names. The NSF Award Search matches awardee names loosely (a query for one university returned 227 awards, 222 of them to other awardees) and spells institutions differently from NIH. The script keeps only awards whose awardee name is the same name, so for Broad, Whitehead, Harvard Medical School and Boston Children's it kept **zero** NSF awards on 2026-10-19: that is the name, not the funding. Needs a small mapping file, `data/funding/org-names.csv`, with one provenance line per row (origin and date), closed by a human. Until then the NSF half undercounts.
- **[TODO DATA SOURCE]** `data/bls/local-wage/metro_oews.csv`, `bea_rpp.csv`, `bls_bea_msa_crosswalk.csv`, `sample.csv`. `recipes/local-wage-adjustment.md` says they are ingested; they are not on `main`. Needed so that the wage floor is a Boston number rather than a national one.
- **[TODO DEV]** `ats:liveness` returned `uncertain` ("content present but no visible apply control found") for a Greenhouse posting id that does not exist, instead of `expired`. A closed posting is indistinguishable from a page that never had an apply button. Proposed: treat a redirect to the board root as `expired`. Until built, this recipe treats `uncertain` as **not live**.

## Typed decisions still open

- **[TODO DEFINE]** `--min-months-left` (default 6): how long an award must run past the start date to count. The default is the author's guess; the person whose search this is must set it, with one sentence of reasoning.
- **[TODO DEFINE]** The two lists of award activity codes in the script: which pay for work by someone other than a named trainee (R01, R21, R35, U01 and so on) and which are trainee-only (F31, F32, K99, T32 and so on). The lists are the author's reading of the NIH code tables, not an NIH ruling.
- **[TODO REPORT FIELD]** The human report: the columns, who reads it, and the decision it enables. Proposed columns are in the output contract; the reader is the person whose search this is, and the decision is "which funded projects do I look at the lab page for". Needs his confirmation.

(That is six open items: three `DATA SOURCE`/`DEV` above and three `DEFINE`/`REPORT FIELD` here. The first-run `APPROVE` gate is in the phase gates, not counted here: it is a gate, not a checkbox.)

## Phase gates

Each stops at the first failure for that award. A failed gate is recorded, not dropped.

| Gate | Test, as the script can check it | Pass | Fail |
|---|---|---|---|
| G0 profile (human) | The person has stated the start date, hours, distance rule and that no sponsorship is needed, in the run's input. | continue | refuse to run |
| G3 organisation name | A control query for the organisation with **no topic** returns at least one award for the fiscal year, and the report lists every organisation name the database returned (NIH accepts a partial name loosely: `HARVARD` matched three organisations). | topic queries run | `name_matched: false`; no topic query; the report says **the name is wrong, not the funding** |
| G1 active | The award's end date is at least `--min-months-left` months after the start date. | counts | recorded as ended or ending too soon |
| G2 type | The activity code is a research-project code, not a fellowship, career or training code. | `research-project` | `trainee-only` (an unknown code is `unclassified`, decided by a person) |
| G4 liveness | If a page claims an opening: `npm run ats:liveness -- <url>` returns `active`. `uncertain` counts as not live. | the opening is treated as live | no opening is claimed; the lab is cold outreach and is never scored as hiring |
| G5 human look | A named person has looked at the lab's own page and writes the date in the log. | may write | nothing is drafted, sent or posted as an opening |

Liveness and the human look are gates, not votes: neither can be outweighed by a good funding number.

## What it can and cannot verify

**It can verify (and the script is the evidence):**
- that a named organisation holds, or does not hold, an award in NIH RePORTER or the NSF Award Search whose text matches a topic, with the award number, amount, start and end dates, as the database states them;
- that an award has ended or is about to, and whether its type is one that pays a trainee only;
- that an organisation name is one the database recognises, and which organisations it matched. NSF has no control query, so for NSF a zero is never evidence.

**It cannot verify, and says so:**
- that the money is available to pay **you**. Awards are tied to specific aims; a research award is not a budget line for a collaborator, and nothing here shows what the lab can spend;
- whose award it is. Principal investigators are deliberately never requested, so a person looks up who holds each award, locally;
- that the work is a good fit, that a lab wants help, or that it would reply. Fit is a judgment, labelled as one, and belongs to the person;
- money that is not federal: industry, foundation and internal funds do not appear in either database, so "none found" is **not** "unfunded";
- whether an award is still being paid. Both databases state an end date, not whether funds were frozen or terminated;
- what an institution pays in Boston: the local wage script cannot run (above), so the wage floor is a national figure.

## Output contract

Two artifacts, because one cannot serve both readers.

**Agent log (JSON):** `runs/<date>.json`, written by the script: `config` (organisations, terms, fiscal year, window start, months left), `orgs_status` (per organisation, whether the name matched and the control total), `queries` (every query, with the total the database reported), `by_org` (counts by gate), `awards` (each award with its three gate results and an `amount_kind` of `annual (one fiscal year)` or `total (estimated, whole award)`), and `labels` stating which fields are records, which are script output, and that interpretation is not produced here. No person's name appears in it.

**Human report (Markdown):** `runs/<date>.md`, which opens with a plain-language executive summary and then a table with one row per institution:

| Institution | Name matched in NIH | Awards found | Research awards running into the window | Trainee-only | Ended or ending too soon | NIH annual $ of the passing awards |
|---|---|---|---|---|---|---|

Then provenance (every query and its reported total). NIH annual amounts and NSF totals are never added together.

## Stop conditions

Refuse to produce a result, and say why, when:

- a database cannot be reached (the script exits non-zero; it never reports an empty result for an unreachable source);
- the control query for an organisation finds nothing (no topic result is reported for it);
- asked to rank labs, or to say a lab "would hire" the person: that is a judgment, and it belongs to the person after the human look gate;
- asked to look up or write down principal investigators in a tracked file: they stay in a local, untracked file;
- asked to draft or send a message to a lab: the person writes and sends every message.

## Log template for `logs/RUN_LOG.md`

```markdown
## YYYY-MM-DD, case-part-time-funded-research-lab v0.1.0
- Inputs: organisations <list>, terms <list>, fiscal year <fy>, window start <date>, months left <n>
- Commands: python3 scripts/funding/check-awards.py ...; (npm run ats:liveness -- <url>, if a page claims an opening)
- Outputs: runs/<date>.json, runs/<date>.md
- Result: <awards found / research awards running into the window>; name mismatches: <list or none>
- Gates: G5 human look: <who, date, or not yet>
- Open issues: <TODOs still open; anything the run could not check>
```

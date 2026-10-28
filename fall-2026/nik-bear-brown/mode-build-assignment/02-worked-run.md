# Worked run: the funded-research mode, run for real on 2026-10-19

## Executive summary

**What this is.** The record of actually running the mode: the engine's own commands against real data, a new script run against two live federal award databases, and the attempts I made to break it. **Why read it.** The mode file says what the mode does; this says what happened when it ran, including four things that broke and what the breaking taught. **What it found.** The engine's conformance and scan commands ran as documented; its liveness command cannot tell a closed posting from a page with no apply button; its local-wage command cannot run on a fresh copy because its input data is not in the repository; and the new award check works, with one run covering six institutions (349 awards, 223 that could pay a collaborator starting January 2027) and four honest limits. The mode is **DRAFT**, not further: six decisions are still a human's.

## Inputs (nothing here is private)

- **The person:** the profile in the recipe (US citizen, Boston, about 20 hours a week in term, full-time in summer, no sponsorship needed). No personal data was used.
- **Start date for the work:** 2027-01-01, with a six-month minimum (the script's default, an open decision in the recipe).
- **Topic:** `single cell`, as a stand-in for computational biology. That it is a good stand-in is my judgment, not something the script established.
- **Institutions:** six Boston-area institutions, spelled as NIH RePORTER spells them.
- **Engine copy:** a fresh clone of the repository at commit `015843d`, installed with `npm install`. My own files were copied into it only to run the conformance and doctor checks.

## Commands and the real output

### 1. The conformance check, before touching anything

```text
$ npm run verify
npm notice run the-reallocation-engine@1.0.0 verify
npm notice run node scripts/conformance.mjs && node scripts/manifest-check.mjs
conformance: 158 files (85 md · 36 py · 30 js · 4 sh · 3 json)
✓ all conform (machine half of P4). Adequacy is still the human gate.
MANIFEST CHECK — The Reallocation Engine
==========================================

WARN (3):
  W1 ignore path not in .gitignore: archive/
  W2 private path not gitignored (PII/secret risk): private/
  W2 private path not gitignored (PII/secret risk): data/ats/

✓ manifest check passed (3 warnings)
```

The three warnings are the repository's own (it ignores `private/` and `data/ats/` in a way the manifest check does not credit); they were there before my files.

### 2. The doctor, before my recipe

```text
$ npm run doctor
  ✓ to-markdown    scripts/to-markdown.mjs
  ✓ score          scripts/score/role-scorer.mjs
  ✓ score:gates    scripts/score/gate-harness.mjs
  ✓ ats:dedup      scripts/ats/dedup-tracker.mjs
  ✓ ats:liveness   scripts/ats/check-liveness.mjs
  ✓ ats:merge      scripts/ats/merge-tracker.mjs
  ✓ ats:normalize  scripts/ats/normalize-statuses.mjs
  ✓ ats:scan       scripts/ats/scan.mjs
  ✓ ats:verify     scripts/ats/verify-pipeline.mjs
  ✓ resumes:pdf    scripts/resumes/generate-pdf.mjs
  ✓ svg-to-png     scripts/svg-to-png.mjs
  ✓ audit:layout   scripts/svg-layout-audit.mjs
  ✓ postsvg-to-png scripts/svg-layout-audit.mjs
  ✓ skill-demand   scripts/score/skill-demand-monitor.mjs
  ✓ skill-demand:test scripts/score/skill-demand-monitor.test.mjs
  ✓ fetch-postings scripts/ats/fetch-real-postings.py
  ✓ pii-scan       scripts/pii-scan.mjs

DOMAIN DIRECTORIES
  ✓ data/sec
  ✓ data/bls
  ✓ data/ats
  ✓ data/80-days-to-stay
  ✓ scripts/sec
  ✓ scripts/bls
  ✓ scripts/ats
  ✓ scripts/resumes

PRIVACY (no personal data committed)
  ✓ no private/PII paths are tracked

RECIPES (33)
  with lifecycle frontmatter: 33   missing: 0
  by status: DRAFT 28 · RUNNABLE-SAMPLE 4 · RUNNABLE-LIVE  # DRAFT | SPECIFIED | RUNNABLE-SAMPLE | RUNNABLE-LIVE | VERIFIED 1
  open TODOs: 318 declared (in frontmatter) · 318 [TODO markers in bodies

SUMMARY
  environment: ✓ runnable
  recipes: 33/33 carry lifecycle frontmatter — all tracked
  next: continue
```

### 3. The engine's ATS scan, dry run, on four boards from my watch list

This is the job-board side of the same search. It needs a private `data/ats/portals.yml`, which I wrote for this run (not committed). Without it the command stops: `Error: portals.yml not found. Run onboarding first.`

```text
$ npm run ats:scan -- --dry-run
npm notice run the-reallocation-engine@1.0.0 ats:scan
npm notice run node scripts/ats/scan.mjs --dry-run
Scanning 4 companies via providers (0 local parser; 0 skipped — no provider matched)
(dry run — no files will be written)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Portal Scan — 2026-10-19
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Companies scanned:     4
Total jobs found:      937
Filtered by title:     813 removed
Filtered by location:  117 removed
Duplicates:            0 skipped
New offers added:      7

New offers:
  + Figma | Account Executive, Enterprise | San Francisco, CA • New York, NY • United States
  + Figma | Account Executive, Strategic | San Francisco, CA • New York, NY • United States
  + Figma | Director, Technical Revenue Accounting | San Francisco, CA • New York, NY • United States
  + Figma | Manager, Distribution Partnerships | San Francisco, CA • New York, NY • United States
  + Figma | Manager, Tech & Ecosystem Partnerships | San Francisco, CA • New York, NY • United States
  + Figma | Senior Account Executive, SMB | San Francisco, CA • New York, NY • United States
  + Figma | Technical Account Manager | San Francisco, CA • New York, NY • United States

(dry run — run without --dry-run to save results)

Review new offers in data/ats/pipeline.md.
```

What I read in it, as a reader and not as the script: every "new offer" is Figma. **`Director, Technical Revenue Accounting` appears because the title filter matches the substring `Account` in "Accounting"**; the scan has no check on the posting's body, so a finance role passes as an account role. My own Lectern filter requires evidence in the body as well as the title and would reject it. That is why this mode does not use the scan to find lab roles.

### 4. Liveness, on three URLs

```text
$ npm run ats:liveness -- <figma posting> <dash page> <made-up closed greenhouse id>   (playwright 1.61.0 installed with --no-save to match the cached browser)
npm notice run the-reallocation-engine@1.0.0 ats:liveness
npm notice run node scripts/ats/check-liveness.mjs https://boards.greenhouse.io/figma/jobs/6118332004?gh_jid=6118332004 https://damore-mckim.northeastern.edu/dash/about/ https://boards.greenhouse.io/figma/jobs/1000000001
Checking 3 URL(s)...

✅ active     https://boards.greenhouse.io/figma/jobs/6118332004?gh_jid=6118332004
⚠️ uncertain  https://damore-mckim.northeastern.edu/dash/about/
           content present but no visible apply control found
⚠️ uncertain  https://boards.greenhouse.io/figma/jobs/1000000001
           content present but no visible apply control found

Results: 1 active  0 expired  2 uncertain
```

The first URL is a live posting (`active`). The second is a lab-style page: `uncertain`, because the command looks for an apply button and a page about a research hub has none. The third is a Greenhouse posting id I made up: **`uncertain`, not `expired`**. The command cannot tell a closed posting from a page that never had an apply control. The mode therefore treats `uncertain` as not live. (To make the command run at all I had to install Playwright 1.61.0 with `--no-save`; the 1.62.1 the lockfile resolves to wanted a browser build I did not have.)

### 5. The engine's local wage command, which could not run

```text
$ npm run bls:local-wage -- --metro "Boston-Cambridge-Nashua, MA-NH" --soc 19-1042 --json
missing .venv — create it with:
  python3.13 -m venv .venv
  .venv/bin/pip install -r data/bls/local-wage/requirements.txt

$ npm run bls:local-wage -- --metro "Boston-Cambridge-Nashua, MA-NH" --soc 15-2051 --json
missing .venv — create it with:
  python3.13 -m venv .venv
  .venv/bin/pip install -r data/bls/local-wage/requirements.txt

$ npm run bls:local-wage -- --metro "Boston-Cambridge-Nashua, MA-NH" --soc 19-1029 --json
missing .venv — create it with:
  python3.13 -m venv .venv
  .venv/bin/pip install -r data/bls/local-wage/requirements.txt
```

The recipe says the compact inputs are "already ingested". In the repository on `main` there is no `data/bls/local-wage/` and no commit that ever contained it (checked with `git log --all`). I did not build the data. The recipe carries this as a typed TODO, and the wage floor is national, from the engine's own extract:

```text
$ python3 -c "...read data/bls/compact/soc_occupation_compact.csv for four SOC codes (.00 rows)"
15-2051.00  Data Scientists                            OEWS 2024  employment 233440.0  annual median 112590.0  hourly median 54.13  (national)
19-1021.00  Biochemists and Biophysicists              OEWS 2024  employment 34520.0  annual median 103650.0  hourly median 49.83  (national)
19-1029.00  Biological Scientists, All Other           OEWS 2024  employment 59710.0  annual median 93330.0  hourly median 44.87  (national)
19-1042.00  Medical Scientists, Except Epidemiologists OEWS 2024  employment 156300.0  annual median 100590.0  hourly median 48.36  (national)
```

### 6. The new script: its unit tests, then the live run

```text
$ python3 scripts/funding/test_check_awards.py
----------------------------------------------------------------------
Ran 17 tests in 0.002s

OK
```

```text
$ python3 scripts/funding/check-awards.py --orgs "NORTHEASTERN UNIVERSITY" "BROAD INSTITUTE, INC." "WHITEHEAD INSTITUTE FOR BIOMEDICAL RES" "MASSACHUSETTS INSTITUTE OF TECHNOLOGY" "HARVARD MEDICAL SCHOOL" "BOSTON CHILDREN'S HOSPITAL" --terms "single cell" --fy 2026 --window-start 2027-01-01 --redact-ids --with-pi --private-file private/awards-with-names.json --out-json runs/awards-2026-10-19.json --out-md runs/awards-2026-10-19.md
found 349 awards; 223 research-project awards running into the window; wrote runs/awards-2026-10-19.json and runs/awards-2026-10-19.md
exit 0
```

The report it wrote, `runs/awards-2026-10-19.md` (award numbers are stand-ins, no person's name appears; the full list of awards is in `runs/awards-2026-10-19.json`):

````text
# Funded-research award check

## Executive summary

This report asks two public federal award databases which of 6 Boston-area institutions hold active research money on the topic "single cell". It exists because a lab's own web page never says whether the lab can pay anyone; the money is on record elsewhere. For work starting 2027-01-01, it found 349 awards, of which 223 are research-project awards still running at least 6 months into the window. A zero for an institution means either no money or a misspelled name; the table says which. This is a list of funded projects, not of labs that want a collaborator: whose project each one is, and whether they would talk, is the next, human step.

## What the numbers mean

- NIH amounts are one fiscal year's award; NSF amounts are an estimated total over the whole award. They are never added together.
- *Trainee-only* awards (fellowships, career and training grants) pay one named person's training; they are not a source of pay for anyone else.
- No person's name is in this report. Looking up who holds an award is a separate, local step.

## By institution

| Institution | Name matched in NIH | Awards found | Research awards running into the window | Trainee-only | Ended or ending too soon | NIH annual $ of the passing awards |
|---|---|---|---|---|---|---|
| NORTHEASTERN UNIVERSITY | yes | 21 | 17 | 1 | 3 | 6,991,910 |
| BROAD INSTITUTE, INC. | yes | 41 | 29 | 5 | 6 | 36,462,770 |
| WHITEHEAD INSTITUTE FOR BIOMEDICAL RES | yes | 10 | 4 | 4 | 2 | 2,187,900 |
| MASSACHUSETTS INSTITUTE OF TECHNOLOGY | yes | 51 | 34 | 5 | 9 | 32,148,097 |
| HARVARD MEDICAL SCHOOL | yes | 99 | 54 | 29 | 15 | 28,115,387 |
| BOSTON CHILDREN'S HOSPITAL | yes | 127 | 85 | 24 | 22 | 68,334,896 |

## Provenance

- nih_reporter · NORTHEASTERN UNIVERSITY · (control, no topic) · reported total 103 · fetched only the total was read
- nih_reporter · NORTHEASTERN UNIVERSITY · single cell · reported total 16 · fetched 16
- nsf_award_search · NORTHEASTERN UNIVERSITY · single cell · no total reported by this source · fetched 227 · kept 5 under the same awardee name, dropped 222 other awardees
- nih_reporter · BROAD INSTITUTE, INC. · (control, no topic) · reported total 113 · fetched only the total was read
- nih_reporter · BROAD INSTITUTE, INC. · single cell · reported total 41 · fetched 41
- nsf_award_search · BROAD INSTITUTE, INC. · single cell · no total reported by this source · fetched 24 · kept 0 under the same awardee name, dropped 24 other awardees
- nih_reporter · WHITEHEAD INSTITUTE FOR BIOMEDICAL RES · (control, no topic) · reported total 20 · fetched only the total was read
- nih_reporter · WHITEHEAD INSTITUTE FOR BIOMEDICAL RES · single cell · reported total 10 · fetched 10
- nsf_award_search · WHITEHEAD INSTITUTE FOR BIOMEDICAL RES · single cell · no total reported by this source · fetched 19 · kept 0 under the same awardee name, dropped 19 other awardees
- nih_reporter · MASSACHUSETTS INSTITUTE OF TECHNOLOGY · (control, no topic) · reported total 211 · fetched only the total was read
- nih_reporter · MASSACHUSETTS INSTITUTE OF TECHNOLOGY · single cell · reported total 54 · fetched 54
- nsf_award_search · MASSACHUSETTS INSTITUTE OF TECHNOLOGY · single cell · no total reported by this source · fetched 136 · kept 3 under the same awardee name, dropped 133 other awardees
- nih_reporter · HARVARD MEDICAL SCHOOL · (control, no topic) · reported total 308 · fetched only the total was read
- nih_reporter · HARVARD MEDICAL SCHOOL · single cell · reported total 99 · fetched 99
- nsf_award_search · HARVARD MEDICAL SCHOOL · single cell · no total reported by this source · fetched 4 · kept 0 under the same awardee name, dropped 4 other awardees
- nih_reporter · BOSTON CHILDREN'S HOSPITAL · (control, no topic) · reported total 451 · fetched only the total was read
- nih_reporter · BOSTON CHILDREN'S HOSPITAL · single cell · reported total 130 · fetched 130
- nsf_award_search · BOSTON CHILDREN'S HOSPITAL · single cell · no total reported by this source · fetched 2 · kept 0 under the same awardee name, dropped 2 other awardees

Retrieved 2026-10-19T19:16:34+00:00. Window start 2027-01-01; minimum months left 6.
````

### 7. Conformance and doctor with my recipe and script in the clean copy

```text
$ node scripts/conformance.mjs recipes/case-part-time-funded-research-lab.md scripts/funding/check-awards.py scripts/funding/test_check_awards.py
conformance: 3 files (1 md · 2 py)
✓ all conform (machine half of P4). Adequacy is still the human gate.

$ npm run doctor   (recipe section only)
RECIPES (34)
  with lifecycle frontmatter: 34   missing: 0
  by status: DRAFT 29 · RUNNABLE-SAMPLE 4 · RUNNABLE-LIVE  # DRAFT | SPECIFIED | RUNNABLE-SAMPLE | RUNNABLE-LIVE | VERIFIED 1
  open TODOs: 324 declared (in frontmatter) · 324 [TODO markers in bodies

SUMMARY

$ npm run verify
conformance: 161 files (86 md · 38 py · 30 js · 4 sh · 3 json)
✓ all conform (machine half of P4). Adequacy is still the human gate.
MANIFEST CHECK — The Reallocation Engine
==========================================

WARN (3):
  W1 ignore path not in .gitignore: archive/
  W2 private path not gitignored (PII/secret risk): private/
  W2 private path not gitignored (PII/secret risk): data/ats/

✓ manifest check passed (3 warnings)
```

The doctor's open-TODO count rose from 318 to 324, and the declared and body counts agree: my recipe declares 6 and has 6 markers.

## Verified versus inferred

| Statement | Status | Where it comes from |
|---|---|---|
| The repository's 158 files conform; the manifest check passes with 3 warnings | verified | `npm run verify` (command 1) |
| The ATS scan found 937 postings on four boards and kept 7, all Figma | verified | `npm run ats:scan -- --dry-run` (command 3) |
| One of those 7 is an accounting role matched on the substring "Account" | verified that it was kept, judged that it is a false positive | the title is in the output; reading it is mine |
| A live posting is `active`; a made-up closed one is `uncertain` | verified | `npm run ats:liveness` (command 4) |
| The Boston wage floor cannot be produced from this repository | verified | the command's own message; no such directory in any commit |
| 349 awards at six institutions; 223 are research-project awards running at least six months past 2027-01-01 | verified, as the script and the databases state them | `runs/awards-2026-10-19.json` |
| NIH counts match an independent query, and the database's own total overcounts distinct projects | verified | `runs/12-cross-check-counts.txt` |
| "single cell" stands in for computational biology | **judgment** | mine; not tested |
| A research-project award could pay a collaborator | **judgment** | the script says only that its type is not trainee-only |
| Which of these awards belong to groups worth a look | **not decided** | a person, after looking up whose award it is and reading the lab's page |

## Verification

### Cross-checking a count against the source

I queried RePORTER a second, separate way for each institution and counted distinct project numbers, then compared with the script's NIH counts:

```text
$ independent cross-check of the script's NIH counts: a second, separate RePORTER query per institution (distinct project numbers) vs runs/awards-2026-10-19.json
  NORTHEASTERN UNIVERSITY                    reporter total  16  distinct project numbers  16  script NIH awards  16  OK
  BROAD INSTITUTE, INC.                      reporter total  41  distinct project numbers  41  script NIH awards  41  OK
  WHITEHEAD INSTITUTE FOR BIOMEDICAL RES     reporter total  10  distinct project numbers  10  script NIH awards  10  OK
  MASSACHUSETTS INSTITUTE OF TECHNOLOGY      reporter total  54  distinct project numbers  48  script NIH awards  48  OK
  HARVARD MEDICAL SCHOOL                     reporter total  99  distinct project numbers  99  script NIH awards  99  OK
  BOSTON CHILDREN'S HOSPITAL                 reporter total 130  distinct project numbers 127  script NIH awards 127  OK
```

All six agree. The database's own `total` does not: it reported 54 for MIT and 130 for Boston Children's, but 48 and 127 distinct projects. A person reading the database's total would overcount by 6 and 3.

### Deliberate attempts to break it

```text
## Break attempt 1: a misspelled organisation name (NIH RePORTER wants the exact name)
$ python3 scripts/funding/check-awards.py --orgs "NORTHEASTERN UNIV" --terms "single cell" --fy 2026 --window-start 2027-01-01 --sources nih --redact-ids --out-json t.json --out-md t.md
found 16 awards; 14 research-project awards running into the window; wrote <tmp>/t.json and <tmp>/t.md
exit 0
## By institution

| Institution | Name matched in NIH | Awards found | Research awards running into the window | Trainee-only | Ended or ending too soon | NIH annual $ of the passing awards |
|---|---|---|---|---|---|---|
| NORTHEASTERN UNIV | yes | 16 | 14 | 1 | 1 | 6,991,910 |

## Provenance

## Break attempt 2: a start date so late that almost every award has ended (G1)
$ ... --orgs "NORTHEASTERN UNIVERSITY" --terms "single cell" --window-start 2031-01-01 --sources nih
found 16 awards; 3 research-project awards running into the window; wrote <tmp>/g.json and <tmp>/g.md
| Institution | Name matched in NIH | Awards found | Research awards running into the window | Trainee-only | Ended or ending too soon | NIH annual $ of the passing awards |
|---|---|---|---|---|---|---|
| NORTHEASTERN UNIVERSITY | yes | 16 | 3 | 1 | 13 | 1,354,179 |

## Break attempt 3: write award numbers and names to a path that is not under private/
$ ... --with-pi --private-file runs/names.json
STOP: runs/names.json is not under a 'private' directory; refusing to write award numbers or names there.
exit 2
ls: runs/names.json: No such file or directory

## Break attempt 4: the database cannot be reached (a dead proxy stands in for an outage)
$ https_proxy=http://127.0.0.1:9 ... --sources nih
STOP: a database could not be reached (<urlopen error [Errno 61] Connection refused>). Refusing to report an empty result.
exit 2
ls: <tmp>/o.json: No such file or directory
```

The first attempt did not behave as I had assumed. I expected `NORTHEASTERN UNIV` to return zero, because the recipe draft said the database wants exact names. It matched the full name: **the database accepts a partial name**. I redid the attempt with a real typo and with a partial name:

```text
## Break attempt 1 (redone): a genuinely wrong organisation name, then a partial one
$ python3 scripts/funding/check-awards.py --orgs "NORTHEASTERN UNIVERSTY" --terms "single cell" --fy 2026 --window-start 2027-01-01 --sources nih --redact-ids ...   (a typo)
  NORTHEASTERN UNIVERSTY: NAME NOT MATCHED in NIH RePORTER (control query found nothing); no topic query run
found 0 awards; 0 research-project awards running into the window; wrote t.json and t.md
exit 0
| Institution | Name matched in NIH | Awards found | Research awards running into the window | Trainee-only | Ended or ending too soon | NIH annual $ of the passing awards |
|---|---|---|---|---|---|---|
| NORTHEASTERN UNIVERSTY | NO: the name is wrong, not the funding | 0 | 0 | 0 | 0 | 0 |

$ ... --orgs "HARVARD" --terms "single cell"   (a partial name)
  HARVARD: the database matched 3 different organisation names; a partial name matches loosely
found 147 awards; 84 research-project awards running into the window; wrote h.json and h.md
| Institution | Name matched in NIH | Awards found | Research awards running into the window | Trainee-only | Ended or ending too soon | NIH annual $ of the passing awards |
|---|---|---|---|---|---|---|
| HARVARD | yes | 147 | 84 | 38 | 25 | 54,787,918 |

**The name matched more than one organisation:** HARVARD returned 3 names (HARVARD MEDICAL SCHOOL, HARVARD UNIVERSITY, HARVARD UNIVERSITY D/B/A HARVARD SCHOOL OF PUBLIC HEALTH). A partial name is accepted loosely; use the exact name.
```

The typo is caught by the control query; the partial name `HARVARD` matches three organisations, which the report now lists. The recipe draft's claim was wrong and has been corrected.

### What broke during the run, and the fixes

The first two runs are kept as evidence: `runs/10a-first-run-before-nsf-paging.md` (the NSF search stopped at 25 results per institution without saying so) and `runs/10b-second-run-before-nsf-name-filter.md` (the headline said 588 awards found, but only 350 belonged to the institutions asked about).

## Reflection

**What went well.** Starting from the money instead of from lab pages gave a list that a reader can act on in minutes rather than weeks, and the gates did their work on real data: 126 of 349 awards were set aside, some as ended too soon, some as trainee-only. The control query and the list of returned organisation names turned two silent errors into visible ones. Every number here traces to a command whose output is pasted above.

**What the mode got wrong or missed.** It lists funded *projects*, not *groups*. Whose award each one is, I deliberately did not put in a tracked file, so the step that matters most, choosing a lab, is still a manual, local one. The NSF half is weak: for Broad, Whitehead, Harvard Medical School and Boston Children's it kept no award because NSF spells those names differently, so the NSF numbers undercount. "Single cell" is a blunt topic. Nothing in the run shows that any lab would take a part-time collaborator, and nothing could.

**What I would do next.** (1) Close the six typed TODOs in the recipe: the NSF name mapping, the local-wage data, a liveness fix for closed Greenhouse postings, and the three decisions that are the person's own. (2) Run the first human look: take one institution's passing awards, look up whose they are locally, read the lab pages, and write the date in the log; only then can the recipe leave DRAFT. (3) Try a second topic that is not a stand-in, to see whether the control query still earns its keep.

## Attestation

- Recipe: case-part-time-funded-research-lab v0.1.0
- By: Claude Code for Professor Bear · 2026-10-19 (Professor Bear has not read this run; his reading is the human half of the gate)

### Tested

| Ran | Saw | Expected |
|---|---|---|
| `npm run verify` on a clean clone | 158 files conform; manifest check passed with 3 warnings | conformance passes |
| `npm run doctor` with my recipe added | 34 recipes carry frontmatter; declared TODOs 324 equal body markers 324 | no declared-vs-body mismatch |
| `npm run ats:scan -- --dry-run` on four boards | 937 postings, 7 kept, all Figma, one an accounting role | a scan that completes without writing |
| `npm run ats:liveness` on a live posting | `active` | `active` |
| **Break attempt:** liveness on a made-up closed Greenhouse id | `uncertain` ("no visible apply control") | `expired` |
| **Break attempt:** liveness on a research-hub page | `uncertain` | not `active` |
| `python3 scripts/funding/test_check_awards.py` | 17 tests passed, no network | all pass |
| `check-awards.py` live, six institutions, `single cell`, start 2027-01-01 | 349 awards, 223 pass G1 and G2 | counts consistent with the databases |
| Second RePORTER query per institution, distinct project numbers | equal to the script's NIH counts for all six | equal |
| **Break attempt:** `--orgs "NORTHEASTERN UNIVERSTY"` (typo) | `NAME NOT MATCHED`, no topic query, report says the name is wrong | zero must not read as "no funding" |
| **Break attempt:** `--orgs HARVARD` (partial) | matched 3 organisation names, reported | the match must be visible |
| **Break attempt:** start date 2031-01-01 | 3 of 16 Northeastern awards pass; 13 ended too soon | G1 removes ended awards |
| **Break attempt:** `--private-file runs/names.json` | `STOP`, exit 2, no file written | refusal outside `private/` |
| **Break attempt:** a dead proxy in place of the database | `STOP`, exit 2, no output file | an outage must not become an empty result |

### Did not test

- The NSF half with a correct organisation-name mapping (the mapping does not exist yet).
- The Boston wage floor (`bls:local-wage` cannot run: its data is not in the repository).
- The liveness gate on a real lab "open positions" page that is live and one that is closed.
- The human look gate (G5): no one has looked at any lab page for this mode, and nothing was posted or sent.
- A topic other than `single cell`; a start date other than 2027-01-01 and 2031-01-01; a fiscal year other than 2026.
- NIH result sets larger than the script's 500-row page (the largest here was 130).
- Whether an award shown as active is actually being paid (neither database says).
- Anything on Windows or Linux.

### Broke during testing, fixed

- **A hang.** The control query paged through every award one row at a time (thousands of requests) and had to be killed after about six minutes. Fixed: the control query reads one page; a test asserts exactly one request.
- **A silent cap.** The NSF search returned 25 results a page and the script stopped there, so three institutions showed exactly 25. Fixed: it pages until a short page, and flags a result cut off at the page limit.
- **A wrong headline.** The NSF search matches awardee names loosely, so the headline said 588 awards while 350 belonged to the institutions asked about. Fixed: only awards under the same awardee name are kept, and the report counts the ones dropped.
- **An empty name file.** The first investigator file had no names because the database answers with a different key than the one requested. Fixed, with a test; 341 of 349 entries now carry names (the other 8 are NSF awards, whose investigators the script does not fetch).
- **A wrong assumption in my own recipe.** I wrote that the database wants exact organisation names. Break attempt 1 showed it accepts partial names. Fixed in the recipe and in the report.
- **Not fixed:** the missing wage data, and the liveness command's inability to say `expired`. Both are typed TODOs.

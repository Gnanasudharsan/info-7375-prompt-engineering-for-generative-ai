# CLAIMS — show-tell-reallocation-recipe-pitch

One row per narration sentence in `beat_sheet.json` (built by `make_sheet.py`).

Repo = `the-reallocation-engine`, branch `contrib/2026fa-Sreevarshann-newgrad-de-ml-optwindow`, HEAD `ded8454`, checked read-only on 2026-10-11. `S/` = `course/2026fa/submissions/Sreevarshann/`. `P/` = `scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/`.

**Tags**
- **SHOWN**: a repo file or output proves it (cited).
- **WILL**: not built yet, so it is narrated with "will".
- **CONSTRUCTED**: fictional; labelled CONSTRUCTED on screen.
- I added two more tags so nothing is mislabelled:
  - **EXTERNAL**: a claim about a third-party site that comes from the brief, not the repo. It needs its own evidence.
  - **FRAMING**: a signpost, opinion or motivation that states no checkable fact.

## Step 1 — verification of "Exists today"

| # | Brief line | Verdict | Real value / proof |
|---|---|---|---|
| 1 | Prototype runs end to end on `meera-krishnan` through the real scorer | CONFIRMED | `S/runs/2026-10-02/report.md` records `npm run score … → exit 0`. Rerun on 2026-10-11 into a scratch folder: exit 0, "Apply 0 · Consider 0 · Skip 3", funnel and conflict rows identical to the committed report. |
| 2 | Funnel 30,369 → 114 → 64 entry-eligible / 50 senior-only | CONFIRMED | `report.md` lines 34–38. These are companies. In roles, the plan has 53 network roles and 61 verify-posting roles (`report.md` lines 13–14). |
| 3a | R4 and R5, with tests | CONFIRMED | R4 = `6202dc8`, R5 = `806ce8a`. Tests: `ConflictTest` (`P/tests/test_core.py:354`), incl. `test_same_date_human_check_beats_ai_check_in_either_order` (`:402`). |
| 3b | "51 tests passed at commit `0c6c941`" | CHANGED | `0c6c941` no longer exists. The history was rewritten before the first push, and it is now `6202dc8` (`S/TEST-REPORT.md:350`). 51 tests pass at `6202dc8` (rerun 2026-10-11). |
| 3c | Current test count | CHANGED → **58** | `Ran 58 tests … OK` at HEAD, rerun 2026-10-11 (also `S/TEST-REPORT.md:40`, `S/SUBMISSION.md`). |
| 4 | AMGEN conflict: AI said open, `ats:liveness` → HTTP 404 | CONFIRMED | `S/inputs/posting-checks.csv` row 2 (status `open`, checked_by "Claude (chat) web search, not human-verified"). `S/runs/ats-liveness-2026-10-02.txt` lines 4–12 (`❌ expired … HTTP 404`). `report.md` lines 60, 219. |
| 5 | AMGEN INC 1882.0 and HUMAN INC 1382.0 checked by hand in my own Terminal | CONFIRMED | Two checks, recorded under **Hand check (HC)** below. **Original (HC-1):** early October 2026, Assignment 2, backed by your statement and `S/WORKED-RUN.md:191,199`. **Re-run (HC-2):** 2026-10-11, screenshot `../../evidence/hand-check-terminal.png` (evidence only, not on screen). |
| 6 | Break-attempts log, incl. crash on missing input file, then fixed | CONFIRMED | `S/runs/break-attempts-2026-10-02.txt`: attempt d = `FileNotFoundError` traceback (line 12), and after the fix, `HALT: input file not found` (lines 89–96). Fix commit is `2cb57e8`, formerly `f3ddb9a`. |
| 7a | Recipe held at DRAFT, 5 open TODOs | CONFIRMED | `recipes/cases/2026fa/Sreevarshann-newgrad-de-ml-optwindow.md` lines 2–3 (`status: DRAFT`, `todos_open: 5`), TODOs at lines 59–63. |
| 7b | PR #32 open | CONFIRMED | GitHub API, 2026-10-11: `state: open`, not a draft, not merged, head `ded8454`, last updated 2026-10-04. |
| 8a | No human checked a posting | CONFIRMED | `report.md` line 16. Every `checked_by` in `posting-checks.csv` is "not human-verified". |
| 8b | Nothing reached Apply | CONFIRMED | Scorer: "Apply 0 · Consider 0 · Skip 3". |
| 8c | CI shows red | CHANGED | CI has never run on PR #32. Six workflow runs (`verify`, `Contrib Gate` on `98188e1`, `abf6a6a`, `ded8454`) all ended `action_required`, meaning they wait for a maintainer to approve them. `S/TEST-REPORT.md:137` only *predicts* that the `harness-regression` job fails for every PR. The film does not mention CI. |

Other brief claims that differ from the repo:
- **R4 authorship.** The brief says Claude proposed R4 and you accepted it. `S/FRICTIONAL.md:89–90` says "Added R4" and "I chose the rules". The film says "I added rule R4", which fits both.
- **Course and assignment number.** "INFO 7375" and "Assignment 2" do not appear in the repo. It calls the work "The Reallocation Engine — Recipe Design Assignment". The dates (commits 2026-10-02 to 2026-10-03) are confirmed.

## Hand check (HC)

Command, run from the repo root (`the-reallocation-engine`):

```
python3 -c "import csv; [print(r['company_name'], r['Total Approvals']) for r in csv.DictReader(open('data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv')) if r['company_name'] in ('HUMAN INC','AMGEN INC')]"
```

| ID | When | What | Evidence | Status |
|---|---|---|---|---|
| HC-1 | Early October 2026 (Assignment 2) | The original hand check: you ran the one-liner above and saw `AMGEN INC 1882.0` and `HUMAN INC 1382.0`. | Your statement (2026-10-11) and `S/WORKED-RUN.md:191,199`, which records the check ("a csv.DictReader one-liner") but not the exact command. | Attested. The Assignment 2 chat transcript is intentionally excluded: the assignment forbids private conversation transcripts in the submission. |
| HC-2 | 2026-10-11 09:47:31 EDT | Re-run of the same command | `../../evidence/hand-check-terminal.png`: shows the command above, output `AMGEN INC 1882.0` / `HUMAN INC 1382.0`, and `date` output, run from the `the-reallocation-engine` folder. | Verified by viewing the screenshot 2026-10-11. **Evidence only: the screenshot is never shown in the film.** |

## Step 3 — narration claims

Matches the narration as voiced on 2026-10-11 (21 beats, 238.2 s measured, Kokoro `am_michael` at `--speed 1.09`). The three rubric lines cut in the first build (B11's done-criterion, all of B14, B15's opening) are restored. Seven FRAMING lines remain cut; they are listed at the end.

**Pronunciation aid.** The narration text spells my name `Shreevarshun Saa-thee-ya-moorthy` so Kokoro says it correctly; whisper (small.en) hears "Srivarshan Sathiyamurthy" in both BIDEA and BOUT. This respelling exists only in the narration text (`SAY_NAME` in `make_sheet.py`). Every on-screen label, the byline and all metadata use the real spelling, Sreevarshan Sathiyamurthy.

| # | Beat | Sentence | Tag | Proof / note |
|---|---|---|---|---|
| 1 | BIDEA | Hello. I'm Sreevarshan Sathiyamurthy. (spoken from the respelling above) | SHOWN | `S/SUBMISSION.md` (Student field) |
| 2 | BIDEA | New graduates on OPT ask which companies are hiring. | FRAMING | the naive question the writer types |
| 3 | BIDEA | Better to ask which have actually sponsored people at my level. | FRAMING | the corrected question |
| — | BIDEA (on screen) | "Narrated with a synthetic voice (Kokoro am_michael)" | SHOWN | `beat_sheet.json` metadata `voice_kokoro: am_michael`; every beat `engine: kokoro` |
| 4 | BDEFS | A record: a value from a real file or tool output. | SHOWN | `report.md` line 9; recipe md line 40 (`tool_result` = record) |
| 5 | BDEFS | A model judgment: a value an AI produced, not yet checked. | SHOWN | `posting-checks.csv` (AI checks labelled model-judgment); `report.md` line 5 |
| 6 | BDEFS | A gate: a rule that stops the run when evidence is missing. | SHOWN | break attempts a and c (`HALT`, exit 2) |
| 7 | B00 | This is my project: a command line pipeline that shows an international new graduate which companies have sponsored people at their level. | SHOWN | `P/run.py`; `report.md` funnel (entry-eligible vs senior-only) |
| 8 | B00 | When it's done, it will refuse to call a job open unless a record backs it. | WILL | brief §1 |
| 9 | B00 | I built the prototype for my INFO 7375 Assignment 2, in early October 2026. | SHOWN (dates) | `git log`: commits 2026-10-02 → 2026-10-03. The course and assignment number come from your brief only. |
| 10 | B02 | It will save new graduates the manual cross-checking of sponsorship history against live postings. | WILL | brief §2 |
| 11 | B02 | Sponsor sites like Ellis and F1Jobs count past visa filings; | EXTERNAL | Your checks of Ellis and F1Jobs on 2026-10-11 (9:26–9:47 AM): `ellis-amgen.png`, `ellis-amgen-2.png`, `ellis-amgen-3.png`, `f1jobs-amgen.png`, `f1jobs-amgen-2.png`. On screen: "Ellis" and "F1Jobs" labels above the past-filings stack. |
| 12 | B02 | …mine will also check that a posting is live, and match occupation and level. | WILL | brief §2 |
| 13 | B03 | In the first minute, a hiring manager for an ML or AI engineer role will open the README, run one command on a made-up persona, Meera Krishnan, and open the report. | WILL + CONSTRUCTED | brief §3 (reader: a hiring manager or engineer evaluating me for an ML / AI engineer role). Persona files `P/fixtures/persona-meera-krishnan.json`, `search/examples/meera-krishnan/profile.yml` are fictional; stamped CONSTRUCTED on screen. Narration text spells "M L" and "read me" for Kokoro. |
| 14 | B04 | The report opens with its warnings. | SHOWN | `report.md` lines 5–7 |
| 15 | B04 | Then the funnel from my worked run: 30,369 companies, 114 matching my role keywords, 64 entry-eligible, and 50 senior-only. | SHOWN | `report.md` lines 34–38 |
| 16 | B05 | Then a conflict row: an AI web search called an Amgen posting open, the liveness check returned HTTP 404, so the record won, and the role went back to be verified. | SHOWN | `posting-checks.csv` row 2; `ats-liveness-2026-10-02.txt` lines 4–12; `report.md` lines 60, 219 |
| 17 | B06 | What does it prove? | FRAMING | — |
| 18 | B06 | Every value is labelled record, model judgment, or your input. | SHOWN | `report.md` line 9 and every table's Label column |
| 19 | B07 | Gates are hard stops. | SHOWN | break attempts a and c |
| 20 | B07 | I added rule R4: when an AI claim and a record disagree, the record wins. | SHOWN | `6202dc8`; `ConflictTest`; `S/FRICTIONAL.md:89` |
| 21 | B07 | And R5: a human check wins a same-day tie with an AI check. | SHOWN | `806ce8a`; `test_core.py:402` |
| 22 | B08 | The evidence: the commit history, 58 passing offline tests, and a break attempts log. | SHOWN | `git log`; `evidence/unittest-58.txt` (`Ran 58 tests … OK`); `S/runs/break-attempts-2026-10-02.txt` |
| 23 | B08 | One attempt crashed the run on a missing input file; I had it fixed, and it now halts cleanly. | SHOWN | break log line 12 and lines 89–96; `2cb57e8`; `S/FRICTIONAL.md:99` |
| 24 | B09 | It doesn't prove model training; no model is trained here. | SHOWN | `P/README.md:31` (stdlib-only prototype); no training code in `P/` |
| 25 | B10 | It will never auto-apply to jobs, scrape behind logins, or use real personal data. | WILL | brief §5 |
| 26 | B10 | Personas are fictional. | CONSTRUCTED | `S/SUBMISSION.md` ("fictional persona"). B10's on-screen item reads "personal data" (what is excluded); the CONSTRUCTED stamp appears only on the meera-krishnan file in B03. |
| 27 | B11 | First will come an offline evaluation log comparing AI-sourced posting claims with liveness records. | WILL | brief §5 / "Will exist" |
| 27b | B11 | It's done when one command prints an agree and conflict table, and the tests pass in a clean environment. | WILL | brief §5 (restored 2026-10-11, rubric) |
| 28 | B12 | What could sink it is entity resolution. | FRAMING | brief §6 |
| 29 | B12 | In my run, HUMAN INC had 1382 approvals, but I couldn't confirm it was HUMAN Security; its sponsored titles looked like enterprise IT. | SHOWN | `S/WORKED-RUN.md:185–191`; `S/DOMAIN-JUSTIFICATION.md:20`. The "enterprise IT" read is labelled model-judgment, unverified, in the repo. |
| 30 | B13 | So ambiguous matches will be labelled model judgment, confirmed by a human before scoring, and measured on a small hand-checked sample. | WILL | brief §6 |
| 30b | B14 | Why this project? | FRAMING | brief §7 (restored 2026-10-11, rubric) |
| 30c | B14 | Mostly new learning, and a real problem for students on OPT that I wanted to answer with records, not guesses. | FRAMING | brief §7, motivation (restored 2026-10-11, rubric) |
| 30d | B15 | New to me: hard-stop gates, labelled values, and catching an AI mistake against a record. | FRAMING | brief §7. The AMGEN catch itself is row 16 (restored 2026-10-11, rubric) |
| 31 | B15 | I checked the Amgen and HUMAN approval counts by hand, in my own terminal. | SHOWN | Refers to the **original** early-October check (HC-1). The values drawn on screen are captioned "re-run 2026-10-11" and backed by HC-2. See **Hand check (HC)**. |
| 32 | B16 | Claude and Claude Code drafted much of the code and documents; I reviewed them. | SHOWN | all 26 branch commits carry `Co-Authored-By: Claude`; `S/FRICTIONAL.md:71,90,104`; commit `a7ef669` ("AI-drafted, reviewed by me") |
| 33 | B16 | Claude advised holding the recipe at draft, and I agreed. | SHOWN | `S/FRICTIONAL.md:100` |
| 34 | B16 | I chose to skip human posting checks in that run. | SHOWN | `S/FRICTIONAL.md:89–90` |
| 35 | B17 | The recipe was held at draft with five open to-dos, and pull request 32 is still open. | SHOWN | recipe md lines 2–3; GitHub API 2026-10-11 |
| 36 | B17 | No human checked a posting, so nothing reached Apply. | SHOWN | `report.md` line 16; scorer "Apply 0" |
| 38 | B18 | In my worked run, the liveness tool contradicted both postings an AI had called open. | SHOWN | `report.md` line 13 ("2 of them because an AI-reported status was contradicted by the liveness tool"). AMGEN and TWILIO are the only `open` rows in `posting-checks.csv`. On screen: "2 of 2", captioned "per report.md, worked run 2026-10-02". Twilio's result was "insufficient content", which the tool can also give for a bot-blocked page, so the film says "contradicted", not "dead". |
| 39 | B18 | Two is a sample, not a rate. | FRAMING | a caveat on row 38 |
| 40 | B18 | The log will measure it properly. | WILL | brief §5 |
| 41 | BOUT | I'm Sreevarshan Sathiyamurthy. (spoken from the respelling above) | SHOWN | as row 1 |
| 42 | BOUT | This narration uses a synthetic voice. | SHOWN | Kokoro `am_michael`, `--speed 1.09` (`beat_sheet.json` metadata) |
| 43 | BOUT | I drafted the script with Claude and checked every claim. | SHOWN | SOURCES.md (Claude (chat) and Claude Code drafted, I reviewed); this file and FACTCHECK.md are the claim checks |

**Still cut for length** (FRAMING only; no SHOWN fact, no rubric line):
- BDEFS "Three terms."
- B06 "That I can build an LLM-assisted pipeline that stays honest."
- B09 "It shows reliability engineering around LLM output: part of the job, not all of it."
- B10 "What is out?"
- B17 "Here is where it stands."
- B18 "Why build the evaluation log first?" (cut 2026-10-11 to keep the film under 3:59 after naming Ellis/F1Jobs and the target role)
- BOUT the spoken title and "Thanks for watching." (the title stays on the outro card)

## On-screen Terminal output and Claude replies → `evidence/`

No Claude composer or chat reply appears on screen. The AI's "open" claim is drawn as a posting-checks row; no transcript is added, because the assignment forbids private conversation transcripts in the submission. The terminal lines below are drawn in the film from these files. All live in `final-project-film/evidence/` (`../../evidence/` from this folder):

| ID | Beat | On screen | File in `evidence/` | Original date | Status |
|---|---|---|---|---|---|
| T1 | B03 | `run.py` command line | `run-py-terminal.txt` | captured 2026-10-11 11:08 EDT by Claude Code (re-run of the 2026-10-02 worked run into /tmp; header line states this) | in place, exit 0, "Apply 0 · Consider 0 · Skip 3" |
| T2 | B05 | `HTTP 404` | `ats-liveness-2026-10-02.txt` | 2026-10-02 (committed `8cde854`) | in place, byte-identical copy of `S/runs/ats-liveness-2026-10-02.txt` |
| T3 | B08 | `Ran 58 tests — OK` | `unittest-58.txt` | captured 2026-10-11 11:08 EDT by Claude Code (header line) | in place, `Ran 58 tests in 8.513s` / `OK` |
| T4 | B08 | `HALT: input file not found` | `break-attempts-2026-10-02.txt` | 2026-10-02 (committed `2cb57e8`) | in place, byte-identical copy (lines 89–96) |
| T5 | B15 | **Drawn:** two record cards `AMGEN INC 1882.0` / `HUMAN INC 1382.0`, caption `re-run 2026-10-11` | `hand-check-terminal.png` | your re-run 2026-10-11 09:47:31 EDT | in place (yours), evidence only, never shown on screen |
| C1 | B05, B18 | AI's "open" claim (row tag `open?`, model-judgment) | `posting-checks-2026-10-02.csv` | 2026-10-02 (committed `8cde854`) | in place, byte-identical copy of `S/inputs/posting-checks.csv` |
| R1 | B04 | drawn funnel bars labelled `30,369`, `114`, `64 · 50`, beside the report page with its warning dot | `report-2026-10-02.md` | 2026-10-02 (committed `bf8b65d`) | in place, byte-identical copy of `S/runs/2026-10-02/report.md` |
| X1 | B02 | (none on screen; narration only) | `ellis-amgen.png`, `ellis-amgen-2.png`, `ellis-amgen-3.png`, `f1jobs-amgen.png`, `f1jobs-amgen-2.png` | yours, 2026-10-11 9:26–9:47 AM | in place (all five) |

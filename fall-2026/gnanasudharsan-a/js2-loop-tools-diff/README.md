# Job-Search Agent 2 — The Loop, the Tools, and the Diff
Gnanasudharsan Ashokumar · INFO 7375 Fall 2026 · fictional persona Ananya Rao (persona/)

A bounded loop that watches four job boards on three applicant-tracking systems, under a permission policy enforced in code, with one Claude Code change reviewed on evidence.
**Started from:** my own Job-Search Agent 1 code (js1-contract-and-watch, final e0d0e7e), copied at d76a1a6. I did not use Lectern or the Reallocation Engine providers.

## Language and toolchain
Python 3.14.0 (venv) · pytest 8.4.2 · macOS 27.2 · git 2.54.0 · Claude Code 2.1.319 (used for the build and for one patch).
The loop, transport and policy use the standard library only (urllib). requirements.txt is inherited from JS1 (anthropic and requests are used only by the JS1 Claude judge backend).

## Run it from a fresh clone
```bash
cd fall-2026/gnanasudharsan-a/js2-loop-tools-diff
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q                                   # 146 passed, no network
python -m jobwatch.loop --boards boards.json; echo $? # LIVE: 4 GETs, exits 2 (incomplete) because board 4 is a deliberate 404
```
A live run writes `runs/<UTC>/trace.jsonl`, `report.json`, `report.md` and `raw/`, and updates `state/seen_ids.json`.
Evidence scripts (they need `PYTHONPATH=.`):
```bash
PYTHONPATH=. python scripts/seeded_run.py A seeded_demo   # SEEDED: notion replaced by a constructed 200 {"jobs": []}
PYTHONPATH=. python scripts/seeded_run.py B seeded_demo   # all real, continues from A's state
python scripts/check_run.py <run_dir> <prior_state.json> [board url]   # independent check, does not import jobwatch
python scripts/wrong_versions.py                          # plants each GATE §7 wrong version in a temp copy
```

## What ran (past tense, all on 2026-11-06)
| run | kind | exit | what it shows |
|---|---|---|---|
| runs/20261106T203437Z | LIVE, pre-patch | incomplete (2) | 3 boards baseline (670/154/84); deliberate 404 board failed `not_found`, 1 attempt, null counts, not in state. Recomputed independently: evidence/run1_recomputation_*.txt |
| seeded/runs/20261106T203850Z-SEEDED-A | **SEEDED** | finished (0) — **wrong** | notion constructed empty: removed 154, state [] |
| seeded/runs/20261106T203859Z-SEEDED-B | SEEDED continuation, real responses | finished (0) — **wrong** | all 154 real notion postings reported new |
| seeded_after_patch/runs/20261106T210118Z-SEEDED-A | **SEEDED**, patched code | incomplete (2) | notion `suspect_empty`, 154 ids kept |
| runs/20261106T210821Z | LIVE, patched code | incomplete (2) | anthropic 2 real new postings; independent recount 672 = 672 |
Raw bodies are gzipped after each run; the sha256 in each trace is of the uncompressed body.

## Where each deliverable is
| deliverable | file |
|---|---|
| Gate (exits, budgets, repeat rule, error and permission policy, wrong versions, Amendment 1) | GATE.md (80dece3; Amendment 1 at 900c905) |
| Code | jobwatch/policy.py, loop.py, transport.py, normalize.py (+ JS1 rule/persona/judge) |
| Tests | tests/test_policy_boundary.py (B1–B16), tests/test_loop.py (L1–L19), tests/test_review_empty_board.py (R1–R5), JS1 tests |
| Boundary-test table with predictions and generated results | BOUNDARY_TESTS.md |
| Wrong versions caught | evidence/wrong_versions_caught_*.txt (10 of 10) |
| Agent trace of a real run incl. the deliberate failure | runs/20261106T203437Z/trace.jsonl, report.md |
| Finished-wrong-answer demonstration | FINISHED_WRONG_ANSWER.md |
| Review packet | REVIEW_PACKET.md |
| Sources and Claude's contributions | SOURCES.md |
| Honest log | FRICTIONAL.md |

## Sign-off — Job-Search Agent 2
**Checked**
- Permission policy, by my boundary tests B1–B16 (tests/test_policy_boundary.py): predictions committed at 82cdbc1 and the tests committed failing at cbabc53, both before policy.py existed. Results generated from pytest output in BOUNDARY_TESTS.md.
- Exits, budgets checked before the action, the bounded retry, null counts for failed boards and state kept, by L1–L19 (tests/test_loop.py), committed failing at 385515b before loop.py existed.
- The §8 fix, by R1–R5 (tests/test_review_empty_board.py), committed at 900c905 before the patch.
- That my tests catch the GATE §7 wrong versions: scripts/wrong_versions.py, 10 of 10 caught.
- Live runs 1 and 2: counts, id sets and sha256 recomputed from the raw bodies without importing jobwatch; run 2 also recounted with a direct request (672 = 672).
- The finished wrong answer: caught by scripts/check_run.py (empty-after-nonempty, direct recount 154 ≠ 0, all-new-after-empty-state).
- The patch on the real reproduction: the SEEDED A scenario re-run on the patched code ended incomplete with state kept.

**How**
- By tests written before reading Claude's code: B1–B16, L1–L19, R1–R5. Claude chat drafted the test code; I chose the cases, ran them first, and committed them failing.
- By recomputation: run 1 and run 2 (evidence/run1_recomputation_*.txt, evidence/check_run2.txt).
- By hand: I read policy.py, normalize.py, transport.py in full and loop.py lines 1–420 before committing (740343c), and the patch diff line by line (REVIEW_PACKET.md §4).
- With Claude's help: Claude chat drafted GATE.md's structure and proposed values (I added the seconds rule and chose the boards from my probe), the check and mutation scripts, and the hunk-by-hunk diff reading. Claude Code diagnosed the test_L6 setup bug; I confirmed it from the failure line.

**Not checked**
- No response size cap; a very large body is read fully.
- A request can run about twice the 30 s timeout (the deadline is checked between chunks), so the 120 s budget can be overshot.
- The real transport (redirect refusal, proxy bypass, headers) has no tests in the repo; Claude Code's scratch checks are not committed.
- The JS1 location rule misses Ashby "City, State" formats, so US Ashby jobs are likely judged NOT_RELEVANT.
- A large partial drop (e.g. 154 → 3) is still reported ok (REVIEW_PACKET.md §8).
- `--i-approve` approves every suspect board in a run, not one board, and is untested through the CLI.
- Check-then-write races (a symlink created after check_path) and case-variant paths on macOS.
- Wrong versions #1, #2, #4 and #7 are each caught by only one test.
- The Claude judge is not run by the loop; max_judge_calls is declared but unused.
- Python versions other than 3.14.0; boards other than these four.

**Not claiming**
- That any verdict is right for a real person, or that the rule judge's NOT_RELEVANT calls are complete.
- That the agent monitors continuously: it ran twice live.
- That the 403 from Ashby was caused by the User-Agent (adding one fixed it; that is all I showed).
- That `suspect_empty` is a complete defense against bad board responses.

**Signed:** Gnanasudharsan Ashokumar, 2026-11-06

## Driver's seat
| part | what Claude did | what I did | why it stays mine | evidence |
|---|---|---|---|---|
| Loop: the gate | Claude chat drafted GATE.md structure and proposed values | probed the boards myself, chose the boards, added the seconds rule, accepted the values, committed before any code | what the agent may do and when it must stop is my decision, not the tool's | c869cf3, 80dece3 |
| Loop: tests first | Claude chat drafted B, L and R test code | chose the cases, wrote the predictions, ran them failing, committed before code | the tests are my definition of "correct"; if the tool writes them against its own code they prove nothing | 82cdbc1, cbabc53, 385515b |
| Loop: build | Claude Code (session 7096e7f8) wrote policy, loop, transport, normalize | ran it in default mode, approved each action, declined auto mode, read all four files, recorded 29 choices and the open gaps | I am responsible for what the code may do on the network and on disk | 740343c, evidence/claude_code_choices_2026-11-06.txt |
| Loop: runs and checks | Claude chat drafted the check scripts | ran every live and seeded run, wrote predictions first, caught and fixed my check's 403 crash | only an independent check can tell me a "finished" run is wrong | 5e606a8, 55df5ca |
| Review: decision of the fix | Claude chat proposed Amendment 1's wording | accepted it, kept the partial drop out of scope | changing what the agent counts as true is a policy decision | 900c905 |
| Review: test before patch | Claude chat drafted R1–R5 | ran them before the patch; recorded that my R2 prediction was wrong | the reproduction must exist before the fix, or the fix proves nothing | 900c905, FRICTIONAL |
| Review: patch | Claude Code (session 7a088b59) wrote +26 −2 in loop.py | scoped it to one file, ran the tests and the real reproduction myself, read the diff | the tool proposes; accepting a change to my agent's behavior is mine | 644e6ec, evidence/review_patch_diff.txt |
| Review: decision | — | ACCEPT, with per-run approval recorded as a limitation | the decision has to rest on evidence I can explain | REVIEW_PACKET.md §7 |

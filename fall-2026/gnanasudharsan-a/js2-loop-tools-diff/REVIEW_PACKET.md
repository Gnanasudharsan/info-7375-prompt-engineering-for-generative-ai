# Review packet — one Claude Code change (Chapter 6)

**The change:** implement GATE Amendment 1 (`suspect_empty`) in jobwatch/loop.py.
Chosen because it is the defect behind my finished-wrong-answer, a behavior change (not a rename), and it touches state, exits and the approval rule.

## 1. The defect, reproduced before any patch
SEEDED run `seeded/runs/20261106T203850Z-SEEDED-A`, on the unpatched code (740343c): notion returned a constructed 200 `{"jobs": []}`. The agent reported **exit finished (code 0)**, notion removed 154, and wrote notion's state as `[]` (`evidence/seeded_state_after_A.json`). The next real run (`...-SEEDED-B`) reported all 154 real postings as new. My independent check caught both (`evidence/check_seeded_A.txt`, `evidence/check_seeded_B.txt`). Full account: FINISHED_WRONG_ANSWER.md.

## 2. My test, written before the patch
`tests/test_review_empty_board.py`, committed at 900c905, before the Claude Code session. Before the patch: **R1 and R5 fail** (the reproductions), R2–R4 pass (guards that must keep passing: approved reset, first-sight baseline, already-empty board). I predicted R2 would fail; it passed, because with approval Amendment 1 wants the old behavior. Recorded in FRICTIONAL; the 900c905 message is wrong on that point and is corrected there, not rewritten.
Evidence: `evidence/review_tests_before_patch_*.txt`.

## 3. What I asked Claude Code for (session <PATCH_SESSION>, default permission mode)
Implement Amendment 1 in jobwatch/loop.py only; with approval keep today's behavior and record it; change no other file; no network, no CLI, no commit; minimal change; run pytest and show the diff stat.

## 4. The diff read as a change in behavior (`evidence/review_patch_diff.txt`, +26 −2)
| hunk | behavior change |
|---|---|
| `_Loop.__init__`, `run_loop` call | passes `approved` into the loop; no behavior change by itself |
| `run_board`: `suspect_empty = not ids and bool(prior)` | prior None (first sight) → False: baseline unchanged. prior [] → False: unchanged. prior non-empty and zero postings → True |
| not approved | board failed, reason suspect_empty; returns before `ok_ids` is set, so its state is not written; new/removed/count stay None; no retry (the retry loop already ended on an "ok" verdict); trace events `suspect_empty` and `board_result` |
| approved | exactly the pre-patch behavior, plus `approved_reset` in the record and trace |
| `format_report_md` | new "Approved state resets" section; unapproved suspect boards appear in the existing "Failed boards" section with their detail |

## 5. Did it stay in scope?
Yes. `git status` showed only `M jobwatch/loop.py`; no test, config, GATE or script edits; no unrelated refactor.

## 6. Commands I ran myself
- `git status --short`, `git diff --stat`, `git diff jobwatch/loop.py > evidence/review_patch_diff.txt`
- `python -m pytest -q` → **146 passed** (`evidence/review_tests_after_patch_*.txt`)
- The real reproduction again on the patched code, in a separate folder: `PYTHONPATH=. python scripts/seeded_run.py A seeded_after_patch` → **exit incomplete (code 2)**, notion failed `suspect_empty`, null counts, **154 notion ids still in state**
- `python scripts/check_run.py <that run> evidence/state_after_run1.json` → no problem found (`evidence/check_after_patch_A.txt`)

## 7. Decision: ACCEPT
Evidence: the reproduction tests R1 and R5 now pass, the guards R2–R4 still pass, the full suite is green, and the exact SEEDED scenario that produced a finished wrong answer now ends `incomplete` with state kept.
Known limitation accepted, not fixed: **approval is per run, not per board.** One `--i-approve` approves the reset of every suspect board in that run. Amendment 1 talks about "the board"; per-board approval would be more precise. Accepted because it only matters when several boards go empty in the same run, and I would see each one in report.md.

## 8. A case my tests would still miss
A large **partial** drop, e.g. notion 154 → 3. It is not "zero postings", so the board is `ok`, 151 ids are reported removed, and state is overwritten with 3 ids. Amendment 1 leaves this out on purpose. Also untested: `--i-approve` end to end through the CLI (R2 calls run_loop with approved=True directly).

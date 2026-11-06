# FRICTIONAL — Job-Search Agent 2

## 2026-11-06 ~17:30 UTC — My probe script invented two values
Expected: the probe would report the real status, size, and job count for each board.
What happened: lever-palantir showed "HTTP 000 | 9 bytes". The 9 bytes were the previous Ashby response left in /tmp/probe.json; curl had timed out at 20 s and wrote nothing. lever-BADNAME showed "jobs=0" for a 404 because my count used d.get('jobs', []).
Changed: probe2 deletes the temp file first, uses a 60 s timeout, and prints NO-jobs-KEY / no-body instead of 0. Re-probe at 17:32 UTC: palantir 200 in 6 s (305 jobs), spotify 200 (85), Lever bad name 404 {"ok":false,"error":"Document not found"}.
Learned: defaulting a missing field to [] turns an error into "zero jobs". That became GATE wrong version #4. The Palantir timeout-then-success became my reason for allowing one retry on timeouts (GATE §5).
Evidence: evidence/board_probe_2026-11-06T1730Z.txt (c869cf3)

## 2026-11-06 ~13:15 ET — Copied JS1 tests needed a file I didn't copy
Expected: the copied JS1 tests would pass unchanged in the JS2 folder.
What happened: 2 collection errors, both FileNotFoundError for experiment/run_judge.py (the JS1 prompt-experiment runner, which JS2 does not include).
Decision: removed tests/test_run_judge.py and lines 199-end of tests/test_claude_cli_backend.py (the run_judge loader + 2 tests). All 11 claude_cli backend tests are kept. This is not weakening a test: the code they test is not shipped in JS2, and they still pass in js1-contract-and-watch at e0d0e7e.
Evidence: evidence/js1_baseline_in_js2_*.txt

## 2026-11-06 ~15:27 ET — A loop test was wrong, not the code
Expected: all 141 tests pass after Claude Code's build.
What happened: 140 passed, 1 failed: test_L6[gh-no-jobs-key], "assert ['1'] == ['x']". When board is GH, the seed dict {board["id"]: ["x"], GH["id"]: ["1"]} has the same key twice, so the seed was ["1"]. Every check of the code's behavior (failed / bad_shape / 1 attempt / count and new None) passed.
Claude Code's final reply (2026-11-06T20:27:05Z) gave the same diagnosis and did not edit tests/, as my prompt required. I confirmed it myself from the failure line before accepting it.
Changed: only the test setup (seed GH once when board is GH). No assertion changed, so the test was not weakened. The test was drafted with Claude chat; I accepted it without catching the duplicate key.
Evidence: evidence/L6_gh_failure_*.txt, evidence/claude_code_choices_2026-11-06.txt, evidence/tests_after_build_*.txt

## 2026-11-06 ~15:38 ET — The seeded demo, three small failures before it worked
1. `python scripts/seeded_run.py` failed with ModuleNotFoundError: jobwatch, because scripts/ (not the project folder) was on the import path. The next commands still ran and failed one after another, and `tee` left two empty evidence files. Nothing was written to seeded/ or state/ (checked). Fix: PYTHONPATH=. and chaining with &&; deleted the empty files.
2. My independent check flagged notion correctly, then crashed on the direct recount: HTTP 403 Forbidden from api.ashbyhq.com. It sent the default Python-urllib User-Agent; the loop's transport (custom UA) got 200 seconds earlier. After adding a User-Agent the recount returned 154. This supports, but does not prove, that Ashby blocks the default UA.
3. An independent check that crashes is not a check. check_run.py now reports a failed recount as UNAVAILABLE instead of crashing, and never turns a failure into a number.
Result: the agent said "finished" (code 0) for both seeded runs; my check caught both (FINISHED_WRONG_ANSWER.md).

## 2026-11-06 ~15:41 ET — My review-test prediction was wrong for R2
Predicted: R1, R2, R5 fail before the patch. Actual: R1 and R5 fail; R2 passes (evidence/review_tests_before_patch_*.txt).
Why: with --i-approve, Amendment 1 asks for exactly what the old code already does (ok, removed = prior ids, state []), so R2 is a guard that the patch must keep, not a reproduction. The commit message of 900c905 states the wrong prediction; it is corrected here, not rewritten.
Reproduction tests: R1 (Ashby dict) and R5 (Lever list). Guards: R2, R3, R4.

## 2026-11-06 ~16:00 ET — Review patch session
Claude Code (session 7a088b59-a0f1-417c-9b7c-ff067faaac7c, default mode) asked only to read files, run pytest, and edit jobwatch/loop.py; I approved each one and denied nothing. Diff +26 −2 in one file. I re-ran the SEEDED reproduction myself in seeded_after_patch/: exit incomplete, notion suspect_empty, 154 ids kept.
Mistake: I committed 644e6ec with the placeholder <PATCH_SESSION> in REVIEW_PACKET.md and the commit message. Filled in afterwards; the 644e6ec message stays as it is.

## 2026-11-06 ~16:10 ET — Fresh clone and sign-off
Fresh clone of my fork at fd0b4fa into /tmp: 146 passed, wrong versions 10/10 caught, offline check of run 2 clean (evidence/freshclone_test_2026-11-06.txt). No live requests from the clone. Signed the README sign-off after reading it.
Unresolved: everything in the sign-off's "Not checked" list, especially the timeout overshoot, the untested transport, and the partial-drop case.

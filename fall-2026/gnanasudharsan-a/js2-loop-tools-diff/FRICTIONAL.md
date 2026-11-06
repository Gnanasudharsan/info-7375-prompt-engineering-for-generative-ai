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

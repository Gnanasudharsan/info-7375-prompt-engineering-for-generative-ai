# GATE — Job-Search Agent 2
Author: Gnanasudharsan Ashokumar · Written: 2026-11-06 · Starting point: JS1 code at d76a1a6 (from e0d0e7e)
Evidence used: `evidence/board_probe_2026-11-06T1730Z.txt`

The JS1 `CONTRACT.md` rule and persona stay unchanged unless amended here.

## 1. Boards
| id | ATS | endpoint |
|---|---|---|
| `greenhouse:anthropic` | Greenhouse | `https://boards-api.greenhouse.io/v1/boards/anthropic/jobs?content=true` |
| `ashby:notion` | Ashby | `https://api.ashbyhq.com/posting-api/job-board/notion` |
| `lever:spotify` | Lever | `https://api.lever.co/v0/postings/spotify?mode=json` |
| `greenhouse:zz-no-such-board-7375` | Greenhouse | deliberate failure (404 on 2026-11-06) |

## 2. Exits — every way the loop ends
A loop that stops is not a loop that succeeded. Every run writes `runs/<UTC>/trace.jsonl` and `report.json` with exactly one exit status:

| exit | when | reports |
|---|---|---|
| `finished` | every listed board was attempted and none failed | per board: count, new ids, removed ids; requests used; seconds used |
| `incomplete` | the loop reached the end, ≥1 board failed under §5, ≥1 succeeded | the same as finished for good boards; failed boards with reason, attempts, and new=null/removed=null (never 0) |
| `budget-exhausted` | a §3 budget would be exceeded by the next action | boards done, boards not attempted, which budget, the counter values |
| `error` | a policy violation (§6), invalid persona/config, unreadable state, or zero boards succeeded | the reason; nothing written to `state/` |

* **Exit codes:** `finished=0`, `incomplete=2`, `budget-exhausted=3`, `error=1`.
* `"finished"` means the loop ran to the end. It does not mean the answer is right (see §8).

## 3. Budgets (per run)
* **Max boards:** 5
* **Max HTTP requests:** 10 (4 boards × at most 2 attempts = 8, plus headroom)
* **Max wall-clock seconds:** 120; per-request timeout: 30 s (Palantir hit 20 s once on 2026-11-06, then answered in 6 s)
  * **Seconds rule:** before starting a request, if (elapsed seconds + 30 s per-request timeout) > 120, the request is not started and the run exits `budget-exhausted`.
* **Max Claude judge calls:** 10
* A budget is checked **BEFORE** the action. An action that would exceed a budget is not taken.
* Only I change a budget, by a dated amendment to this file committed before the run that uses it. Code reads budgets from `gate_config.json`, and a test asserts that it matches this section. Claude Code may not edit either.

## 4. Repeat rule
* The same action = the same `(method, normalized URL)` within one run.
* Each URL is fetched at most once, plus at most one retry allowed by §5. A third attempt is refused and logged as `repeat_blocked`.
* A board listed twice in config is deduplicated. The second entry is logged as `skipped_duplicate`.
* State is keyed by `(ats, board, posting id)`, so ids from different ATS never collide.

## 5. Error policy (per board; the loop continues to the next board)
| failure | action | why |
|---|---|---|
| 404 / 410 | no retry → board failed: `not_found` | a bad name will not fix itself; retrying wastes budget |
| timeout, connection error, 5xx | retry once after 2 s → still failing → board failed | transient: Palantir went from a timeout to 200 in 6 s on 2026-11-06 |
| 429 | retry once only if `Retry-After` ≤ 5 s, else board failed | respect the site |
| 200 but not JSON, or wrong shape (no `jobs` list for Greenhouse/Ashby, not a list for Lever) | no retry → board failed: `bad_shape` | never default a missing field to `[]` |
| allow-list or path violation | stop the whole run → exit error | a policy breach is not a board problem |

* A failed board's state is never written. Its `new`/`removed` are `null`, never invented.
* **Escalation to me:** a non-zero exit code plus the failed boards listed at the top of `report.md`. The code never edits config to "fix" a board.

## 6. Permission policy (enforced in code, not in a prompt)
* **Network:** GET only, HTTPS only, to exactly these hosts: `boards-api.greenhouse.io`, `api.ashbyhq.com`, `api.lever.co`. Exact hostname match. A redirect to any other host is refused. No cookies or auth headers.
* **Read:** `persona/`, `prompts/`, `state/`, `gate_config.json`, `boards.json`.
* **Write:** `runs/` and `state/` only. A path is allowed only if its resolved real path (symlinks and `..` resolved) is inside an allowed root by path-component comparison, not string prefix.
* **Needs my approval:** deleting or resetting any file in `state/` (requires the `--i-approve` flag typed by me; refused without it).
* **Never:** apply, email, message, log in, submit forms, POST/PUT/DELETE, write outside `runs/` and `state/`.
* The Claude judge keeps JS1 Amendment 2: a fresh `claude -p`, an empty temp cwd, `--tools ""`.

## 7. Wrong versions my tests must catch
1. Path check by string prefix (`runs-evil/` passes as `runs/`).
2. Path check without resolving symlinks.
3. Host check by substring/endswith (`api.lever.co.evil.com`, `evilapi.lever.co`).
4. A missing `jobs` key treated as `[]` (an error body counted as an empty board). This is the bug I made myself in the probe script on 2026-11-06.
5. Exit "finished" although a board failed.
6. Retrying a 404, or retrying without a bound.
7. A budget checked after the request (overshoots by one).
8. A failed board's state overwritten with an empty set (every id is "new" next run).
9. `new=0` recorded for a failed board instead of null.
10. A read-allowed folder treated as writable (writing into `persona/`).

## 8. Known open case (not decided yet)
A well-formed 200 with `"jobs": []` for a board that previously had postings. v1 treats it as a truly empty board. I expect this to be a finished-wrong-answer, will demonstrate it with a SEEDED response, catch it with an independent check, and decide the fix in a dated amendment.
## Amendment 1 — 2026-11-06 (decides the §8 open case)
Evidence: FINISHED_WRONG_ANSWER.md (SEEDED runs A and B; agent said "finished" twice, independent check caught both).
Rule: a well-formed 200 with zero postings, for a board whose prior state has at least one id, is **suspect_empty**.
- Without --i-approve: the board is failed, reason `suspect_empty`, new=null, removed=null, its state is NOT written, and the run cannot exit `finished` (GATE §2 then gives `incomplete`, or `error` if no other board succeeded).
- With --i-approve: I am confirming the board really is empty. The board is ok, removed = the prior ids, and its state is written as [] (this is the "resetting state needs my approval" rule of §6, now used by the loop).
- Unchanged: a board seen for the first time with zero postings is a normal baseline; a board whose prior state is already [] and stays empty is ok.
Out of scope, on purpose: a large but partial drop (e.g. 154 -> 3) is not covered by this rule.

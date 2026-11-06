"""JS2 loop over several job boards. GATE.md §2-§5 define every behavior here.

    python -m jobwatch.loop --boards boards.json [--i-approve]

One run writes runs/<run_id>/trace.jsonl (every observation, as it happens),
raw/ (every response body), report.json and report.md, and ends with exactly
one exit status. State (state/seen_ids.json, keyed by board id such as
"greenhouse:anthropic") is written last and never on exit "error".
"""
import argparse
import hashlib
import json
import os
import re
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from .claude_judge import CLAUDE_LABEL
from .normalize import NORMALIZERS, normalize
from .persona import DEFAULT_PERSONA, load_persona
from .policy import Policy, PolicyViolation
from .rule import judge_posting
from .transport import Response, TransportError, TransportTimeout, UrllibTransport

__all__ = ["run_loop", "Response", "TransportTimeout", "TransportError", "EXIT_CODES",
           "LoopResult", "main"]

EXIT_CODES = {"finished": 0, "incomplete": 2, "budget-exhausted": 3, "error": 1}
BUDGET_KEYS = ("max_boards", "max_requests", "max_seconds", "request_timeout", "max_judge_calls")
MAX_ATTEMPTS = 2                # GATE §4/§5: the first try plus one retry
RETRY_WAIT_SECONDS = 2          # GATE §5: timeout, connection error, 5xx
MAX_RETRY_AFTER_SECONDS = 5     # GATE §5: 429 is retried only if Retry-After <= 5
STATE_FILE = Path("state") / "seen_ids.json"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RUN_ID_FORMAT = "%Y%m%dT%H%M%SZ"


@dataclass
class LoopResult:
    exit: str
    exit_code: int
    reason: str = None
    budget_hit: str = None
    boards: dict = field(default_factory=dict)
    requests_used: int = 0
    seconds_used: float = 0.0
    skipped_duplicates: list = field(default_factory=list)
    run_dir: Path = None


class _BudgetHit(Exception):
    def __init__(self, name):
        super().__init__(name)
        self.name = name


class _ConfigError(Exception):
    pass


# --- helpers --------------------------------------------------------------------

def normalize_url(url: str) -> str:
    """GATE §4 "same action" key: lowercase scheme and host, drop :443 and fragment."""
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    if parts.port not in (None, 443):
        host = f"{host}:{parts.port}"
    return urlunsplit((parts.scheme.lower(), host, parts.path or "/", parts.query, ""))


def _safe_name(board_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", board_id)


def _header(headers: dict, name: str):
    return next((v for k, v in (headers or {}).items() if k.lower() == name.lower()), None)


def _retry_after_seconds(headers: dict):
    """Seconds from a numeric Retry-After, else None (an HTTP-date is not retried)."""
    value = _header(headers, "Retry-After")
    try:
        seconds = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return seconds if seconds >= 0 else None


def _validate_budgets(budgets) -> dict:
    if not isinstance(budgets, dict) or set(budgets) != set(BUDGET_KEYS):
        raise _ConfigError(f"budgets must have exactly the keys {list(BUDGET_KEYS)}")
    for key, value in budgets.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
            raise _ConfigError(f"budget {key} must be a positive number, not {value!r}")
    return budgets


def _validate_boards(boards) -> list:
    if not isinstance(boards, list):
        raise _ConfigError("boards must be a list")
    for board in boards:
        if not (isinstance(board, dict) and isinstance(board.get("id"), str)
                and board.get("ats") in NORMALIZERS and isinstance(board.get("url"), str)):
            raise _ConfigError(f"invalid board entry: {board!r}")
    return boards


def _load_state(root: Path, policy: Policy) -> dict:
    path = policy.check_path(root / STATE_FILE, "read")
    if not path.exists():
        return {}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise _ConfigError(f"unreadable state {STATE_FILE}: {exc}") from exc
    if not isinstance(state, dict) or not all(
            isinstance(ids, list) and all(isinstance(i, str) for i in ids)
            for ids in state.values()):
        raise _ConfigError(f"unreadable state {STATE_FILE}: expected {{board id: [id, ...]}}")
    return state


def _parse_jobs(ats: str, body: bytes):
    """The posting list, or None for bad_shape. A missing list is never read as []."""
    try:
        data = json.loads(body)
    except ValueError:
        return None, "body is not JSON"
    if ats == "lever":
        jobs = data if isinstance(data, list) else None
        if jobs is None:
            return None, "Lever body is not a list"
    else:
        jobs = data.get("jobs") if isinstance(data, dict) else None
        if not isinstance(jobs, list):
            return None, 'no "jobs" list'
    for job in jobs:
        job_id = job.get("id") if isinstance(job, dict) else None
        if isinstance(job_id, bool) or not isinstance(job_id, (str, int)):
            return None, "a posting has no usable id"
    return jobs, None


def _judge_record(board_id: str, posting: dict, persona: dict) -> dict:
    rule = judge_posting(posting, persona)
    return {
        "board": board_id,
        "id": posting["id"],
        "title": posting["title"],
        "location": (posting["location"] or {}).get("name"),
        "department": "; ".join(d["name"] for d in posting["departments"] or []) or None,
        "updated_at": posting["updated_at"],
        "absolute_url": posting["absolute_url"],
        "fields_missing_at_source": sorted(k for k, v in posting.items() if v is None),
        "rule_verdict": {"verdict": rule["verdict"], "label": rule["label"]},
        "claude_verdict": {"label": CLAUDE_LABEL, "status": "not_run", "model": None,
                           "output": None, "reason": "Claude judge not wired into the JS2 loop"},
        "justification": rule["justification"],
    }


# --- recording ------------------------------------------------------------------

class _Recorder:
    """Every write goes through policy.check_path(..., "write")."""

    def __init__(self, root: Path, policy: Policy, run_id: str, clock, start: float):
        self.policy, self.clock, self.start = policy, clock, start
        self.run_dir = root / "runs" / run_id
        policy.check_path(self.run_dir / "trace.jsonl", "write")
        self.run_dir.mkdir(parents=False, exist_ok=False)  # never reuse an earlier run's folder
        self.trace_path = self.run_dir / "trace.jsonl"

    def elapsed(self) -> float:
        return self.clock() - self.start

    def trace(self, event: str, **fields) -> None:
        line = {"event": event, "t": round(self.elapsed(), 3), **fields}
        self.policy.check_path(self.trace_path, "write")
        with open(self.trace_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(line, sort_keys=False) + "\n")

    def write_new(self, relative: str, data: bytes) -> Path:
        path = self.policy.check_path(self.run_dir / relative, "write")
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "xb") as f:
            f.write(data)
        return path


# --- the loop -------------------------------------------------------------------

class _Loop:
    def __init__(self, root, policy, transport, budgets, clock, sleep, recorder, persona):
        self.root, self.policy, self.transport = root, policy, transport
        self.budgets, self.clock, self.sleep = budgets, clock, sleep
        self.rec, self.persona = recorder, persona
        self.requests_used = 0
        self.boards_attempted = 0
        self.url_attempts = {}
        self.records = {}
        self.ok_ids = {}
        self.new_postings = {}
        self.skipped = []

    def plan(self, boards: list) -> list:
        """GATE §4: a board listed twice (same id or same GET URL) is fetched once."""
        unique, seen_ids, seen_urls = [], set(), set()
        for board in boards:
            key = ("GET", normalize_url(board["url"]))
            if board["id"] in seen_ids or key in seen_urls:
                self.skipped.append(board["id"])
                self.rec.trace("skipped_duplicate", board=board["id"], url=board["url"])
                continue
            seen_ids.add(board["id"])
            seen_urls.add(key)
            unique.append(board)
            self.records[board["id"]] = {
                "ats": board["ats"], "url": board["url"], "status": "not_attempted",
                "reason": None, "attempts": 0, "count": None, "new": None,
                "removed": None, "baseline": None}
        return unique

    def check_budgets_before_request(self) -> None:
        b = self.budgets
        if self.requests_used + 1 > b["max_requests"]:
            raise _BudgetHit("max_requests")
        if self.rec.elapsed() + b["request_timeout"] > b["max_seconds"]:
            raise _BudgetHit("max_seconds")

    def attempt(self, board: dict):
        """One request, or a refusal. Returns a Response or a transport exception."""
        record = self.records[board["id"]]
        key = ("GET", normalize_url(board["url"]))
        if self.url_attempts.get(key, 0) >= MAX_ATTEMPTS:
            self.rec.trace("repeat_blocked", board=board["id"], url=board["url"])
            return None
        try:
            self.policy.check_url(board["url"], method="GET")
        except PolicyViolation as exc:
            record.update(status="failed", reason="policy_violation")
            self.rec.trace("policy_violation", board=board["id"], url=board["url"], detail=str(exc))
            raise
        self.check_budgets_before_request()

        self.requests_used += 1
        self.url_attempts[key] = self.url_attempts.get(key, 0) + 1
        record["attempts"] += 1
        n, started = record["attempts"], self.rec.elapsed()
        event = {"board": board["id"], "url": board["url"], "attempt": n, "t_start": round(started, 3)}
        try:
            outcome = self.transport(board["url"], self.budgets["request_timeout"])
        except (TransportTimeout, TransportError) as exc:
            self.rec.trace("attempt", **event, error=type(exc).__name__, detail=str(exc) or None)
            return exc
        except PolicyViolation as exc:  # e.g. a redirect to another host
            record.update(status="failed", reason="policy_violation")
            self.rec.trace("attempt", **event, error="PolicyViolation", detail=str(exc))
            raise
        raw = self.rec.write_new(f"raw/{_safe_name(board['id'])}.attempt{n}.body", outcome.body)
        self.rec.trace("attempt", **event, status=outcome.status, bytes=len(outcome.body),
                       sha256=hashlib.sha256(outcome.body).hexdigest(),
                       raw_file=str(raw.relative_to(self.rec.run_dir)),
                       location=_header(outcome.headers, "Location"),
                       retry_after=_header(outcome.headers, "Retry-After"))
        return outcome

    def classify(self, board: dict, outcome):
        """("ok", jobs) | ("failed", reason, detail) | ("retry", reason, wait_seconds)."""
        if outcome is None:
            return ("failed", "repeat_blocked", None)
        if isinstance(outcome, TransportTimeout):
            return ("retry", "timeout", RETRY_WAIT_SECONDS)
        if isinstance(outcome, TransportError):
            return ("retry", "connection_error", RETRY_WAIT_SECONDS)
        status = outcome.status
        if status == 200:
            jobs, problem = _parse_jobs(board["ats"], outcome.body)
            return ("ok", jobs) if jobs is not None else ("failed", "bad_shape", problem)
        if status in (404, 410):
            return ("failed", "not_found", f"HTTP {status}")
        if 500 <= status < 600:
            return ("retry", "server_error", RETRY_WAIT_SECONDS)
        if status == 429:
            wait = _retry_after_seconds(outcome.headers)
            if wait is not None and wait <= MAX_RETRY_AFTER_SECONDS:
                return ("retry", "rate_limited", wait)
            return ("failed", "rate_limited", f"Retry-After {_header(outcome.headers, 'Retry-After')!r}")
        if 300 <= status < 400:
            return ("failed", "redirect", _header(outcome.headers, "Location"))
        return ("failed", f"http_{status}", None)

    def run_board(self, board: dict, state: dict) -> None:
        record = self.records[board["id"]]
        while True:
            verdict = self.classify(board, self.attempt(board))
            if verdict[0] == "retry" and record["attempts"] < MAX_ATTEMPTS:
                self.rec.trace("retry_wait", board=board["id"], reason=verdict[1], seconds=verdict[2])
                self.sleep(verdict[2])
                continue
            break

        if verdict[0] != "ok":
            detail = verdict[2] if verdict[0] == "failed" else "still failing after one retry"
            # GATE §5: a failed board's counts are null, never 0, and its state is not written.
            record.update(status="failed", reason=verdict[1], detail=detail)
            self.rec.trace("board_result", board=board["id"], status="failed",
                           reason=verdict[1], attempts=record["attempts"])
            return

        jobs = verdict[1]
        by_id = {str(job["id"]): job for job in jobs}
        ids = set(by_id)
        prior = state.get(board["id"])
        baseline = prior is None
        new = [] if baseline else sorted(ids - set(prior))
        removed = [] if baseline else sorted(set(prior) - ids)
        record.update(status="ok", count=len(ids), new=new, removed=removed, baseline=baseline)
        self.ok_ids[board["id"]] = sorted(ids)
        self.new_postings[board["id"]] = [normalize(board["ats"], by_id[i]) for i in new]
        self.rec.trace("board_result", board=board["id"], status="ok", count=len(ids),
                       postings_in_body=len(jobs), new=new, removed=removed,
                       baseline=baseline, attempts=record["attempts"])

    def run(self, boards: list, state: dict) -> None:
        for board in self.plan(boards):
            if self.boards_attempted + 1 > self.budgets["max_boards"]:
                raise _BudgetHit("max_boards")
            self.boards_attempted += 1
            self.rec.trace("board_start", board=board["id"], ats=board["ats"], url=board["url"])
            self.run_board(board, state)

    def judge_new_postings(self) -> list:
        if self.persona is None:
            return []
        return [_judge_record(board_id, posting, self.persona)
                for board_id, postings in self.new_postings.items() for posting in postings]


def _write_state(root: Path, policy: Policy, state: dict, ok_ids: dict) -> None:
    """Only boards that succeeded are replaced; every other entry is kept as it was."""
    merged = {**state, **ok_ids}
    path = policy.check_path(root / STATE_FILE, "write")
    tmp = policy.check_path(root / STATE_FILE.with_suffix(".json.tmp"), "write")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(json.dumps(merged, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _decide_exit(records: dict) -> tuple:
    ok = [b for b, r in records.items() if r["status"] == "ok"]
    failed = [b for b, r in records.items() if r["status"] == "failed"]
    if not ok:
        return "error", "zero boards succeeded"
    if failed:
        return "incomplete", f"{len(failed)} board(s) failed"
    return "finished", None


def run_loop(boards, *, root, policy, transport, budgets, clock=time.monotonic,
             sleep=time.sleep, run_id, persona=None, approved=False) -> LoopResult:
    """Run GATE §2-§5 over `boards`. `transport(url, timeout)` returns a Response
    or raises TransportTimeout/TransportError; it is only called after the policy
    and budget checks pass."""
    root = Path(root)
    start = clock()
    rec = _Recorder(root, policy, run_id, clock, start)
    rec.trace("run_start", run_id=run_id, budgets=budgets, boards_listed=len(boards or []),
              approved=bool(approved))
    loop = _Loop(root, policy, transport, budgets, clock, sleep, rec, persona)
    budget_hit, judged, exit_status, reason = None, [], None, None

    try:
        _validate_budgets(budgets)
        _validate_boards(boards)
        state = _load_state(root, policy)
        try:
            loop.run(boards, state)
        except _BudgetHit as hit:
            budget_hit = hit.name
            exit_status = "budget-exhausted"
            reason = f"budget {hit.name} would be exceeded by the next action"
            for record in loop.records.values():
                if record["status"] == "not_attempted" and record["attempts"]:
                    record.update(status="interrupted", reason=f"budget:{hit.name}")
            rec.trace("budget_exhausted", budget=hit.name, requests_used=loop.requests_used,
                      boards_attempted=loop.boards_attempted, seconds_used=round(rec.elapsed(), 3))
        if exit_status is None:
            exit_status, reason = _decide_exit(loop.records)
        judged = loop.judge_new_postings()
        if exit_status != "error":
            _write_state(root, policy, state, loop.ok_ids)
            rec.trace("state_written", boards=sorted(loop.ok_ids))
    except PolicyViolation as exc:
        exit_status, reason = "error", f"policy violation: {exc}"
    except _ConfigError as exc:
        exit_status, reason = "error", str(exc)
    except Exception as exc:  # an unexpected failure still ends with a report, never state
        exit_status, reason = "error", f"unexpected {type(exc).__name__}: {exc}"
        rec.trace("exception", traceback=traceback.format_exc())
    if exit_status == "error":
        rec.trace("state_not_written", reason=reason)

    result = LoopResult(
        exit=exit_status, exit_code=EXIT_CODES[exit_status], reason=reason,
        budget_hit=budget_hit, boards=loop.records, requests_used=loop.requests_used,
        seconds_used=round(rec.elapsed(), 3), skipped_duplicates=loop.skipped,
        run_dir=rec.run_dir)
    report = _report(result, run_id, budgets, loop, judged, approved)
    rec.trace("run_end", exit=exit_status, exit_code=result.exit_code, reason=reason)
    rec.write_new("report.json", (json.dumps(report, indent=2) + "\n").encode("utf-8"))
    rec.write_new("report.md", format_report_md(report).encode("utf-8"))
    return result


def _error_run(root: Path, policy: Policy, run_id: str, reason: str, clock=time.monotonic) -> LoopResult:
    """A run that could not start (bad config or persona) still writes trace and report."""
    rec = _Recorder(root, policy, run_id, clock, clock())
    rec.trace("run_start", run_id=run_id)
    rec.trace("state_not_written", reason=reason)
    rec.trace("run_end", exit="error", exit_code=EXIT_CODES["error"], reason=reason)
    result = LoopResult(exit="error", exit_code=EXIT_CODES["error"], reason=reason, run_dir=rec.run_dir)
    report = _report(result, run_id, None, None, [], False)
    rec.write_new("report.json", (json.dumps(report, indent=2) + "\n").encode("utf-8"))
    rec.write_new("report.md", format_report_md(report).encode("utf-8"))
    return result


# --- reports --------------------------------------------------------------------

def _report(result: LoopResult, run_id: str, budgets, loop, judged: list, approved) -> dict:
    boards = result.boards
    return {
        "run_id": run_id,
        "exit": result.exit,
        "exit_code": result.exit_code,
        "reason": result.reason,
        "note": '"finished" means the loop ran to the end, not that the answer is right (GATE §2, §8).',
        "budgets": budgets,
        "budget_hit": result.budget_hit,
        "counters": {
            "requests_used": result.requests_used,
            "seconds_used": result.seconds_used,
            "boards_attempted": loop.boards_attempted if loop else 0,
            "judge_calls_used": 0,
        },
        "failed_boards": [b for b, r in boards.items() if r["status"] in ("failed", "interrupted")],
        "boards_done": [b for b, r in boards.items() if r["status"] in ("ok", "failed")],
        "boards_not_attempted": [b for b, r in boards.items() if r["status"] == "not_attempted"],
        "skipped_duplicates": result.skipped_duplicates,
        "boards": boards,
        "approved_flag": bool(approved),
        "state_written": result.exit != "error",
        "new_postings": judged,
    }


def _fmt_ids(ids):
    if ids is None:
        return "null"
    return ", ".join(ids) if ids else "-"


def format_report_md(report: dict) -> str:
    lines = [f"# jobwatch run {report['run_id']}", "",
             f"**Exit: {report['exit']}** (code {report['exit_code']})"
             + (f" — {report['reason']}" if report["reason"] else ""), "",
             f"_{report['note']}_", ""]
    boards = report["boards"]

    # GATE §5 escalation: failed boards first.
    lines += ["## Failed boards", ""]
    if report["failed_boards"]:
        for b in report["failed_boards"]:
            r = boards[b]
            lines.append(f"- **{b}**: {r['status']}, reason `{r['reason']}`, attempts {r['attempts']}"
                         + (f" ({r['detail']})" if r.get("detail") else "")
                         + "; new=null, removed=null; state not changed")
    else:
        lines.append("- none")
    lines.append("")

    if report["budget_hit"]:
        c = report["counters"]
        lines += ["## Budget exhausted", "",
                  f"- budget: `{report['budget_hit']}`",
                  f"- requests used {c['requests_used']}, seconds used {c['seconds_used']}, "
                  f"boards attempted {c['boards_attempted']}",
                  f"- boards done: {', '.join(report['boards_done']) or '-'}",
                  f"- boards not attempted: {', '.join(report['boards_not_attempted']) or '-'}", ""]

    if boards:
        lines += ["## Boards", "", "| board | status | count | new | removed | attempts |",
                  "|---|---|---|---|---|---|"]
        for b, r in boards.items():
            count = "null" if r["count"] is None else r["count"]
            new = "baseline" if r["baseline"] else _fmt_ids(r["new"])
            lines.append(f"| {b} | {r['status']} | {count} | {new} | {_fmt_ids(r['removed'])} "
                         f"| {r['attempts']} |")
        lines.append("")

    if report["skipped_duplicates"]:
        lines += ["## Skipped duplicates", "", *[f"- {b}" for b in report["skipped_duplicates"]], ""]

    if report["new_postings"]:
        lines += ["## New postings (rule judge, record (recomputable))", ""]
        for p in report["new_postings"]:
            lines.append(f"- {p['rule_verdict']['verdict']} — {p['board']} {p['id']}: "
                         f"{p['title']} ({p['location']})")
        lines.append("")

    c = report["counters"]
    lines += ["## Counters", "",
              f"requests {c['requests_used']}, seconds {c['seconds_used']}, "
              f"boards attempted {c['boards_attempted']}, judge calls {c['judge_calls_used']}; "
              f"state written: {report['state_written']}", ""]
    return "\n".join(lines)


# --- CLI ------------------------------------------------------------------------

def _read_json(policy: Policy, path: Path):
    resolved = policy.check_path(path, "read")
    with open(resolved, encoding="utf-8") as f:
        return json.load(f)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m jobwatch.loop")
    parser.add_argument("--boards", type=Path, required=True, help="board list (GATE §1)")
    parser.add_argument("--i-approve", action="store_true",
                        help="approve deleting or resetting files in state/ (GATE §6)")
    args = parser.parse_args(argv)

    root = PROJECT_ROOT
    policy = Policy(root)
    run_id = datetime.now(timezone.utc).strftime(RUN_ID_FORMAT)
    (root / "runs").mkdir(exist_ok=True)
    try:
        budgets = _read_json(policy, root / "gate_config.json")
        boards = _read_json(policy, args.boards.resolve())
        persona = load_persona(policy.check_path(DEFAULT_PERSONA, "read"))
    except (PolicyViolation, OSError, ValueError) as exc:  # PersonaRefused is a ValueError
        result = _error_run(root, policy, run_id, f"config: {type(exc).__name__}: {exc}")
    else:
        result = run_loop(boards, root=root, policy=policy, transport=UrllibTransport(policy),
                          budgets=budgets, clock=time.monotonic, sleep=time.sleep,
                          run_id=run_id, persona=persona, approved=args.i_approve)

    print(f"exit={result.exit} code={result.exit_code} reason={result.reason}")
    for board_id, r in result.boards.items():
        print(f"{board_id}: {r['status']} reason={r['reason']} count={r['count']} "
              f"new={r['new']} removed={r['removed']} attempts={r['attempts']}")
    print(f"report={result.run_dir / 'report.md'}")
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())

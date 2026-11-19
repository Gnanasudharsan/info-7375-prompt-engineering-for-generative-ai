"""The watch: fetch (or read a saved response), diff ids against state, report.

First run with no state file is a baseline: 0 new, every id recorded.
Later runs report postings whose id is not in state, then add them to state.
Each new posting gets a result record with both judges (CONTRACT.md "Out").
"""
import json
from datetime import datetime, timezone
from pathlib import Path

from . import fetcher
from .claude_judge import CLAUDE_LABEL
from .persona import DEFAULT_PERSONA, load_persona
from .rule import judge_posting

TIMESTAMP_FORMAT = "%Y%m%dT%H%M%SZ"


def _utc_stamp(now: datetime) -> str:
    return now.astimezone(timezone.utc).strftime(TIMESTAMP_FORMAT)


def _write_new_file(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # "xb" refuses to overwrite an earlier run's file with the same timestamp.
    with open(path, "xb") as f:
        f.write(data)


def load_state(state_path: Path):
    if not state_path.exists():
        return None
    with open(state_path, encoding="utf-8") as f:
        return json.load(f)


def result_record(job: dict, persona: dict, claude_judge=None) -> dict:
    """One CONTRACT.md "Out" record. claude_judge=None means --no-claude."""
    rule = judge_posting(job, persona)
    if claude_judge is None:
        claude = {"label": CLAUDE_LABEL, "status": "not_run", "model": None,
                  "output": None, "failed_attempts": [], "reason": "--no-claude"}
    else:
        claude = claude_judge(job, persona)
    return {
        "id": job["id"],
        "title": job.get("title"),
        "location": (job.get("location") or {}).get("name"),
        "department": "; ".join(d["name"] for d in job.get("departments") or []) or None,
        "updated_at": job.get("updated_at"),
        "rule_verdict": {"verdict": rule["verdict"], "label": rule["label"]},
        "claude_verdict": claude,
        "justification": rule["justification"],
    }


def run_watch(root: Path, now: datetime, from_file: Path = None, session=None,
              persona: dict = None, claude_judge=None) -> dict:
    root = Path(root)
    stamp = _utc_stamp(now)
    state_path = root / "state" / "seen_ids.json"

    if from_file is not None:
        raw_path = Path(from_file)
        body = raw_path.read_bytes()
    else:
        body = fetcher.fetch(fetcher.BOARD_URL, session=session)
        raw_path = root / "data" / "raw" / f"anthropic_{stamp}.json"
        _write_new_file(raw_path, body)

    jobs = json.loads(body)["jobs"]
    state = load_state(state_path)
    is_baseline = state is None
    seen = set() if is_baseline else set(state["seen_ids"])

    if is_baseline:
        new_jobs = []
    else:
        new_jobs = [job for job in jobs if job["id"] not in seen]

    if persona is None:
        persona = load_persona(DEFAULT_PERSONA)
    # Judging happens before anything is written, so a crash leaves state untouched.
    results = [result_record(job, persona, claude_judge) for job in new_jobs]

    if from_file is not None:
        run_type = "seeded"
    elif is_baseline:
        run_type = "baseline"
    else:
        run_type = "live"

    run_time = now.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    report = {
        "run_type": run_type,
        "label": "SEEDED" if run_type == "seeded" else None,
        "baseline": is_baseline,
        "run_time_utc": run_time,
        "raw_file": str(raw_path),
        "total_postings": len(jobs),
        "new_count": len(new_jobs),
        "new_postings": [{"id": job["id"], "title": job["title"]} for job in new_jobs],
        "claude_enabled": claude_judge is not None,
        "results": results,
    }
    report_path = root / "data" / "runs" / f"{stamp}.json"
    _write_new_file(report_path, (json.dumps(report, indent=2) + "\n").encode("utf-8"))
    report["report_file"] = str(report_path)

    # State is written last, so a failure above leaves the previous state intact.
    new_state = {
        "seen_ids": sorted(seen | {job["id"] for job in jobs}),
        "last_run_utc": run_time,
    }
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(new_state, indent=2) + "\n", encoding="utf-8")
    return report


def format_summary(report: dict) -> str:
    prefix = "SEEDED " if report["run_type"] == "seeded" else ""
    lines = [
        f"{prefix}run_type={report['run_type']} baseline={report['baseline']}",
        f"{prefix}raw_file={report['raw_file']}",
        f"{prefix}total_postings={report['total_postings']} new={report['new_count']}",
    ]
    for posting in report["new_postings"]:
        lines.append(f"{prefix}NEW {posting['id']} {posting['title']}")
    for result in report.get("results", []):
        claude = result["claude_verdict"]
        claude_text = claude["output"]["verdict"] if claude["status"] == "ok" else claude["status"]
        lines.append(f"{prefix}RULE {result['id']} {result['rule_verdict']['verdict']} "
                     f"[{result['rule_verdict']['label']}]")
        lines.append(f"{prefix}CLAUDE {result['id']} {claude_text} [{claude['label']}]")
    lines.append(f"{prefix}report={report['report_file']}")
    return "\n".join(lines)

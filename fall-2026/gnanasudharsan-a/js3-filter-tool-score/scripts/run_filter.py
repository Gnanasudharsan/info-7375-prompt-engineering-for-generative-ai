"""Run FILTER.md v1.0 over a saved run folder. No network.

Usage: PYTHONPATH=. python scripts/run_filter.py runs/<id> [--changes C1,C2]

Reads runs/<id>/raw/*.body (the latest attempt per board in boards.json), normalizes each
posting with jobwatch.normalize, runs jobwatch.filter.evaluate, writes runs/<id>/filter_v1.jsonl
(or, with --changes, runs/<id>/filter_v1_C1_C2.jsonl with the switch ids sorted) and prints
counts. A board whose body has no posting list is reported as excluded, never as 0.
An existing output file is never overwritten.
"""
import argparse
import gzip
import json
import re
import sys
from collections import Counter
from pathlib import Path

from jobwatch.filter import FILTER_V1, FILTER_V1_1, STAGE_A, evaluate
from jobwatch.loop import _parse_jobs, _safe_name
from jobwatch.normalize import normalize

ROOT = Path(__file__).resolve().parent.parent
OUT_NAME = "filter_v1.jsonl"


def parse_changes(value: str) -> frozenset:
    ids = [part.strip().upper() for part in value.split(",") if part.strip()]
    unknown = sorted(set(ids) - set(FILTER_V1_1["switches"]))
    if not ids or unknown:
        raise argparse.ArgumentTypeError(
            f"expected a comma list of {', '.join(FILTER_V1_1['switches'])}; got {value!r}")
    return frozenset(ids)


def out_name(changes: frozenset) -> str:
    return f"filter_v1_{'_'.join(sorted(changes))}.jsonl" if changes else OUT_NAME


def latest_body(raw_dir: Path, board_id: str):
    """The highest attemptN body for the board; .body preferred over .body.gz for the same N."""
    pattern = re.compile(re.escape(_safe_name(board_id)) + r"\.attempt(\d+)\.body(\.gz)?$")
    found = [(int(m.group(1)), not m.group(2), p) for p in raw_dir.iterdir()
             if (m := pattern.match(p.name))]
    return max(found)[2] if found else None


def read_body(path: Path) -> bytes:
    data = path.read_bytes()
    return gzip.decompress(data) if path.name.endswith(".gz") else data


def main(argv) -> int:
    parser = argparse.ArgumentParser(description="Run FILTER.md over a saved run folder (offline).")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--changes", type=parse_changes, default=frozenset(),
                        help="v1.1 switches to turn on, e.g. C1,C2")
    args = parser.parse_args(argv[1:])
    changes = args.changes
    run_dir = args.run_dir
    raw_dir = run_dir / "raw"
    out_path = run_dir / out_name(changes)
    if not raw_dir.is_dir():
        print(f"no raw/ folder in {run_dir}", file=sys.stderr)
        return 2
    if out_path.exists():
        print(f"{out_path} already exists; not overwriting", file=sys.stderr)
        return 2
    boards = json.loads((ROOT / "boards.json").read_text(encoding="utf-8"))

    rows, per_board, excluded = [], {}, {}
    for board in boards:
        body_path = latest_body(raw_dir, board["id"])
        if body_path is None:
            excluded[board["id"]] = "no raw body in this run"
            continue
        jobs, problem = _parse_jobs(board["ats"], read_body(body_path))
        if jobs is None:
            excluded[board["id"]] = f"{body_path.name}: {problem}"
            continue
        counts = Counter()
        for job in jobs:
            posting = normalize(board["ats"], job)
            result = evaluate(posting, changes=changes)
            counts[result["decision"]] += 1
            rows.append({"board": board["id"], "id": posting["id"], "title": posting["title"],
                         "location": (posting["location"] or {}).get("name"), **result})
        per_board[board["id"]] = counts

    with out_path.open("x", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    total = Counter(r["decision"] for r in rows)
    fired = Counter(rule for r in rows for rule in r["rejected_by"])
    close = sum(1 for r in rows if r["score"] in (4, 5, 6))
    switches = ",".join(sorted(changes)) or "none"
    print(f"FILTER v{FILTER_V1['version']} (v1.1 switches: {switches}) on {run_dir} -> {out_path}"
          f" ({len(rows)} postings)")
    for board_id, counts in per_board.items():
        n = sum(counts.values())
        print(f"  {board_id}: {n} postings | keep {counts['keep']} | reject {counts['reject']}"
              f" | cannot_tell {counts['cannot_tell']}")
    for board_id, reason in excluded.items():
        print(f"  {board_id}: EXCLUDED (absent, not zero) - {reason}")
    print(f"  total: keep {total['keep']} | reject {total['reject']} | cannot_tell {total['cannot_tell']}")
    print("  Stage A rules fired (a posting can fire several): "
          + ", ".join(f"{rule} {fired[rule]}" for rule in STAGE_A))
    print(f"  rejected on score only (< {FILTER_V1['keep_threshold']}): "
          f"{sum(1 for r in rows if r['decision'] == 'reject' and not r['rejected_by'])}")
    print(f"  close calls (score 4-6): {close}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

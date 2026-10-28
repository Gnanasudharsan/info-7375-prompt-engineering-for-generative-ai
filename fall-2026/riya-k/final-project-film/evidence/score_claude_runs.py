#!/usr/bin/env python3
"""Score saved Claude runs against the gold set (2026-10-21).

Replays the raw SQL saved in claude_runs/<date>/run*_raw.json. Nothing calls a
model here: each saved query runs on the read-only Chinook database and its rows
are compared with the gold rows, using the same comparator as run_slice.py.

Usage:  python3 score_claude_runs.py [claude_runs/2026-10-21]
"""
import json
import sqlite3
import sys
from pathlib import Path

from run_slice import HERE, normalise, run, same_result, string_match


def main():
    run_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "claude_runs" / "2026-10-21"
    spec = json.loads((HERE / "gold_set.json").read_text())
    con = sqlite3.connect(f"file:{HERE / spec['database']}?mode=ro", uri=True)
    runs = sorted(run_dir.glob("run*_raw.json"))
    print(f"scoring {len(runs)} saved runs from {run_dir.name}\n")
    totals = {r.stem: [0, 0] for r in runs}
    for q in spec["questions"]:
        gold = run(con, q["gold"])
        print(f"{q['id']}  {q['question']}")
        print(f"     gold      -> {normalise(gold, q['ordered'])[:3]}")
        for r in runs:
            sql = json.loads(r.read_text())[q["id"]]
            if not sql.lstrip().upper().startswith("SELECT"):
                verdict, note = False, "contract violation: not a single SELECT"
            else:
                try:
                    cand = run(con, sql)
                    verdict = same_result(gold, cand, q["ordered"])
                    note = "" if verdict else f"got {normalise(cand, q['ordered'])[:3]}"
                except sqlite3.Error as e:
                    verdict, note = False, f"error: {e}"
            totals[r.stem][0] += verdict
            totals[r.stem][1] += string_match(q["gold"], sql)
            print(f"     {r.stem:<9} rows {'PASS' if verdict else 'FAIL'}  {note}")
    print()
    n = len(spec["questions"])
    for name, (rows_ok, text_ok) in totals.items():
        print(f"{name}: {rows_ok}/{n} correct by comparing rows, {text_ok}/{n} by comparing SQL text")
    return 0


if __name__ == "__main__":
    sys.exit(main())

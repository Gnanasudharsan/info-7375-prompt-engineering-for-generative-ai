#!/usr/bin/env python3
"""First runnable slice of the text-to-SQL eval harness (2026-10-09).

What this checks: the gold answers run, and the execution-based comparator
judges the variants (drafted with Claude, labels checked by Riya) the way a human would -- equivalent SQL passes,
plausible wrong SQL fails. No model is called. Nothing here is model output.

Usage:  python3 run_slice.py            (standard library only, offline)
"""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(con, sql):
    return con.execute(sql).fetchall()


def normalise(rows, ordered):
    """Compare values, not column names; round floats; ignore row order unless it matters."""
    out = [tuple(round(v, 2) if isinstance(v, float) else v for v in row) for row in rows]
    return out if ordered else sorted(out, key=repr)


def same_result(gold_rows, cand_rows, ordered):
    return normalise(gold_rows, ordered) == normalise(cand_rows, ordered)


def string_match(a, b):
    """The naive check a lot of quick demos use: is the SQL text the same?"""
    return " ".join(a.lower().split()) == " ".join(b.lower().split())


def main():
    spec = json.loads((HERE / "gold_set.json").read_text())
    con = sqlite3.connect(f"file:{HERE / spec['database']}?mode=ro", uri=True)
    agree = total = string_agree = 0
    for q in spec["questions"]:
        gold = run(con, q["gold"])
        # A gold answer can be wrong too: an empty or all-NULL gold "matches" broken SQL.
        # (v0 of Q08 asked about a year with no invoices and did exactly that.)
        assert any(v is not None for row in gold for v in row), f"{q['id']}: gold result is empty or all NULL"
        print(f"{q['id']}  {q['question']}")
        print(f"     gold -> {gold[:3]}{' ...' if len(gold) > 3 else ''}  ({len(gold)} rows)")
        for v in q["variants"]:
            cand = run(con, v["sql"])
            verdict = same_result(gold, cand, q["ordered"])
            expected = v["kind"] == "equivalent"
            ok = verdict == expected
            agree += ok
            total += 1
            string_agree += string_match(q["gold"], v["sql"]) == expected
            label = v.get("label", "different SQL, same answer")
            print(f"     {v['kind']:<10} judged {'PASS' if verdict else 'FAIL'}"
                  f"  {'as expected' if ok else 'WRONG JUDGEMENT'}  -- {label}")
            print(f"                cand -> {cand[:3]}{' ...' if len(cand) > 3 else ''}")
    print()
    print(f"execution comparator agreed with the hand label on {agree}/{total} variants")
    print(f"exact-string comparator agreed on {string_agree}/{total} variants")
    return 0 if agree == total else 1


if __name__ == "__main__":
    sys.exit(main())

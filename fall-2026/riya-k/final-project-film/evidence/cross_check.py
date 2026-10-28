#!/usr/bin/env python3
"""Second, independent check of every gold answer (2026-10-21).

The gold answers in gold_set.json are SQL. This script recomputes each one a different
way: it reads the raw tables with plain `SELECT *` (no joins, no GROUP BY, no SUM in SQL)
and does the joining, counting and adding in ordinary Python. If both ways give the same
rows, the gold answer is confirmed. It also flags questions that are risky to grade:
a tie at a LIMIT cut-off, or an answer that equals a whole-table total.

Usage:  python3 cross_check.py            (standard library only, offline)
"""
import json
import sqlite3
import sys
from collections import Counter, defaultdict

from run_slice import HERE, normalise, run


def table(con, name):
    cur = con.execute(f"SELECT * FROM {name}")
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def top(counter, n):
    """Top n by value, ties broken by name; also report whether a tie crosses the cut-off."""
    ranked = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
    tie = len(ranked) > n and ranked[n - 1][1] == ranked[n][1]
    counts = [v for _, v in ranked[:n]]
    tie_inside = len(set(counts)) < len(counts)
    return ranked[:n], tie, tie_inside


def main():
    spec = json.loads((HERE / "gold_set.json").read_text())
    con = sqlite3.connect(f"file:{HERE / spec['database']}?mode=ro", uri=True)
    cust, inv, line, track = (table(con, t) for t in ("Customer", "Invoice", "InvoiceLine", "Track"))
    genre = {g["GenreId"]: g["Name"] for g in table(con, "Genre")}
    emp = {e["EmployeeId"]: e for e in table(con, "Employee")}
    inv_by_id = {i["InvoiceId"]: i for i in inv}
    track_by_id = {t["TrackId"]: t for t in track}
    notes = {}

    py = {}
    py["Q01"] = [(len(cust),)]

    per_country = Counter(c["Country"] for c in cust)
    rows, tie, tie_inside = top(per_country, 5)
    py["Q02"] = rows
    if tie_inside:
        notes["Q02"] = "ordered question with tied counts inside the top 5 and no tie rule in the question"
    elif tie:
        notes["Q02"] = "a tie crosses the LIMIT 5 cut-off"

    revenue = defaultdict(float)
    for i in inv:
        revenue[i["BillingCountry"]] += i["Total"]
    py["Q03"] = [(k, round(v, 2)) for k, v in sorted(revenue.items(), key=lambda kv: -kv[1])[:3]]
    lines_total = defaultdict(float)
    for l in line:
        lines_total[inv_by_id[l["InvoiceId"]]["BillingCountry"]] += l["UnitPrice"] * l["Quantity"]
    if any(abs(lines_total[k] - revenue[k]) > 0.005 for k in revenue):
        notes["Q03"] = "Invoice.Total and the sum of its lines disagree for some country"

    rock_buyers = {inv_by_id[l["InvoiceId"]]["CustomerId"] for l in line
                   if genre.get(track_by_id[l["TrackId"]]["GenreId"]) == "Rock"}
    py["Q04"] = [(len(rock_buyers),)]
    if len(rock_buyers) == len(cust):
        notes["Q04"] = "answer equals every customer, so it cannot tell 'bought Rock' from 'all customers'"

    reps = Counter(c["SupportRepId"] for c in cust if c["SupportRepId"] is not None)
    best = sorted(reps.items(), key=lambda kv: -kv[1])
    py["Q05"] = [(emp[best[0][0]]["FirstName"], emp[best[0][0]]["LastName"], best[0][1])]
    if len(best) > 1 and best[0][1] == best[1][1]:
        notes["Q05"] = "two employees tie for the most customers"

    py["Q06"] = [(sum(1 for t in track if t["Milliseconds"] > 5 * 60 * 1000),)]

    per_genre = Counter(t["GenreId"] for t in track)
    py["Q07"] = [(genre[g],) for g, n in per_genre.items() if n > 100]

    py["Q08"] = [(round(sum(i["Total"] for i in inv if str(i["InvoiceDate"]).startswith("2013")), 2),)]

    agree = 0
    for q in spec["questions"]:
        gold = normalise(run(con, q["gold"]), q["ordered"])
        mine = normalise(py[q["id"]], q["ordered"])
        ok = gold == mine
        agree += ok
        print(f"{q['id']}  {'AGREE   ' if ok else 'DISAGREE'}  sql {gold[:3]}  python {mine[:3]}")
        if q["id"] in notes:
            print(f"     flag: {notes[q['id']]}")
    print()
    print(f"gold SQL and the plain-Python recomputation agree on {agree}/{len(spec['questions'])} questions; "
          f"{len(notes)} flagged")
    return 0 if agree == len(spec["questions"]) else 1


if __name__ == "__main__":
    sys.exit(main())

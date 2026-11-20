"""Offline score experiments on my held-out labels: one change at a time against v1.0 at threshold 5."""
import csv, json
from collections import Counter
run = "runs/20261119T162945Z"
load = lambda f: {(r["board"], str(r["id"])): r for r in map(json.loads, open(f"{run}/{f}"))}
v10, v11 = load("filter_v1.jsonl"), load("filter_v1_C1_C4.jsonl")
s = {x["n"]: x for x in json.load(open("heldout/sample.json"))}
mine = {(s[int(r["n"])]["board"], s[int(r["n"])]["id"]): r["my_verdict"] for r in csv.DictReader(open("heldout/hand_verdicts.csv"))}
def at_threshold(res, t):
    out = {}
    for k, r in res.items():
        out[k] = r["decision"] if r["decision"] != "keep" and (r["rejected_by"] or r["score"] is None) else ("keep" if r["score"] is not None and r["score"] >= t else "reject")
    return out
def report(name, dec):
    c = Counter((dec[k], m) for k, m in mine.items())
    keep = sum(v == "keep" for k, v in dec.items() if k in mine)
    print(f"{name:<34} held-out keeps {keep:>2} | keep&NOT_RELEVANT (false keep) {c[('keep','NOT_RELEVANT')]:>2} | keep&CANNOT_TELL {c[('keep','CANNOT_TELL')]:>2} | reject&CANNOT_TELL {c[('reject','CANNOT_TELL')]:>2}")
    return dec
base = report("baseline v1.0, threshold 5", {k: r["decision"] for k, r in v10.items()})
for t in (6, 4):
    d = report(f"setting: threshold 5 -> {t}", at_threshold(v10, t))
    print("   flips on held-out:", [(v10[k]["title"][:40], base[k], d[k], mine[k]) for k in mine if d[k] != base[k]])
d = report("filter file: v1.0 -> v1.1 (C4)", {k: r["decision"] for k, r in v11.items()})
print("   flips on held-out:", [(v10[k]["title"][:40], base[k], d[k], mine[k]) for k in mine if d[k] != base[k]])
